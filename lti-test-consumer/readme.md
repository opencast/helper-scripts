Opencast LTI Test Consumer
==========================


Run Consumer
------------

```sh
# optionally setup virtual environment
virtualenv venv
. ./venv/bin/activate

# install requirements
pip install -r requirements.txt

# run test consumer
python3 lticonsumer.py
```

Configuration
-------------

You can configure some some basic settings by editing the following variables in
`lticonsumer.py`:

```
CONSUMER_KEY = 'CONSUMERKEY'
CONSUMER_SECRET = 'CONSUMERSECRET'
LAUNCH_URL = 'http://localhost:8080/lti'
```
