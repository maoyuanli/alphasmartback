from django.shortcuts import render
from newsapi import NewsApiClient
from rest_framework.views import APIView
from homepage.views import Sentilyzer
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse

newsapi = NewsApiClient(api_key='0cd11b45ffd949eaa03bbdbd23c5f95f')


class SearchNewsApiView(APIView):
    def get(self, request):
        qry = request.GET.get('q')
        if qry:
            result_dict = newsapi.get_everything(q=self.query_builder(qry), sort_by='relevancy', language='en', page=5)
            articles_dict_list = result_dict['articles']
            sentilyzer = Sentilyzer(articles_dict_list=articles_dict_list)
            sentilyzed_dict_list = sentilyzer.sentilyze()
            return render(request, 'searchnews/searchnews.html', {'articles': sentilyzed_dict_list})
        else:
            return render(request, 'searchnews/searchnews.html')

    def query_builder(self, query: str):
        keywords = query.split(' ')
        keywords = [kw.strip() for kw in keywords if len(kw)>0]
        print(keywords)
        return ' AND '.join(keywords)

class SearchNewsRestApiView(SearchNewsApiView):
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        qry = request.GET.get('q')
        print(qry)
        result_dict = newsapi.get_everything(q=self.query_builder(qry), sort_by='relevancy', language='en', page=2)
        articles_dict_list = result_dict['articles']
        sentilyzer = Sentilyzer(articles_dict_list=articles_dict_list)
        sentilyzed_dict_list = sentilyzer.sentilyze()
        return JsonResponse({'articles': sentilyzed_dict_list}, safe=False)

