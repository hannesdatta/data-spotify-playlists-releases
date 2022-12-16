library(data.table)
dt=fread('everynoise-new-releases-no-titles.csv', nrows=-1L, select=c('date','albumid'))

dt <- dt[date<='2020-04-01']

albums = unique(dt$albumid)
albums = gsub('spotify:album:','',albums)

# shuffle
set.seed(1234)
albums = albums[order(runif(length(albums)))]

fwrite(albums, 'albums20221216.csv')
