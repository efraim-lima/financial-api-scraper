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

# Install Python dependencies
RUN pip install -r requirements.txt

COPY redis.conf /

RUN touch ./app/db/purchases.db
RUN sqlite3 ./app/db/purchases.db

ENV FLASK_APP=main:create_app
ENV FLASK_ENV=development

# #the port for flask app
EXPOSE 8000
EXPOSE 6379

CMD ["sh", "-c", "python3 ./app/api/main.py"]