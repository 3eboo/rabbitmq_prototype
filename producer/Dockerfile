# Use a base image with Python
FROM python:3.8-slim

# Set the working directory within the container
WORKDIR /app

# Copy the producer script to the container
COPY producer.py .
COPY sample_data.csv .

# Install any necessary dependencies
RUN pip install pika

# Run the producer script when the container starts
CMD ["python", "producer.py"]
