import os
import urllib.request, json 
from time import sleep
from random import randint
from urllib.parse import urlparse
from pathlib import PurePath

print ("Starting...")

QUOTE_URL = "https://www.runtastic.com/check_export_quota"
DOWNLOADS = "/PATH/DOWNLOAD_ACTIVITIES"
LIST_FILE = '/PATH/TO/list.txt'

# https://www.runtastic.com/check_export_quota
quota_call = "curl 'https://www.runtastic.com/check_export_quota' -H 'authori...."

# Split curl headers
HEADERS = quota_call.split(' -H ')

# Get headers from curl-headers
def get_header(headers, param):
    # Cookie will look like:
    # 'cookie: locale=e......50ee1b--200' --compressed
    toSearch = "'{}".format(param)
    for h in headers:
        if h.startswith(toSearch,0,len(toSearch)):
            value = h.split("'")[1][8:]
            return value

# Return boolean based on quota, to determine if we can export new file or not.
def export_allowed():
    print ('Checking export_allowed...')
    req = urllib.request.Request(QUOTE_URL, headers={"cookie":get_header(HEADERS, 'cookie')})
    response = urllib.request.urlopen(req)
    export_quota = json.loads(response.read())
    return export_quota['export_allowed']

# From https://www.runtastic.com/en/users/XXXXXX/sport-sessions/1111111.gpx
# return 1111111.gpx
def get_file_name_from_url(url):
    url_file_path = urlparse(url).path # like /en/users/XXXXXX/sport-sessions/1111111.gpx
    return os.path.basename(url_file_path) # return 1111111.gpx

def download(url):
    print ('Downloading...')
    opener = urllib.request.build_opener()
    opener.addheaders = [('cookie', get_header(HEADERS, 'cookie'))]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, PurePath(DOWNLOADS, get_file_name_from_url(url)))

def check_file_exist(file_name):
    print("File name {}".format(file_name))
    file_path = PurePath(DOWNLOADS, file_name)
    print("Checking if file {} exist".format(file_path))
    return os.path.isfile(file_path)

f = open(LIST_FILE, "r")
line = f.readline().rstrip() # reading first line
while line:
    print("    Working with {}".format(line))
    file_name = get_file_name_from_url(line)
    if not check_file_exist(file_name):
        print("File do not exist")
        if export_allowed():
            download(line)
            sleep(randint(5,20))
        else:
            raise Exception('No export allowed') 
    print("    ---")
    line = f.readline().rstrip()
f.close()
