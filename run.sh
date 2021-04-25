#!/usr/bin/bash

# go into the application directory
if [ $# -ne 1 ]; then
  APP=$(pwd)
else
  APP=$1
fi

cd $APP
echo "You are in the directory $APP"

# export path, install libraries and run the server
echo "Setting up the server..."
export FLASK_APP=chat_room
pip install -e .
echo "Starting the server..."
flask run
