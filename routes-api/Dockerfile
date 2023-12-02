# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10.12-slim

# Set the working directory in docker
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local directory to the working directory
COPY . .

# Specify the command to run on container start
CMD ["python", "app/main.py"]
