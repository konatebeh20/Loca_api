import datetime
from unicodedata import numeric
import uuid
from sqlalchemy import JSON, Column, func
from config.db import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import expression

    # currencies = db.Column(db.JSON, nullable=True)
    # partner_ref = db.Column(db.String(128), nullable=False, default='RM55286585')
    # admin_id = db.Column(db.String(128), db.ForeignKey('admin.admin_id'))
    # description = db.Column(db.Text())

class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vehicle_id = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    drivers_id = db.Column(db.String(128), db.ForeignKey('drivers.drivers_id'))
    company_id = db.Column(db.String(128), db.ForeignKey('company.company_id'))
    license_plate = db.Column(db.String(128), unique=True)
    model = db.Column(db.String(128))
    number_wheel = db.Column(db.Integer)
    ref_wheel = db.Column(db.String(128))
    manufacturer = db.Column(db.String(128))
    year = db.Column(db.Integer, nullable=False)  
    vin = db.Column(db.String(128))
    device_type = db.Column(db.String(128))
    device_id = db.Column(db.String(128), unique=True)  # Assurez-vous que l'index existe
    status = db.Column(db.String(128))
    user_id = db.Column(db.String(128), db.ForeignKey('users.user_id'))
    current_location_id = db.Column(db.String(128))
    color = db.Column(db.String(50), nullable=True)  # Vehicle color
    make = db.Column(db.String(100))  # Vehicle brand
    body_type = db.Column(db.String(50), nullable=True)  # Body type (e.g., SUV, Sedan)
    purchase_price = db.Column(db.Float, nullable=True)  # Purchase price
    current_value = db.Column(db.Float, nullable=True)  # Depreciated or current value
    engine_type = db.Column(db.String(50), nullable=True)  # Engine type (e.g., V6, Electric)
    fuel_type = db.Column(db.String(50), nullable=True)  # Fuel type (Petrol, Diesel, Electric)
    transmission_type = db.Column(db.String(50), nullable=True)  # Transmission type (Manual, Automatic)
    seating_capacity = db.Column(db.Integer, nullable=True)  # Number of seats
    odometer_reading = db.Column(db.Float, nullable=False, default=0.0)  # Mileage
    purchase_date = db.Column(db.Date, nullable=True)  # Purchase date
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)



class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))
    device_protocol = db.Column(db.String(128))
    device_label = db.Column(db.String(128), unique=True)
    last_logitude = db.Column(db.String(128), default='5.358742')
    last_lagitude = db.Column(db.String(128), default='-3.925245')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


class Drivers(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    drivers_id = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))
    company_id = db.Column(db.String(128), db.ForeignKey('company.company_id'))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(128), nullable=False, unique=True)
    phone = db.Column(db.String(128), nullable=False, unique=True)
    license_number = db.Column(db.String(128))
    license_expiry_date = db.Column(db.String(128))
    status = db.Column(db.String(128))
    user_id = db.Column(db.String(128), db.ForeignKey('users.user_id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


class Reports(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reports_id = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))
    vehicle_id = db.Column(db.String(128))
    drivers_id = db.Column(db.String(128))
    kilometers_driven = db.Column(db.String(128))
    fuel_liters = db.Column(db.String(128))
    speeding = db.Column(db.String(128))
    harsh_braking = db.Column(db.String(128)) # True  or False
    trip_duration = db.Column(db.String(128))
    trip_ok_on_time  = db.Column(db.String(128))
    incident_count = db.Column(db.String(128))
    cause_incident = db.Column(db.String(128))
    total_maintenance_cost = db.Column(db.String(128))
    average_maintenance_cost = db.Column(db.String(128))
    number_scheduled = db.Column(db.String(128))
    downtime = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


class Assignments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assign_id = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))
    vehicle_id = db.Column(db.String(128), db.ForeignKey('vehicles.vehicle_id'))
    driver_id = db.Column(db.String(128), db.ForeignKey('drivers.drivers_id'))
    assigned_at = db.Column(db.String(128))
    completed_at = db.Column(db.String(128))
    status = db.Column(db.String(128))
    notes = db.Column(db.String(128))
    routes = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


class Trips(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trips_id = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))
    vehicle_id = db.Column(db.String(128), db.ForeignKey('vehicles.vehicle_id'))
    assignment_id = db.Column(db.String(128), db.ForeignKey('assignments.assign_id'))
    start_location_id = db.Column(db.String(128))
    end_location_id = db.Column(db.String(128))
    distance = db.Column(db.Float, nullable=False)  # Pour la distance en kilomètres
    duration = db.Column(db.String(128))
    start_time = db.Column(db.String(128))
    end_time = db.Column(db.String(128))
    status = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


class Locations(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    locations_id = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))
    latitude = db.Column(db.String(128))
    longitude = db.Column(db.String(128))
    address = db.Column(db.String(128))
    city = db.Column(db.String(128))
    state = db.Column(db.String(128))
    country = db.Column(db.String(128))
    postal_code = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


