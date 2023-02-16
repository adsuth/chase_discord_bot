#!/bin/bash
version=$(python -V 2>&1 | grep -Po '(?<=Python )(.+)')

NULL='\e[0m'
LIME='\e[0;32m'
RED='\e[31m'
YELO='\e[33m'
CYAN='\e[36m'

# check if python is installed
if [[ -z "$version" ]]
then
  echo -e "${RED}Couldn't find Python... Abort.${NULL}" 
  echo 
  exit 727
fi

# prompt user if they arent in venv
if [ "$VIRTUAL_ENV" == "" ];
then
  echo -e "This will install dependencies ${YELO}outside of a Virtual Environment.${NULL}"
  read -p "Are you sure? [y/N] > " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]
  then
    echo -e "${CYAN}You can create a Virtual Environment using the venv.sh script.${NULL}"
    echo 
    exit 1
  fi
fi

echo -e "${YELO}Getting Dependencies${NULL}"
python -m pip install -r requirements.txt
echo -e "${LIME}Retrieved Dependencies!${NULL}"
echo 