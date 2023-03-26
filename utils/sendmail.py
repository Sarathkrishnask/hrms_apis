from io import BytesIO
import os
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import Group
from hrms import settings
from datetime import datetime, timedelta
import pytz,random
from apps.account.models import *
from apps.admin import models as admin_models
import logging
from utils import functions
from num2words import num2words
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa 
from django.conf import settings
from django.contrib.staticfiles import finders
from decouple import config as cnf
from twilio.rest import Client

import urllib

def sendCustomMail(message, recepiants, subject,template):
    email_html_message = render_to_string(template, message)
    email = EmailMultiAlternatives(subject, email_html_message, settings.DEFAULT_FROM_EMAIL, [recepiants])
    email.attach_alternative(email_html_message, "text/html")
    email.send()

# def sendSMS(numbers,message):
#     client = Client(cnf('TWILIO_ACCOUNT_SID'), cnf('TWILIO_AUTH_TOKEN') )
#     client.messages.create(to=numbers,from_=cnf('TWILIO_NUMBER'),body=message)
#     # data = urllib.parse.urlencode(
#     #     {'apikey': settings.TEXT_LOCAL_API_KEY, 'numbers': numbers, 'message': message, 'sender': sender})
#     # data = data.encode('utf-8')
#     # request = urllib.request.Request("https://api.textlocal.in/send/?")
#     # f = urllib.request.urlopen(request, data)
#     # fr = f.read()
#     return True

# def send_mobile_otp(phone_number,country_code,id):
#     otp_val=random.randint(1000,9999)
#     # "dummy otp val static purpose"
#     # otp_val = 1212
#     message = F"Hi there,your verification code is:{otp_val}"
    
#     expire_ts=datetime.now()+timedelta(minutes=2)
#     if not OTPAuth.objects.filter(user_id=id).exists():
#             print("exits or not")
#             otptbl = OTPAuth(otp = otp_val,expired_by = expire_ts,user_id=id)
#             otptbl.save()
#     else:
#         OTPAuth.objects.filter(user_id=id).update(otp = otp_val,expired_by = expire_ts,updated_on=datetime.now())
#     ph_number = str(phone_number)

#     '''send otp to client TextLocal Credentials'''
#     sendSMS(ph_number,message)

#     return otp_val

def send_email_otp(email,id,subject,template):
    otp_val=random.randint(1000,9999)
    # "dummy otp val static purpose"
    # otp_val = 1212
    expire_ts=datetime.now()+timedelta(minutes=2)
    

    context = {
        'email': email,
        'otp': otp_val,
    }
    if not OTPAuth.objects.filter(user_id=id).exists():
            print("exits or not")
            otptbl = OTPAuth(otp = otp_val,expired_by = expire_ts,user_id=id)
            otptbl.save()
    else:
        OTPAuth.objects.filter(user_id=id).update(otp = otp_val,expired_by = expire_ts,updated_on=datetime.now())

    sendCustomMail(context, email, subject,template)
    return otp_val

def temp_mobile_otp(phone_number,country_code):
    otp_val=random.randint(1000,9999)
    # "dummy otp val static purpose"
    # otp_val = 1212
    message = F"temperory otp for registeration:{otp_val}"
    
    expire_ts=datetime.now()+timedelta(minutes=2)
    if not TempOTP.objects.filter(phone=phone_number).exists():
            print("exits or not")
            otptbl = TempOTP(otp = otp_val,expired_by = expire_ts,phone=phone_number)
            otptbl.save()
    else:
        TempOTP.objects.filter(phone=phone_number).update(otp = otp_val,expired_by = expire_ts,updated_on=datetime.now())
    
    id = TempOTP.objects.filter(phone=phone_number).first().id
    ph_number = str(phone_number)

    '''send otp to client TextLocal Credentials'''
    sendSMS(ph_number,message)

    return id

def temp_email_otp(email,subject,template):
    otp_val=random.randint(1000,9999)
    # "dummy otp val static purpose"
    # otp_val = 1212
    # print(otp_val,'----------')
    expire_ts=datetime.now()+timedelta(minutes=2)

    context = {
        'email': email,
        'otp': otp_val,
    }
    if not TempOTP.objects.filter(email=email).exists():
            print("exits or not")
            otptbl = TempOTP(otp = otp_val,expired_by = expire_ts,email=email)
            otptbl.save()
    else:
        TempOTP.objects.filter(email=email).update(otp = otp_val,expired_by = expire_ts,updated_on=datetime.now())
    sendCustomMail(context, email, subject,template)
    id = TempOTP.objects.filter(email=email).first().id
    
    return id

def send_password_email_user(subject,mail_body,to_mail,from_mail,user,password):
    try:
        content = {"username":user,"email":to_mail,"role":"Donar","password":password}
        html_content = render_to_string('email_for_superadmin_create_user.html', content)
        email = EmailMultiAlternatives(subject=subject,body=mail_body,from_email=from_mail,to=[to_mail])
        email.attach_alternative(html_content, "text/html")
        email.send()
        return True
    except Exception as ex:
        logging.warning('mail not send')
        pass
        # raise ex