class VehicleMaintenanceRecords(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))
    vehicle_id = db.Column(db.String(128), db.ForeignKey('vehicles.vehicle_id'))
    maintenance_date = db.Column(db.String(128))
    description = db.Column(db.String(128))
    cost = db.Column(db.String(128))
    status = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))
    fullname = db.Column(db.String(128))
    username = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128), nullable=False, unique=True)
    role = db.Column(db.String(128))
    company_id = db.Column(db.String(128))
    status = db.Column(db.String(128))
    device_token = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128), nullable=False, unique=True)
    role = db.Column(db.String(128))
    status = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


class ContactUs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))
    fullname = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(128))
    subject = db.Column(db.String(128), nullable=False, unique=True)
    message = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


class VehicleLocations(db.Model): 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))
    vehicle_id = db.Column(db.String(128))
    latitude = db.Column(db.String(128))
    longitude = db.Column(db.String(128))
    timestamp = db.Column(db.String(128))
    speed = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


class TrackingDevice(db.Model): 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tracking_device_id = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))
    reference = db.Column(db.String(128), nullable=False)
    vehicle_id = db.Column(db.String(128), db.ForeignKey('vehicles.vehicle_id'))
    user_id = db.Column(db.String(128), db.ForeignKey('users.user_id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


class TireChanges(db.Model): 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vehicle_id = db.Column(db.String(128), db.ForeignKey('vehicles.vehicle_id'))
    tire_change_date = db.Column(db.String(128))
    tire_position = db.Column(db.String(128))
    tire_brand = db.Column(db.String(128))
    tire_size = db.Column(db.String(128))
    mileage_at_change = db.Column(db.Integer)
    cost = db.Column(db.String(128))
    next_expected_change = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)



class SubscriptionPlans(db.Model):
    __tablename__ = 'subscriptionplans'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plan_id = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    plan_name = db.Column(db.String(128), nullable=False, unique=True)  # e.g., Basic, Premium, Pro
    maximum_of_cars = db.Column(db.String(128))  # Description of the plan
    duration_in_month = db.Column(db.String(128), nullable=False)  # Price per billing cycle
    price_per_vehicle_one_month = db.Column(db.String(128), nullable=False)  # Price per billing cycle
    price_total_before_discount = db.Column(db.String(128), nullable=False)  # Price per billing cycle
    discount = db.Column(db.String(50), nullable=False)  # Monthly, yearly, etc.
    total_cost_for_one_vehicle = db.Column(db.String(128), nullable=True)  # JSON for storing features associated with the plan
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    agency_title = db.Column(db.String(128), nullable=False)
    company_ref = db.Column(db.String(128))
    country = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    number = db.Column(db.String(128), nullable=False, unique=True)
    status =  db.Column(db.String(128), nullable=False)
    created_by = db.Column(db.String(128), db.ForeignKey('admin.admin_id'))
    current_plan_id = db.Column(db.String(128), db.ForeignKey('subscriptionplans.plan_id'), nullable=True)
    subscription_start_date = db.Column(db.DateTime, nullable=True)
    subscription_end_date = db.Column(db.DateTime, nullable=True)
    subscription_status = db.Column(db.String(50), nullable=True)  # e.g., active, expired, pending renewal
    payment_status = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    payment_id = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    payment_ref = db.Column(db.String(128), nullable=False)
    payment_id_patner = db.Column(db.String(128), nullable=False)
    payment_token = db.Column(db.Text, nullable=False)
    payment_intent_log = db.Column(db.Text, nullable=False)
    payment_methode = db.Column(db.String(128), nullable=False)
    plan_id = db.Column(db.String(128), db.ForeignKey('subscriptionplans.plan_id'), nullable=False)  # Link to the subscription plan
    amount = db.Column(db.Float, nullable=False)  # Amount paid
    # transaction_reference = db.Column(db.String(128), nullable=True)  # Reference ID from the payment processor
    payment_date = db.Column(db.String(128))
    payment_end = db.Column(db.String(128))
    network = db.Column(db.String(128), nullable=False)
    number = db.Column(db.String(128), nullable=False)
    name_of_card = db.Column(db.String(128))
    card_number = db.Column(db.String(128))
    card_type = db.Column(db.String(128))
    card_expiration_date = db.Column(db.String(128))
    card_cvv = db.Column(db.String(128))
    payment_status = db.Column(db.String(128))
    user_id = db.Column(db.String(128), nullable=False)
    company_ref = db.Column(db.String(128), nullable=False)
    number_of_cars_chosen = db.Column(db.String(128))
    status = db.Column(db.String(128))
    payment_confirmation_id = db.Column(db.String(128))
    payment_confirmation_log = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


class PaymentHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    payment_id = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(128), db.ForeignKey('users.user_id'), nullable=False)  # Link to the user making the payment
    plan_id = db.Column(db.String(128), db.ForeignKey('subscriptionplans.plan_id'), nullable=False)  # Link to the subscription plan
    amount = db.Column(db.Float, nullable=False)  # Amount paid
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)  # Date of the transaction
    payment_method = db.Column(db.String(50), nullable=True)  # e.g., credit card, PayPal
    status = db.Column(db.String(50), nullable=False)  # e.g., successful, failed, pending
    payment_ref = db.Column(db.String(128), nullable=True)  # Reference ID from the payment processor
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


