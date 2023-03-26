from distutils.log import error
import re
import json
from tokenize import Triple

from django.core.exceptions import ValidationError

# from core.constants import MODULE_MISMATCH_MESSAGE_TEMPLATE


def validate_json_object_not_empty(value):
    validate_json_object(value)

    if not len(json.loads(value)):
        raise ValidationError(
            ('%(value)s should contain at least one key-value pair.'),
            params={'value': value},
        )


def validate_json_object(value):
    validate_json(value)

    if not isinstance(json.loads(value), dict):
        raise ValidationError(
            ('%(value)s is not a valid JSON object.'),
            params={'value': value},
        )


def validate_json(value):
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        raise ValidationError(
            ('%(value)s is not a valid JSON.'),
            params={'value': value},
        )
        
# """
# phone number validate
# """
# def is_valid_phone(phone):
#     if phone:
#         phone_number=re.match(r'(^[+0-9]{1,3})*([0-9]{10,11}$)', phone)
#         return phone_number
#     else:
#         return "not valid number"

"""
Email login validators
"""
def Email_Login_Validators(data):
    json_keys =['email','password', 'role']
    for val in json_keys:
        if  val not in dict.keys(data):
            return False
    return True


"""
Phone Otp login validators
"""
def phone_otp_login_validators(data):
    json_keys = ['phone','otp','role']
    for val in json_keys:
        if val not in dict.keys(data):
            return False
    return True

"""
Phone login validators
"""
def Phone_Login_Validators(data):
    json_keys =['country_code','phone']
    for val in json_keys:
        if  val not in dict.keys(data):
            return False
    return True

"""
phone otp validators"""
def Phone_OTP_Login_Validators(data):
    json_keys =['country_code','phone_number']
    for val in json_keys:
        if  val not in dict.keys(data):
            return False
    return True

"""
Email otp validators
"""
def Email_OTP_Login_Validators(data):
    json_keys=['email']
    for val in json_keys:
        if val not in dict.keys(data):
            return False
    return True

"""
verify phone otp validators
"""
def verify_phone_otp_validators(data):
    json_keys = ['otp','phone_number']
    for val in json_keys:
        if val not in dict.keys(data):
            return False
    return True

"""
verify email otp validators
"""
def verify_email_otp_validators(data):
    json_keys = ['otp','email']
    for val in json_keys:
        if val not in dict.keys(data):
            return False
    return True

"""
Role creation validators
"""
def role_validators(data):
    json_keys=['name']
    for val in json_keys:
        if val not in dict.keys(data):
            return False
    return True

"""
Change password
"""
def change_password_validators(data):
    json_keys=['email','password','confirm_password']
    for val in json_keys:
        if val not in dict.keys(data):
            return False
    return True

"""
Admin Email registeration
"""
def admin_email_register_validators(data):
    json_keys=['firstname','lastname','phone','email','password','confirm_password','role']
    for val in json_keys:
        if val not in dict.keys(data):
            return False
    return True

"""
Admin Phone registeration
"""
def admin_phone_register_validators(data):
    json_keys=['firstname','lastname','phone','email','role']
    for val in json_keys:
        if val not in dict.keys(data):
            return False
    return True


"""
User Email registeration
"""
def user_email_register_validators(data):
    json_keys=['firstname','lastname','phone','email','password','confirm_password','role','is_verified','personal_id']
    for val in json_keys:
        if val not in dict.keys(data):
            return False
    return True

"""
User Phone registeration
"""
def user_phone_register_validators(data):
    json_keys=['firstname','lastname','phone','email','role','is_verified','password','confirm_password','personal_id']
    for val in json_keys:
        if val not in dict.keys(data):
            return False
    return True



