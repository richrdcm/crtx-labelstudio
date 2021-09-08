#!/bin/bash

# 1. Check if .env file exist
echo "Setting enviroment variables"
if [ -e .env ]; then
    source .env
else
    echo "Please set up your .env file before starting your environment."
    exit 1
fi
echo "done"

## 2. Start the label-studio container
echo "Running docker-compose"
docker-compose up
echo "done"

# Wait for label studio
# sleep 10
#echo "Waiting for Label-studio"
#while ! nc -z $LS_HOST $LS_PORT; do
#  echo "waiting for Label-Studio ..."
#  sleep 0.5 # wait for 1/10 of the second before check again
#done
#echo "LS is online"

# 3. Run the initial setup
#echo "Setting up the database"
#python src/wakeup/dataset_initial_config.py
#echo "done"