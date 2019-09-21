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
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
import homepage.views
import searchnews.views
import stockmarket.views
import feedback.views
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
index_html = os.path.join(os.path.dirname(BASE_DIR), 'build','index.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('django/home/', homepage.views.HomepageApiView.as_view()),
    # path('django/search/',searchnews.views.SearchNewsApiView.as_view()),
    path('api/homepage/',homepage.views.HomepageRestApiView.as_view()),
    path('api/searchnews/',searchnews.views.SearchNewsRestApiView.as_view()),
    path('api/stockmarket/',stockmarket.views.QuandlMarketRestApiView.as_view()),
    path('api/feedback/',feedback.views.FeedbackView.as_view()),
    # path('',TemplateView.as_view(template_name=index_html))
]