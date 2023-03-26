from __future__ import unicode_literals
from pyexpat import model
from tokenize import Triple

# from utils.kyc_verification import kyc_verify


"""
import django functions
"""
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password,check_password

"""
import apps,models,serializers
"""
from apps.account import models, serializers
from apps.admin import models as admin_models


"""
import restframeworks functions
"""
from rest_framework.decorators import action, api_view, permission_classes,parser_classes
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser
from rest_framework.views import APIView
from rest_framework import generics, parsers, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt import views as jwt_views

"""
import utils functions
"""
from utils import json,validators,sendmail
from utils import permissions as cust_perms
from utils import functions

"""
other imports
"""
import random
from datetime import datetime, timedelta
import json as j
import pytz
from decouple import config as cnf
import logging
# from appsacmec_admin import models as admin_models
logger = logging.getLogger(__name__)
User = get_user_model()


class RegisterUser(APIView):
    """
    Registeration of user
    """

    permission_classes=[permissions.AllowAny,]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RegisterUser, self).dispatch(request, *args, **kwargs)

    @csrf_exempt
    def post(self, request):
        print("data_in")
        datas = j.loads(request.body.decode('utf-8'))
        print(datas)
        try:
            params = self.request.query_params
            if params.get('login_type') == "0":
                """
                mobile registeration
                """
                if validators.user_phone_register_validators(datas)==False:
                    print("user_phone_register_validators")
                    return json.Response({"data":[]},"Required Field is missing",400,False)
                
                if datas["firstname"]=="" or datas["lastname"]=="" or datas["phone"]=="" or datas["email"]=="" or datas["role"]=="" or datas["password"] == "" or datas["confirm_password"]=="":
                    print("empty_Str")
                    return json.Response({"data":[]},"Field is empty",400,False)

                if datas["country_code"]=="": 
                    print("countrycode")
                    return json.Response({"data":[]},"countrycode is empty",400,False)
                
                if datas["country_code"]=="+91":
                    print("91")
                    if datas['personal_id'] !='':
                        print("personal_id")
                        pan=functions.verify_personalid(datas['personal_id'])
                        if pan==False:
                            print("pan_false")
                            return json.Response({"data":[]},"pancard not verified",400, False)
                        if pan==True:
                            print("pan_true")

                # if functions.is_valid_phone(datas['phone']) == False:
                #     print("not valid phone")
                #     return json.Response({"data":[]},"Please enter valid mobile number",400,False)
                
                Users_data = models.User.objects
                User_filter = Users_data.filter(phone_number=datas['phone'])
                User_email = Users_data.filter(email=datas['email'])

                if User_filter.exists():
                    print("phn_exist")
                    return json.Response({"data":[]},"Phone number already exists!",400,False)
                
                if  User_email.exists():
                    print("email_exist")
                    return json.Response({"data":[]},"Email already exists!",400,False)
                
                if datas["password"].lower() != datas["confirm_password"].lower():
                    return json.Response({"data":[]}, "Password and confirm password are not same", 400, False)
                
                if not models.role_master.objects.filter(id=datas['role']).exists():
                    return json.Response({"data":[]},"There is no role for this type",400,False)

                rolelist = models.role_master.objects.filter(id=datas['role']).first()

                if str(rolelist).lower() == "employee":
                    if validators.user_email_register_validators(datas) == False:
                        print("is_verify_missing")
                        return json.Response({"data":[]},"Is_verified Field is missing",400,False)
                    if datas["is_verified"]==False: 
                        print("verify_otp")
                        return json.Response({"data":[]},"OTP not verified. Please verify your otp",400,False)
                    Users_data.create(firstname=datas["firstname"],lastname=datas["lastname"],phone_number=datas['phone'],email=datas['email'],is_active=True,is_email_verified=False,is_phone_verified=True,roles_id=datas["role"],password=make_password(datas["password"]),personalid=datas['personal_id'],country_code=datas['country_code'])
                    user_datas = models.User.objects.get(phone_number=datas['phone'])
                    user_Name_id = models.User.objects.filter(phone_number=datas['phone']).first()
                    user_details = {}
                    getjwt=functions.phoneauth(user_datas,user_Name_id.id)
                    user_details['access_token'] = getjwt['access_token']
                    user_details['refresh_token'] = getjwt['refresh_token']
                    user_details['user_info'] = {"id":user_Name_id.id,
                                                "name":str(user_Name_id.firstname) + str(user_Name_id.lastname),
                                                "email":user_Name_id.email,
                                                "phone_number":user_Name_id.phone_number,
                                                "image":user_Name_id.image}
                    return json.Response({"data":user_details},"User created successfully",201,True)
                
                else:
                    return json.Response({"data":[]},"Only user can be created",400,False)
            
            if params.get('login_type') == "1":
                """
                User Email registeration
                """
                if validators.admin_email_register_validators(datas)==False:
                    return json.Response({"data":[]},"Required field is missing",400,False)

                if datas["firstname"]=="" or datas["lastname"]=="" or datas["phone"]=="" or datas["email"]=="" or datas["role"]=="" or datas["password"] == "" or datas["confirm_password"]=="":
                    return json.Response({"data":[]},"Field is empty",400,False)
                
                if datas["country_code"]=="": 
                    return json.Response({"data":[]},"countrycode is empty",400,False)
                if datas["country_code"]=="+91":
                    if datas['personal_id'] !='':
              
                        pan=functions.verify_personalid(datas['personal_id'])
                        if pan==False:
                            return json.Response({"data":[]},"pancard not verified",400, False)


                # if functions.is_valid_phone(datas['phone']) == False:
                #     return json.Response({"data":[]},"Mobile number is invalid",400,False)

                Users_data = models.User.objects
                User_filter = Users_data.filter(phone_number=datas['phone'])
                User_email = Users_data.filter(email=datas['email'])

                if User_filter.exists():
                    return json.Response({"data":[]},"Phone number already exists!",400,False)
                
                if  User_email.exists():
                    return json.Response({"data":[]},"Email already exists!",400,False)
                
                if datas["password"].lower() != datas["confirm_password"].lower():
                    return json.Response({"data":[]}, "Password and confirm password are not same", 400, False)

                if not models.role_master.objects.filter(id=datas['role']).exists():
                    return json.Response({"data":[]},"There is no role for this type",400,False)

                rolelist = models.role_master.objects.filter(id=datas['role']).first()
    
                if str(rolelist).lower() == "employee":
                    if validators.user_email_register_validators(datas) == False:
                        return json.Response({"data":[]},"Is_verified Field is missing",400,False)
                    if datas["is_verified"]==False:
                        return json.Response({"data":[]},"OTP not verified. Please verify your otp",400,False)
                    Users_data.create(firstname=datas["firstname"],lastname=datas["lastname"],phone_number=datas['phone'],email=datas['email'],is_active=True,is_email_verified=True,is_phone_verified=False,roles_id=datas["role"],password=make_password(datas["password"]),personalid=datas['personal_id'],country_code=datas['country_code'])
                    user_datas = models.User.objects.get(email=datas['email'])
                    user_Name_id = models.User.objects.filter(email=datas['email']).first()
                    user_details = {}
                    getjwt=functions.emailauth(user_datas,user_Name_id.id)
                    user_details['access_token'] = getjwt['access_token']
                    user_details['refresh_token'] = getjwt['refresh_token']
                    user_details['user_info'] = {"id":user_Name_id.id,
                                                "name":str(user_Name_id.firstname) + str(user_Name_id.lastname),
                                                "email":user_Name_id.email,
                                                "phone_number":user_Name_id.phone_number,
                                                "image":user_Name_id.image}
                    return json.Response({"data":user_details},"User created successfully",201,True)
                
                else:
                    return json.Response({"data":[]},"Only user can be created",400,False)
                
        except Exception as e:
            return json.Response({"data":[]},f"{e}Internal Server Error", 400,False)
        

