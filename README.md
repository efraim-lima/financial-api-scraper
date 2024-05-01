# API-test
A simple API that get data from stocks and use it as data for requests and user interaction.

"""
in start we need export 0 environment variables
$export FLASK_APP=main:create_app

and if we are in development environment:
$export FLASK_APP=development

or if we are in production environment:
$export FLASK_APP=production

at least just use
$flask run

or
$python3 <path/to/main.py> 


The redis is used for cache the results of requests.

The initialization is using redis-cli in terminal

The quotes are configured to stay in cahche for 30 seconds, it may be adjusted before.

If want to see redis activity in real time, use:
$redis-cli monitor

for start the project in the dockerfile just run in root 
$sudo service redis-server stop
$docker network create backend
$docker-compose up -d --build


$docker build -t flask .
$docker images
$docker run -d -p 8000:8000 flask
$docker stop $(docker ps -aq)

$docker ps -a
$docker-compose rm --stop --force
$docker compose up -d --build
$docker run -it -d --name 151dca9a122d api-test_app bash

$docker-compose exec webcont python3 <modulo> <comando>
$docker build -t {image name} .
$docker run -it --name {container name} -p 8000:8000 {image name}
$docker compose up --d
$docker compose down
$docker-compose build

For to get data from redis endpoints just run in terminal:

curl -X GET http://localhost:8000/stock/<stock_symbol>
curl -X POST -H "Content-Type: application/json" -d '{"amount": <integer>}' http://localhost:8000/stock/<stock_symbol>


"""