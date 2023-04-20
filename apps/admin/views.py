
"""
import django functions
"""
from django.shortcuts import render
# from account.models import User
from django.db.models import Q,Count,Sum, Max, Min
from django.contrib.auth.hashers import make_password,check_password




"""
import apps,models,serializers
"""
from apps.account import models as account_models
from apps .admin import serializers as admin_serializers

"""
import restframeworks functions
"""
from rest_framework.views import APIView
from rest_framework import generics, parsers, permissions, status, viewsets

# Create your views here.


"""
import utils functions
"""
from utils import json,validators,sendmail
from utils import permissions as cust_perms
from utils import functions
from utils.sorting import sorting_ListUser
from utils.pagination import CustomPagination, pagination_class


"""
other import functions
"""
import json as j


class ListUserApiView(generics.GenericAPIView):
    """
    List users in adminpanel
    """
    permission_classes=[permissions.IsAuthenticated,cust_perms.ISSuperAdmin]
    queryset = account_models.User.objects.all()
    serializer_class = admin_serializers.UserListingSerializer

    def get(self, request):
        try:


            queryset = self.filter_queryset(self.get_queryset())            
            serializer = self.get_serializer(queryset, many=True)
            count= queryset.count()
            print(count)
            data = json.Response(serializer.data,'Listed successfully',200,True)
            return data
        except Exception as e:
            return json.Response({'data':[]},f'{e}Internal Server Error',400,False)
        


class UserDetailApiView(APIView):
    """
    get particular user detail in adminpanel
    """
    permission_classes=[permissions.IsAuthenticated,cust_perms.ISSuperAdmin]

    def get(self, request):
        """
        admin can access particualar user detail with id in params 
        """

        try:
            id_=self.request.query_params.get('id')
            queryset = account_models.User.objects.filter(id=id_)
            serializer = admin_serializers.UserviewingSerializers(queryset, many=True)  
            return json.Response({"data":serializer.data}," particualr user detail view accessed successfully",200,True)
        except Exception as e:
            return json.Response({"data":[]},f"{e}Internal Server Error", 400, False)
        
    def put(self, request):
        id_=request.query_params.get('id')
        datas = j.loads(request.body.decode('utf-8'))
        Users_data = account_models.User.objects
        user_exists = Users_data.filter(id=id_).exists()
        if user_exists:
            print("Existing user")
            Users_data.filter(id=id_).update(firstname=datas["firstname"],
                            lastname=datas["lastname"],
                            phone_number=datas['phone'],
                            email=datas['email'],
                            is_active=True,
                            is_email_verified=True,
                            is_phone_verified=False,
                            roles_id=datas["role"],
                            city=datas["city"],
                            state=datas["state"],
                            country=datas["country"],
                            country_code=datas["country_code"],
                            address1=datas["address1"],
                            address2=datas["address2"],
                            image=datas["image"],
                            pincode=datas["pincode"])
        

            user_Name_id = account_models.User.objects.filter(email=datas['email']).first()
            return json.Response({"data":user_Name_id.id},"User updated successfully",201,True)
        return json.Response({"data":[]},"User not existed",400,False)
    
    def delete(self,request):
        id_=request.query_params.get('id')
        datas = j.loads(request.body.decode('utf-8'))
        Users_data = account_models.User.objects
        
        try:
            user_exists = Users_data.filter(id=id_).exists()
            print(user_exists)
            user_details_ = {}
            if user_exists:
                user_details=account_models.User.objects.get(id=id_)
                user_details.delete()
                print(user_details,user_details.firstname,user_details.lastname,user_details.phone_number)
            return json.Response({"data":user_details.firstname},"User updated successfully",201,True)
                
        except Exception as e:
            return json.Response({"data":[]},f"{e}User not existed",400,False)
        