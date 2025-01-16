from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('careers/', views.careers, name='careers'),
    path('video/', views.video_list, name='video'),
    path('solutions/', views.solutions, name='solutions'),
    path('bank/', views.bank, name='bank'),
    path('cookies/', views.cookies, name='cookies'),
    path('hospital/', views.hospital, name='hospital'),
    path('hotel/', views.hotel, name='hotel'),
    path('school/', views.school, name='school'),
    path('shoppingmall/', views.shoppingmall, name='shoppingmall'),
    path('stadium/', views.stadium, name='stadium'),
    path('warehouse/', views.warehouse, name='warehouse'),
    path('building/', views.building, name='building'),
    path('retail/', views.retail, name='retail'),
    path('privacy/', views.privacy, name='privacy'),
    path('videos/', views.video_list, name='videos'),
]
