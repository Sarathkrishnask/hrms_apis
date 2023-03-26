from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt import serializers as jwt_serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps import account

import jwt

User = get_user_model()


"""
Maintain roles using serializers
"""
class RoleMasterSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = account.models.role_master
        fields = '__all__'


class setPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def update(self, instance,data):
        instance.set_password(data.get('password'))
        instance.save()
        instance.refresh_from_db()
        return instance