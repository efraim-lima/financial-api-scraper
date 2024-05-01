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

COPY . /
WORKDIR /

RUN apt-get update && apt-get install -y sqlite3

RUN apt install -y python3
RUN apt install -y redis-server

RUN service redis-server start

RUN pip install pip-tools
#RUN pip-compile --upgrade --resolver=backtracking requirements.in
RUN pip install -r requirements.txt

# Set the working directory in the container

# Copy the requirements file into the container

# Install Python dependencies
RUN pip install -r requirements.txt

COPY redis.conf /

# Create the SQLite database file
# COPY /app/db/purchases.db /app/db/purchases.db
RUN touch ./app/db/purchases.db
RUN sqlite3 ./app/db/purchases.db

# Exporting api_key as environment variable
# ENV POLYGON_API_KEY="mqJl50msy2bOXpEVFjgNeYpCbsu0zo3f"
ENV FLASK_APP=main:create_app
ENV FLASK_ENV=development

# #the port for flask app
EXPOSE 8000
EXPOSE 6379

CMD ["sh", "-c", "python3 ./app/api/main.py"]

# For run docker compose:
# $ docker-compose up

# I need do docker login in my machine
# $ sudo docker login
# $ sudo docker commit $CONTAINER_ID <username>/<app_name>
# $ sudo docker push <username>/<app_name>
