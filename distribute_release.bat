aws s3 sync release/. s3://uvt-data-music-streaming/everynoise/releases --region eu-central-1  --exclude "*.*" --include "*.csv" 