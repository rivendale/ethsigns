![Ethsigns API](https://github.com/rivendale/ethsigns/workflows/Ethsigns%20API/badge.svg)

# [Ethereum Signs](https://ethsigns.com)


Ethereum - Chinese Zodiac - favorite projects - [Medium journal log](https://resourcehub.medium.com/ethereum-turn-based-strategy-game-and-nfts-working-draft-80f0f247b64e)
</br>
Chinese Zodiacs that can be minted (NFT) based on a user's birth date ([example](https://ethsigns.com/index/earth/pig/)).

As this isn't my primary area and with my limited time I haven't gotten that far other than to create a simple Flask app that my original intention was to create
a REST API for that could pull from a JavaScript front-end to interface with xDai.
This would just be for fun to compare personality traits ([Earth Pig](https://www.thechinesezodiac.org/astrology/zodiac-signs/pig/)).

This could then could morph into something more later, such as a way to import for games that would tilt towards which Zodiacs get along
([compatibility](https://en.wikipedia.org/wiki/Chinese_zodiac)) for team formation (and/or different starting skills based on personality traits).


Reference Links:

[thechinesezodiac.org](https://www.thechinesezodiac.org/)

[Chinese Zodiacs (Wikipedia)](https://en.wikipedia.org/wiki/Chinese_zodiac)



# SETUP NOTES

- There are two options to setup the application

---

<center>OPTION 1 (Manual setup)</center>

---

> > ### VIRTUAL ENVIRONMENT

---

**To Create:**

`make venv`

---

**To Activate:**

`make activate`

---

**Installing dependencies:**

`make install`

---

> > ### THE APPLICATION

---

**run application**

`make run`

---

**run linter**

`make lint`

---

**run tests**

`make test`

> > ### SQL ALCHEMY - DATABASE

---

**initialize the database**

`make init-db`

---

**Create new migrations**

`make migrate message="migration message"`

---

**update database**

`make update-db`

---

**undo last migration**

`make downgrade-db`

---

**seed database**

`make init-app`

> > ### SAVING WORK TO GIT

---

`git add .`

`git commit -m "comment"`

`git push origin main`

> > ### FLASK SHELL

`flask shell`

`exit()`

`db.drop_all()`

`db.create_all()`

---

<center>OPTION 2 (Set Up Development With Docker)</center>

---

1. Download Docker from [here](https://docs.docker.com/)
2. Set up an account to download Docker
3. Install Docker after download
4. Go to your terminal run the command `docker login`
5. Input your Docker email and password

To setup for development with Docker after cloning the repository please do/run the following commands in the order stated below:

- `cd <project dir>` to check into the dir
- `docker-compose build` or `make build` to build the application images
- `docker-compose up -d` or `make start` or `make start_verbose` to start the api after the previous command is successful

The `docker-compose build` or `make build` command builds the docker image where the api and its postgres database would be situated.
Also this command does the necessary setup that is needed for the API to connect to the database.

The `docker-compose up -d` or `make start` command starts the application while ensuring that the postgres database is seeded before the api starts.

The `make start_verbose` command starts the api verbosely to show processes as the container spins up providing for the visualization of errors that may arise.

To stop the running containers run the command `docker-compose down` or `make stop`

**To Clean Up After using docker do the following**

1. In the project directory, run the command `bash cleanup.sh` or `make clean`
2. Wait for all images to be deleted.

**URGENT WARNING** PLEASE DO NOT RUN THE CLEAN-UP COMMAND ABOVE UNLESS YOU ARE ABSOLUTELY SURE YOU ARE DONE WITH THAT DEVELOPMENT SESSION AND HAVE NO DATA THAT WOULD BE LOST IF CLEAN-UP IS DONE!

**Alternative cleanup method**

Instead of using the above command, you can delete images with the command `docker rmi repository:tag`

You can can run the command `docker images` to see the image **repository:tag** you may want to delete

---

---

> > ### VIRTUAL SERVER SETUP NOTES

`sudo apt-get update`

`sudo apt-get upgrade`

`sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools`

---

---

> > **FIREWALL**:

`sudo ufw allow OpenSSH`

`sudo ufw allow 5000`

`sudo ufw allow 5432`

`ufw enable`

`ufw status `
