#!/bin/bash

# Update and install dependencies
sudo apt-get update
sudo apt-get install -y python3-pip

# Install Python dependencies
pip3 install -r requirements.txt

# Export the environment variable for Flask app
export FLASK_APP=app.py

# Run the Flask application
python3 app.py