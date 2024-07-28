# Contract Conditions Extraction and Verification

## Overview
This project is a Flask web application designed to extract and verify contract conditions against a set of tasks. It leverages OpenAI's API to analyze contract documents and task lists, providing a user-friendly interface for uploading documents and viewing compliance results.

## Features
Contract Conditions Extraction: Parses contract documents (including amendments) to extract key terms and conditions.
Task Compliance Verification: Analyzes tasks against the extracted contract conditions, determining compliance and providing reasons for non-compliance.
User Interface: A web interface for uploading contract and task files and displaying analysis results.
Deployment: Hosted on PythonAnywhere for easy access.

## Project Structure
project-directory/
│
├── app.py                  # Main application file
├── requirements.txt        # Dependencies file
├── .env                    # Environment variables (not included in repository for security)
└── templates/
    └── index.html          # HTML template for the web interface


## Setup and Installation
### Prerequisites
  - Python 3.6 or higher
  - pip (Python package installer)
  - OpenAI API Key

### Virtual Environment Setup
1. Create a Virtual Environment:
  python3 -m venv ~/.virtualenvs/myvenv

2. Activate the Virtual Environment:
  source ~/.virtualenvs/myvenv/bin/activate

3. Install Dependencies:
  pip install -r requirements.txt

### Configuration
1. Set Environment Variables:
  - Add your OpenAI API key to a .env file or set it in the environment:
    OPENAI_API_KEY=your_openai_api_key_here

2. Configure WSGI File:
Ensure the WSGI file is set up correctly to point to your Flask app. Example configuration:

  import sys
  import os
  
  project_home = '/home/yourusername/yourprojectname'
  if project_home not in sys.path:
      sys.path.append(project_home)
  
  activate_this = os.path.expanduser('/home/yourusername/.virtualenvs/myvenv/bin/activate_this.py')
  with open(activate_this) as f:
      exec(f.read(), dict(__file__=activate_this))
  
  from app import app as application


## Usage
1. Run the Application:
  To start the Flask application locally, run:
    flask run

2. Access the Web Interface:
  Visit http://127.0.0.1:5000 in your web browser to access the application. Upload the contract and task files, and the application will display the analysis results.
