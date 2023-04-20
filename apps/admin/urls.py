from django.urls import path
from apps.admin import views

app_name = 'admin'

urlpatterns = [
    path('userlist/',views.ListUserApiView.as_view(),name='ListUserApiView'),
    path('userdetails/',views.UserDetailApiView.as_view(), name='userdetails'),
]