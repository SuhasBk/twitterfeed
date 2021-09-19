from tweepy import API, OAuthHandler
from django.conf import settings

consumer_key = settings.TWITTER_CREDENTIALS['KEY']
consumer_secret = settings.TWITTER_CREDENTIALS['SECRET']
token = settings.TWITTER_CREDENTIALS['TOKEN']
token_secret = settings.TWITTER_CREDENTIALS['TOKEN_SECRET']

auth = OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
auth.set_access_token(token, token_secret)
twitterAPI = API(auth)
