#!/bin/bash
NULL='\e[0m'
LIME='\e[0;32m'
RED='\e[31m'
YELO='\e[33m'
CYAN='\e[36m'
UNSC='\e[4m'

if [ -f "env/Scripts/activate" ]; then
  echo -e "${NULL}Detected virtual environment. Done.${NULL}"
else
  echo -e "${YELO}File doesn't exist, creating a new virtual environment...${NULL}"
  python -m venv env
  echo -e "${LIME}Created virtual environment. ${NULL}"
fi 

echo -e "${CYAN}Activate by running -> ${UNSC}. env/Scripts/activate${NULL}"
echo 