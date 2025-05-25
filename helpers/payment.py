import base64
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import random
import bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import date, timedelta
from flask import request, jsonify
import qrcode
import requests
from config.db import db
from config.constant import *
from model.flotys import *
# from send_mail import send_receipt
from helpers.send_mail import *
from helpers.payment_history import *
from werkzeug.security import check_password_hash
from werkzeug.exceptions import BadRequest


gmail_user = EMAIL_USER
gmail_password = EMAIL_PASSWORD

def generate_product_id():
    unique_id = str(uuid.uuid4().hex)[:4].upper()  # Utilisation des 6 premiers caractères de l'UUID généré
    return unique_id



def CreatePayment():

    headers = {
        'ApiKey': HUB2_API_KEY,
        'Environment': ENV,
        'MerchantId': HUB2_IDMERCHANT
    }

    response = {}

    current_date = datetime.datetime.now().strftime("%Y_%m_%d")
    unique_id = str(uuid.uuid4().hex)[:2].upper()
    number_of_cars_chosen = int(request.json.get('number_of_cars_chosen'))
    
    new_payment = Payment()
    new_payment.payment_ref = "FLO" + current_date + unique_id
    new_payment.payment_methode = request.json.get('payment_methode')
    new_payment.plan_id = request.json.get('plan_id')
    new_payment.number_of_cars_chosen = number_of_cars_chosen
    subscription = SubscriptionPlans.query.filter_by(plan_id=new_payment.plan_id).first()
    if number_of_cars_chosen and number_of_cars_chosen > 0 :
        new_payment.amount = int(subscription.total_cost_for_one_vehicle) * number_of_cars_chosen
    else:
        new_payment.amount = subscription.total_cost_for_one_vehicle
    # new_payment.transaction_reference = request.json.get('transaction_reference')
    new_payment.payment_date = datetime.datetime.now().strftime("%Y-%m-%d")
    payment_date_obj = datetime.datetime.strptime(new_payment.payment_date, "%Y-%m-%d")
    payment_end = payment_date_obj + datetime.timedelta(days=30)
    new_payment.payment_end = payment_end.strftime("%Y-%m-%d")
    new_payment.network = request.json.get('network')
    new_payment.number = request.json.get('number')
    new_payment.name_of_card = request.json.get('name_of_card')
    new_payment.card_number = request.json.get('card_number')
    new_payment.card_type = request.json.get('card_type')
    new_payment.card_expiration_date = request.json.get('card_expiration_date')
    new_payment.card_cvv = request.json.get('card_cvv')
    new_payment.company_ref = request.json.get('company_ref')
    new_payment.number_of_cars_chosen = request.json.get('number_of_cars_chosen')
    new_payment.user_id = request.json.get('user_id')

    data = {}
    data['customerReference'] = str(new_payment.company_ref)
    data['purchaseReference'] = str(new_payment.payment_ref)
    data['amount'] = int(new_payment.amount)
    data['currency'] = "XOF"
    data['overrideBusinessName'] = "Flotys"
    
    if data['amount'] > 0:
        res = requests.post(HUB2_SERVICE_API+'payment-intents',json=data,headers=headers)
        data_response = json.loads(res.content)
        # print(data_response)
        new_payment.payment_id_patner = data_response['id']
        new_payment.payment_token = data_response['token']
        new_payment.payment_intent_log = str(data_response)

    db.session.add(new_payment)
    db.session.commit()

    # rs = {}
    # rs['payment_id'] = new_payment.payment_id
    # rs['payment_methode'] = new_payment.payment_methode
    # rs['plan_id'] = new_payment.plan_id
    # rs['amount'] = new_payment.amount
    # rs['transaction_reference'] = new_payment.transaction_reference
    # rs['payment_date'] = new_payment.payment_date
    # rs['payment_end'] = new_payment.payment_end
    # rs['network'] = new_payment.network
    # rs['number'] = new_payment.number
    # rs['name_of_card'] = new_payment.name_of_card
    # rs['card_number'] = new_payment.card_number
    # rs['card_type'] = new_payment.card_type
    # rs['card_expiration_date'] = new_payment.card_expiration_date
    # rs['card_cvv'] = new_payment.card_cvv
    # rs['payment_status'] = new_payment.payment_status

    response['status'] = 'Success'
    response['payment_id'] = new_payment.payment_id

    return response


