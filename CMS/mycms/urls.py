from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import render, redirect

app_name = 'mycms'
from mycms.views import *

urlpatterns = [
    path('index/', index, name='index'),
    path('detail/<id>/', detail, name='detail'),
    path('comments/', pub_comment, name='comments'),
    path('category/<id>', show_category),
    path('person_category/<id>', person_category),
    path('pub_content/', pub_content),
    path('pub_success/', pub_success),
    path('login_in/', login_in),
    path('personinfo/', Person_info),
    path('change_password/',changepassword),
    path('manage/',manage,name = 'manage'),
    # path('person_cms/',person_cms),
    # path('person_category/',person_category),
    path('delete/<id>',delete_cms),
    path('changeinfo/',change_info),
    path('search/',search),
    path('search_q/',search_q),
]
