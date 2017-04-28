import random
import requests
from bs4 import BeautifulSoup
import re

# SOME NEEDED TOOLS
# sudo apt-get install python-pip
# sudo pip install --upgrade pip
# sudo pip install requests
# sudo pip install beautifulsoup4

# SOME MAYBE NOT NEEDED TOOLS
# import urllib
# import urllib2
# import urlparse
# import sys

# CONFIG VARIABLES #############################################################
number_of_ingest = 1
server = 'http://localhost:8080/ingest/addMediaPackage/fast'
digest_login = 'opencast_system_account:CHANGE_ME'
video_file = '/home/eugen/Downloads/video.mp4'
names_file = 'names.txt'
excuses_file = 'excuses.txt'
languages_file = 'languages.txt'
mode = 'r'

# RANDOM NAME FROM FILE (NAME) #################################################
list_names = open(names_file, mode)
names = list_names.readlines()
names = [x.strip() for x in names]
list_names.close()

# RANDOM EXCUSE FROM FILE (TITLE) ##############################################
list_excuses = open(excuses_file, mode)
excuses = list_excuses.readlines()
excuses = [x.strip() for x in excuses]
list_excuses.close()

# RANDOM LANGUAGE FROM FILE (LANGUAGE) #########################################
list_languages = open(languages_file, mode)
languages = list_languages.readlines()
languages = [x.strip() for x in languages]
list_languages.close()


# DEBUG INFORMATION GENERATOR #################################################
# print(random.choice(excuses))
# print(random.choice(names))
# print(random.choice(languages))

# TRANSLATE METHOD #############################################################
def translate_string(str_to_translate):
    language = random.choice(languages)
    url = 'http://translation2.paralink.com/do.asp'
    payload = {'src': str_to_translate, 'dir': 'en/' + language, 'provider': 'microsoft', 'ctrl': 'target'}
    headers = {}
    res = requests.post(url, data=payload, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    # print soup.prettify()
    translated_string = re.findall(r'"([^"]*)"', soup.script.string)
    if len(translated_string[0]) == 0:
        return str_to_translate
    else:
        return translated_string[0]


# VARIABLES FOR INGEST #########################################################
metadata_language = random.choice(languages)
metadata_name = random.choice(names)
metadata_title = translate_string(random.choice(excuses))
metadata_description = translate_string(random.choice(excuses))
metadata_license = translate_string(random.choice(excuses))
metadata_source = translate_string(random.choice(excuses))
metadata_subject = translate_string(random.choice(excuses))
metadata_contributor = translate_string(random.choice(excuses))
metadata_rightsholder = translate_string(random.choice(excuses))

# INGEST MEDIA #################################################################
print digest_login
print server
print video_file
print metadata_title
print metadata_name

# Wie kann man das in Python umsetzen?
# curl -f -i --digest -u ${DIGEST_LOGIN} \
#	-H "X-Requested-Auth: Digest" \
#	"${SERVER}/ingest/addMediaPackage/fast" \
#  	-F flavor="presenter/source" \
#  	-F "BODY=@${VIDEO_FILE}" -F title="${TITLE}" \
#  	-F creator="${NAME}" \
#  	-F description="${DESCRIPTION}" \
#  	-F language="${LANGUAGE}" \
#  	-F license="${LICENSE}" \
#  	-F source="${SOURCE}" \
#  	-F subject="${SUBJECT}" \
#  	-F contributor="${CONTRIBUTOR}" \
#  	-F rightsHolder="${RIGHTSHOLDER}"
