# azure functions python db access example
This repository is an example of accessing a database from a containerized Azure Function written in Python using NetBird's Netstack mode.

Netstack mode allows you to access resources in a NetBird network from an Azure Function. This mode is helpful if you want to access a database or other resource not exposed to the public internet from a limited environment like Azure functions.

## How it works
The function_app.py contains the testing code. It uses socks and socket libraries to connect to the Postgres database. NetBird provides the socks proxy. The Postgres driver uses the socket connection to connect to the remote database.

Besides the Python code and Azure function specifics. We've added two custom files:
- Dockerfile: This file is used to build the docker image for the Azure function with NetBird installed.
- command.sh: This file is used as a docker command for the image; it starts NetBird in the background and then starts the Azure function server.

## Prerequisites
- An existing Azure function. You can follow the steps here: https://learn.microsoft.com/en-us/azure/azure-functions/functions-deploy-container?tabs=docker%2Cbash%2Cazure-cli&pivots=programming-language-python
- Docker for local build
- An internal Postgres database with netbird enabled

## Create the database table
Access the Postgres database and create the table using the following statement:
```sql
CREATE TABLE visits (
        id SERIAL PRIMARY KEY,
        ip_address VARCHAR(255),
        visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
## Create the function image
Build the function image using the following command:
```bash
docker build -t <your docker hub username>/azure-functions-python-db-access .
```
## Push the image to docker hub
Push the image to the docker hub using the following command:
```bash
docker push <your docker hub username>/azure-functions-python-db-access
```

## Set the environment variables
You need to configure the following environment variables in your Azure function's application settings page:
- `POSTGRES_HOST`: The hostname of your Postgres database
- `POSTGRES_USER`: The username of your Postgres database
- `POSTGRES_PASSWORD`: The password of your Postgres database
- `POSTGRES_DB`: The name of your Postgres database
- `NB_SETUP_KEY`: The setup key of your NetBird network (We recommend using an ephemeral setup key. See https://netbird.dev/docs/setup-key for more details)

## Deploy the function
Replace the docker image in your Azure functions deployment plan with the image you just pushed to the docker hub.