# Aquarium Sample Search and Data Browser Prototype
Flask-based prototype for searching samples and browsing data in Aquarium

## Requirements

This app is designed to be run in Docker
* Install [Docker](https://www.docker.com/get-started)

## Setup
### 1. Clone
Clone using [git](https://git-scm.com/) with the command

```bash
git clone https://github.com/aquariumbio/aq-search-prototype.git
```

### 2. Get a production database
This app is designed to work with a full database, and has no provision for adding data. The first time this app is run, the database is initialized from the database dump `data/mysql_init/dump.sql`. Although this file exists in the cloned repo, you will need to replace it with a dump of a full database. You can get one [here](https://drive.google.com/file/d/1w1CSL8YZygU94c6i_z5BdInW4SH4geVe/view?usp=sharing). (Ask for access if you don't have it already.) Copy this file to `data/mysql_init` and
then remove any contents of the data/db directory with the following command:

```bash
rm -rf data/db/*
```
**Note:** If you are running a large database, such as the BIOFAB production database, the app will be very slow if the database is not indexed. Please ask for help if you notice page loads of more than a few seconds.

### 3. Start with Docker Compose
```bash
docker-compose build # if running for the first time
docker-compose up
```

### 4. Open in a browser
Point a browser to `http://0.0.0.0:5000/`. You should see a page titled **Contents** that has links to the sample search and data browser pages.
