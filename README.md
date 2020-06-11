# DaVi-Dash-App

Die Applikation kann direkt unter [DaVi-Dash-App](http://imsand.teamserver.ch:8842/) getestet werden.

## Installation

Voraussetzung ist **Ubuntu 18.04.4 LTS!**

In einem Terminal die folgenden Befehle ausführen:

```
# Install needed packages
sudo apt-get install python3-pip python3.8-venv python3.8-dev git

# Checkout sources
git clone https://github.com/iwanimsand/ffhs-semarb-statda-davi-public-app.git
cd ffhs-semarb-statda-davi-public-app

# Create and activate virtual python environment
python3.8 -m venv ~/.virtualenvs/ffhs/semarb-davi
source ~/.virtualenvs/ffhs/semarb-davi/bin/activate

# Install packages
pip install -r requirements.txt

# Run server
gunicorn --bind 0.0.0.0:8842 \
  --daemon \
  --pid gunicorn.pid \
  --access-logfile access.log \
  --log-file gunicorn.log \
  --log-level info \
  --threads 2 \
  --workers 2 \
  app:server && tail -f gunicorn.log

# Open browser and navigate to http://localhost:8842
```
