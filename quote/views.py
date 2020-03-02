from datetime import datetime, timedelta

import requests
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from utils.fetch_token import TokenFetcher


class QuandlQuoteRestApiView(APIView):
    renderer_classes = (JSONRenderer,)
    quandl_token = TokenFetcher('token.json').fetch_token('quandl_key')
    url_prefix = 'https://www.quandl.com/api/v3/datasets/EURONEXT/{0}.json?api_key={1}&start_date={2}&end_date={3}'
    tickers = ['ABN', 'ADYEN', 'INGA', 'KPN', 'RDSA', 'BNP']

    def get(self, request):
        start_date, end_date = self.start_end_dates(365)
        datasets = []
        for ticker in self.tickers:
            request_url = self.url_prefix.format(ticker, self.quandl_token, start_date, end_date)
            res = requests.get(request_url)
            dataset = res.json()
            datasets.append(dataset)
        return JsonResponse({'quotes': datasets}, safe=False)

    def start_end_dates(self, days_diff):
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days_diff)
        end_date_str = end_date.strftime('%Y-%m-%d')
        start_date_str = start_date.strftime('%Y-%m-%d')
        return (start_date_str, end_date_str)
