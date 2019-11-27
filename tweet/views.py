from django.shortcuts import render

import tweepy
from tweepy import OAuthHandler, API
from django.http import JsonResponse
from rest_framework.views import APIView


class TweetRestApiView(APIView):
    auth = OAuthHandler('BhUKZxdqhPEylXHSG4dXl42TB',
                        'oxo2R7n47xBVnvyjojZuYfg4AfX7R7NgUPYNyZBQi8JsoUfjHs')
    auth.set_access_token('3225745957-jwvwQAWknVkZDSuHjwTDHcZIglDICUYZtSbjX9i',
                          'bhC6p8Q5niKg5zQpx6JTqTFWepeeSMBq8JsNscorfoNgk')
    tweet_src = ['marketwatch', 'wsj', 'ft', 'business', 'theeconomist', 'cnbc', 'barronsonline']

    def get(self,request):
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
    def tweet_query_builder(sourc_list:list):
        from_prefix = 'FROM:'
        or_prefix = ' OR '
        query = ''
        for i, s in enumerate(sourc_list):
            if i != len(sourc_list) -1:
                query = query + from_prefix + s + or_prefix
            else:
                query = query + from_prefix + s
        return query