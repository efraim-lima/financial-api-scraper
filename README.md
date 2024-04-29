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
"""