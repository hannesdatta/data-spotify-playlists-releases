import json


# Open file
dirn = '../../rawdata-confidential/webapi-newreleases_json/*.json' # input files
csvfn='../../releases/webapi-new-releases.csv' # output file
csvtitlefn='../../releases/webapi-new-releases-acoustics.csv' # output file

acoustics = ['id','danceability','energy','key','loudness','mode','speechiness',
'acousticness','instrumentalness','liveness','valence','tempo','duration', 'time_signature']

import glob
import os
try:
	os.mkdir('../../releases')
except:
	print('directory exists')

files = []
for fn in glob.iglob(dirn):
    files.append(fn)


f=open(csvfn, 'w',encoding='utf-8')
f.write('albumid\trelease_date\tntracks\talbumgenres\n')
f.close()

g=open(csvtitlefn,'w',encoding='utf-8')
info = ['albumid']
for item in acoustics:
    info.append(item)
g.write('\t'.join(info)+'\n')
g.close()


def parse(line):

    obj=json.loads(line)

    id=obj.get('album').get('id')
    albgenres = ','.join(obj.get('album').get('genres'))
    rd=obj.get('album').get('release_date')
    ntracks=obj.get('album').get('tracks').get('total')


    f=open(csvfn, 'a',encoding='utf-8')
    f.write(id+'\t'+rd+'\t'+str(ntracks)+'\t'+albgenres+'\n')
    f.close()

    g=open(csvtitlefn,'a',encoding='utf-8')

    for chunk in obj.get('acoustic_attributes'):
        for tr in chunk.get('audio_features'):
            info = [id]
            for item in acoustics:
                try:
                    info.append(str(tr.get(item)))
                except:
                    info.append('NA')
            g.write('\t'.join(info)+'\n')
    g.close()

cnt=0

print('Getting data for ' +str(len(files))+' files')
for fn in files:
    cnt+=1
    #print(cnt)
    if cnt%1000==0: print(cnt) #print(fn)
    try:
        fi=open(fn, 'r',encoding='utf-8')
        parse(fi.read())
        fi.close()
    except:
        print('error: '+fn)