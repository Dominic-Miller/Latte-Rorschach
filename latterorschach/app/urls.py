from django.urls import path

from . import views

urlpatterns = [
    path('', views.today, name='today'),
    path('menu', views.menu, name='menu'),
    path('login', views.user_login , name='login'),  
    path('register', views.register, name='register'),
    path('account', views.account, name='account'),
    path('history', views.history, name='history'),
    path('addlatte', views.add_latte, name='addlatte'),
    path('topinterpretations', views.topinterpretations, name='topinterpretations'),
    path('accountsettings', views.accountsettings, name='accountsettings'),
    path('changeusername', views.changeusername, name='changeusername'),
    path('changepassword', views.changepassword, name='changepassword'),
    path('errorpage', views.errorpage, name='errorpage'),
]