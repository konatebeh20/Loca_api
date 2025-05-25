from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta
from flask import request, jsonify
from config.db import db
from model.flotys import *

from sqlalchemy import func


def CreateReports():
    response = {}
    
    new_reports = Reports()
    new_reports.vehicle_id = request.json.get('vehicle_id')
    new_reports.drivers_id = request.json.get('drivers_id')
    new_reports.kilometers_driven = request.json.get('kilometers_driven')
    new_reports.fuel_liters = request.json.get('fuel_liters')
    new_reports.speeding = request.json.get('speeding')
    new_reports.harsh_braking = request.json.get('harsh_braking')
    new_reports.trip_duration = request.json.get('trip_duration')
    new_reports.trip_ok_on_time = request.json.get('trip_ok_on_time')
    new_reports.incident_count = request.json.get('incident_count')
    new_reports.cause_incident = request.json.get('cause_incident')
    new_reports.total_maintenance_cost = request.json.get('total_maintenance_cost')
    new_reports.average_maintenance_cost = request.json.get('average_maintenance_cost')
    new_reports.number_scheduled = request.json.get('number_scheduled')
    new_reports.downtime = request.json.get('downtime')

    db.session.add(new_reports)
    db.session.commit()

    rs = {}
    rs['vehicle_id'] = new_reports.vehicle_id
    rs['drivers_id'] = new_reports.drivers_id
    rs['kilometers_driven'] = new_reports.kilometers_driven
    rs['fuel_liters'] = new_reports.fuel_liters
    rs['speeding'] = new_reports.speeding
    rs['harsh_braking'] = new_reports.harsh_braking
    rs['trip_duration'] = new_reports.trip_duration
    rs['trip_ok_on_time'] = new_reports.trip_ok_on_time
    rs['incident_count'] = new_reports.incident_count
    rs['cause_incident'] = new_reports.cause_incident
    rs['total_maintenance_cost'] = new_reports.total_maintenance_cost
    rs['average_maintenance_cost'] = new_reports.average_maintenance_cost
    rs['number_scheduled'] = new_reports.number_scheduled
    rs['downtime'] = new_reports.downtime

    response['status'] = 'Succes'
    response['reports_infos'] = rs

    return response



def GetAllReports():
    response = {}
    try:
        all_reports = Reports.query.all()
        reports_info = []
        for reports  in all_reports:
            reports_infos = {
               'vehicle_id': reports.vehicle_id,  
               'drivers_id': reports.drivers_id,  
               'kilometers_driven': reports.kilometers_driven,  
               'fuel_liters': reports.fuel_liters,  
               'speeding': reports.speeding,  
               'harsh_braking': reports.harsh_braking,  
               'trip_duration': reports.trip_duration,  
               'trip_ok_on_time': reports.trip_ok_on_time,  
               'incident_count': reports.incident_count,  
               'cause_incident': reports.cause_incident,  
               'total_maintenance_cost': reports.total_maintenance_cost,  
               'average_maintenance_cost': reports.average_maintenance_cost,  
               'number_scheduled': reports.number_scheduled,  
               'downtime': reports.downtime,  
            }
            reports_info.append(reports_infos)
        response['status'] = 'success'
        response ['reports'] = reports_info

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response



def GetSingleReports():
    response = {}

    try:
        uid = request.json.get('reports_id')
        single_reports = Reports.query.filter_by(reports_id=uid).first()
        reports_infos = {
                'vehicle_id': single_reports.vehicle_id,  
                'drivers_id': single_reports.drivers_id,  
                'kilometers_driven': single_reports.kilometers_driven,  
                'fuel_liters': single_reports.fuel_liters,  
                'speeding': single_reports.speeding,  
                'harsh_braking': single_reports.harsh_braking,  
                'trip_duration': single_reports.trip_duration,  
                'trip_ok_on_time': single_reports.trip_ok_on_time,  
                'incident_count': single_reports.incident_count,  
                'cause_incident': single_reports.cause_incident,  
                'total_maintenance_cost': single_reports.total_maintenance_cost,  
                'average_maintenance_cost': single_reports.average_maintenance_cost,  
                'number_scheduled': single_reports.number_scheduled,  
                'downtime': single_reports.downtime,   
        }
        response['status'] = 'success'
        response['reports'] = reports_infos

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response 


