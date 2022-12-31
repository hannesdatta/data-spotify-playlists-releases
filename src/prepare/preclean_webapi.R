library(data.table)
library(stringi)

nrows = -1L

raw <- fread('../../temp/everynoise-new-releases.csv', nrows=nrows, quote = "", encoding = 'UTF-8', na.strings=c('NA','None'))

raw[, rank_cleaned:=as.numeric(gsub('^.*[:] ','', gsub(',', '', rank)))]

raw[, trackId:=gsub('spotify:track:','', trackId)]
raw[, artistId:=gsub('spotify:artist:','', artistId)]
raw[, albumId:=gsub('spotify:albumId:','', albumId)]

raw[, rank:=NULL]
setnames(raw, 'rank_cleaned','rank')

raw <- raw[!is.na(everyNoiseDate)]
raw[, date:=paste0(substr(everyNoiseDate,1,4),'-', substr(everyNoiseDate,5,6),'-', substr(everyNoiseDate,7,8))]

raw[, scrapeDate:=NULL]
raw[, everyNoiseDate:=NULL]

setnames(raw, tolower(colnames(raw)))

setcolorder(raw, c('date','countrycode','rank','trackid','artistid','albumid','artistname','albumname'))

dir.create('../../release')
fwrite(raw, '../../release/everynoise-new-releases.csv')
fwrite(raw[, grep('name',colnames(raw), invert=T, value=T),with=F], '../../release/everynoise-new-releases-no-titles.csv')

