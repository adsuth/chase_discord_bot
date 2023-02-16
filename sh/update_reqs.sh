NULL='\e[0m'
LIME='\e[0;32m'
RED='\e[31m'
YELO='\e[33m'
CYAN='\e[36m'

pip list --format=freeze > requirements.txt
echo -e "${LIME}Created requirements.txt !${NULL}"