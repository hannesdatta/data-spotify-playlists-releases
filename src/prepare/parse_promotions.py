import json

# Open file
dirn = '../../rawdata-confidential/promotions/*.json' # input files
csvfn='../../release/everynoise-playlist-promotions.csv' # output file


import glob


fn='../externals/worldbrowser\everynoise_worldbrowser_20200129_1510.json'

# Read file line-by-line


variables = ['sectionName', 
     'countryName',
     'countryCode',
     'scrapeUnix',
     'scrapeDate',
     'everyNoiseHour',
     'everyNoiseHourReference']

def parse(line):
    chunkobj = json.loads(line.replace('\n',''))
    
    
    count=0
    for playlist in chunkobj.get('playlistIdArray'):
        count+=1
        for var in variables:
            out.write(str(chunkobj.get(var))+'\t')
        out.write(str(count)+'\t')
        out.write(playlist.replace('spotify:playlist:','')+'\n')

def parse_file(fn):
  items = open(fn, 'r')
  for line in items.readlines():
      parse(line)  
  items.close()
  
  
cnt=0

out=open(csvfn, 'w', encoding='utf-8')

for var in variables:
    out.write(var+'\t')
out.write('count\tplaylist_id\n')

for fn in glob.iglob(dirn):
    cnt+=1
    print(fn)
    #if (cnt>10): break
    parse_file(fn)
    
out.close()
print('done.')