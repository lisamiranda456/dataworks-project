# Use official Python image as base
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy application files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the API port
EXPOSE 5000

# Set environment variables
ENV AIPROXY_TOKEN=""

# Run the application
CMD ["python", "app.py"]
