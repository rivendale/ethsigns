# Ethereum Signs - ETHSigns.com 
Ethereum - Chinese Zodiac - favorite projects - Medium journal log: https://resourcehub.medium.com/ethereum-turn-based-strategy-game-and-nfts-working-draft-80f0f247b64e
</br>
</br>
Chinese Zodiacs that can be minted (NFT) based on a user's birth date (example: https://ethsigns.com/index/earth/pig/). 
As this isn't my primary area and with my limited time I haven't gotten that far other than to create a simple Flask app that my original intention was to create
a REST API for that could pull from a JavaScript front-end to interface with xDai. 
This would just be for fun to compare personality traits (Earth Pig : https://www.thechinesezodiac.org/astrology/zodiac-signs/pig/). 
This could then could morph into something more later, such as a way to import for games that would tilt towards which Zodiacs get along
(compatibility- https://en.wikipedia.org/wiki/Chinese_zodiac)  for team formation (and/or different starting skills based on personality traits). 

</br>
Reference Links:
https://www.thechinesezodiac.org/

https://en.wikipedia.org/wiki/Chinese_zodiac </br>

# SETUP NOTES </br>

### VIRTUAL ENVIRONMENT </br>
sudo apt install python3-venv </br>
python3 -m venv venv </br>
**To Activate:** source venv/bin/activate </br>

### VIRTUAL SERVER SETUP NOTES &nbsp;
sudo apt-get update </br>
sudo apt-get upgrade </br>
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools </br>

**FIREWALL**: </br>
sudo ufw allow OpenSSH </br>
sudo ufw allow 5000 </br>
sudo ufw allow 5432 </br>
ufw enable </br>
ufw status </br>
