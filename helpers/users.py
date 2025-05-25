from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta
from datetime import datetime
from flask import request, jsonify
from config.db import db
from config.constant import *
from model.flotys import *
from helpers.send_mail import send_mailer
from werkzeug.security import check_password_hash

gmail_user = EMAIL_USER
gmail_password = EMAIL_PASSWORD

def generate_product_id():
    unique_id = str(uuid.uuid4().hex)[:4].upper()  # Utilisation des 6 premiers caractères de l'UUID généré
    return unique_id


def test_name():

    payment_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Ajouter 30 jours à la date de paiement
    payment_date_obj = datetime.datetime.strptime(payment_date, "%Y-%m-%d")
    payment_end = payment_date_obj + datetime.timedelta(days=30)

    # current_date = datetime.datetime.now().strftime("%Y_%m_%d")
    # unique_id = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    print(payment_date, payment_end.strftime("%Y-%m-%d"))

    return True


def CreateUser():
    response = {}

    try:
        uid = generate_product_id()

        password = "Wellcome"
        new_user = Users()
        new_user.fullname = request.json.get('fullname')
        new_user.username = "Bonjour123" + uid
        new_user.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Assurez-vous de hacher le mot de passe
        new_user.email = request.json.get('email')
        new_user.role = request.json.get('role') #admin_company or user_company
        new_user.company_id = request.json.get('company_id') 
        new_user.device_token = request.json.get('device_token')
        new_user.status = request.json.get('status')

        db.session.add(new_user)
        db.session.commit()

        rs = {}
        rs['user_id'] = new_user.user_id
        rs['fullname'] = new_user.fullname
        rs['username'] = new_user.username
        rs['email'] = new_user.email
        rs['role'] = new_user.role
        rs['company_id'] = new_user.company_id
        rs['device_token'] = new_user.device_token
        rs['status'] = new_user.status

        send_mailer(new_user.username ,new_user.email, password)

        response['status'] = 'Success'
        response['user_info'] = rs

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response



def GetAllUserByCompany():
    response = {}
    try:
        uid = request.json.get('company_id')
        all_user_company = Users.query.filter_by(company_id=uid).all()
        user_company_info = []
        for user_company in all_user_company:
            info_user_company = {
                'user_id': user_company.user_id,
                'fullname': user_company.fullname,
                'username': user_company.username,
                'email': user_company.email,
                'role': user_company.role,
                'company_id': user_company.company_id,
                'status': user_company.status,
            }
            user_company_info.append(info_user_company)
        response['status'] = 'success'
        response['user_company'] = user_company_info

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response

    

def GetAllUserCompany():
    response = {}
    try:
        all_user_company = Users.query.filter_by(role='user_company').all()
        user_company_info = []
        for user_company in all_user_company:
            info_user_company = {
                'user_id': user_company.user_id,
                'fullname': user_company.fullname,
                'username': user_company.username,
                'email': user_company.email,
                'role': user_company.role,
                'company_id': user_company.company_id,
                'status': user_company.status,
            }
            user_company_info.append(info_user_company)
        response['status'] = 'success'
        response['user_company'] = user_company_info

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response


def GetAllAdminCompany():
    response = {}
    try:
        all_user_company = Users.query.filter_by(role='admin_company').all()
        user_company_info = []
        for user_company in all_user_company:
            info_user_company = {
                'user_id': user_company.user_id,
                'fullname': user_company.fullname,
                'username': user_company.username,
                'email': user_company.email,
                'role': user_company.role,
                'company_id': user_company.company_id,
                'status': user_company.status,
            }
            user_company_info.append(info_user_company)
        response['status'] = 'success'
        response['user_company'] = user_company_info

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response



def GetSingleUser():
    response = {}

    try:
        user_id = request.json.get('user_id')
        single_user = Users.query.filter_by(user_id=user_id).first()
        if single_user:
            info_user = {
                'user_id': single_user.user_id,
                'fullname': single_user.fullname,
                'username': single_user.username,
                'email': single_user.email,
                'role': single_user.role,
                'company_id': single_user.company_id,
                'status': single_user.status,
            }
            response['status'] = 'success'
            response['users_infos'] = info_user
        else:
            response['status'] = 'error'
            response['error_description'] = 'User not found'

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response



