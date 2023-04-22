# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from turtle import Turtle
# from types import CoroutineType

from django.contrib.auth import models as auth_models
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from apps.account import managers
from apps.generics import models as generic_models
# from apps.generics import tasks



class User(auth_models.AbstractBaseUser):
    """Custom user model that supports using email instead of username"""

    firstname = models.CharField(max_length=64)

    lastname = models.CharField(max_length=64)

    email = models.EmailField(max_length=64, unique=True)

    address1 = models.TextField(blank=True, null=True)

    address2 = models.TextField(blank=True, null=True)

    phone_number = models.CharField(max_length=100, blank=True, null=True)

    roles = models.ForeignKey('role_master', blank=True, null=True, on_delete=models.CASCADE)

    image = models.CharField(max_length=255, null=True,blank=True)

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    last_login = models.DateTimeField(null=True)

    login_count = models.PositiveIntegerField(null=True)

    is_email_verified = models.BooleanField(default=False)

    is_phone_verified = models.BooleanField(default=False)

    city = models.CharField(max_length=100, blank=True, null=True)

    state = models.CharField(max_length=200, blank=True, null=True)

    country_code = models.CharField(max_length=10, blank=True, null=True)

    country = models.CharField(max_length=200, blank=True, null=True)

    pincode = models.IntegerField(null =True,blank=True)

    personalid = models.CharField(max_length=50,null =True,blank=True)


    objects = managers.UserManager()

    USERNAME_FIELD = 'email'

    @property
    def get_roles(self):
        if self.roles:
            return self.roles.name

    @property
    def is_admin(self):
        return self.get_roles and self.get_roles in ['SuperAdmin','Admin','Employee']
    
    def has_perm(self, perm, obj=None):
       return self.is_admin
    
    def has_module_perms(self, app_label):
        return self.is_admin


    @classmethod
    def create_user(cls, email):
        if email and not User.objects.filter(email=email).exists():
            role, _ = role_master.objects.get_or_create(name='User')
            User.objects.create_user(email=email, roles=role)


class OTPAuth(models.Model):
    "Model for handling user authentication via OTP"

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    otp = models.CharField(max_length=12)
    expired_by = models.DateTimeField(null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    updated_on = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name = _('OTP Auth')
        verbose_name_plural = _('OTP Auth')



class role_master(models.Model):
    "Model for handling user role"
    
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _('Role master')
        verbose_name_plural = _('Role masters')

class MangeUserLog(generic_models.UUIDModel):
    """
    Models for handling users page log time and which page logged"""

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    types = models.CharField(max_length= 200,null=True)
    descriptions = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name = _('Manage User Log')
        verbose_name_plural = _('Manage User Logs')

class TempOTP(models.Model):
    """
    Model for handling user authentication via OTP
    """
    
    phone = models.CharField(max_length=20,null=True,blank=True)
    email = models.EmailField(null=True,blank=True,max_length=200)
    otp = models.CharField(max_length=12)
    expired_by = models.DateTimeField(null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    updated_on = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name = _('OTP Temp')
        verbose_name_plural = _('OTP Temp')

