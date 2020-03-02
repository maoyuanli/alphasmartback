import json

from django.test import TestCase, RequestFactory

from .views import QuandlMarketRestApiView


class ViewTests(TestCase):
    def test_get_index(self):
        self.factory = RequestFactory()
        request = self.factory.get('api/stockmarket')
        qm_view = QuandlMarketRestApiView()
        response = qm_view.get(request)
        rslt = json.loads(response.content)
        sent_score = qm_view.get_sentiment_score()
        print(sent_score)
        print(rslt)