class loginApi(APIView):
    """
    login using Email
    """
    
    permission_classes=[permissions.AllowAny]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(loginApi, self).dispatch(request, *args, **kwargs)

    @csrf_exempt
    def post(self,request):
        try:
            datas = j.loads(request.body.decode('utf-8'))
            if validators.Email_Login_Validators(datas) == False:
                print("email_false")
                return json.Response({"data":[]},"Required field is missing",400,False)
            
            user_data = models.User.objects

            if not user_data.filter(email=datas['email']).exists():
                print("exist")
                return json.Response({"data":[]},"Please enter registered email",400, False)

            if not user_data.filter(email=datas['email'],roles_id=datas['role']).exists():
                print("exist1")
                return json.Response({"data":[]},"Please enter registered email Id",400, False)

            if len(datas['password']) == 0 or datas['password'] == '':
                print("psswd")
                return json.Response({"data":[]},"Please enter password",400, False)


            users = user_data.get(email=datas['email'])

            if check_password(datas['password'],users.password) == False:
                print("check_password")
                return json.Response({"data":[]},"Incorrect password",400, False)

            user_datas = models.User.objects.get(email=datas['email'])
            user_Name_id = models.User.objects.filter(email=datas['email']).first()

            user_details = {}
            if int(user_Name_id.roles_id) == 2:
                userentity = admin_models.counter_entity_master.objects.filter(auth_user_id=user_Name_id.id).first()
                getjwt=functions.emailauth(user_datas,user_Name_id.id)
                user_details['access_token'] = getjwt['access_token']
                user_details['refresh_token'] = getjwt['refresh_token']
                user_details['user_info'] = {"id":user_Name_id.id,
                                                    "name":str(user_Name_id.firstname)+' '+str(user_Name_id.lastname),
                                                    "email":user_Name_id.email,
                                                    "phone_number":user_Name_id.phone_number,
                                                    "image":user_Name_id.image,
                                                    "role_id":user_Name_id.roles_id,
                                                    "entity_id":userentity.entity_id}
            else:
                users.login_count +=1
                users.save()
                getjwt=functions.emailauth(user_datas,user_Name_id.id)
                user_details['access_token'] = getjwt['access_token']
                user_details['refresh_token'] = getjwt['refresh_token']
                user_details['user_info'] = {"id":user_Name_id.id,
                                                    "name":str(user_Name_id.firstname)+' '+str(user_Name_id.lastname),
                                                    "email":user_Name_id.email,
                                                    "phone_number":user_Name_id.phone_number,
                                                    "image":user_Name_id.image,
                                                    "role_id":user_Name_id.roles_id,
                                                    "login_count":user_Name_id.login_count + 1}
            return json.Response({"data":user_details},"Logged In Successfully",200,True)

        except Exception as e:
            return json.Response({"data":[]},f"{e}Internal Server Error", 400,False)