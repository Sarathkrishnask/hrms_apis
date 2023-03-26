from cmath import exp
from hashlib import sha512
import json
import pytz
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
import re
from apps.admin import models as admin_models

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa  
import csv
import operator
import hashlib
from random import randint
import uuid
# import qrcode
from base64 import b64encode
import requests

#expiry time for verifing otp
def verifyexpiry_time(expirytime):
    utc = pytz.UTC
    curnt_time = datetime.now()
    dt_string = str(expirytime)
    new_dt = dt_string[:19]
    curnt_time = datetime.strptime(str(curnt_time), '%Y-%m-%d %H:%M:%S.%f')
    expire_ts = datetime.strptime(new_dt, '%Y-%m-%d %H:%M:%S')
    month_name = expirytime.strftime("%d")+" "+expirytime.strftime("%b") +" "+expirytime.strftime("%Y")
    time = expirytime.strftime("%H")+":"+expirytime.strftime("%M")
    print('month name: ', month_name, "time: ",)
    curnt_time = curnt_time.replace(tzinfo=utc)
    expire_ts = expire_ts.replace(tzinfo=utc)
    return expire_ts,curnt_time

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

def is_valid_phone(phone):
        phone_number=re.compile(r'(^[+0-9]{1,3})*([0-9]{5,15}$)')
        data_phone=phone_number.match(phone)
        if data_phone != None:
            return True
        else:
            return False



def html_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def nested_getattr(obj, attribute, split_rule='__'):
    """
    This function is responsible for getting the nested record from the given obj parameter
    :param obj: whole item without splitting
    :param attribute: field after splitting
    :param split_rule:
    :return:
    """
    split_attr = attribute.split(split_rule)
    for attr in split_attr:
        if not obj:
            break
        obj = getattr(obj, attr)
    return obj


def export_to_csv(queryset, fields, titles, file_name):
    """
    will export the model data in the form of csv file
    :param queryset: queryset that need to be exported as csv
    :param fields: fields of a model that will be included in csv
    :param titles: title for each cell of the csv record
    :param file_name: the exported csv file name
    :return:
    """
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    # force download
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(file_name)
    # the csv writer
    writer = csv.writer(response)
    if fields:
        headers = fields
        if titles:
            titles = titles
        else:
            titles = headers
    else:
        headers = []
        for field in model._meta.fields:
            headers.append(field.name)
        titles = headers

    # Writes the title for the file
    writer.writerow(titles)

    # write data rows
    for item in queryset:
        writer.writerow([nested_getattr(item, field) for field in headers])
    return response


def verify_personalid(data):
        regex = "[A-Z]{5}[0-9]{4}[A-Z]{1}"
        a_regex ="^[0-9]{1}[0-9]{3}[0-9]{4}[0-9]{4}$"
        # regex ='^(([A-Z]{2}[0-9]{2})( )|([A-Z]{2}-[0-9]{2}))((19|20)[0-9][0-9])[0-9]{7}$'

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
