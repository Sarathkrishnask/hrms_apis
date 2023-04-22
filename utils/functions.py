
from datetime import datetime
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
import re


from random import randint

# import qrcode
from base64 import b64encode


def emailauth(user,id):
    access = AccessToken.for_user(user)
    refresh=RefreshToken.for_user(user)

    access['email']=user.email
    access['user_id']=id
    refresh['email']=user.email
    refresh['user_id']=id
    
    return {"access_token": str(access),
    "refresh_token":str(refresh)}

def phoneauth(user,id):
    access = AccessToken.for_user(user)
    refresh=RefreshToken.for_user(user)

    access['email']=user.phone_number
    access['user_id']=id
    refresh['email']=user.phone_number
    refresh['user_id']=id
    
    return {"access_token": str(access),
    "refresh_token":str(refresh)}




def verify_personalid(data):
        regex = "[A-Z]{5}[0-9]{4}[A-Z]{1}"
        a_regex ="^[0-9]{1}[0-9]{3}[0-9]{4}[0-9]{4}$"

        datas=(str(data)).upper()   
        if bool(re.search(regex, str(datas), re.I)):
                # pan=kyc_verify.pan_verification(datas['personalid'])
                # if pan['success']==False:
                #     return json.Response({"data":[]},str(pan['response_message']),400, False)
            return True
            
        elif bool(re.search(a_regex, str(data), re.I)):
                # pan=kyc_verify.aadhar_verification(datas['personalid'])
                # print(pan,'[[[[[[')
                # if pan['success']==False:
                #     return json.Response({"data":[]},str(pan['response_message']),400, False)
            return True

        else:
            return False
