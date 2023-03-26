import logging
from django.db.models import Count
from django.db.models.functions import Lower


def split_pagedatas(page,item):
    page = int(page)
    item = int(item)
    start = item *(page-1)
    end = item * page
    return [start,end]


def sorting_ListUser(query,req):
    try:
        if 'firstname_asc' in req:
            query = query.order_by(Lower('firstname'))
        if 'firstname_desc' in req:
            query = query.order_by(Lower('firstname')).reverse()
        if 'lastname_asc' in req:
            query = query.order_by(Lower('lastname'))
        if 'lastname_desc' in req:
            query = query.order_by(Lower('lastname')).reverse()
        if 'id_asc' in req:
            query = query.order_by('id')
        if 'id_desc' in req:
            query = query.order_by('-id')
        if 'phone_number_asc' in req:
            query = query.order_by('phone_number')
        if 'phone_number_desc' in req:
            query = query.order_by('-phone_number')
        if 'email_asc' in req:
            query = query.order_by(Lower('email'))
        if 'email_desc' in req:
            query = query.order_by(Lower('email')).reverse()
        
            
        return query
    

    except Exception as e:
        logging.info('sort_user error')
        return query



def sort_managemaster(query,req):
    try:
        if 'category__name_asc' in req:
            query = query.order_by(Lower('category__name'))
        if 'category__name_desc' in req:
            query = query.order_by(Lower('category__name')).reverse()
        if 'properties__property_name_desc' in req:
            query = query.order_by(Lower('properties__property_name')).reverse()
        if 'properties__property_name_asc' in req:
            query = query.order_by(Lower('properties__property_name'))
        if 'category__is_active_asc' in req:
            query = query.order_by('category__is_active')
        if 'category__is_active_desc' in req:
            query = query.order_by('-category__is_active')
        if 'category__is_counteradmin_asc' in req:
            query = query.order_by('category__is_counteradmin')
        if 'category__is_counteradmin_desc' in req:
            query = query.order_by('-category__is_counteradmin')
        if 'category__is_donar_asc' in req:
            query = query.order_by('category__is_donar')
        if 'category__is_donar_desc' in req:
            query = query.order_by('-category__is_donar')
        
        return query
    
    except Exception as e:
        logging.info('sort_managemaster error')
        return query


def sort_ListEntity(query,req):
    try:
       
        if 'entity_asc' in req:
            query = query.order_by(Lower('entity'))
        if 'entity_desc' in req:
            query = query.order_by(Lower('entity')).reverse()
        if 'legal_name_desc' in req:
            query = query.order_by(Lower('legal_name')).reverse()
        if 'legal_name_asc' in req:
            query = query.order_by(Lower('legal_name'))
        if 'companycode_asc' in req:
            query = query.order_by(Lower('companycode'))
        if 'companycode_desc' in req:
            query = query.order_by(Lower('companycode')).reverse()
        if 'cash_limit_asc' in req:
            query = query.order_by('cash_limit')
        if 'cash_limit_desc' in req:
            query = query.order_by('-cash_limit')
        if 'phone_number_asc' in req:
            query = query.order_by('phone_number')
        if 'phone_number_desc' in req:
            query = query.order_by('-phone_number')

        return query
    
    except Exception as e:
        logging.info('sort_entitylist error')
        return query



def sort_counterpaymenthistory(query,req):
    try:
        if 'payment_mode_asc' in req:
            query = query.order_by(Lower('payment_mode'))
        if 'payment_mode_desc' in req:
            query = query.order_by(Lower('payment_mode')).reverse()
        if 'donation_id_desc' in req:
            query = query.order_by('-donation_id')
        if 'donation_id_asc' in req:
            query = query.order_by('donation_id')
        if 'billing_master__firstname_asc' in req:
            query = query.order_by(Lower('billing_master__firstname'))
        if 'billing_master__firstname_desc' in req:
            query = query.order_by(Lower('billing_master__firstname')).reverse()
        if 'refernce_no_asc' in req:
            query = query.order_by('refernce_no')
        if 'refernce_no_desc' in req:
            query = query.order_by('-refernce_no')
        if 'donated_at_asc' in req:
            query = query.order_by('donated_at')
        if 'donated_at_desc' in req:
            query = query.order_by('-donated_at')
        if 'bank_name_asc' in req:
            query = query.order_by(Lower('bank_name'))
        if 'bank_name_desc' in req:
            query = query.order_by(Lower('bank_name')).reverse()
        if 'amount_asc' in req:
            query = query.order_by('amount')
        if 'amount_desc' in req:
            query = query.order_by('-amount')
        
        return query
    
    except Exception as e:
        logging.info('sort_donationlist error')
        return query
    