def ConfirmPayment():
    response = {}
    headers = {
        'ApiKey': HUB2_API_KEY,
        'Environment': ENV,
        'MerchantId': HUB2_IDMERCHANT
    }
    
    payment_id = request.json.get('payment_id')
    payment = Payment.query.filter_by(payment_id=payment_id).first()

    if int(payment.amount) > 0:
        data = {}
        data['token'] = str(payment.payment_token)
        data['paymentMethod'] = "mobile_money"
        data['country'] = "CI"
        data['provider'] = request.json.get('provider')
        data['mobileMoney'] = {}
        data['mobileMoney']['msisdn'] = payment.number
        data['mobileMoney']['otp'] = request.json.get('otp')
        data['mobileMoney']['onSuccessRedirectionUrl'] = 'https://keletick.ci/main/payment/onSuccessRedirectionUrl'
        data['mobileMoney']['onFailedRedirectionUrl'] = 'https://keletick.ci/main/payment/onFailedRedirectionUrl'
        data['mobileMoney']['onCancelRedirectionUrl'] = 'https://keletick.ci/main/payment/onCancelRedirectionUrl'
        data['mobileMoney']['onFinishRedirectionUrl'] = 'https://keletick.ci/main/payment/onFinishRedirectionUrl'
        data['mobileMoney']['workflow'] = 'otp'
        data['onCancelRedirectionUrl'] = 'https://keletick.ci/main/payment/onCancelRedirectionUrl'
        data['onFinishRedirectionUrl'] = 'https://keletick.ci/main/payment/onFinishRedirectionUrl'
        print("data: ",data)

        # return True 
        res = requests.post(HUB2_SERVICE_API+'payment-intents/'+str(payment.payment_id_patner)+'/payments',json=data,headers=headers)
        data_response = json.loads(res.content)
        print('AVANT',data_response)
        
        try:
            
            payment.payment_methode = request.json.get('payment_methode')
            payment.status = "PROCESSED"
            payment.payment_status = "PAID"
            payment.payment_confirmation_id = data_response['payments'][0]['id']
            payment.payment_confirmation_log = str(data_response)
            payment.status = 'active'
            
            db.session.add(payment)
            db.session.commit()
            
            response['payment_id'] = payment.payment_id
            response['payment_status'] = "PAID"
            response['payment_confirmation_id'] = data_response['payments'][0]['id']
            response['amount'] = payment.amount
            response['amount'] = payment.amount
            response['number'] = payment.number
            response['network'] = payment.network
            response['payment_methode'] = payment.payment_methode
            response['plan_id'] = payment.plan_id
            response['payment_ref'] = payment.payment_ref
            response['company_ref'] = payment.company_ref
            response['number_of_cars_chosen'] = payment.number_of_cars_chosen
            response['payment_date'] = payment.payment_date
            response['payment_end'] = payment.payment_end
            response['response'] = 'success'
            
            print('APRES',data_response)
            generate_receipt(payment.payment_ref)
            RegisterPaymentHistory(payment.user_id, payment.plan_id, payment.amount, payment.payment_date, payment.payment_methode, payment.status, payment.payment_ref)
        except:
            payment.payment_methode = request.json.get('payment_methode')
            payment.status = "ERROR"
            payment.payment_status = "FAILED"
            
            db.session.add(payment)
            db.session.commit()
        
            response['status'] = "ERROR"
            response['response'] = str(data_response)
            response['message'] = 'Une erreur est survenue! veuillez verifiez votre numero ou reessayez plutard!', payment.number
            e = BadRequest(data_response)
            e.data = response
            raise e
    else:
        today = date.today()
        year = today.year
        order_number = 'FREE'+str(year)+str(random.randrange(111111, 999999, 7))
        payment.payment_methode = request.json.get('payment_methode')
        payment.status = "PROCESSED"
        payment.payment_status = "PAID"
        payment.payment_confirmation_id = order_number
        
        db.session.add(payment)
        db.session.commit()
        
        response['payment_id'] = payment.payment_id
        response['payment_status'] = "PAID"
        response['payment_confirmation_id'] = order_number
        response['response'] = 'success'
        # generate_receipt(order.order_reference)
    return response


