from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta, datetime
from flask import request, jsonify
from config.db import db
from model.flotys import *
from werkzeug.security import check_password_hash
import random


def CreateCompany():
    response = {}

    try:
        unique_id = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        new_company = Company()
        new_company.company_ref = "COM" + unique_id
        new_company.agency_title = request.json.get('agency_title')
        new_company.country = request.json.get('country')
        new_company.address = request.json.get('address')
        new_company.email = request.json.get('email')
        new_company.number = request.json.get('number')
        new_company.created_by = request.json.get('created_by')
        new_company.current_plan_id = request.json.get('current_plan_id') #Trial, Basic, Premium or Pro
        new_company.subscription_status = request.json.get('subscription_status') #Trial, Actived
        new_company.status = "actif"
        
        db.session.add(new_company)
        db.session.commit()

        response['status'] = 'Succes'
        response['company_id'] = new_company.company_id 
        response['company_ref'] = new_company.company_ref 
        response['agency_title'] = new_company.agency_title
        response['country'] = new_company.country
        response['address'] = new_company.address
        response['email'] = new_company.email
        response['number'] = new_company.number
        response['created_by'] = new_company.created_by
        response['subscription_status'] = new_company.subscription_status
        response['current_plan_id'] = new_company.current_plan_id
        response['status'] = new_company.status

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response



def GetAllCompany():
    response = {}
    
    try:
        all_company = Company.query.all()
        company_info = []

        for company  in all_company:
            company_infos = {
                'company_id': company.company_id,  
                'company_ref': company.company_ref,  
                'agency_title': company.agency_title,  
                'country': company.country,  
                'address': company.address,  
                'email': company.email,  
                'number': company.number,  
                'created_by': company.created_by,  
                'subscription_status': company.subscription_status,  
                'current_plan_id': company.current_plan_id,  
                'status': company.status,  
            }
            company_info.append(company_infos)

        response['status'] = 'success'
        response ['company_info'] = company_info

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response


def GetSingleCompany():
    response = {}

    try:
        uid = request.json.get('company_id')
        single_company = Company.query.filter_by(company_id=uid).first()

        company_infos = {
            'company_id': single_company.company_id,
            'company_ref': single_company.company_ref,
            'agency_title': single_company.agency_title,
            'country': single_company.country,
            'address': single_company.address,
            'email': single_company.email,
            'number': single_company.number,            
            'created_by': single_company.created_by,            
            'subscription_status': single_company.subscription_status,            
            'current_plan_id': single_company.current_plan_id,            
            'status': single_company.status,            
        }

        response['status'] = 'success'
        response['company_infos'] = company_infos

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response 



def UpdateCompany (): # You can use this fonction for create Subscription Plans
    response = {}

    try:
        uid = request.json.get('company_id')
        update_company = Company.query.filter_by(company_id=uid).first()
        if update_company:
            update_company.agency_title = request.json.get('agency_title', update_company.agency_title)            
            update_company.country = request.json.get('country', update_company.country)            
            update_company.address = request.json.get('address', update_company.address)
            update_company.email = request.json.get('email', update_company.email)
            update_company.number = request.json.get('number', update_company.number)
            update_company.current_plan_id = request.json.get('current_plan_id', update_company.current_plan_id)
            update_company.subscription_status = request.json.get('subscription_status', update_company.subscription_status)
            update_company.payment_status = request.json.get('payment_status', update_company.payment_status)
            update_company.status = request.json.get('status', update_company.status)

            db.session.add(update_company)
            db.session.commit()

            rs = {}
            rs['company_id'] = update_company.company_id
            rs['company_ref'] = update_company.company_ref
            rs['agency_title'] = update_company.agency_title
            rs['country'] = update_company.country
            rs['address'] = update_company.address
            rs['email'] = update_company.email
            rs['number'] = update_company.number
            rs['created_by'] = update_company.created_by
            rs['subscription_status'] = update_company.subscription_status
            rs['current_plan_id'] = update_company.current_plan_id
            rs['status'] = update_company.status

            response['status'] = 'Succes'
            response['company_infos'] = rs
        else:
            response['status'] = 'Company not found'

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)
    return response



def SubscriptionRenewal (): # You can use this fonction for create Subscription Plans
    response = {}
    try:
        uid = request.json.get('company_id')
        update_company = Company.query.filter_by(company_id=uid).first()

        if update_company:
            update_company.current_plan_id = request.json.get('current_plan_id', update_company.current_plan_id)
            update_company.subscription_status = request.json.get('subscription_status', update_company.subscription_status)
            update_company.subscription_start_date = request.json.get('subscription_start_date', update_company.subscription_start_date)
            update_company.subscription_end_date = request.json.get('subscription_end_date', update_company.subscription_end_date)
            update_company.payment_status = request.json.get('payment_status', update_company.payment_status)

            db.session.add(update_company)
            db.session.commit()

            rs = {}
            rs['company_id'] = update_company.company_id
            rs['company_ref'] = update_company.company_ref
            rs['agency_title'] = update_company.agency_title
            rs['country'] = update_company.country
            rs['address'] = update_company.address
            rs['email'] = update_company.email
            rs['number'] = update_company.number
            rs['created_by'] = update_company.created_by
            rs['subscription_status'] = update_company.subscription_status
            rs['subscription_start_date'] = str(update_company.subscription_start_date)
            rs['subscription_end_date'] = str(update_company.subscription_end_date)
            rs['current_plan_id'] = update_company.current_plan_id
            rs['status'] = update_company.status

            response['status'] = 'Succes'
            response['company_infos'] = rs
        else:
            response['status'] = 'Company not found'

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response



def AutoUpdateCompany():
    response = {}
    try:
        uid = request.json.get('company_id')
        company = Company.query.filter_by(company_id=uid).first()
        now_date = datetime.datetime.now()
        now_time = now_date.time()
        subscription_end_date = company.subscription_end_date
        pending_end_date = company.subscription_end_date - datetime.timedelta(days=7)

        if now_date >= subscription_end_date and now_time == datetime.min.time():
            print('Time Expired at Midnight')
            company.subscription_status = 'Expired'
            db.session.add(company)
            db.session.commit()
            response['subscription_status'] = company.subscription_status
            response['message'] = 'Subscription status updated to Expired.'

        elif pending_end_date <= now_date and now_date < subscription_end_date and now_time == datetime.min.time():
            print('Time Pending at Midnight')
            company.subscription_status = 'Pending'
            db.session.add(company)
            db.session.commit()
            response['subscription_status'] = company.subscription_status
            response['message'] = 'Subscription status updated to Pending.'

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response


def DeleteCompany():
    response = {}

    try:
        uid = request.json.get('company_id')
        delete_company = Company.query.filter_by(company_id=uid).first()
        if delete_company:
            db.session.delete(delete_company)
            db.session.commit()
            response['status'] = 'success'
        else:
            response['status'] = 'error'
            response['motif'] = 'Company non trouvé'

    except Exception as e:
        response['error_description'] = str(e)
        response['status'] = 'error'

    return response