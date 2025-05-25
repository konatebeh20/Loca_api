from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta
from flask import request, jsonify
from config.db import db
from model.flotys import *


def generate_product_id(license_plate):
    prefix = license_plate[:2].upper()
    unique_id = str(uuid.uuid4().hex)[:10].upper()  # Utilisation des 6 premiers caractères de l'UUID généré
    ref_wheel = prefix + unique_id
    return ref_wheel


def RegisterVehicles():
    response = {}
    
    new_vehicle = Vehicles()
    new_vehicle.drivers_id = request.json.get('drivers_id')
    single_driver = Drivers.query.filter_by(drivers_id=new_vehicle.drivers_id).first()
    if single_driver:
        company_id = single_driver.company_id
        user_id = single_driver.user_id
        print("Company ID:", company_id)
    else:
        print("User not found.")
    new_vehicle.company_id = company_id
    new_vehicle.license_plate = request.json.get('license_plate')
    new_vehicle.model = request.json.get('model')
    new_vehicle.number_wheel = request.json.get('number_wheel')
    new_vehicle.ref_wheel = generate_product_id(new_vehicle.license_plate)
    new_vehicle.manufacturer = request.json.get('manufacturer')      
    new_vehicle.year = request.json.get('year')
    new_vehicle.vin = request.json.get('vin')
    new_vehicle.device_type = request.json.get('device_type')
    new_vehicle.device_id = request.json.get('device_id')
    new_vehicle.status = request.json.get('status')
    new_vehicle.user_id = user_id
    new_vehicle.current_location_id = request.json.get('current_location_id')
    new_vehicle.color = request.json.get('color')
    new_vehicle.make = request.json.get('make')
    new_vehicle.body_type = request.json.get('body_type')
    new_vehicle.purchase_price = request.json.get('purchase_price')
    new_vehicle.current_value = request.json.get('current_value')
    new_vehicle.engine_type = request.json.get('engine_type')
    new_vehicle.fuel_type = request.json.get('fuel_type')
    new_vehicle.transmission_type = request.json.get('transmission_type')
    new_vehicle.seating_capacity = request.json.get('seating_capacity')
    new_vehicle.odometer_reading = request.json.get('odometer_reading')
    new_vehicle.purchase_date = request.json.get('purchase_date')
    
    db.session.add(new_vehicle)
    db.session.commit()

    rs = {}
    rs['vehicle_id'] = str(new_vehicle.vehicle_id)
    rs['drivers_id'] = str(new_vehicle.drivers_id)
    rs['company_id'] = str(new_vehicle.company_id)
    rs['license_plate'] = str(new_vehicle.license_plate)
    rs['model'] = str(new_vehicle.model)
    rs['number_wheel'] = str(new_vehicle.number_wheel)
    rs['ref_wheel'] = str(new_vehicle.ref_wheel)
    rs['manufacturer'] = str(new_vehicle.manufacturer)
    rs['year'] = str(new_vehicle.year)
    rs['vin'] = str(new_vehicle.vin)
    rs['status'] = str(new_vehicle.status)
    rs['current_location_id'] = str(new_vehicle.current_location_id)
    rs['user_id'] = str(new_vehicle.user_id)
    rs['color'] = str(new_vehicle.color)
    rs['make'] = str(new_vehicle.make)
    rs['body_type'] = str(new_vehicle.body_type)
    rs['purchase_price'] = str(new_vehicle.purchase_price)
    rs['current_value'] = str(new_vehicle.current_value)
    rs['engine_type'] = str(new_vehicle.engine_type)
    rs['fuel_type'] = str(new_vehicle.fuel_type)
    rs['transmission_type'] = str(new_vehicle.transmission_type)
    rs['seating_capacity'] = str(new_vehicle.seating_capacity)
    rs['odometer_reading'] = str(new_vehicle.odometer_reading)
    rs['purchase_date'] = str(new_vehicle.purchase_date)
    rs['device_id'] = str(new_vehicle.device_id)
    rs['device_type'] = str(new_vehicle.device_type)

    response['status'] = 'Succes'
    response['vehicle_infos'] = rs

    return response



def GetAllVehicles():
    response = {}
    
    try:
        all_vehicles = Vehicles.query.all()
        vehicles_info = []
        for vehicles  in all_vehicles:
            vehicles_infos = {
                'vehicle_id': vehicles.vehicle_id,  
                'drivers_id': vehicles.drivers_id,  
                'company_id': vehicles.company_id,  
                'license_plate': vehicles.license_plate,  
                'model': vehicles.model,  
                'number_wheel': vehicles.number_wheel,  
                'ref_wheel': vehicles.ref_wheel,           
                'manufacturer': vehicles.manufacturer,           
                'year': vehicles.year,           
                'vin': vehicles.vin,           
                'status': vehicles.status,           
                'current_location_id': vehicles.current_location_id,           
                'user_id': vehicles.user_id,           
                'color': vehicles.color,           
                'make': vehicles.make,           
                'body_type': vehicles.body_type,           
                'purchase_price': vehicles.purchase_price,           
                'current_value': vehicles.current_value,           
                'engine_type': vehicles.engine_type,           
                'fuel_type': vehicles.fuel_type,           
                'transmission_type': vehicles.transmission_type,           
                'seating_capacity': vehicles.seating_capacity,           
                'odometer_reading': vehicles.odometer_reading,           
                'purchase_date': vehicles.purchase_date,           
                'device_id': vehicles.device_id,           
                'device_type': vehicles.device_type,           
            }
            vehicles_info.append(vehicles_infos)
        response['status'] = 'success'
        response ['vehicles'] = vehicles_info

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response