def GetSingleReportsBy():
    response = {}

    try:
        uid = request.json.get('item')
        single_reports = Reports.query.filter_by(reports_id=uid).first()
        reports_infos = {
                'vehicle_id': single_reports.vehicle_id,  
                'drivers_id': single_reports.drivers_id,  
                'kilometers_driven': single_reports.kilometers_driven,  
                'fuel_liters': single_reports.fuel_liters,  
                'speeding': single_reports.speeding,  
                'harsh_braking': single_reports.harsh_braking,  
                'trip_duration': single_reports.trip_duration,  
                'trip_ok_on_time': single_reports.trip_ok_on_time,  
                'incident_count': single_reports.incident_count,  
                'cause_incident': single_reports.cause_incident,  
                'total_maintenance_cost': single_reports.total_maintenance_cost,  
                'average_maintenance_cost': single_reports.average_maintenance_cost,  
                'number_scheduled': single_reports.number_scheduled,  
                'downtime': single_reports.downtime,   
        }
        response['status'] = 'success'
        response['reports'] = reports_infos

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response 


def UpdateReports():

    response = {}
    uid = request.json.get('reports_id')
    update_reports = Reports.query.filter_by(reports_id=uid).first()
    if update_reports:
        update_reports.vehicle_id = request.json.get('vehicle_id', update_reports.vehicle_id)
        update_reports.drivers_id = request.json.get('drivers_id', update_reports.drivers_id)
        update_reports.kilometers_driven = request.json.get('kilometers_driven', update_reports.kilometers_driven)
        update_reports.fuel_liters = request.json.get('fuel_liters', update_reports.fuel_liters)
        update_reports.speeding = request.json.get('speeding', update_reports.speeding)
        update_reports.harsh_braking = request.json.get('harsh_braking', update_reports.harsh_braking)
        update_reports.trip_duration = request.json.get('trip_duration', update_reports.trip_duration)
        update_reports.trip_ok_on_time = request.json.get('trip_ok_on_time', update_reports.trip_ok_on_time)
        update_reports.incident_count = request.json.get('incident_count', update_reports.incident_count)
        update_reports.cause_incident = request.json.get('cause_incident', update_reports.cause_incident)
        update_reports.total_maintenance_cost = request.json.get('total_maintenance_cost', update_reports.total_maintenance_cost)
        update_reports.average_maintenance_cost = request.json.get('average_maintenance_cost', update_reports.average_maintenance_cost)
        update_reports.number_scheduled = request.json.get('number_scheduled', update_reports.number_scheduled)
        update_reports.downtime = request.json.get('downtime', update_reports.downtime)

        db.session.add(update_reports)
        db.session.commit()

        response['status'] = 'Succes'
        response['vehicle_id'] = update_reports.vehicle_id
        response['drivers_id'] = update_reports.drivers_id
        response['kilometers_driven'] = update_reports.kilometers_driven
        response['fuel_liters'] = update_reports.fuel_liters
        response['speeding'] = update_reports.speeding
        response['harsh_braking'] = update_reports.harsh_braking
        response['trip_duration'] = update_reports.trip_duration
        response['trip_ok_on_time'] = update_reports.trip_ok_on_time
        response['incident_count'] = update_reports.incident_count
        response['cause_incident'] = update_reports.cause_incident
        response['total_maintenance_cost'] = update_reports.total_maintenance_cost
        response['average_maintenance_cost'] = update_reports.average_maintenance_cost
        response['number_scheduled'] = update_reports.number_scheduled
        response['downtime'] = update_reports.downtime
    else:
        response['status'] = 'reports not found'

    return response



