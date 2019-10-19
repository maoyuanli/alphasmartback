from datetime import datetime, timedelta
import requests
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView


class QuandlQuoteRestApiView(APIView):
    renderer_classes = (JSONRenderer,)
    urlPrefix = 'https://www.quandl.com/api/v3/datasets/EURONEXT/{0}.json?api_key=f_tQibQDxz8s2CABjKZU&start_date={1}&end_date={2}'
    tickers = ['ABN', 'ADYEN', 'INGA', 'KPN', 'RDSA', 'BNP']

    def get(self, request):
        start_date, end_date = self.start_end_dates(365)
        datasets = []
        for ticker in self.tickers:
            request_url = self.urlPrefix.format(ticker, start_date, end_date)
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