def GetSingleVehicles():
    response = {}

    try:
        uid = request.json.get('vehicle_id')
        single_vehicles = Vehicles.query.filter_by(vehicle_id=uid).first()
        vehicles_infos = {
            'vehicle_id': single_vehicles.vehicle_id,
            'drivers_id': single_vehicles.drivers_id,
            'company_id': single_vehicles.company_id,
            'license_plate': single_vehicles.license_plate,  
            'model': single_vehicles.model,  
            'number_wheel': single_vehicles.number_wheel,              
            'ref_wheel': single_vehicles.ref_wheel,              
            'manufacturer': single_vehicles.manufacturer,              
            'year': single_vehicles.year,              
            'vin': single_vehicles.vin,              
            'status': single_vehicles.status,              
            'current_location_id': single_vehicles.current_location_id,              
            'user_id': single_vehicles.user_id,              
            'color': single_vehicles.color,              
            'make': single_vehicles.make,              
            'body_type': single_vehicles.body_type,              
            'purchase_price': single_vehicles.purchase_price,              
            'current_value': single_vehicles.current_value,              
            'engine_type': single_vehicles.engine_type,              
            'fuel_type': single_vehicles.fuel_type,              
            'transmission_type': single_vehicles.transmission_type,              
            'seating_capacity': single_vehicles.seating_capacity,              
            'odometer_reading': single_vehicles.odometer_reading,              
            'purchase_date': single_vehicles.purchase_date,              
            'device_id': single_vehicles.device_id,              
            'device_type': single_vehicles.device_type,              
        }
        response['status'] = 'success'
        response['vehicles'] = vehicles_infos

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response 


def UpdateVehicles():

    response = {}
    uid = request.json.get('vehicle_id')
    update_vehicles = Vehicles.query.filter_by(vehicle_id=uid).first()
    if update_vehicles:
        update_vehicles.model = request.json.get('model', update_vehicles.model)
        update_vehicles.manufacturer = request.json.get('manufacturer', update_vehicles.manufacturer)
        update_vehicles.year = request.json.get('year', update_vehicles.year) 
        update_vehicles.vin = request.json.get('vin', update_vehicles.vin)
        update_vehicles.status = request.json.get('status', update_vehicles.status)
        update_vehicles.current_location_id = request.json.get('current_location_id', update_vehicles.current_location_id)
        update_vehicles.color = request.json.get('color', update_vehicles.color)
        update_vehicles.make = request.json.get('make', update_vehicles.make)
        update_vehicles.body_type = request.json.get('body_type', update_vehicles.body_type)
        update_vehicles.purchase_price = request.json.get('purchase_price', update_vehicles.purchase_price)
        update_vehicles.current_value = request.json.get('current_value', update_vehicles.current_value)
        update_vehicles.engine_type = request.json.get('engine_type', update_vehicles.engine_type)
        update_vehicles.fuel_type = request.json.get('fuel_type', update_vehicles.fuel_type)
        update_vehicles.transmission_type = request.json.get('transmission_type', update_vehicles.transmission_type)
        update_vehicles.seating_capacity = request.json.get('seating_capacity', update_vehicles.seating_capacity)
        update_vehicles.odometer_reading = request.json.get('odometer_reading', update_vehicles.odometer_reading)
        update_vehicles.purchase_date = request.json.get('purchase_date', update_vehicles.purchase_date)
        update_vehicles.device_id = request.json.get('device_id', update_vehicles.device_id)
        update_vehicles.device_type = request.json.get('device_type', update_vehicles.device_type)

        db.session.add(update_vehicles)
        db.session.commit()

        response['status'] = 'Succes'
        response['vehicle_id'] = update_vehicles.vehicle_id
        response['drivers_id'] = update_vehicles.drivers_id
        response['company_id'] = update_vehicles.company_id
        response['license_plate'] = update_vehicles.license_plate
        response['model'] = update_vehicles.model
        response['number_wheel'] = update_vehicles.number_wheel
        response['ref_wheel'] = update_vehicles.ref_wheel
        response['manufacturer'] = update_vehicles.manufacturer
        response['year'] = update_vehicles.year
        response['vin'] = update_vehicles.vin
        response['status'] = update_vehicles.status
        response['current_location_id'] = update_vehicles.current_location_id
        response['user_id'] = update_vehicles.user_id
        response['color'] = update_vehicles.color
        response['make'] = update_vehicles.make
        response['body_type'] = update_vehicles.body_type
        response['purchase_price'] = update_vehicles.purchase_price
        response['current_value'] = update_vehicles.current_value
        response['engine_type'] = update_vehicles.engine_type
        response['fuel_type'] = update_vehicles.fuel_type
        response['transmission_type'] = update_vehicles.transmission_type
        response['seating_capacity'] = update_vehicles.seating_capacity
        response['odometer_reading'] = update_vehicles.odometer_reading
        response['purchase_date'] = update_vehicles.purchase_date
        response['device_id'] = update_vehicles.device_id
        response['device_type'] = update_vehicles.device_type
    else:
        response['status'] = 'Vehicles not found'

    return response



def DeleteVehicles():
    
    response = {}
    try:
        uid = request.json.get('vehicle_id')
        delete_vehicles = Vehicles.query.filter_by(vehicle_id=uid).first()
        if delete_vehicles:
            db.session.delete(delete_vehicles)
            db.session.commit()
            response['status'] = 'success'
        else:
            response['status'] = 'error'
            response['motif'] = 'Vehicles non trouvé'

    except Exception as e:
        response['error_description'] = str(e)
        response['status'] = 'error'

    return response