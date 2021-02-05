# ethsigns
Ethereum - Chinese Zodiac - favorite projects - Medium journal log: https://resourcehub.medium.com/ethereum-turn-based-strategy-game-and-nfts-working-draft-80f0f247b64e

Chinese Zodiacs that can be minted (NFT) based on a user's birth date (example: https://ethsigns.com/index/earth/pig/). As this isn't my primary area and with my limited time I haven't gotten that far other than to create a simple Flask app that my original intention was to create a REST API for that could pull from a JavaScript front-end to interface with xDai. This would just be for fun to compare personality traits (Earth Pig : https://www.thechinesezodiac.org/astrology/zodiac-signs/pig/) and then could morph into something more later, such as a way to import for games that would tilt towards which Zodiacs get along (compatibility- https://en.wikipedia.org/wiki/Chinese_zodiac)  for team formation (and/or different starting skills based on personality traits). 

Reference Links:
https://www.thechinesezodiac.org/

https://en.wikipedia.org/wiki/Chinese_zodiac

# SETUP NOTES

### VIRTUAL ENVIRONMENT
sudo apt install python3-venv
python3 -m venv venv
**To Activate:** source venv/bin/activate

### VIRTUAL SERVER SETUP NOTES
sudo apt-get update

sudo apt-get upgrade

sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools

**FIREWALL**:
sudo ufw allow OpenSSH

sudo ufw allow 5000

sudo ufw allow 5432

ufw enable

ufw status
