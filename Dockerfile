# for start this container: 
# $ docker build api-image .

# for run this container: 
# $ docker run -d --rm --name api-container api-image

# for run scripts in active docker: 
# $ docker exec -i api-container <command> < <path to file>

# for run commands in active docker but as terminal: 
# $ docker exec -it api-container /bin/bash

#  Only for educational motives, for share a folder from host to container: 
# $ docker stop api-container
# $ docker run -d -v $(pwd)/app/data:/var/lib/sqlite --rm --name api-container api-image
# $ docker exec -i api-container <command> < <path to file>

# Use the official Python image as the base image
FROM python:3.11.2

# Set the working directory in the container
WORKDIR /

# Copy the requirements file into the container
COPY requirements.txt /

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Use the official Redis image from Docker Hub
FROM redis

# Copy a custom Redis configuration file to the container
COPY redis.conf /usr/local/etc/redis/redis.conf

# Start Redis server with the custom configuration file
CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]
