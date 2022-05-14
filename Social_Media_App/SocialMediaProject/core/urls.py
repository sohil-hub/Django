from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signUp, name='signup'),
    path('signin', views.signIn, name='signin'),
    path('logout', views.logOut, name='logout'),
    path('setting', views.setting, name='setting'),
]