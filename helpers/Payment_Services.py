from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta
from flask import request, jsonify
from config.db import db
from model.flotys import *
from werkzeug.security import check_password_hash
import uuid
import json

def CreatePaymentPlan():
    response = {}
    try:
        new_payment_plan = Payment_Services()
        payment_id = str(uuid.uuid4())
        new_payment_plan.payment_id = payment_id
        new_payment_plan.projet = request.json.get('projet')
        new_payment_plan.firstname = request.json.get('firstname')
        new_payment_plan.lastname = request.json.get('lastname')
        new_payment_plan.email = request.json.get('email')
        new_payment_plan.mobile = request.json.get('mobile')
        new_payment_plan.country = request.json.get('country')
        new_payment_plan.city = request.json.get('city')
        new_payment_plan.plan_title = request.json.get('plan_title')
        new_payment_plan.amount = request.json.get('amount')
        new_payment_plan.description = request.json.get('description')  
        new_payment_plan.status = 'Active'
        
        db.session.add(new_payment_plan)
        db.session.commit()

        rs = {
            'payment_id': new_payment_plan.payment_id,
            'projet': new_payment_plan.projet,
            'firstname': new_payment_plan.firstname,
            'lastname': new_payment_plan.lastname,
            'email': new_payment_plan.email,
            'mobile': new_payment_plan.mobile,
            'country': new_payment_plan.country,
            'city': new_payment_plan.city,
            'plan_title': new_payment_plan.plan_title,
            'amount': new_payment_plan.amount,
            'description': new_payment_plan.description,
            'status': new_payment_plan.status,
            'created_at': str(new_payment_plan.created_at)
        }

        response['status'] = 'success'
        response['payment_infos'] = rs

    except Exception as e:
        response['error_description'] = str(e)
        response['status'] = 'error'

    return response


def ReadAllPaymentPlan():
    response = {}
    
    try:
        all_payment = Payment_Services.query.all()
        payment_info = []
        for payment in all_payment:
            payment_infos = {
                'payment_id': payment.payment_id,
                'firstname': payment.firstname,
                'lastname': payment.lastname,
                'email': payment.email,
                'mobile': payment.mobile,
                'country': payment.country,
                'city': payment.city,
                'plan_title': payment.plan_title,
                'amount': payment.amount,
                'description': payment.description,
                'status': payment.status,
                'created_at': str(payment.created_at),
            }
            payment_info.append(payment_infos)

        response['status'] = 'success'
        response['payment_infos'] = payment_info

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response


def ReadSinglePaymentPlan():
    response = {}

    try:
        payment_id = request.json.get('payment_id')
        single_payment = Payment_Services.query.filter_by(payment_id=payment_id).first()
        payment_infos = {
            'payment_id': single_payment.payment_id,
            'firstname': single_payment.firstname,
            'lastname': single_payment.lastname,
            'email': single_payment.email,
            'mobile': single_payment.mobile,
            'country': single_payment.country,
            'city': single_payment.city,
            'plan_title': single_payment.plan_title,
            'amount': single_payment.amount,
            'description': single_payment.description,
            'status': single_payment.status,
            'created_at': str(single_payment.created_at),
        }
        response['status'] = 'success'
        response['payment_infos'] = payment_infos

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response 


def UpdatePaymentStatus():
    response = {}

    payment_id = request.json.get('payment_id')
    update_payment_status = Payment_Services.query.filter_by(payment_id=payment_id).first()

    if update_payment_status:
        update_payment_status.order_status = request.json.get('order_status')
        update_payment_status.order_payment_status = request.json.get('order_payment_status')
        update_payment_status.order_payment_confirmation_id = request.json.get('order_payment_confirmation_id')
   
        db.session.add(update_payment_status)
        db.session.commit()

        response['status'] = 'success'
        response['payment_id'] = update_payment_status.payment_id
        response['firstname'] = update_payment_status.firstname
        response['lastname'] = update_payment_status.lastname
        response['email'] = update_payment_status.email
        response['mobile'] = update_payment_status.mobile
        response['country'] = update_payment_status.country
        response['city'] = update_payment_status.city
        response['projet'] = update_payment_status.projet
        response['plan_title'] = update_payment_status.plan_title
        response['amount'] = update_payment_status.amount
        response['description'] = update_payment_status.description
        response['order_status'] = update_payment_status.order_status
        response['order_payment_status'] = update_payment_status.order_payment_status
        response['order_payment_confirmation_id'] = update_payment_status.order_payment_confirmation_id
        response['created_at'] = str(update_payment_status.created_at)
        response['updated_on'] = str(update_payment_status.updated_on)
    else:
        response['status'] = 'Payment not found'

    return response
