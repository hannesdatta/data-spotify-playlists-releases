aws s3 sync s3://uvt-data-music-streaming/everynoise/raw/webapi-newreleases/ ../../rawdata-confidential/webapi-newreleases_json --region eu-central-1 --exclude "*" --include "*.json"