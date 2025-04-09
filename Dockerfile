FROM python:3.9-slim

# Install dependencies
RUN pip install requests

# Copy your script
COPY autoscaler.py /app/autoscaler.py

# Set the working directory
WORKDIR /app

# Run the script
CMD ["python", "autoscaler.py"]
