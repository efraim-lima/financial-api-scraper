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
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Exporting api_key as environment variable
ENV POLYGON_API_KEY="mqJl50msy2bOXpEVFjgNeYpCbsu0zo3f"

#the port for flask app
EXPOSE 8000

CMD ["python3", "api/app.py"]

# For run docker compose:
# $ docker-compose up

# I need do docker login in my machine
# $ sudo docker login
# $ sudo docker commit $CONTAINER_ID <username>/<app_name>
# $ sudo docker push <username>/<app_name>