def DeleteReports():
    
    response = {}
    try:
        uid = request.json.get('reports_id')
        delete_reports = Reports.query.filter_by(reports_id=uid).first()
        if delete_reports:
            db.session.delete(delete_reports)
            db.session.commit()
            response['status'] = 'success'
        else:
            response['status'] = 'error'
            response['motif'] = 'reports non trouvé'

    except Exception as e:
        response['error_description'] = str(e)
        response['status'] = 'error'

    return response



# 1. Vehicle Usage & Efficiency Report
# def get_vehicle_usage_report(session, vehicle_id, date):
def get_vehicle_usage_report():

    # session = request.json.get('session')
    vehicle_id = request.json.get('vehicle_id')
    date = request.json.get('date')

    report = db.session.query(
        Trips.vehicle_id,
        func.sum(Trips.distance).label("total_distance"),
        func.sum(Trips.duration).label("total_duration"),
        func.sum(ExpenseTracking.amount).filter(ExpenseTracking.expense_type == "fuel").label("fuel_cost")
    ).join(ExpenseTracking, ExpenseTracking.vehicle_id == Trips.vehicle_id
    ).filter(Trips.vehicle_id == vehicle_id
    ).group_by(Trips.vehicle_id).first()
    return report

# 2. Driver Performance Report
# def get_driver_performance_report(session, driver_id, date):
def get_driver_performance_report():

    session = request.json.get('session')
    driver_id = request.json.get('driver_id')
    date = request.json.get('date')

    report = session.query(
        DriverBehavior.driver_id,
        func.count(DriverBehavior.event_type).filter(DriverBehavior.event_type == "speeding").label("speeding_events"),
        func.count(DriverBehavior.event_type).filter(DriverBehavior.event_type == "harsh_braking").label("harsh_braking_events"),
        func.count(ComplianceLog.compliance_type).filter(ComplianceLog.status == "failed").label("failed_compliance")
    ).join(ComplianceLog, ComplianceLog.driver_id == DriverBehavior.driver_id
    ).filter(DriverBehavior.driver_id == driver_id
    ).group_by(DriverBehavior.driver_id).first()
    return report

# 3. Route Optimization Report
# def get_route_optimization_report(session, vehicle_id, date):
def get_route_optimization_report():

    session = request.json.get('session')
    vehicle_id = request.json.get('vehicle_id')
    date = request.json.get('date')

    routes = session.query(
        Trips.vehicle_id,
        Trips.start_location_id,
        Trips.end_location_id,
        func.sum(Trips.distance).label("total_distance"),
        func.sum(Trips.duration).label("total_duration"),
        func.count(GeofenceLog.event_type).filter(GeofenceLog.event_type == "Entry").label("geofence_entries")
    ).join(GeofenceLog, GeofenceLog.vehicle_id == Trips.vehicle_id
    ).filter(Trips.vehicle_id == vehicle_id
    ).group_by(Trips.vehicle_id).all()
    return routes

# 4. Maintenance & Health Report
# def get_maintenance_health_report(session, vehicle_id, date):
def get_maintenance_health_report():

    session = request.json.get('session')
    vehicle_id = request.json.get('vehicle_id')
    date = request.json.get('date')

    maintenance = session.query(
        VehicleMaintenanceRecords.vehicle_id,
        func.count(VehicleMaintenanceRecords.id).label("total_maintenance_count"),
        func.sum(VehicleMaintenanceRecords.cost).label("total_maintenance_cost"),
        func.avg(VehicleMaintenanceRecords.cost).label("average_maintenance_cost"),
        func.max(VehicleMaintenanceRecords.maintenance_date).label("last_maintenance_date")
    ).filter(VehicleMaintenanceRecords.vehicle_id == vehicle_id
    ).group_by(VehicleMaintenanceRecords.vehicle_id).first()
    return maintenance

