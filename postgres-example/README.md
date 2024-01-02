# Postgres example deployment
This repository is an example of deploying a Postgres database with NetBird in a docker host using `docker compose`.

## Requirement
- Docker
- Docker compose
- A NetBird network and a setup key

## Add the setup key
Update the docker-compose.yml file with your setup key:
```yaml
    environment:
      - NB_SETUP_KEY=<your setup key>
```

## Run the container
Run the container using the following command:
```bash
docker compose up -d
```

## Connect to the database and create the example table
You can connect to the database using the following commands:
```bash
docker compose exec -ti postgres bash
su -l postgres
psql
```

### Create the database table
Create the table using the following statement:
```sql
CREATE TABLE visits (
        id SERIAL PRIMARY KEY,
        ip_address VARCHAR(255),
        visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Remove the container
Remove the container using the following command:
```bash
docker compose down
```

