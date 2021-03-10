import json

# Open file
dirn = '../../rawdata-confidential/new-releases/*.json' # input files
csvfn='../../temp/everynoise-new-releases.csv' # output file

import glob
import os
try:
	os.mkdir('../../temp')
except:
	print('directory exists')

     

fn='../externals/newreleases\everynoise_newreleases_20200413.json'

# Read file line-by-line


variables = ['countryCode', 
     'trackId',
     'artistId', 
     'albumId',
     'rank',
     'artistName',
     'albumName',
     'everyNoiseDate',
     'scrapeDate']

def parse(line):
    chunkobj = json.loads(line.replace('\n',''))
    
    #for var in variables:
    #    print(str(chunkobj.get(var)))
    
    for var in variables:
        out.write(str(chunkobj.get(var)))
        if not var==variables[-1]: out.write('\t')
    out.write('\n')

def parse_file(fn):
  items = open(fn, 'r', encoding = 'utf-8')
  for line in items.readlines():
      parse(line)  
  items.close()
  
  
cnt=0

out=open(csvfn, 'w', encoding='utf-8')

for var in variables:
    out.write(var)
    if not var==variables[-1]: out.write('\t')
out.write('\n')
    
for fn in glob.iglob(dirn):
    cnt+=1
    print(fn)
    #if (cnt>10): break
    parse_file(fn)
    
out.close()
print('done.')