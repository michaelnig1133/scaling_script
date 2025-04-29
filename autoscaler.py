import requests
import os
import time

# Prometheus query
QUERY = 'rate(container_cpu_usage_seconds_total{name="gatepassapp-container"}[1m])'
PROMETHEUS_URL = "http://prometheus:9900"  # or "http://localhost:9900" if exposed

# Thresholds
MAX_CPU_THRESHOLD = 0.5
MIN_CPU_THRESHOLD = 0.1

# Polling interval in seconds
POLL_INTERVAL = 60  # 1 minute

def get_cpu_usage():
    try:
        res = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={"query": QUERY})
        data = res.json()
        if data['data']['result']:
            return float(data['data']['result'][0]['value'][1])
    except Exception as e:
        print(f"Error fetching CPU usage: {e}")
    return 0.0

def scale_service(scale_to):
    print(f"Scaling service to {scale_to} replicas")
    os.system(f"docker service scale your_service_name={scale_to}")

def monitor_and_scale():
    while True:
        cpu = get_cpu_usage()
        print(f"[Monitor] CPU usage: {cpu}")

        if cpu > MAX_CPU_THRESHOLD:
            scale_service(5)
        elif cpu < MIN_CPU_THRESHOLD:
            scale_service(1)

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    monitor_and_scale()
