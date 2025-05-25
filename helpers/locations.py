from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta
from flask import request, jsonify
from config.db import db
from model.flotys import *


def CreateLocation():
    response = {}
    
    new_location = Locations()
    new_location.latitude = request.json.get('latitude')
    new_location.longitude = request.json.get('longitude')
    new_location.address = request.json.get('address')
    new_location.city = request.json.get('city')
    new_location.state = request.json.get('state')
    new_location.country = request.json.get('country')
    new_location.postal_code = request.json.get('postal_code')

    db.session.add(new_location)
    db.session.commit()

    rs = {}
    rs['locations_id'] = new_location.locations_id
    rs['latitude'] = new_location.latitude
    rs['longitude'] = new_location.longitude
    rs['address'] = new_location.address
    rs['city'] = new_location.city
    rs['state'] = new_location.state
    rs['country'] = new_location.country
    rs['postal_code'] = new_location.postal_code

    response['status'] = 'Success'
    response['location_info'] = rs

    return response



def GetAllLocations():
    response = {}
    try:
        all_locations = Locations.query.all()
        locations_info = []
        for location in all_locations:
            info_location = {
                'locations_id': location.locations_id,
                'latitude': location.latitude,
                'longitude': location.longitude,
                'address': location.address,
                'city': location.city,
                'state': location.state,
                'country': location.country,
                'postal_code': location.postal_code,
            }
            locations_info.append(info_location)
        response['status'] = 'success'
        response['locations'] = locations_info

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response


def GetSingleLocation():
    response = {}

    try:
        uid = request.json.get('locations_id')
        single_location = Locations.query.filter_by(locations_id=uid).first()
        if single_location:
            info_location = {
                'locations_id': single_location.locations_id,
                'latitude': single_location.latitude,
                'longitude': single_location.longitude,
                'address': single_location.address,
                'city': single_location.city,
                'state': single_location.state,
                'country': single_location.country,
                'postal_code': single_location.postal_code,
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


def UpdateLocation():
    response = {}
    uid = request.json.get('locations_id')
    location_to_update = Locations.query.filter_by(locations_id=uid).first()
    if location_to_update:
        location_to_update.latitude = request.json.get('latitude', location_to_update.latitude)
        location_to_update.longitude = request.json.get('longitude', location_to_update.longitude)
        location_to_update.address = request.json.get('address', location_to_update.address)
        location_to_update.city = request.json.get('city', location_to_update.city)
        location_to_update.state = request.json.get('state', location_to_update.state)
        location_to_update.country = request.json.get('country', location_to_update.country)
        location_to_update.postal_code = request.json.get('postal_code', location_to_update.postal_code)

        db.session.commit()

        rs = {}
        rs['locations_id'] = location_to_update.locations_id
        rs['latitude'] = location_to_update.latitude
        rs['longitude'] = location_to_update.longitude
        rs['address'] = location_to_update.address
        rs['city'] = location_to_update.city
        rs['state'] = location_to_update.state
        rs['country'] = location_to_update.country
        rs['postal_code'] = location_to_update.postal_code

        response['status'] = 'Success'
        response['location_id'] = rs
    else:
        response['status'] = 'error'
        response['error_description'] = 'Location not found'

    return response



def DeleteLocation():
    response = {}
    try:
        uid = request.json.get('locations_id')
        location_to_delete = Locations.query.filter_by(locations_id=uid).first()
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

