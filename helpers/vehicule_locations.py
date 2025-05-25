from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta
from flask import request, jsonify
from config.db import db
from model.flotys import *


def CreateVehicleLocation():
    response = {}
    
    new_location = VehicleLocations()
    new_location.vehicle_id = request.json.get('vehicle_id')
    new_location.latitude = request.json.get('latitude')
    new_location.longitude = request.json.get('longitude')
    new_location.timestamp = request.json.get('timestamp')
    new_location.speed = request.json.get('speed')

    db.session.add(new_location)
    db.session.commit()

    rs = {}
    rs['vehicle_id'] = new_location.vehicle_id
    rs['latitude'] = new_location.latitude
    rs['longitude'] = new_location.longitude
    rs['timestamp'] = new_location.timestamp
    rs['speed'] = new_location.speed
    rs['uid'] = new_location.uid

    response['status'] = 'Success'
    response['uid'] = rs

    return response


def GetAllVehicleLocations():
    response = {}
    try:
        all_locations = VehicleTrackingHistory.query.all()
        locations_info = []
        for location in all_locations:
            info_location = {
                'uid': location.uid,
                'vehicle_id': location.vehicle_id,
                'latitude': location.latitude,
                'longitude': location.longitude,
                'timestamp': location.timestamp,
                'speed': location.speed,
                'created_at': str(location.created_at),
            }
            locations_info.append(info_location)
        response['status'] = 'success'
        response['locations'] = locations_info

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response


def GetSingleVehicleLocation():
    response = {}

    try:
        uid = request.json.get('uid')
        single_location = VehicleTrackingHistory.query.filter_by(uid=uid).last()
        if single_location:
            info_location = {
                'uid': single_location.uid,
                'vehicle_id': single_location.vehicle_id,
                'latitude': single_location.latitude,
                'longitude': single_location.longitude,
                'timestamp': single_location.timestamp,
                'speed': single_location.speed,
                'created_at': str(single_location.created_at),
            }
            response['status'] = 'success'
            response['location'] = info_location
        else:
            response['status'] = 'error'
            response['error_description'] = 'Location not found'

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response


def UpdateVehicleLocation():
    response = {}
    uid = request.json.get('uid')
    location_to_update = VehicleTrackingHistory.query.filter_by(uid=uid).first()
    if location_to_update:
        location_to_update.latitude = request.json.get('latitude', location_to_update.latitude)
        location_to_update.longitude = request.json.get('longitude', location_to_update.longitude)
        location_to_update.timestamp = request.json.get('timestamp', location_to_update.timestamp)
        location_to_update.speed = request.json.get('speed', location_to_update.speed)

        db.session.commit()

        rs = {}
        rs['vehicle_id'] = location_to_update.vehicle_id
        rs['latitude'] = location_to_update.latitude
        rs['longitude'] = location_to_update.longitude
        rs['timestamp'] = location_to_update.timestamp
        rs['speed'] = location_to_update.speed
        rs['uid'] = location_to_update.uid

        response['status'] = 'Success'
        response['uid'] = rs
    else:
        response['status'] = 'error'
        response['error_description'] = 'Location not found'

    return response


def DeleteVehicleLocation():
    response = {}
    try:
        uid = request.json.get('uid')
        location_to_delete = VehicleTrackingHistory.query.filter_by(uid=uid).first()
        if location_to_delete:
            db.session.delete(location_to_delete)
            db.session.commit()
            response['status'] = 'success'
        else:
            response['status'] = 'error'
            response['error_description'] = 'Location not found'

    except Exception as e:
        response['error_description'] = str(e)
        response['status'] = 'error'

    return response
