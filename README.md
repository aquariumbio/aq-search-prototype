# pydent-jupyter
Assorted Jupyter notebooks for tasks using pydent 

## Requirements

* [Trident](https://github.com/klavinslab/trident)
* An Aquarium login

This library is designed to be run in Docker
* Install [Docker](https://www.docker.com/get-started)

Running in Docker eliminates the need to install Trident or manage your Python version. 

## Setup
### 1. Clone
[git](https://git-scm.com/) with the command

```bash
git clone git@github.com:dvnstrcklnd/pydent-scripts.git
cd pydent-scripts
```

### 2. Add credentials
In order to add credentials for your Aquarium instance(s), `cp util/secrets_template.json util/secrets.json`, and add your login and url information to the new file. You can have more than two instances, and the keys (e.g., `laptop` and `production`) can be changed to whatever you want them to be.

```json
{
  "laptop": {
    "login": "neptune",
    "password": "aquarium",
    "aquarium_url": "http://localhost/"
  },
  "production": {
    "login": "your_production_username",
    "password": "your_production_password",
    "aquarium_url": "production_production_url"
  }
}
```

### 3. Start Docker
```bash
docker-compose build # if running for the first time
docker-compose up
```
Then paste the provided url into a browser and navigate to the `work` directory.
