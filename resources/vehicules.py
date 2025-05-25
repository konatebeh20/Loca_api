from flask_restful import Resource
from flask import request
from helpers.vehicules import *


class VehiculeApi(Resource):
    def post(self, route):
        if route == "registervehicule":
            return RegisterVehicles()

        if route == "getsinglevehicles":
            return GetSingleVehicles()
        

    def get(self, route):
        if route == "getallvehicule":
            return GetAllVehicles()
        

    def patch(self, route):
        if route == "updatevehicule":
            return UpdateVehicles()
        
        
    def delete(self, route):
        if route == "deletevehicule":
            return DeleteVehicles()

