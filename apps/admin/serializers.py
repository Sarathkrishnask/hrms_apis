from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.account import models as account_model
User = get_user_model()

"""
Users Listing serializer
"""
class UserListSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField('get_roles')
    role_id = serializers.SerializerMethodField('get_role_id')

    

    def get_roles(self,data):
        role = account_model.role_master.objects.get(id=data.roles_id)
        return str(role)

    def get_role_id(self,data):
        role = data.roles_id
        return str(role)
    
    class Meta:
        model = User
        fields = ['id','firstname','lastname','email','is_email_verified','phone_number','roles','role_id','is_phone_verified','is_active','image','country','address1','city','state','address2','pincode']



class UserDetailViewSerializers(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField('get_roles')
    role_id = serializers.SerializerMethodField('get_role_id')

    def get_roles(self,data):
        role = account_model.role_master.objects.get(id=data.roles_id)
        return str(role)

    def get_role_id(self,data):
        role = data.roles_id
        return role

    class Meta:
        model = User
        fields = ['id','firstname','lastname','email','is_email_verified','phone_number','roles','role_id','is_phone_verified','is_active','image','country','country_code','address1','city','state','address2','pincode']