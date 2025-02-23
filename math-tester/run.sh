
#!/bin/bash

# Install virtualenv if not installed
if ! command -v virtualenv &> /dev/null
then
    echo "virtualenv could not be found. Installing..."
    pip install virtualenv
fi

# Create a virtual environment
echo "Creating virtual environment..."
virtualenv venv

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install the required packages
echo "Installing required packages..."
pip install -r requirements.txt

# Run the Flask application
echo "Running the Flask application..."
python app.py
