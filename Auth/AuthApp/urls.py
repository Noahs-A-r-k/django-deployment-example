from django.urls import path
from AuthApp import views

# Template urls requres app_name!
app_name = 'AuthApp'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_login/',views.user_login,name='user_login'),
    path('special/',views.special,name='special'),
]
