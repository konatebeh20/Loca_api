from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta
from flask import request, jsonify
from config.db import db
from model.flotys import *



def RegisterTrackingDevice():
    response = {}
    
    new_tracking_device = TrackingDevice()
    new_tracking_device.reference = request.json.get('reference')
    new_tracking_device.vehicle_id = request.json.get('vehicle_id')
    new_tracking_device.user_id = request.json.get('user_id')

    db.session.add(new_tracking_device)
    db.session.commit()

    rs = {}
    rs['tracking_device_id'] = new_tracking_device.tracking_device_id
    rs['reference'] = new_tracking_device.reference
    rs['vehicle_id'] = new_tracking_device.vehicle_id
    rs['user_id'] = new_tracking_device.user_id

    response['status'] = 'Succes'
    response['tracking_device_infos'] = rs

    return response



def GetAllTrackingDevice():
    response = {}
    try:
        all_tracking_device = TrackingDevice.query.all()
        tracking_device_info = []
        for tracking_device  in all_tracking_device:
            tracking_device_infos = {
                'tracking_device_id': tracking_device.tracking_device_id,  
                'reference': tracking_device.reference,  
                'vehicle_id': tracking_device.vehicle_id,  
                'user_id': tracking_device.user_id,  
            }
            tracking_device_info.append(tracking_device_infos)
        response['status'] = 'success'
        response ['tracking_device'] = tracking_device_info

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response



def GetSingleTrackingDevice():
    response = {}

    try:
        uid = request.json.get('tracking_device_id')
        single_tracking_device = TrackingDevice.query.filter_by(tracking_device_id=uid).first()
        tracking_device_infos = {
            'tracking_device_id': single_tracking_device.tracking_device_id,
            'reference': single_tracking_device.reference,
            'vehicle_id': single_tracking_device.vehicle_id,  
            'user_id': single_tracking_device.user_id,  
        }
        response['status'] = 'success'
        response['tracking_device'] = tracking_device_infos

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response 



def UpdateTrackingDevice():

    response = {}
    uid = request.json.get('tracking_device_id')
    update_tracking_device = TrackingDevice.query.filter_by(tracking_device_id=uid).first()
    if update_tracking_device:
        update_tracking_device.reference = request.json.get('reference', update_tracking_device.reference)
        update_tracking_device.vehicle_id = request.json.get('vehicle_id', update_tracking_device.vehicle_id) 

        db.session.add(update_tracking_device)
        db.session.commit()

        response['status'] = 'Succes'
        response['tracking_device_id'] = update_tracking_device.tracking_device_id
        response['reference'] = update_tracking_device.reference
        response['vehicle_id'] = update_tracking_device.vehicle_id
        response['user_id'] = update_tracking_device.user_id
    else:
        response['status'] = 'tracking_device not found'

    return response



def DeleteTrackingDevice():
    
    response = {}
    try:
        uid = request.json.get('tracking_device_id')
        delete_tracking_device = TrackingDevice.query.filter_by(tracking_device_id=uid).first()
        if delete_tracking_device:
            db.session.delete(delete_tracking_device)
            db.session.commit()
            response['status'] = 'success'
        else:
            response['status'] = 'error'
            response['motif'] = 'tracking device non trouvé'

    except Exception as e:
        response['error_description'] = str(e)
        response['status'] = 'error'

    return response