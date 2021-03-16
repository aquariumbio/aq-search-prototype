# Aquarium Sample Search Prototype
Flask-based prototype for Aquarium search

## Requirements

This library is designed to be run in Docker
* Install [Docker](https://www.docker.com/get-started)

## Setup
### 1. Clone
Clone using [git](https://git-scm.com/) with the command

```bash
git clone https://github.com/aquariumbio/aq-search-prototype.git
cd aq-search-prototype
```

### 2. Change the Database
Aquarium database files are stored in data/db, which allows the database to persist between runs. If this directory is empty, such as the first time this app is run, the database is initialized from the database dump `data/mysql_init/dump.sql`. If the dump file does not already exist, then run

```bash
mv data/mysql_init/default.sql data/mysql_init/dump.sql
```

You can use a different database dump by renaming it to this file with

```bash
mv data/mysql_init/dump.sql data/mysql_init/dump-backup.sql
mv my_dump.sql data/mysql_init/dump.sql
```
then removing the contents of the data/db directory

```bash
rm -rf data/db/*
```

### 3. Start with Docker Compose
```bash
docker-compose build # if running for the first time
docker-compose up
```

### 4. Open in a browser
Point a browser to `http://0.0.0.0:5000/`. You should see a page titled **Search Samples**.
