from flask_restful import Resource
from flask import request
from helpers.vehicule_locations import *


class VehicleLocationsApi(Resource):
    def post(self, route):
        if route == "createvehiclelocation":
            return CreateVehicleLocation()

        if route == "getsinglevehiclelocation":
            return GetSingleVehicleLocation()

    def get(self, route):
        if route == "getallvehiclelocations":
            return GetAllVehicleLocations()

    def patch(self, route):
        if route == "updatevehiclelocation":
            return UpdateVehicleLocation()
        
    def delete(self, route):
        if route == "deletevehiclelocation":
            return DeleteVehicleLocation()
