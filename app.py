# import eventlet
# eventlet.monkey_patch()

from urllib import request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask import Flask, render_template
import os
from flask_restful import Resource, Api
from config.db import db
from config.constant import *
from model.flotys import *
from helpers.gps_data import *
from resources.vehicules import VehiculeApi
from resources.drivers import DriversApi
from resources.assignments import AssignmentsApi
from resources.trips import TripsApi
from resources.company import CompanyApi
from resources.locations import LocationsApi
from resources.vehicule_maintenance_records import VehicleMaintenanceRecordsApi
from resources.users import UsersApi
from resources.admin import AdminApi
from resources.vehicule_locations import VehicleLocationsApi
from resources.tracking_device import TrackingDeviceApi
from resources.device import DeviceApi
from resources.reports import ReportsApi
from resources.payment import PaymentApi
from resources.subscription_plans import SubscriptionPlansApi 
from resources.payment_history import PaymentHistoryApi
from resources.contact_us import ContactUsApi
from resources.payment_services import PaymentServicesApi
from flask_migrate import Migrate
from flask_cors import CORS
import socket
import threading
import logging
from logging.handlers import RotatingFileHandler

import pika
import time
from flask_socketio import SocketIO



import redis


# Initialize Flask app and configurations
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Redis client setup
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
REDIS_CHANNEL = 'gps_updates'

# Info Logger
info_handler = RotatingFileHandler('logs/info.log', maxBytes=100000, backupCount=3)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Error Logger
error_handler = RotatingFileHandler('logs/error.log', maxBytes=100000, backupCount=3)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Adding handlers to the Flask logger
socketio_logger = logging.getLogger('socketio')
app.logger.addHandler(info_handler)
app.logger.addHandler(error_handler)


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# JWT configuration
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

# Database configuration
app.secret_key = os.urandom(24)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = SQL_DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)



@app.route('/a')    
def home():
    logger.info('FlotysHub')
    return render_template('index.html')

# API routes
api.add_resource(VehiculeApi, '/api/vehicule/<string:route>', endpoint='all_vehicule', methods=['GET', 'POST', 'DELETE', 'PATCH'])
api.add_resource(DriversApi, '/api/drivers/<string:route>', endpoint='all_drivers', methods=['GET', 'POST', 'DELETE', 'PATCH'])
api.add_resource(AssignmentsApi, '/api/assignments/<string:route>', endpoint='all_assignments', methods=['GET', 'POST', 'DELETE', 'PATCH'])
api.add_resource(TripsApi, '/api/trips/<string:route>', endpoint='all_trips', methods=['GET', 'POST', 'DELETE', 'PATCH'])
api.add_resource(LocationsApi, '/api/locations/<string:route>', endpoint='all_locations', methods=['GET', 'POST', 'DELETE', 'PATCH'])
api.add_resource(VehicleMaintenanceRecordsApi, '/api/vehiclemaintenancerecords/<string:route>', endpoint='all_vehiclemaintenancerecords', methods=['GET', 'POST', 'DELETE', 'PATCH'])
api.add_resource(UsersApi, '/api/users/<string:route>', endpoint='all_users', methods=['GET', 'POST', 'DELETE', 'PATCH'])
api.add_resource(AdminApi, '/api/admin/<string:route>', endpoint='all_admin', methods=['GET', 'POST', 'DELETE', 'PATCH'])
api.add_resource(VehicleLocationsApi, '/api/vehiclelocations/<string:route>', endpoint='all_vehiclelocations', methods=['GET', 'POST', 'DELETE', 'PATCH'])
api.add_resource(TrackingDeviceApi, '/api/trackingdevice/<string:route>', endpoint='all_trackingdevice', methods=['GET', 'POST', 'DELETE', 'PATCH'])
api.add_resource(CompanyApi, '/api/company/<string:route>', endpoint='all_company', methods=['GET', 'POST', 'DELETE', 'PATCH'])
api.add_resource(DeviceApi, '/api/device/<string:route>', endpoint='all_device', methods=['GET', 'POST', 'DELETE', 'PATCH'])
api.add_resource(ReportsApi, '/api/reports/<string:route>', endpoint='all_reports', methods=['GET', 'POST', 'DELETE', 'PATCH'])
api.add_resource(SubscriptionPlansApi, '/api/subscription_plans/<string:route>', endpoint='all_subscription_plans', methods=['GET', 'POST', 'DELETE', 'PATCH']) 
api.add_resource(PaymentHistoryApi, '/api/payment_history/<string:route>', endpoint='all_payment_history', methods=['GET', 'POST'])
api.add_resource(ContactUsApi, '/api/contact_us/<string:route>', endpoint='all_contact_us', methods=['GET', 'POST'])
api.add_resource(PaymentServicesApi, '/api/payment_services/<string:route>', endpoint='all_payment', methods=['GET', 'POST', 'DELETE', 'PATCH'])


if __name__ == '__main__':
    # Start the Flask app
    # socketio.run(app, debug=True, host="0.0.0.0", port=5000)  # Use socketio.run for real-time capabilities
    # socketio.run(app, host='0.0.0.0', port=5000, debug=True)

    # Run Flask app
    app.run(debug=True, host="0.0.0.0", port=5000)  # Specify your main Flask app port
