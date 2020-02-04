"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
#pages
from web.views import base_page , test , cell_phone , login_page , register_page , logout_page , error_page , setting_page
#functions
from web.views import getproductprice , getbutton , get_phone_data , get_new_celllp_data , get_brands , sign_in , sign_up , changePW


urlpatterns = [
    url(r'^$', base_page),
    url(r'^test/', test),
    url(r'^cell_phone/', cell_phone),
    url(r'^login_page/', login_page),
    url(r'^register_page/', register_page),
    url(r'^logout_page/', logout_page),
    url(r'^404/', error_page),
    url(r'^setting/', setting_page),

    url(r'^ajax/sign_in/$', sign_in),
    url(r'^ajax/sign_up/$', sign_up),
    url(r'^ajax/changePW/$', changePW),

    url(r'^ajax/getproductprice/$', getproductprice),
    url(r'^ajax/getbutton/$', getbutton),
    url(r'^ajax/get_phone_data/$', get_phone_data),
    url(r'^ajax/get_new_celllp_data/$', get_new_celllp_data),
    url(r'^ajax/get_brands/$', get_brands),

]
