library(data.table)
library(stringi)

nrows=-1L
raw <- fread('../../temp/everynoise-playlist-promotions.csv', nrows=nrows)


raw[!nchar(countryCode)==2, countryCode:='GLOB']

raw <- raw[nchar(as.character(playlist_id))==22] # keep only data w/ playlist IDs (others are not Spotify playlist IDs)

raw[sectionName=='test_latin', sectionName:='latin']

agg = raw[, list(1), by = c('scrapeDate', 'sectionName', 'countryCode', 'playlist_id')]
agg[, countryCode:=tolower(stri_trim(countryCode))]

# country codes
# from: https://github.com/datasets/country-codes/blob/master/data/country-codes.csv

countries <- fread('country-codes.csv', encoding = 'UTF-8', na.strings='')

countries[, countryCode:=tolower(stri_trim(`ISO3166-1-Alpha-2`))]

countries[, Continent_Name:=tolower(gsub(' ', '', Continent))]


setkey(countries, countryCode)
setkey(agg, countryCode)
agg[countries, continent:=i.Continent_Name]
agg[countryCode=='glob', continent:='glob']


dates <- data.table(scrapeDate=unique(agg$scrapeDate))
dates[, date:=as.Date(as.character(scrapeDate), format = '%Y%m%d')]

setkey(dates, scrapeDate)
setkey(agg, scrapeDate)

agg[dates, date:=i.date]
agg[, scrapeDate:=NULL]


# only list whether it was listed, not how much?!
setcolorder(agg, c('countryCode','continent','sectionName', 'date','playlist_id'))

agg[, V1:=NULL]


stopifnot(nrow(agg[is.na(continent)])==0)

dir.create('../../release/')
fwrite(agg, '../../release/promotions.csv')

