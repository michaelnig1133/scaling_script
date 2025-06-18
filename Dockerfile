FROM python:3.9-slim
#docker swarm join --token SWMTKN-1-4hz3iz5pt24385qa9buizj1wj2l3f8rvtahyqb9frkqy2b0nl5-co1vw3dx6mywn7qsetcucp69z 192.168.65.9:2377
# Install dependencies
RUN pip install requests

# Copy your script
COPY autoscaler.py /app/autoscaler.py

# Set the working directory
WORKDIR /app

# Run the script
CMD ["python", "autoscaler.py"]
