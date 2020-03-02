import tweepy
from django.http import JsonResponse
from rest_framework.views import APIView
from tweepy import OAuthHandler, API

from utils.fetch_token import TokenFetcher


class TweetRestApiView(APIView):
    token_fetcher = TokenFetcher('token.json')
    api_key = token_fetcher.fetch_token('api_key')
    api_secret = token_fetcher.fetch_token('api_secret')
    access_token = token_fetcher.fetch_token('access_token')
    access_secret = token_fetcher.fetch_token('access_secret')
    auth = OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret)
    tweet_src = ['marketwatch', 'wsj', 'ft', 'business', 'theeconomist', 'cnbc', 'barronsonline']

    def get(self, request):
        tweets_list = TweetRestApiView.generate_tweets()
        return JsonResponse({'tweets': tweets_list}, safe=False)

    @staticmethod
    def generate_tweets():
        api = API(TweetRestApiView.auth)
        search_query = TweetRestApiView.tweet_query_builder(TweetRestApiView.tweet_src)
        tweets = tweepy.Cursor(api.search, q=search_query, lang='en').items(200)
        tweets_json = []
        for tweet in tweets:
            tweets_json.append(tweet._json)
        return tweets_json

    @staticmethod
    def tweet_query_builder(sourc_list: list):
        from_prefix = 'FROM:'
        or_prefix = ' OR '
        query = ''
        for i, s in enumerate(sourc_list):
            if i != len(sourc_list) - 1:
                query = query + from_prefix + s + or_prefix
            else:
                query = query + from_prefix + s
        return query
