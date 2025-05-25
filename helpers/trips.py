from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta
from flask import request, jsonify
from config.db import db
from model.flotys import *



def CreateTrips():
    response = {}
    
    new_trips = Trips()
    new_trips.assignment_id = request.json.get('assignment_id')
    new_trips.start_location_id = request.json.get('start_location_id')
    new_trips.end_location_id = request.json.get('end_location_id')
    new_trips.distance = request.json.get('distance')
    new_trips.duration = request.json.get('duration')
    new_trips.start_time = request.json.get('start_time')      
    new_trips.end_time = request.json.get('end_time')
    new_trips.status = request.json.get('status')

    db.session.add(new_trips)
    db.session.commit()

    rs = {}
    rs['assignment_id'] = new_trips.assignment_id
    rs['start_location_id'] = new_trips.start_location_id
    rs['end_location_id'] = new_trips.end_location_id
    rs['distance'] = new_trips.distance
    rs['duration'] = new_trips.duration
    rs['start_time'] = new_trips.start_time
    rs['end_time'] = new_trips.end_time
    rs['status'] = new_trips.status
    rs['trips_id'] = new_trips.trips_id

    response['status'] = 'Succes'
    response['trips_infos'] = rs

    return response



def GetAllTrips():
    response = {}
    try:
        all_trips = Trips.query.all()
        trips_info = []
        for trips  in all_trips:
            trips_infos = {
                'assignment_id': trips.assignment_id,  
                'start_location_id': trips.start_location_id,  
                'end_location_id': trips.end_location_id,  
                'distance': trips.distance,  
                'duration': trips.duration,  
                'start_time': trips.start_time,           
                'end_time': trips.end_time,           
                'status': trips.status,           
                'trips_id': trips.trips_id,           
            }
            trips_info.append(trips_infos)
        response['status'] = 'success'
        response ['trips'] = trips_info

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response



def GetSingleTrips():
    response = {}

    try:
        uid = request.json.get('trips_id')
        single_trips = Trips.query.filter_by(trips_id=uid).first()
        trips_infos = {
            'assignment_id': single_trips.assignment_id,
            'start_location_id': single_trips.start_location_id,
            'end_location_id': single_trips.end_location_id,  
            'distance': single_trips.distance,  
            'duration': single_trips.duration,              
            'start_time': single_trips.start_time,              
            'end_time': single_trips.end_time,              
            'status': single_trips.status,              
            'trips_id': single_trips.trips_id,              
        }
        response['status'] = 'success'
        response['trips'] = trips_infos

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response 


def UpdateTrips():

    response = {}
    uid = request.json.get('trips_id')
    update_trips = Trips.query.filter_by(trips_id=uid).first()
    if update_trips:
        update_trips.distance = request.json.get('distance', update_trips.distance)
        update_trips.duration = request.json.get('duration', update_trips.duration)
        update_trips.start_time = request.json.get('start_time', update_trips.start_time)
        update_trips.end_time = request.json.get('end_time', update_trips.end_time)
        update_trips.status = request.json.get('status', update_trips.status)

        db.session.add(update_trips)
        db.session.commit()

        response['status'] = 'Succes'
        response['assignment_id'] = update_trips.assignment_id
        response['start_location_id'] = update_trips.start_location_id
        response['end_location_id'] = update_trips.end_location_id
        response['distance'] = update_trips.distance
        response['duration'] = update_trips.duration
        response['start_time'] = update_trips.start_time
        response['end_time'] = update_trips.end_time
        response['status'] = update_trips.status
        response['trips_id'] = update_trips.trips_id
    else:
        response['status'] = 'trips not found'

    return response



def DeleteTrips():
    
    response = {}
    try:
        uid = request.json.get('trips_id')
        delete_trips = Trips.query.filter_by(trips_id=uid).first()
        if delete_trips:
            db.session.delete(delete_trips)
            db.session.commit()
            response['status'] = 'success'
        else:
            response['status'] = 'error'
            response['motif'] = 'trips non trouvé'

    except Exception as e:
        response['error_description'] = str(e)
        response['status'] = 'error'

    return response