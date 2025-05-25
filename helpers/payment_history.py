from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import date, timedelta
from flask import request, jsonify
from config.db import db
from config.constant import *
from model.flotys import *
from helpers.send_mail import *
from werkzeug.security import check_password_hash
from werkzeug.exceptions import BadRequest


def RegisterPaymentHistory(user_id, plan_id, amount, payment_date, payment_method, payment_ref, status):

    response = {}

    new_payment_history = PaymentHistory()
    new_payment_history.user_id = user_id
    new_payment_history.plan_id = plan_id
    new_payment_history.amount = amount
    new_payment_history.payment_date = payment_date
    new_payment_history.payment_method = payment_method
    new_payment_history.status = status      
    new_payment_history.payment_ref = payment_ref

    db.session.add(new_payment_history)
    db.session.commit()

    rs = {}
    rs['user_id'] = new_payment_history.user_id
    rs['plan_id'] = new_payment_history.plan_id
    rs['amount'] = new_payment_history.amount
    rs['payment_date'] = new_payment_history.payment_date
    rs['payment_method'] = new_payment_history.payment_method
    rs['payment_ref'] = new_payment_history.payment_ref
    rs['status'] = new_payment_history.status

    response['status'] = 'Succes'
    response['payment_history_infos'] = rs

    return response



def GetAllPaymentHistory():
    response = {}
    try:
        all_payment_history = PaymentHistory.query.all()
        payment_history_info = []
        for payment_history  in all_payment_history:
            payment_history_infos = {
                'user_id': payment_history.user_id,  
                'plan_id': payment_history.plan_id,  
                'amount': payment_history.amount,  
                'payment_date': payment_history.payment_date,  
                'payment_method': payment_history.payment_method,  
                'payment_ref': payment_history.payment_ref,           
                'status': payment_history.status,           
            }
            payment_history_info.append(payment_history_infos)
            
        response['status'] = 'success'
        response ['payment_history'] = payment_history_info

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response
