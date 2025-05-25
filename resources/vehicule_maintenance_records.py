from flask_restful import Resource
from flask import request
from helpers.vehicule_maintenance_records import *


class VehicleMaintenanceRecordsApi(Resource):
    def post(self, route):
        if route == "createmaintenance":
            return CreateMaintenanceRecord()

        if route == "getsinglemaintenancerecords":
            return GetSingleMaintenanceRecord()

    def get(self, route):
        if route == "getallmaintenancerecords":
            return GetAllMaintenanceRecords()

    def patch(self, route):
        if route == "updatemaintenancerecords":
            return UpdateMaintenanceRecord()
        
    def delete(self, route):
        if route == "deletemaintenancerecords":
            return DeleteMaintenanceRecord()
