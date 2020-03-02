"""careerhub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.urls import path

import account.views
import feedback.views
import homepage.views
import order.views
import quote.views
import searchnews.views
import stockmarket.views
import tweet.views

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
index_html = os.path.join(os.path.dirname(BASE_DIR), 'build','index.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/homepage/',homepage.views.HomepageRestApiView.as_view()),
    path('api/searchnews/',searchnews.views.SearchNewsRestApiView.as_view()),
    path('api/stockmarket/',stockmarket.views.QuandlMarketRestApiView.as_view()),
    path('api/feedback/',feedback.views.FeedbackView.as_view()),
    path('api/quote/',quote.views.QuandlQuoteRestApiView.as_view()),
    path('api/tweet/',tweet.views.TweetRestApiView.as_view()),
    path('api/order/',order.views.OrderView.as_view()),
    path('api/register/', account.views.UserRegisterView.as_view()),
    path('api/login/',account.views.UserLoginView.as_view())
]
