from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta
from flask import request, jsonify
from config.db import db
from model.flotys import *



def RegisterDrivers():
    response = {}
    
    new_drivers = Drivers()
    new_drivers.first_name = request.json.get('first_name')
    new_drivers.last_name = request.json.get('last_name')
    new_drivers.email = request.json.get('email')
    new_drivers.phone = request.json.get('phone')
    new_drivers.license_number = request.json.get('license_number')
    new_drivers.license_expiry_date = request.json.get('license_expiry_date')      
    new_drivers.status = request.json.get('status')
    new_drivers.user_id = request.json.get('user_id')
    single_driver = Users.query.filter_by(user_id=new_drivers.user_id).first()
    if single_driver:
        company_id = single_driver.company_id
        print("Company ID:", company_id)
    else:
        print("User not found.")
    new_drivers.company_id = company_id

    db.session.add(new_drivers)
    db.session.commit()

    rs = {}
    rs['first_name'] = new_drivers.first_name
    rs['last_name'] = new_drivers.last_name
    rs['email'] = new_drivers.email
    rs['phone'] = new_drivers.phone
    rs['license_number'] = new_drivers.license_number
    rs['license_expiry_date'] = new_drivers.license_expiry_date
    rs['status'] = new_drivers.status
    rs['drivers_id'] = new_drivers.drivers_id
    rs['user_id'] = new_drivers.user_id
    rs['company_id'] = new_drivers.company_id

    response['status'] = 'Succes'
    response['drivers_infos'] = rs

    return response



def GetAllDrivers():
    response = {}
    try:
        all_drivers = Drivers.query.all()
        drivers_info = []
        for drivers  in all_drivers:
            drivers_infos = {
                'first_name': drivers.first_name,  
                'last_name': drivers.last_name,  
                'email': drivers.email,  
                'phone': drivers.phone,  
                'license_number': drivers.license_number,  
                'license_expiry_date': drivers.license_expiry_date,           
                'status': drivers.status,           
                'drivers_id': drivers.drivers_id,           
                'user_id': drivers.user_id,           
                'company_id': drivers.company_id,           
            }
            drivers_info.append(drivers_infos)
        response['status'] = 'success'
        response ['drivers'] = drivers_info

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response



def GetSingleDrivers():
    response = {}

    try:
        uid = request.json.get('drivers_id')
        single_drivers = Drivers.query.filter_by(drivers_id=uid).first()
        drivers_infos = {
            'first_name': single_drivers.first_name,
            'last_name': single_drivers.last_name,
            'email': single_drivers.email,  
            'phone': single_drivers.phone,  
            'license_number': single_drivers.license_number,              
            'license_expiry_date': single_drivers.license_expiry_date,              
            'status': single_drivers.status,              
            'drivers_id': single_drivers.drivers_id,              
            'user_id': single_drivers.user_id,              
            'company_id': single_drivers.company_id,              
        }
        response['status'] = 'success'
        response['drivers'] = drivers_infos

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response 


def UpdateDrivers():

    response = {}
    uid = request.json.get('drivers_id')
    update_drivers = Drivers.query.filter_by(drivers_id=uid).first()
    if update_drivers:
        update_drivers.first_name = request.json.get('first_name', update_drivers.first_name)
        update_drivers.last_name = request.json.get('last_name', update_drivers.last_name)
        update_drivers.email = request.json.get('email', update_drivers.email) 
        update_drivers.phone = request.json.get('phone', update_drivers.phone)
        update_drivers.license_number = request.json.get('license_number', update_drivers.license_number)
        update_drivers.license_expiry_date = request.json.get('license_expiry_date', update_drivers.license_expiry_date)
        update_drivers.status = request.json.get('status', update_drivers.status)

        db.session.add(update_drivers)
        db.session.commit()

        response['status'] = 'Succes'
        response['first_name'] = update_drivers.first_name
        response['last_name'] = update_drivers.last_name
        response['email'] = update_drivers.email
        response['phone'] = update_drivers.phone
        response['license_number'] = update_drivers.license_number
        response['license_expiry_date'] = update_drivers.license_expiry_date
        response['status'] = update_drivers.status
        response['drivers_id'] = update_drivers.drivers_id
        response['user_id'] = update_drivers.user_id
        response['company_id'] = update_drivers.company_id
    else:
        response['status'] = 'Drivers not found'

    return response



def DeleteDrivers():
    
    response = {}
    try:
        uid = request.json.get('drivers_id')
        delete_drivers = Drivers.query.filter_by(drivers_id=uid).first()
        if delete_drivers:
            db.session.delete(delete_drivers)
            db.session.commit()
            response['status'] = 'success'
        else:
            response['status'] = 'error'
            response['motif'] = 'Drivers non trouvé'

    except Exception as e:
        response['error_description'] = str(e)
        response['status'] = 'error'

    return response