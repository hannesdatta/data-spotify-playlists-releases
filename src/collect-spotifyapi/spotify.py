# Download EchoNest data
# Currently only downloads album tracks from Spotify API and posts to mongo (also writes into file)

# Load required packages
import time
import os

import json
import requests

from ratelimit import limits, sleep_and_retry




import io
import time
from datetime import datetime
import os
from urllib.parse import parse_qs, urlparse
import boto3
import logging

bucket_name = "uvt-data-music-streaming"
bucket_dir = 'everynoise/raw/new-releases/'

def makedir(dirname):
        try:
            os.stat(dirname)
        except:
            os.mkdir(dirname)

makedir('output')


#########
# SETUP #
#########

# Authentication keys for Spotify's Web API: obtain these directly from Spotify, see https://developer.spotify.com/web-api/

client_id = os.getenv('SPOTIFY_CLIENT')
client_secret = os.getenv('SPOTIFY_SECRET')


##########################
# (1) Common functions #
##########################


expiry_time = 0

# get authentication token
def get_token():
    global client_id, client_secret
    grant_type = 'client_credentials'
    body_params = {'grant_type' : grant_type}
    url='https://accounts.spotify.com/api/token'
    response=requests.post(url, data=body_params, auth = (client_id, client_secret))
    expiry_time = time.time()+60*59 # expiry in 1 hour
    decoded = json.loads(response.text)
    token = decoded["access_token"]
    return token, expiry_time


@sleep_and_retry
@limits(calls=30, period=5)
def get_from_spotify(url):
    global expiry_time, token
    
    timestamp = time.time() 
    if timestamp > expiry_time: (token, expiry_time) = get_token()
    headers = {'Authorization': 'Bearer ' + token}
    r = requests.get(url, headers=headers)
    status_code = r.status_code
    data = r.json()
    data['status_code'] = status_code
    data['timestamp'] = timestamp
    return(data)



# function to backup on S3
def uploadToS3(filepath, filename):

    logging.info("Trying to upload to S3 file... %s", filename)

    # uploads the file via a managed uploader, which will split up large files automatically and upload in parallel
    try:
        s3.upload_file(filepath, bucket_name, filename)
        logging.info("Upload to S3 OK.")
        return True
    except boto3.exceptions.S3UploadFailedError as e:
        logging.critical("Upload to S3 ERROR.", exc_info=True)
        return False

########
# CODE #
########https://open.spotify.com/album/4JIrN4EZdXCpfT0y3OCsq3?si=nGMFc5d4Tyq3cddVAdGHnQ

def get_album(id):

    album=get_from_spotify('https://api.spotify.com/v1/albums/'+id)

    # assess whether extra queries for tracks need to be done
    album.get('tracks').get('limit')
    
    more_tracks = []
    if album.get('tracks').get('next') is not None:
        next_url = album.get('tracks').get('next')
        while next_url is not None:
            next_tracks=get_from_spotify(next_url)
            more_tracks.append(next_tracks)
            next_url = next_tracks.get('next')
    
    # retrieve all track ids to retrieve acoustic attributes
    track_ids = []
    for track in album.get('tracks').get('items'): track_ids.append(track.get('id'))

    for nexttracks in more_tracks:
        for track in nexttracks.get('items'): track_ids.append(track.get('id'))
    
    # split in chunks of 50    
    track_chunks = [track_ids[i:i + 50] for i in range(0, len(track_ids), 50)]

    acoustics = []
    for items in track_chunks:
        audio = get_from_spotify('https://api.spotify.com/v1/audio-features/?ids='+','.join(items))
        acoustics.append(audio)
        
    res = {'album': album, 'more_tracks': more_tracks, 'acoustic_attributes': acoustics}
    f=open('output/' + id+'.json','w',encoding='utf-8')
    f.write(json.dumps(res))
    f.close()

    return(res)


#res=get_album('3tx7gfr0MqTzooGk00l9tB')

##########################
# (0) Auxilary functions #
##########################

# Print iteration progress (from https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console)
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()


# load albums
f=open('albums20221216.csv','r')
con=f.readlines()
albumids = []
for i in con[1:]: albumids.append(i.replace('\n',''))
f.close()

# load available file names
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir('output') if isfile(join('output/', f))]
availids = []
for o in onlyfiles: availids.append(o.replace('.json',''))

albumupt = list(set(albumids).difference(set(availids)))


it=0
tot=len(albumupt)
for id in albumupt:
    it+=1
    printProgressBar(it,tot)
    get_album(id)