# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import imp

from django.contrib.auth import models as auth_models
from django.utils.translation import gettext_lazy as _
from apps.account import models

class UserManager(auth_models.BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):

        "Creates and saves a new user"

        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(email=self.normalize_email(email), **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):

        "Creates and saves a new superuser"

        user = self.create_user(email, password)
        has_value = models.role_master.objects.filter().count()
        roles = ['SuperAdmin','Admin','Employee']

        # guest_email = "guest_user@gmail.com"
        # guest_password = "Guest@123"
        # guest_value = models.User.objects.filter(email=guest_email).exists()
 
        if has_value ==0:
            for rol in roles:
                role=models.role_master(name=rol)
                role.save()

        user.is_staff = True
        user.is_superuser = True
        user.roles_id=1
        user.save(using=self._db)

        # if guest_value == False:
        #     new_user = self.create_user(guest_email,guest_password)
        #     new_user.roles_id=3
        #     new_user.is_superuser = False
        #     new_user.save(using=self._db)
        

        return user