class DriverAssignmentHistory(db.Model):    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    driver_id = db.Column(db.String(128), db.ForeignKey('drivers.drivers_id'), nullable=False)
    vehicle_id = db.Column(db.String(128), db.ForeignKey('vehicles.vehicle_id'), nullable=False)
    assigned_at = db.Column(db.DateTime, nullable=False)
    unassigned_at = db.Column(db.DateTime, nullable=True)  # If the driver is unassigned from this vehicle
    status = db.Column(db.String(128), nullable=False)  # e.g., 'active', 'completed', etc.
    notes = db.Column(db.Text, nullable=True)

    # Relationships
    driver = db.relationship('Drivers', backref='assignment_history', lazy=True)
    vehicle = db.relationship('Vehicles', backref='driver_assignments', lazy=True)
        
        
class VehicleTrackingHistory(db.Model):    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vehicle_id = db.Column(db.String(128), nullable=False)
    latitude = db.Column(db.String(128), nullable=False)
    longitude = db.Column(db.String(128), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    speed = db.Column(db.Float, nullable=True)
    recorded_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    
    # Relationships
    # vehicle = db.relationship('Vehicles', backref='tracking_history', lazy=True)
    
class Geofence(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    geofence_id = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)  # Geofence name
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    radius = db.Column(db.Float)  # Radius in meters
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

class GeofenceLog(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    log_id = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    vehicle_id = db.Column(db.String(128), db.ForeignKey('vehicles.vehicle_id'))
    geofence = db.Column(db.String(128), db.ForeignKey('geofence.geofence_id'))
    event_type = db.Column(db.String(50), nullable=False)  # Entry or Exit
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

class DriverBehavior(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    behavior_id = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    driver_id = db.Column(db.String(128), db.ForeignKey('drivers.drivers_id'))
    vehicle_id = db.Column(db.String(128), db.ForeignKey('vehicles.vehicle_id'))
    event_type = db.Column(db.String(128), nullable=False)  # e.g., "speeding", "harsh_braking"
    event_value = db.Column(db.Float, nullable=True)  # e.g., speed at the time of speeding
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

class ComplianceLog(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    compliance_id = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    vehicle_id = db.Column(db.String(128), db.ForeignKey('vehicles.vehicle_id'))
    compliance_type = db.Column(db.String(128), nullable=False)  # e.g., "inspection", "regulation_check"
    status = db.Column(db.String(128), nullable=False)  # e.g., "passed", "failed"
    description = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

class MaintenanceSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    schedule_id = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    vehicle_id = db.Column(db.String(128), db.ForeignKey('vehicles.vehicle_id'))
    task_name = db.Column(db.String(128), nullable=False)  # e.g., "Oil Change", "Tire Rotation"
    interval_km = db.Column(db.Integer, nullable=True)  # Interval in kilometers
    interval_days = db.Column(db.Integer, nullable=True)  # Interval in days
    last_performed_date = db.Column(db.DateTime, nullable=True)
    next_due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

class EmissionData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emission_id = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    vehicle_id = db.Column(db.String(128), db.ForeignKey('vehicles.vehicle_id'))
    trip_id = db.Column(db.String(128), db.ForeignKey('trips.trips_id'))
    co2_emissions = db.Column(db.Float, nullable=False)  # CO2 emissions in grams
    fuel_consumed = db.Column(db.Float, nullable=False)  # Liters or gallons of fuel
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

class ForecastData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    forecast_id = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    vehicle_id = db.Column(db.String(128), db.ForeignKey('vehicles.vehicle_id'))
    metric_name = db.Column(db.String(128), nullable=False)  # e.g., "maintenance_cost", "fuel_usage"
    metric_value = db.Column(db.Float, nullable=False)
    forecast_date = db.Column(db.Date, nullable=False)  # Date the forecast applies to
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

class ExpenseTracking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    expense_id = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    vehicle_id = db.Column(db.String(128), db.ForeignKey('vehicles.vehicle_id'))
    expense_type = db.Column(db.String(128), nullable=False)  # e.g., "fuel", "maintenance"
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=False, default=datetime.datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


class DeviceTokens(db.Model):
    __tablename__ = 'device_tokens'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(128), db.ForeignKey('users.user_id'), nullable=False)
    device_token = db.Column(db.String(255), unique=True, nullable=False)  # The APNs/FCM token
    device_type = db.Column(db.String(50), nullable=False)  # e.g., "ios" or "android"
    is_active = db.Column(db.Boolean, default=True)  # Whether the token is active
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)  # When the token was created
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)  # When it was last updated

class Payment_Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.String(128))
    firstname = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=False)
    mobile = db.Column(db.String(128))
    country = db.Column(db.String(128))
    city = db.Column(db.String(128))
    projet = db.Column(db.String(128))
    plan_title = db.Column(db.String(128))
    amount = db.Column(db.String(128))
    description = db.Column(JSON)
    order_status = db.Column(db.String(128))
    order_payment_status = db.Column(db.String(128))
    order_payment_confirmation_id = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)