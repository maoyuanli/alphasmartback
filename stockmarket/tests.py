from django.test import TestCase, RequestFactory
from .views import QuandlMarketRestApiView
import json


class ViewTests(TestCase):
    def test_get_index(self):
        self.factory = RequestFactory()
        request = self.factory.get('api/stockmarket')
        qm_view = QuandlMarketRestApiView()
        response = qm_view.get(request)
        rslt = json.loads(response.content)
        print(rslt)