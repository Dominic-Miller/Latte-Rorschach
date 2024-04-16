from django.urls import path

from . import views

urlpatterns = [
    path('', views.today, name='today'),
    path('menu', views.menu, name='menu'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('account', views.account, name='account'),
    path('history', views.history, name='history'),
    path('topinterpretations', views.topinterpretations, name='topinterpretations'),
]