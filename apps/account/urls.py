from django.urls import path
from apps.account import views

app_name = 'account'

urlpatterns = [

    path('registeruser/',views.RegisterUser.as_view(),name='registeruser'),
    path('email_login/',views.loginApi.as_view(),name='email_login'),


]