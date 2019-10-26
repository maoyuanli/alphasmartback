from datetime import datetime, timedelta
import pandas as pd
import quandl
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from homepage.views import HomepageRestApiView
import json


class QuandlMarketRestApiView(APIView):
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        score = self.get_sentiment_score()
        need_positive = True
        if score < 0:
            need_positive = False
        rslt = self.index_return(need_positive)
        return JsonResponse({'market_return': rslt}, safe=False)

    def index_return(self, need_positive: bool):
        three_month_back = datetime.now() - timedelta(days=90)
        qdf = quandl.get("NASDAQOMX/XQC", authtoken="f_tQibQDxz8s2CABjKZU",
                         start_date=three_month_back.strftime('%Y-%m-%d'))
        qdf.sort_index(ascending=False, inplace=True)
        nonzero_qdf = qdf[qdf['Index Value'] != 0]
        idx_val = nonzero_qdf['Index Value']
        latest = idx_val[0]
        rest = idx_val[1:]

        change_sets = {}

        for i, v in rest.items():
            benchmark = v
            change = latest / benchmark - 1
            timeframe = (idx_val.index[0] - i).days
            rslt_dict = {'change': change, 'latest_date': idx_val.index[0].date().strftime('%Y-%m-%d'),
                         'latest_val': latest,
                         'benchmark_date': i.date().strftime('%Y-%m-%d'), 'benchmark_val': v, 'timeframe': timeframe}
            if len(change_sets) < 2:
                if change > 0:
                    change_sets['positive'] = rslt_dict
                elif change < 0:
                    change_sets['negative'] = rslt_dict
            else:
                break
            latest = rest[i]

        if need_positive:
            return change_sets['positive']
        else:
            return change_sets['negative']

    def get_sentiment_score(self):
        homepage_view = HomepageRestApiView()
        homepage_rslt = homepage_view.get(request='api/homepage/')
        homepage_rslt_dict = json.loads(homepage_rslt.content)
        homepage_rslt_df = pd.DataFrame.from_records(homepage_rslt_dict['articles'])
        sent_col_df = homepage_rslt_df[['sentiment']]
        avg_sent_score = sent_col_df.mean(axis=0, skipna=True)[0]
        return avg_sent_score
