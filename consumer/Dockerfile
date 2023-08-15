# Use a base image with Python
FROM python:3.8-slim

# Set the working directory within the container
WORKDIR /app

# Copy the consumer script to the container
COPY consumer.py .

# Install rabbitmq client pika
RUN pip install pika

# Run the consumer script when the container starts
CMD ["python", "consumer.py"]
