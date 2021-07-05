# Mini Project

## Prerequisites

It is advised to have a version of python 3.7 or above on the system and a Virtual Environment to run the flask development server.
A recent version of postman is preferred to test the server via HTTP 

## Instructions to run the flask server

 - Clone the repository
 - change directory to the flask app folder
 - run the virtual environment, if using pipenv, run the following code to start a shell in the current directory
 - `pipenv shell`
 -  pip install the required packages
 - run the following code in the terminal (with the virtual environment active) to point flask to the file that is to the app
 -  `export FLASK_APP=server.py`
 - run the following code to run the flask server on http://localhost:5000
 - `flask run`
## Pinging the server
send a get request to http://localhost:5000 using postman or any http testing client of choice to get a response 
