from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps import account

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