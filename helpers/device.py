from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta
from flask import request, jsonify
from config.db import db
from model.flotys import *



def CreateDevice():
    response = {}
    all_device = []

    device = {
        "Blueberry GT06N",
        "Coban GPS303-C",
        "Concox GT06N",
        "GPS103-B",
        "GT06",
        "SinoTrack ST-901",
        "Teltonika FM1100",
        "Teltonika FMB125"
    }
    
    for item in device:
        print("Device: ",item)
        new_device = Device()
        new_device.device_protocol = "GT06"
        new_device.device_label = item

        db.session.add(new_device)
        db.session.commit()

        rs = {
            'device_id': new_device.device_id,
            'device_protocol': new_device.device_protocol,
            'device_label': new_device.device_label
        }
        all_device.append(rs)

        response['status'] = 'Success'
        response['device_infos'] = all_device

    return response




def GetAllDevice():
    response = {}
    try:
        all_device = Device.query.all()
        device_info = []
        for device  in all_device:
            device_infos = {
                'device_id': device.device_id,  
                'device_protocol': device.device_protocol,  
                'device_label': device.device_label,            
            }
            device_info.append(device_infos)
        response['status'] = 'success'
        response ['device'] = device_info

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response



def GetSingleDevice():
    response = {}

    try:
        device_id = request.json.get('device_id')
        single_device = Device.query.filter_by(device_id=device_id).first()
        device_infos = {
            'device_id': single_device.device_id,
            'device_protocol': single_device.device_protocol,  
            'device_label': single_device.device_label,              
        }
        response['status'] = 'success'
        response['device'] = device_infos

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response 


def UpdateDevice():

    response = {}
    device_id = request.json.get('device_id')
    update_device = Device.query.filter_by(device_id=device_id).first()
    if update_device:
        update_device.device_protocol = request.json.get('device_protocol', update_device.device_protocol)
        update_device.device_label = request.json.get('device_label', update_device.device_label) 

        db.session.add(update_device)
        db.session.commit()

        response['status'] = 'Succes'
        response['device_id'] = update_device.device_id
        response['device_protocol'] = update_device.device_protocol
        response['device_label'] = update_device.device_label
    else:
        response['status'] = 'Device not found'

    return response



def DeleteDevice():
    
    response = {}
    try:
        device_id = request.json.get('device_id')
        delete_device = Device.query.filter_by(device_id=device_id).first()
        if delete_device:
            db.session.delete(delete_device)
            db.session.commit()
            response['status'] = 'success'
        else:
            response['status'] = 'error'
            response['motif'] = 'device non trouvé'

    except Exception as e:
        response['error_description'] = str(e)
        response['status'] = 'error'

    return response