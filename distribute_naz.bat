aws s3 sync release/. s3://uvt-streaming-phd/raw/sorthinghat_by_country/2021_03_12 --region eu-central-1 --exclude "*.*" --include "*new-release*"
aws s3 sync release/. uvt-streaming-phd/raw/playlist_promotion_by_country/2021_03_31/ --region eu-central-1 --exclude "*.*" --include "*promotions*"