def UpdateUser():
    response = {}
    user_id = request.json.get('user_id')
    user_to_update = Users.query.filter_by(user_id=user_id).first()
    if user_to_update:
        user_to_update.fullname = request.json.get('fullname', user_to_update.fullname)
        user_to_update.username = request.json.get('username', user_to_update.username)
        user_to_update.password_hash = request.json.get('password_hash', user_to_update.password_hash)  # Hachez le mot de passe si nécessaire
        user_to_update.email = request.json.get('email', user_to_update.email)
        user_to_update.role = request.json.get('role', user_to_update.role)
        user_to_update.status = request.json.get('status', user_to_update.status)

        db.session.commit()

        rs = {}
        rs['user_id'] = user_to_update.user_id
        rs['fullname'] = user_to_update.fullname
        rs['username'] = user_to_update.username
        rs['email'] = user_to_update.email
        rs['role'] = user_to_update.role
        rs['company_id'] = user_to_update.company_id
        rs['status'] = user_to_update.status
        response['status'] = 'Success'
        response['users_infos'] = rs
    else:
        response['status'] = 'error'
        response['error_description'] = 'User not found'

    return response



def UpdateIdentifier():
    response = {}
    try:
        user_id = request.json.get('user_id')
        user_to_update = Users.query.filter_by(user_id=user_id).first()
        if user_to_update:
            user_to_update.username = request.json.get('username', user_to_update.username)  # Hachez le mot de passe si nécessaire
            password = request.json.get('password_hash', user_to_update.password_hash)  # Hachez le mot de passe si nécessaire
            user_to_update.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Assurez-vous de hacher le mot de passe

            db.session.commit()
            rs = {}
            rs['user_id'] = user_to_update.user_id
            rs['username'] = user_to_update.username

            response['status'] = 'Success'
            response['users_infos'] = rs
        else:
            response['status'] = 'error'
            response['error_description'] = 'User not found'
    except Exception as e:
        response['error_description'] = str(e)
        response['status'] = 'error'

    return response



def DeleteUser():
    response = {}
    try:
        user_id = request.json.get('user_id')
        user_to_delete = Users.query.filter_by(user_id=user_id).first()
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
            response['status'] = 'success'
        else:
            response['status'] = 'error'
            response['error_description'] = 'User not found'

    except Exception as e:
        response['error_description'] = str(e)
        response['status'] = 'error'

    return response



def LoginUsers():
    reponse = {}
    try:
        identifier = request.json.get('identifier')
        password_hash = request.json.get('password_hash')

        login_users = Users.query.filter((Users.email == identifier) | (Users.username == identifier)).first()
        company = Company.query.filter_by(company_id = login_users.company_id).first()
        print(login_users.company_id)

        username = login_users.username
        if login_users:
            if bcrypt.checkpw(password_hash.encode('utf-8'), login_users.password_hash.encode('utf-8')):
                if username.startswith("Bonjour123"):
                    reponse['login_type'] = 'new'
                users_infos = {
                    'user_id': login_users.user_id,
                    'fullname': login_users.fullname,
                    'username': login_users.username,
                    'email': login_users.email,
                    'role': login_users.role,
                    'company_id': login_users.company_id,
                    'status': login_users.status,
                }
                expires = timedelta(hours=1)
                access_token = create_access_token(identity=identifier)

                reponse['status'] = 'success'
                reponse['users_infos'] = users_infos
                reponse['access_token'] = access_token
            else:
                reponse['status'] = 'error'
                reponse['message'] = 'Invalid email/username or password'
        else:
            reponse['status'] = 'error'
            reponse['message'] = 'User not found'

    except Exception as e:
        reponse['error_description'] = str(e)
        reponse['status'] = 'error'

    return reponse
