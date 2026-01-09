from django.urls import path
from . import views

urlpatterns = [
    path('', views.land , name='land'),
    path('home/', views.home , name='home'),
    path('main/', views.main , name='main'),
    path('createaccount/', views.createaccount , name='createaccount'),
    path('makepayment/', views.makepayment , name='makepayment'),
    path('search/', views.search , name='search'),
    path('all_data/', views.all_data , name='all_data'),
    path('logout/', views.logout , name='logout'),
    path('createkatha/',views.createkatha ,name = 'createkatha'),
    path('viewkathas/',views.viewkathas,name='viewkathas'),
    path('personpayments/<int:id>',views.personpayments,name='personpayments'),
    path('user/',views.user,name='user'),
    path('usermain/',views.usermain,name='usermain'),
    path('userlogout/',views.userlogout,name='userlogout'),


]