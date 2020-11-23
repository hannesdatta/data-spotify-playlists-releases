# Documentation of "Playlist promotions and New Releases at Spotify (2019 - today)"

This is a repository which hosts the source code to scrape and prepare the public version of the data set:

Datta, Hannes, 2020, "Playlist promotions and New Releases at Spotify", https://doi.org/10.34894/0RK0KK, DataverseNL.

If you are...
- a (potential) user of the data, you can [download the data](https://doi.org/10.34894/0RK0KK), or view its detailed [documentation here](doc/). 
- part of the maintenance team, you can use this repository to update the dataset or its documentation.
- interested in creating your own reproducible workflows for anonymizing and sharing data with the public, you can use this repository as a template.

<!-- remove if necessary-->
__Note:__ The data set is not released to the public yet (expected mid of 2021). For questions, get in touch via email, please.
<!-- -->

## Overview about the data

This repository contains data collected with two webscrapers from everynoise.com. 

(1) **New releases**: A list of (weekly) album and single releases to Spotify, by country
![Screenshot](/doc/everynoise_newrelease_by_genre.png)

*The data is scraped from everynoise.com/new_releases_by_genre.cgi.*

(2) **Worldbrowser**: A list of "promoted"/"featured" playlists on Spotify, by playlist category, hour-of-the-day (if available), and country.

![Screenshot](/doc/everynoise_worldbrowser.png)

While the data is collected from everynoise.com/worldbrowser.cgi, the data *actually* comes directly from the Spotify Web API, which powers the *browse* interface of the Spotify platform.

![Screenshot of the playlist browse feature on Spotify](/doc/spotify_browse.png)

## Workflow for maintaining the data and its documentation

### Setup

- Obtain a valid API key from Dataverse ("API Token" in the main menu), and store it as a user's environment variable called DATAVERSE_TOKEN.
- Install Java
- Download the most recent version of the [Dataverse uploading tool](https://github.com/GlobalDataverseCommunityConsortium/dataverse-uploader/) (run `bash init.sh` on Mac, or paste the link contained in the file in your browser on Windows)


### File and directory structure

```
├── credentials.txt         <- stores API credentials
├── doc                     <- put any documentation here
│   └── readme-template.txt (start from this template)
├── rawdata-confidential    <- folder with confidential data
├── release                 <- folder with public releases
├── src                     <- source code 
│   └── collect                (data collection) 
│   └──                        (parsing and preparation for public release)
```

### Workflow

* __Archive confidential raw data on Dataverse__: `push_raw.sh` pushes the raw data to Dataverse (done once, `bash push_raw.sh`; or paste code into your command prompt on Windows). Remember to __restrict access to the folder__, by editing the file/directory permissions directly on Dataverse.

* __Add/change data preparation code__ (e.g., to anonymize data) in `src\`; run this code yourself to produce derivate datasets for the (to-be-made public) `release\` folder.

* __Release public versions__ of the data to Dataverse: `release.sh` pushes (updates) to the documentation in `doc\`, or the prepared data set in `release\`.

* Done? Publish your data set on Dataverse (via the web interface).

Note: API keys used in the `.sh` scripts is deprecated.


## Workflow for collecting the raw data 

### Setup

First, please install...
- Python distribution via Anaconda
- Scrapy (toolkit for webscraping)
  `pip install scrapy` 

Then, you can run the data collections:
- Run everynoise.py file (weekly)
`python everynoise.py`

- Run everynoise_worldbrowser.py file (hourly)
`python everynoise_worldbrowser.py`

### Documentation of output

The two webscrapers write the output of the data collections to JSON files.

(1) **New releases**

The data is written to new-line separated JSON files, named everynoise_newreleases_YYYYMMDD.json (whereas YYYYMMDD refers to the datestamp when the scraper was run. It lists the weekly releases to the Spotify platform by country. Each release is characterized by an albumId/albumName, and and associated artistName/artistId. The trackId in the data below represents a preview snipped of the album that users can click to listen to (a part) of the release. Singles are released as single-track albums.

*JSON file structure*

``` 
{
  "countryCode": "EC", # two-letter country code
  "trackId": "spotify:track:2rRhbOTbTwAUq45qdllfST", # Spotify track ID of a preview track of the album release
  "artistId": "spotify:artist:07YUOmWljBTXwIseAUd9TW", # Spotify artist ID of the album release
  "rank": "EC rank: 10", # Rank (probably popularity rank; exact definition is pending)
  "artistName": "Sebastián Yatra", # Artist name associated with album release
  "albumId": "spotify:album:2B4n5Uy0rYJ1btdqtUsrw8", # Spotify album ID
  "albumName": "Un Año (En Vivo)", # Album name
  "scrapeUnix": 1570447279, # Unix time stamp when the data was scraped
  "scrapeDate": "20191007", # Datestamp when the data was scraped
  "everynoiseDate": "20191004" # Date when track/album was released to Spotify
}

``` 

(2) **Worldbrowser**

The data is written to new-line separated JSON files, named everynoise_worldbrowser_YYYYMMDD__HHMM.json (whereas YYYYMMDD refers to the datestamp, and HHMM to the hour-minute timestamp when the scraper was run.


*JSON file structure*

```
{
  "sectionName": "featured",
  "countryName": "Global",
  "countryCode": "3",
  "playlistIdArray": [
    "spotify:playlist:37i9dQZF1DX3rxVfibe1L0",
    "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M",
    "spotify:playlist:37i9dQZF1DX1s9knjP51Oa",
    "spotify:playlist:37i9dQZF1DX0XUsuxWHRQd",
    "spotify:playlist:37i9dQZF1DX4pUKG1kS0Ac",
    "spotify:playlist:37i9dQZF1DWSXBu5naYCM9",
    "spotify:playlist:37i9dQZF1DWXRqgorJj26U",
    "spotify:playlist:37i9dQZF1DX7ZUug1ANKRP",
    "spotify:playlist:37i9dQZF1DWWQRwui0ExPn",
    "spotify:playlist:37i9dQZF1DWYmmr74INQlb",
    "spotify:playlist:37i9dQZF1DX2Nc3B70tvx0",
    "spotify:playlist:37i9dQZF1DWVViFqIfGGV7"
  ],
  "scrapeUnix": 1572350843,
  "scrapeDate": "20191029",
  "everyNoiseHour": "08:07am",
  "everyNoiseHourReference": "-23"
}
```

* SectionName: Playlist category, one of Featured, Top Lists, Pop, Hip-Hop, Mood, Decades, Country, Workout, Rock, Latin, Focus, Chill, Dance/Electronic, Tastemakers, R&B, Indie, Folk & Acoustic, Party, Wellness, Sleep, Classical, Jazz, Soul, Christian, Gaming, Romance, K-Pop, Anime, Pop culture, Arab, Desi, Afro, Comedy, Metal, Regional Mexican, Reggae, Blues, Punk, Funk, Student, Dinner, Black history is now, Spotify Singles, Commute, Kids & Family, Word, Yoga, Nature Sounds, Self love, Exercise, Meditation.
* CountryName: Country
* CountryCode: Country in numeric coding
* playlistIdArray: Spotify playlist IDs that were featured in a given category
* scrapeUnix: Unix timestamp of data retrieval (seconds passed since 1970-01-01, 00:00)
* scrapeDate: Date of data retrieval
* everyNoiseHour: Playlists from the *featured* category vary by hour of the day
* everyNoiseHourReference: Coding of everynoise hour category