def send_password_email_counter(subject,mail_body,to_mail,from_mail,user,password):
    try:
        content = {"username":user,"email":to_mail,"role":"Counter Admin","password":password}
        html_content = render_to_string('email_for_superadmin_create_user.html', content)
        email = EmailMultiAlternatives(subject=subject,body=mail_body,from_email=from_mail,to=[to_mail])
        email.attach_alternative(html_content, "text/html")
        email.send()
        return True
    except Exception as ex:
        logging.warning('mail not send')
        pass

def send_receipt(id,subject,mail_body,to_mail,from_mail):
    try:
        data = admin_models.payment_master.objects.filter(id= id).first()
        manage_master_data=admin_models.manage_master.objects.filter(id=data.manage_master_id).first()
        category_master_name=admin_models.category_master.objects.filter(id=manage_master_data.category_id).first()
        category_name = category_master_name.name
        dailyabhisegam_exists=admin_models.dailyabhishegam_form_report.objects.filter(payment_master_id=id).exists()
        event_exists=admin_models.event_form_report.objects.filter(payment_master_id=id).exists()
        if not dailyabhisegam_exists and not event_exists:
            entity_map=admin_models.entity_mapping.objects.filter(entity_80g_id=data.entity_id)
            if entity_map.exists():
                receipt="80G Receipt"
            else:
                receipt="Receipt"
            vendor_address = admin_models.billing_master.objects.get(id=data.billing_master_id)
            address = str(vendor_address.address1)+", "+str(vendor_address.address2)+", "+str(vendor_address.city)+", "+str(vendor_address.state)+", "+str(vendor_address.zip)
            amount_words=num2words(data.amount)
            donated_date=data.donated_at
            donated_data =donated_date.strftime('%d/%m/%Y')
            content={'data': data,'donated_data':donated_data,'amount_words':amount_words,'category_name':category_name,'donar_address':address,'vendor_address':vendor_address,"receipts":receipt}
            template_path='Receipt.html'
            try:
                template = get_template(template_path)
                html  = template.render(content)
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, link_callback=link_callback)
                pdf = result.getvalue()
                filename = F'{id}.pdf'
                email = EmailMultiAlternatives(subject=subject,body=mail_body,from_email=from_mail,to=[to_mail])
                email.attach(filename, pdf, "application/pdf")
                email.send()
            except Exception as e:
                message="mail not send"
                return message
            return True
        elif dailyabhisegam_exists and not event_exists:
            dailyabhisegam=admin_models.dailyabhishegam_form_report.objects.filter(payment_master_id=id).values('payment_master','booked_date','abhishegam_date')
            # dailyabhisegam_ser=admin_serializers.dailyabhishegam_form_reportSerializer(dailyabhisegam, many=True)
            # '''transaction_no, abhishegam_date, booked_date, occasion,type_name, payment_master, tokens_id '''
            # '''Token No :
            #  55,Reference No: 60584,Phone : 6380904449, Name : SANMATHI VASANTHAN,Place : SALEM,Date:2022-12-13 Tuesday'''
            qr_list=[]
            for abhi in dailyabhisegam:
                abhi['token_no']=abhi['payment_master']
                abhi['booked_date']=abhi['booked_date'].strftime('%d/%m/%Y')
                abhi['date']=abhi['abhishegam_date'].strftime('%d/%m/%Y')
                qr_data = admin_models.payment_master.objects.get(id=abhi['payment_master'])
                donar_data = admin_models.billing_master.objects.get(id=qr_data.billing_master_id)
                abhi['name']=donar_data.firstname
                abhi['phone']=donar_data.phone
                abhi['place']=donar_data.city

                
                abhi['qr_codeurl'] = functions.qr_code_generation(abhi)

            vendor_address = admin_models.billing_master.objects.get(id=data.billing_master_id)
            address = str(vendor_address.address1)+", "+str(vendor_address.address2)+", "+str(vendor_address.city)+", "+str(vendor_address.state)+", "+str(vendor_address.zip)
            amount_words=num2words(data.amount)
            donated_date=data.donated_at
            donated_data =donated_date.strftime('%d/%m/%Y')
            receipt="Receipt"
            content={'data': data,'receipt':receipt,'donated_data':donated_data,'amount_words':amount_words,'category_name':category_name,'donar_address':address,'vendor_address':vendor_address,'dataurl':dailyabhisegam}

            # html_content = render_to_string('QRcode.html', content)
            template_path='QRcode.html'
            try:
                template = get_template(template_path)
                html  = template.render(content)
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, link_callback=link_callback)
                pdf = result.getvalue()
                filename = F'{id}.pdf'
                email = EmailMultiAlternatives(subject=subject,body=mail_body,from_email=from_mail,to=[to_mail])
                email.attach(filename, pdf, "application/pdf")
                email.send()
            except Exception as e:
                message="mail not send"
                return message
            return True
        else:
            event_=admin_models.event_form_report.objects.filter(payment_master_id=id,abhishegam_date=None)
            if event_:
                entity_map=admin_models.entity_mapping.objects.filter(entity_80g_id=data.entity_id)
                if entity_map.exists():
                    receipt="80G Receipt"
                else:
                    receipt="Receipt"
                vendor_address = admin_models.billing_master.objects.get(id=data.billing_master_id)
                address = str(vendor_address.address1)+", "+str(vendor_address.address2)+", "+str(vendor_address.city)+", "+str(vendor_address.state)+", "+str(vendor_address.zip)
                amount_words=num2words(data.amount)
                donated_date=data.donated_at
                donated_data =donated_date.strftime('%d/%m/%Y')
                content={'data': data,'donated_data':donated_data,'amount_words':amount_words,'category_name':category_name,'donar_address':address,'vendor_address':vendor_address,"receipts":receipt}
                template_path='Receipt.html'
                try:
                    template = get_template(template_path)
                    html  = template.render(content)
                    result = BytesIO()
                    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, link_callback=link_callback)
                    pdf = result.getvalue()
                    filename = F'{id}.pdf'
                    email = EmailMultiAlternatives(subject=subject,body=mail_body,from_email=from_mail,to=[to_mail])
                    email.attach(filename, pdf, "application/pdf")
                    email.send()
                except Exception as e:
                    message="mail not send"
                    return message
                return True
            else:
                dailyabhisegam=admin_models.event_form_report.objects.filter(payment_master_id=id).values('payment_master','donation_date','abhishegam_date','quantity')
                # dailyabhisegam_ser=admin_serializers.dailyabhishegam_form_reportSerializer(dailyabhisegam, many=True)
                # '''transaction_no, abhishegam_date, booked_date, occasion,type_name, payment_master, tokens_id '''
                # '''Token No :
                #  55,Reference No: 60584,Phone : 6380904449, Name : SANMATHI VASANTHAN,Place : SALEM,Date:2022-12-13 Tuesday'''
                qr_list=[]
                for abhi in dailyabhisegam:
                    abhi['token_no']=abhi['payment_master']
                    abhi['booked_date']=abhi['donation_date'].strftime('%d/%m/%Y')
                    abhi['date']=abhi['abhishegam_date'].strftime('%d/%m/%Y')
                    abhi['qty']=abhi['quantity']
                    qr_data = admin_models.payment_master.objects.get(id=abhi['payment_master'])
                    donar_data = admin_models.billing_master.objects.get(id=qr_data.billing_master_id)
                    abhi['name']=donar_data.firstname
                    abhi['phone']=donar_data.phone
                    abhi['place']=donar_data.city

                    
                    abhi['qr_codeurl'] = functions.qr_code_generation(abhi)

                vendor_address = admin_models.billing_master.objects.get(id=data.billing_master_id)
                address = str(vendor_address.address1)+", "+str(vendor_address.address2)+", "+str(vendor_address.city)+", "+str(vendor_address.state)+", "+str(vendor_address.zip)
                amount_words=num2words(data.amount)
                donated_date=data.created_at
                donated_data =donated_date.strftime('%d/%m/%Y')
                receipt="Receipt"
                content={'data': data,'receipt':receipt,'donated_data':donated_data,'amount_words':amount_words,'category_name':category_name,'donar_address':address,'vendor_address':vendor_address,'dataurl':dailyabhisegam}
                # html_content = render_to_string('QRcode.html', content)
                template_path='event_qrcode.html'
                try:
                    template = get_template(template_path)
                    html  = template.render(content)
                    result = BytesIO()
                    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, link_callback=link_callback)
                    pdf = result.getvalue()
                    filename = F'{id}.pdf'
                    email = EmailMultiAlternatives(subject=subject,body=mail_body,from_email=from_mail,to=[to_mail])
                    email.attach(filename, pdf, "application/pdf")
                    email.send()
                except Exception as e:
                    message="mail not send"
                    return message
                return True
                
        
    except Exception as ex:
        logging.warning('mail not send')
        pass


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
            if not isinstance(result, (list, tuple)):
                    result = [result]
            result = list(os.path.realpath(path) for path in result)
            path=result[0]
    else:
            sUrl = settings.STATIC_URL        # Typically /static/
            sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL         # Typically /media/
            mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                    path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                    path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                    return uri

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                    'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path

def send_donation_conformation_SMS(id):
    try:
        data = admin_models.payment_master.objects.filter(id= id).first()
        manage_master_data=admin_models.manage_master.objects.filter(id=data.manage_master_id).first()
        category_master_name=admin_models.category_master.objects.filter(id=manage_master_data.category_id).first()
        category_name = category_master_name.name
        vendor_address = admin_models.billing_master.objects.get(id=data.billing_master_id)
        message=F"Donation Conformation Details: Purpose:{category_name} and Amount:{data.amount}"
        client = Client(cnf('TWILIO_ACCOUNT_SID'), cnf('TWILIO_AUTH_TOKEN') )
        client.messages.create(to=vendor_address.phone,from_=cnf('TWILIO_NUMBER'),body=message)
        return True
    except Exception as e:
        message="sms not send"
        return message
