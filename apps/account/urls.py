from django.urls import path
from apps.account import views

app_name = 'account'

urlpatterns = [

    path('registeruser/',views.UserRegister.as_view(),name='registeruser'),
    path('email_login/',views.loginApi.as_view(),name='email_login'),
    path('changepassword/',views.ChangePassword.as_view(),name='changepassword'),
    path('role_view/',views.roles_master.as_view(),name='roleview'),

]