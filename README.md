# Dummy Tesserae API

This repo contains code for a dummy server that acts as a guide for expected behavior of an implementation of the Tesserae API.

## Installation

Set up and activate your Python environment and then install pre-requisite libraries:
```
python3 -m venv <environment name>
source <environment name>/bin/activate
pip3 install -r requirements.txt
```

If there is a bdist error when install the pre-requisite libraries, you can safely ignore it.

## Run the Development Server

Be sure that your environment is activated and pre-requisites have been installed.  Then start the flask server:
```
FLASK_APP=server.py python3 -m flask run
```

## Run Query Script

Again, be sure that your environment is activated and pre-requisites have been installed.  Then run the query script:
```
python3 run.py
```

## API Specification

Under construction
