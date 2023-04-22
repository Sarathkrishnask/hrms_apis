from distutils.log import error
import json


from django.core.exceptions import ValidationError


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