# 5. Financial & Cost Analysis
# def get_financial_cost_analysis(session, vehicle_id, date):
def get_financial_cost_analysis():

    session = request.json.get('session')
    vehicle_id = request.json.get('vehicle_id')
    date = request.json.get('date')

    financials = session.query(
        ExpenseTracking.vehicle_id,
        func.sum(ExpenseTracking.amount).filter(ExpenseTracking.expense_type == "fuel").label("fuel_cost"),
        func.sum(ExpenseTracking.amount).filter(ExpenseTracking.expense_type == "maintenance").label("maintenance_cost"),
        func.sum(ExpenseTracking.amount).label("total_cost")
    ).filter(ExpenseTracking.vehicle_id == vehicle_id
    ).group_by(ExpenseTracking.vehicle_id).first()
    return financials

# 6. Compliance & Safety Report
# def get_compliance_safety_report(session, vehicle_id, date):
def get_compliance_safety_report():

    session = request.json.get('session')
    vehicle_id = request.json.get('vehicle_id')
    date = request.json.get('date')

    compliance = session.query(
        ComplianceLog.vehicle_id,
        func.count(ComplianceLog.id).label("total_compliance_checks"),
        func.count(ComplianceLog.status).filter(ComplianceLog.status == "failed").label("failed_compliance_checks"),
        func.count(DriverBehavior.event_type).filter(DriverBehavior.event_type == "incident").label("incidents")
    ).join(DriverBehavior, DriverBehavior.vehicle_id == ComplianceLog.vehicle_id
    ).filter(ComplianceLog.vehicle_id == vehicle_id
    ).group_by(ComplianceLog.vehicle_id).first()
    return compliance

# 7. Geofencing & Security Report
# def get_geofencing_security_report(session, vehicle_id, date):
def get_geofencing_security_report():

    session = request.json.get('session')
    vehicle_id = request.json.get('vehicle_id')
    date = request.json.get('date')

    geofence_report = session.query(
        GeofenceLog.vehicle_id,
        func.count(GeofenceLog.event_type).filter(GeofenceLog.event_type == "Entry").label("geofence_entries"),
        func.count(GeofenceLog.event_type).filter(GeofenceLog.event_type == "Exit").label("geofence_exits")
    ).filter(GeofenceLog.vehicle_id == vehicle_id
    ).group_by(GeofenceLog.vehicle_id).first()
    return geofence_report

# 8. Environmental Impact Report
# def get_environmental_impact_report(session, vehicle_id, date):
def get_environmental_impact_report():

    session = request.json.get('session')
    vehicle_id = request.json.get('vehicle_id')
    date = request.json.get('date')

    emissions = session.query(
        EmissionData.vehicle_id,
        func.sum(EmissionData.co2_emissions).label("total_co2_emissions"),
        func.sum(EmissionData.fuel_consumed).label("total_fuel_consumed")
    ).filter(EmissionData.vehicle_id == vehicle_id
    ).group_by(EmissionData.vehicle_id).first()
    return emissions

# 9. Real-Time & Historical Tracking Report
# def get_historical_tracking_report(session, vehicle_id, start_date, end_date):
def get_historical_tracking_report():

    session = request.json.get('session')
    vehicle_id = request.json.get('vehicle_id')
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')

    tracking_history = session.query(
        VehicleTrackingHistory.vehicle_id,
        VehicleTrackingHistory.latitude,
        VehicleTrackingHistory.longitude,
        VehicleTrackingHistory.timestamp
    ).filter(
        VehicleTrackingHistory.vehicle_id == vehicle_id,
        VehicleTrackingHistory.timestamp.between(start_date, end_date)
    ).order_by(VehicleTrackingHistory.timestamp).all()
    return tracking_history

# 10. Customizable & Forecasting Report
def get_forecasting_report():

    session = request.json.get('session')
    vehicle_id = request.json.get('vehicle_id')
    date = request.json.get('date')

    forecast = session.query(
        ForecastData.vehicle_id,
        ForecastData.metric_name,
        ForecastData.metric_value,
        ForecastData.forecast_date
    ).filter(ForecastData.vehicle_id == vehicle_id
    ).order_by(ForecastData.forecast_date).all()
    return forecast