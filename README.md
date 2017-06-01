# mlc

## Prerequisites

* ```docker``` version 17.04 or higher.
* ```docker-compose``` version 1.9.0 or higher
* ```python3.3```
* ```pip```

## Preparing the environment

First, download and install ```docker```:
```
curl -sSL get.docker.com | sudo sh # also follow the instruction on your screen
```

Then, download and install ```docker-compose```:
```
sudo -i
curl -L https://github.com/docker/compose/releases/download/1.12.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
exit
```

Also, install python3 and pip3:

For Debian distributions:
```
sudo apt-get install python3 python3-pip
```

For Redhat distributions:
```
sudo yum install python3 python3-pip
```

## Installation

Download the release and extract to a directory of your choice

In the terminal, change the working directory to the location of your extracted files. Then:
```
docker-compose up -d # starts the database on localhost:5432, also creating the database directory where your database related data is stored
```

## Deploying

To run the admin server use: ```./runAdminServer.py```. This will start the admin web server on localhost:8081
To run the backend server use: ```./rundBackendServer.py```. This will start the backend server on localhost:8080


## For developers:

### Precommit hooks

Add pre-hook before commiting:
 * install ```pep8``` and ```pyflakes```
 * run ```chmod 755 hooks/pre-commit```
 * run ```ln hooks/pre-commit .git/hooks/pre-commit```

This checks your python code and helps the team write quality code!


### Preparing the database and the connection

Inside the DB folder, there is a file named config.json.example. First you must create a copy of the file inside the same folder named config.json:
```
cp config.json.example config.json
```

Then edit the config file, specifying your desired parameters.

To create the user and the database for the first time inside the docker container:
```
docker exec -it mlc_db_1 bash
su postgres
createuser --username=postgres --pwprompt <<desired user name>> # you will be prompted for a password here
createdb --username=postgres --owner=<<desired user name>> <<desired database name>>
psql --username=postgres --dbname=<<desired database name>> --command='ALTER SCHEMA public OWNER TO <<desired user name>>'
exit
exit
```
