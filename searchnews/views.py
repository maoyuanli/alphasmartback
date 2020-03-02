from django.http import JsonResponse
from newsapi import NewsApiClient
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from homepage.views import Sentilyzer
from utils.fetch_token import TokenFetcher


class SearchNewsRestApiView(APIView):
    token_fetcher = TokenFetcher('token.json')
    newsapi = NewsApiClient(api_key=token_fetcher.fetch_token('news_api'))
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        qry = request.GET.get('q')
        result_dict = self.newsapi.get_everything(q=self.query_builder(qry), sort_by='relevancy', language='en', page=2)
        articles_dict_list = result_dict['articles']
        sentilyzer = Sentilyzer(articles_dict_list=articles_dict_list)
        sentilyzed_dict_list = sentilyzer.sentilyze()
        return JsonResponse({'articles': sentilyzed_dict_list}, safe=False)

    def query_builder(self, query: str):
        keywords = query.split(' ')
        keywords = [kw.strip() for kw in keywords if len(kw) > 0]
        return ' AND '.join(keywords)
