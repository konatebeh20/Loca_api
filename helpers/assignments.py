from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta
from flask import request, jsonify
from config.db import db
from model.flotys import *



def CreateAssignments():
    response = {}
    
    new_assignments = Assignments()
    new_assignments.vehicle_id = request.json.get('vehicle_id')
    new_assignments.driver_id = request.json.get('driver_id')
    new_assignments.assigned_at = request.json.get('assigned_at')
    new_assignments.completed_at = request.json.get('completed_at')
    new_assignments.status = request.json.get('status')
    new_assignments.notes = request.json.get('notes')      
    new_assignments.routes = request.json.get('routes')      

    db.session.add(new_assignments)
    db.session.commit()

    rs = {}
    rs['vehicle_id'] = new_assignments.vehicle_id
    rs['driver_id'] = new_assignments.driver_id
    rs['assigned_at'] = new_assignments.assigned_at
    rs['completed_at'] = new_assignments.completed_at
    rs['status'] = new_assignments.status
    rs['notes'] = new_assignments.notes
    rs['routes'] = new_assignments.routes
    rs['assign_id'] = new_assignments.assign_id

    response['status'] = 'Succes'
    response['assignments_infos'] = rs

    return response



def GetAllAssignments():
    response = {}
    try:
        all_assignments = Assignments.query.all()
        assignments_info = []
        for assignments  in all_assignments:
            assignments_infos = {
                'vehicle_id': assignments.vehicle_id,  
                'driver_id': assignments.driver_id,  
                'assigned_at': assignments.assigned_at,  
                'completed_at': assignments.completed_at,  
                'status': assignments.status,  
                'notes': assignments.notes,           
                'routes': assignments.routes,           
                'assign_id': assignments.assign_id,           
            }
            assignments_info.append(assignments_infos)
        response['status'] = 'success'
        response ['assignments'] = assignments_info

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response



def GetSingleAssignments():
    response = {}

    try:
        uid = request.json.get('assign_id')
        single_assignments = Assignments.query.filter_by(assign_id=uid).first()
        assignments_infos = {
            'vehicle_id': single_assignments.vehicle_id,
            'driver_id': single_assignments.driver_id,
            'assigned_at': single_assignments.assigned_at,  
            'completed_at': single_assignments.completed_at,  
            'status': single_assignments.status,              
            'notes': single_assignments.notes,              
            'routes': single_assignments.routes,              
            'assign_id': single_assignments.assign_id,              
        }
        response['status'] = 'success'
        response['assignments'] = assignments_infos

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response 


def UpdateAssignments():

    response = {}
    uid = request.json.get('assign_id')
    update_assignments = Assignments.query.filter_by(assign_id=uid).first()
    if update_assignments:
        update_assignments.vehicle_id = request.json.get('vehicle_id', update_assignments.vehicle_id)
        update_assignments.driver_id = request.json.get('driver_id', update_assignments.driver_id)
        update_assignments.assigned_at = request.json.get('assigned_at', update_assignments.assigned_at) 
        update_assignments.completed_at = request.json.get('completed_at', update_assignments.completed_at)
        update_assignments.status = request.json.get('status', update_assignments.status)
        update_assignments.notes = request.json.get('notes', update_assignments.notes)
        update_assignments.routes = request.json.get('routes', update_assignments.routes)

        db.session.add(update_assignments)
        db.session.commit()

        response['status'] = 'Succes'
        response['vehicle_id'] = update_assignments.vehicle_id
        response['driver_id'] = update_assignments.driver_id
        response['assigned_at'] = update_assignments.assigned_at
        response['completed_at'] = update_assignments.completed_at
        response['status'] = update_assignments.status
        response['notes'] = update_assignments.notes
        response['routes'] = update_assignments.routes
        response['assign_id'] = update_assignments.assign_id
    else:
        response['status'] = 'Assignments not found'

    return response



def DeleteAssignments():
    
    response = {}
    try:
        uid = request.json.get('assign_id')
        delete_assignments = Assignments.query.filter_by(assign_id=uid).first()
        if delete_assignments:
            db.session.delete(delete_assignments)
            db.session.commit()
            response['status'] = 'success'
        else:
            response['status'] = 'error'
            response['motif'] = 'Assignments non trouvé'

    except Exception as e:
        response['error_description'] = str(e)
        response['status'] = 'error'

    return response