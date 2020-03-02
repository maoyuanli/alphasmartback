import json

from django.test import TestCase, RequestFactory

from .views import QuandlQuoteRestApiView


class ViewTests(TestCase):
    def test_get_index(self):
        self.factory = RequestFactory()
        request = self.factory.get('api/quote')
        qm_view = QuandlQuoteRestApiView()
        response = qm_view.get(request)
        rslt = json.loads(response.content)
        print(rslt)