from django.test import TestCase, RequestFactory

from tweet.views import TweetRestApiView
import json


class ViewTests(TestCase):
    tweet_api = TweetRestApiView()

    def test_get(self):
        self.factory = RequestFactory()
        request = self.factory.get('api/stockmarket')
        response = self.tweet_api.get(request)
        rslt = json.loads(response.content)
        print(rslt)

    def test_tweet_query_builder(self):

        query = self.tweet_api.tweet_query_builder(['marketwatch', 'wsj', 'ft', 'business', 'theeconomist', 'cnbc', 'barronsonline'])
        print(query)

    def test_generate_tweets(self):
        tweets = self.tweet_api.generate_tweets()
        print(tweets)