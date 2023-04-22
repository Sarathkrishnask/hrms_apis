from django.urls import path
from apps.admin import views

app_name = 'admin'

urlpatterns = [
    path('userlist/',views.UserListApiView.as_view(),name='UserListApiView'),
    path('userdetails/',views.UserDetailApiView.as_view(), name='userdetails'),
]