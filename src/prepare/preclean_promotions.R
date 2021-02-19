library(data.table)
library(stringi)

raw <- fread('../../release/everynoise-playlist-promotions.csv', nrows=-1L)


# ever promoted?! / promotion intensity
#levs = levels(raw$countryCode)
#levs[which(!nchar(levs)==2)] <- 'GLOB'
#setattr(raw$countryCode,"levels",levs)

raw[!nchar(countryCode)==2, countryCode:='GLOB']

raw <- raw[nchar(as.character(playlist_id))==22] # keep only data w/ playlist IDs (others are not Spotify playlist IDs)

raw[sectionName=='test_latin', sectionName:='latin']

agg = raw[, list(1), by = c('scrapeDate', 'sectionName', 'countryCode', 'playlist_id')]
agg[, countryCode:=tolower(stri_trim(countryCode))]

# country codes
# from: https://github.com/datasets/country-codes/blob/master/data/country-codes.csv

countries <- fread('country_codes.csv', encoding = 'Latin-1', na.strings='')
countries[, countryCode:=tolower(stri_trim(Two_Letter_Country_Code))]
countries[, Continent_Name:=tolower(gsub(' ', '', Continent_Name))]


setkey(countries, countryCode)
setkey(agg, countryCode)
agg[countries, continent:=i.Continent_Name]
agg[countryCode=='glob', continent:='GLOB']

stopifnot(nrow(agg[is.na(continent)])==0)

tmp = dcast(agg, scrapeDate+sectionName+playlist_id~continent, value.var='V1', fill = 0, fun.aggregate=sum)


dates <- data.table(scrapeDate=unique(agg$scrapeDate))
dates[, date:=as.Date(as.character(scrapeDate), format = '%Y%m%d')]

setkey(dates, scrapeDate)
setkey(tmp, scrapeDate)

tmp[dates, date:=i.date]
tmp[, scrapeDate:=NULL]

setnames(tmp, 'sectionName', 'sectionname')

setcolorder(tmp, c('date','sectionname', 'playlist_id','GLOB'))

dir.create('../output/')
fwrite(tmp, '../output/promotions.csv')
