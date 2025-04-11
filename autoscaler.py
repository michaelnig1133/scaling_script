import requests
import os
import time

# Prometheus config
PROMETHEUS_URL = "http://localhost:9090"

# Container thresholds
CONFIG = {
    "gatepassapp-container": {
        "cpu_limit": 1.0,      # Matches compose.yml
        "max_threshold": 0.5,  # Scale up at 50% CPU
        "min_threshold": 0.1,  # Scale down at 10% CPU
        "max_replicas": 3,     # Maximum replicas
        "compose_service": "gatepass-app"  # Service name in compose.yml
    }
}

def get_cpu_usage(container_name, cpu_limit):
    query = f'rate(container_cpu_usage_seconds_total{{name="{container_name}"}}[1m]) / {cpu_limit}'
    try:
        res = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={"query": query})
        data = res.json()
        if data['data']['result']:
            return float(data['data']['result'][0]['value'][1])
    except Exception as e:
        print(f"Error fetching CPU for {container_name}: {e}")
    return 0.0

def scale_service(service_name, desired_count):
    print(f"[{time.ctime()}] Scaling {service_name} to {desired_count} replicas")
    os.system(f"docker-compose up -d --scale {service_name}={desired_count}")

def monitor_and_scale():
    while True:
        for container, config in CONFIG.items():
            cpu = get_cpu_usage(container, config["cpu_limit"])
            print(f"[{time.ctime()}] {container} CPU: {cpu:.2f}/{config['max_threshold']}")

            current_replicas = len(os.popen(
                f'docker ps -q --filter "name={config["compose_service"]}"'
            ).read().splitlines())

            # Scale up if CPU exceeds threshold and not at max replicas
            if cpu > config["max_threshold"] and current_replicas < config["max_replicas"]:
                scale_service(config["compose_service"], config["max_replicas"])

            # Scale down if CPU is low and more than 1 replica exists
            elif cpu < config["min_threshold"] and current_replicas > 1:
                scale_service(config["compose_service"], 1)

        time.sleep(60)

if __name__ == "__main__":
    monitor_and_scale()
