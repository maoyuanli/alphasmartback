import os
import re
import string
from collections import Counter

import nltk
import pandas as pd
from django.http import JsonResponse
from newsapi import NewsApiClient
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import PorterStemmer
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from utils.fetch_token import TokenFetcher

cur_path = os.path.dirname(__file__)
par_path = os.path.dirname(os.path.dirname(cur_path))
nltk_data_path = os.path.join(par_path, 'static', 'nltk_data')
nltk.data.path.append(nltk_data_path)


class HomepageRestApiView(APIView):
    renderer_classes = (JSONRenderer,)
    token_fetcher = TokenFetcher('token.json')
    newsapi = NewsApiClient(api_key=token_fetcher.fetch_token('news_api'))

    def get(self, request):
        result_dict = self.newsapi.get_top_headlines(category='business', language='en', country='us')
        articles_dict_list = result_dict['articles']
        senti_with_topword = TopWords(articles_dict_list=articles_dict_list)
        sentilyzed_dict_list = senti_with_topword.get_topwords()
        return JsonResponse({'articles': sentilyzed_dict_list}, safe=False)


class Sentilyzer:
    def __init__(self, articles_dict_list):
        self.articles_dict_list = articles_dict_list

    def sentilyze(self):
        articles_df = pd.DataFrame(self.articles_dict_list)
        articles_df['clean_title'] = articles_df['title'].apply(lambda c: self.process_words(c, remove_punc=True))
        analyzer = SentimentIntensityAnalyzer()
        articles_df['sentiment'] = articles_df['clean_title'].apply(
            lambda t: analyzer.polarity_scores(t)['compound'] if t is not None else 'Null')
        sent_dict_list = articles_df.to_dict(orient='records')
        return sent_dict_list

    @staticmethod
    def process_words(raw, remove_punc=False, stem=False):
        link_pattern = [
            r'(http|https)://[a-zA-Z0-9\./]*\s',
            r'\s+(http|https)://[a-zA-Z0-9\./]*\s',
            r'\s+(http|https)://[a-zA-Z0-9\./]*$',
        ]
        if raw:
            clean = raw.lower().strip()
            for ptn in link_pattern:
                clean = re.sub(ptn, '', clean)
            if remove_punc:
                nopunc = [c for c in clean if c not in string.punctuation]
                raw = ''.join(nopunc)

            stopwords_list = []
            stopwords_list_en = set(stopwords.words('english'))
            stopwords_list_fr = set(stopwords.words('french'))
            stopwords_list.extend(stopwords_list_en)
            stopwords_list.extend(stopwords_list_fr)

            nostop = [w for w in raw.split() if w.lower() not in stopwords_list]
            if stem:
                stemmer = PorterStemmer()
                return ' '.join([stemmer.stem(t) for t in nostop])
            else:
                return ' '.join(nostop)


class TopWords(Sentilyzer):
    def get_topwords(self):
        sentilyzed = super().sentilyze()
        sentilyzed_df = pd.DataFrame(sentilyzed)
        sentilyzed_df['top_words'] = sentilyzed_df['clean_title'].apply(
            lambda s: self.top_words(s) if s is not None else '')
        clean_title_list = sentilyzed_df['clean_title'].to_list()
        clean_title_str = ' '.join(clean_title_list)
        sentilyzed_df['top_words_of_all'] = ','.join(self.top_words(clean_title_str))
        sentilyzed_df['title'] = sentilyzed_df['title'].apply(lambda t: self.title_reformat(t))
        dict_list = sentilyzed_df.to_dict(orient='records')
        return dict_list

    @staticmethod
    def top_words(s):
        noise = ['news', 'today', 'us', 'says', 'company', 'companys']
        words_list = s.split()
        filtered_word_list = list(filter(lambda w: w.lower() not in noise, words_list))
        counter = Counter(filtered_word_list)
        most_tuple = counter.most_common(3)
        most_list = [e[0] for e in most_tuple]
        return most_list

    @staticmethod
    def title_reformat(s):
        return re.sub(r'\s-\s*[^-]+$', '', s)