def generate_receipt(ref:any):
    payment_details = Payment.query.filter_by(payment_ref=ref).first()
    company_details = Company.query.filter_by(company_ref=payment_details.company_ref).first()
    user = str(company_details.agency_title)
    # Data to be encoded
    data = payment_details.payment_ref
    # Encoding data using make() function
    img = qrcode.make(data)
    # Saving as an image requestsfile
    img.save('static/order_qr_code.png')
    
    with open('static/order_qr_code.png', 'rb') as image_file:
        base64_bytes = base64.b64encode(image_file.read())
        
        base64_string = base64_bytes.decode()

    email = []
    email.append(company_details.email)
    # send_receipt(company_details.agency_title, payment_details.id, payment_details, base64_string, email)
    return True



def GetAllPayment():
    response = {}
    try:
        uid = request.json.get('payment_id')
        all_payment = Payment.query.filter_by(payment_id=uid).all()
        payment_info = []
        for payment in all_payment:
            info_payment = {
                'payment_id': payment.payment_id,
                'payment_methode': payment.payment_methode,
                'plan_id': payment.plan_id,
                'amount': payment.amount,
                'transaction_reference': payment.transaction_reference,
                'payment_date': payment.payment_date,
                'payment_end': payment.payment_end,
                'network': payment.network,
                'number': payment.number,
                'name_of_card': payment.name_of_card,
                'card_number': payment.card_number,
                'card_type': payment.card_type,
                'card_expiration_date': payment.card_expiration_date,
                'card_cvv': payment.card_cvv,
                'payment_status': payment.payment_status,
            }
            payment_info.append(info_payment)
        response['status'] = 'success'
        response['payment_info'] = payment_info

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response



def GetSinglePayment():
    response = {}
    try:
        payment_id = request.json.get('payment_id')
        single_payment = Payment.query.filter_by(payment_id=payment_id).first()
        if single_payment:
            info_payment = {
                'payment_id': single_payment.payment_id,
                'payment_methode': single_payment.payment_methode,
                'plan_id': single_payment.plan_id,
                'amount': single_payment.amount,
                'transaction_reference': single_payment.transaction_reference,
                'payment_date': single_payment.payment_date,
                'payment_end': single_payment.payment_end,
                'network': single_payment.network,
                'number': single_payment.number,
                'name_of_card': single_payment.name_of_card,
                'card_number': single_payment.card_number,
                'card_type': single_payment.card_type,
                'card_expiration_date': single_payment.card_expiration_date,
                'card_cvv': single_payment.card_cvv,
                'payment_status': single_payment.payment_status,
            }
            response['status'] = 'success'
            response['payment'] = info_payment
        else:
            response['status'] = 'error'
            response['error_description'] = 'Payment not found'

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response



# def UpdatePayment():
#     response = {}
#     payment_id = request.json.get('payment_id')
#     payment_to_update = Payment.query.filter_by(payment_id=payment_id).first()
#     if payment_to_update:
#         payment_to_update.fullname = request.json.get('fullname', payment_to_update.fullname)
#         payment_to_update.username = request.json.get('username', payment_to_update.username)
#         payment_to_update.password_hash = request.json.get('password_hash', payment_to_update.password_hash)  # Hachez le mot de passe si nécessaire
#         payment_to_update.email = request.json.get('email', payment_to_update.email)
#         payment_to_update.role = request.json.get('role', payment_to_update.role)
#         payment_to_update.status = request.json.get('status', payment_to_update.status)

#         db.session.commit()

#         rs = {}
#         rs['payment_id'] = payment_to_update.payment_id
#         rs['payment_methode'] = payment_to_update.payment_methode
#         rs['plan_id'] = payment_to_update.plan_id
#         rs['amount'] = payment_to_update.amount
#         rs['transaction_reference'] = payment_to_update.transaction_reference
#         rs['payment_date'] = payment_to_update.payment_date
#         rs['payment_end'] = payment_to_update.payment_end
#         rs['payment_status'] = payment_to_update.payment_status

#         response['status'] = 'Success'
#         response['payment_id'] = rs
#     else:
#         response['status'] = 'error'
#         response['error_description'] = 'Payment not found'

#     return response



def DeletePayment():
    response = {}
    try:
        payment_id = request.json.get('payment_id')
        payment_to_delete = Payment.query.filter_by(payment_id=payment_id).first()
        if payment_to_delete:
            db.session.delete(payment_to_delete)
            db.session.commit()
            response['status'] = 'success'
        else:
            response['status'] = 'error'
            response['error_description'] = 'Payment not found'

    except Exception as e:
        response['error_description'] = str(e)
        response['status'] = 'error'

    return response