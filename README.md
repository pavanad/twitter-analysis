# Twitter analysis
Applying data science to twitter api

## Install requirements

```bash
pipenv install
python -m textblob.download_corpora
```
## Run MongoDB in docker

```bash
docker run -d -p 27017:27017 --name mongo_twitter mongo
```

## Set keys and tokens Twitter API
```
consumer_key
consumer_secret
access_token
access_token_secret
```