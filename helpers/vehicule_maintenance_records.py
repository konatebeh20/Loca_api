from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta
from flask import request, jsonify
from config.db import db
from model.flotys import *


def CreateMaintenanceRecord():
    response = {}
    
    new_record = VehicleMaintenanceRecords()
    new_record.vehicle_id = request.json.get('vehicle_id')
    new_record.maintenance_date = request.json.get('maintenance_date')
    new_record.description = request.json.get('description')
    new_record.cost = request.json.get('cost')
    new_record.status = request.json.get('status')

    db.session.add(new_record)
    db.session.commit()

    rs = {}
    rs['uid'] = new_record.uid
    rs['vehicle_id'] = new_record.vehicle_id
    rs['maintenance_date'] = new_record.maintenance_date
    rs['description'] = new_record.description
    rs['cost'] = new_record.cost
    rs['status'] = new_record.status

    response['status'] = 'Success'
    response['maintenance_info'] = rs

    return response


def GetAllMaintenanceRecords():
    response = {}
    try:
        all_records = VehicleMaintenanceRecords.query.all()
        records_info = []
        for record in all_records:
            info_record = {
                'uid': record.uid,
                'vehicle_id': record.vehicle_id,
                'maintenance_date': record.maintenance_date,
                'description': record.description,
                'cost': record.cost,
                'status': record.status,
            }
            records_info.append(info_record)
        response['status'] = 'success'
        response['maintenance_records'] = records_info

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response


def GetSingleMaintenanceRecord():
    response = {}

    try:
        uid = request.json.get('uid')
        single_record = VehicleMaintenanceRecords.query.filter_by(uid=uid).first()
        if single_record:
            info_record = {
                'uid': single_record.uid,
                'vehicle_id': single_record.vehicle_id,
                'maintenance_date': single_record.maintenance_date,
                'description': single_record.description,
                'cost': single_record.cost,
                'status': single_record.status,
            }
            response['status'] = 'success'
            response['maintenance_record'] = info_record
        else:
            response['status'] = 'error'
            response['error_description'] = 'Maintenance record not found'

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response



def UpdateMaintenanceRecord():
    response = {}
    uid = request.json.get('uid')
    record_to_update = VehicleMaintenanceRecords.query.filter_by(uid=uid).first()
    if record_to_update:
        record_to_update.description = request.json.get('description', record_to_update.description)
        record_to_update.cost = request.json.get('cost', record_to_update.cost)
        record_to_update.status = request.json.get('status', record_to_update.status)

        db.session.commit()

        rs = {}
        rs['uid'] = record_to_update.uid
        rs['vehicle_id'] = record_to_update.vehicle_id
        rs['maintenance_date'] = record_to_update.maintenance_date
        rs['description'] = record_to_update.description
        rs['cost'] = record_to_update.cost
        rs['status'] = record_to_update.status

        response['status'] = 'Success'
        response['uid'] = rs
    else:
        response['status'] = 'error'
        response['error_description'] = 'Maintenance record not found'

    return response



def DeleteMaintenanceRecord():
    response = {}
    try:
        uid = request.json.get('uid')
        record_to_delete = VehicleMaintenanceRecords.query.filter_by(uid=uid).first()
        if record_to_delete:
            db.session.delete(record_to_delete)
            db.session.commit()
            response['status'] = 'success'
        else:
            response['status'] = 'error'
            response['error_description'] = 'Maintenance record not found'

    except Exception as e:
        response['error_description'] = str(e)
        response['status'] = 'error'

    return response


