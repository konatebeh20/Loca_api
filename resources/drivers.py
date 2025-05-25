from flask_restful import Resource
from flask import request
from helpers.drivers import *


class DriversApi(Resource):
    def post(self, route):
        if route == "registerdrivers":
            return RegisterDrivers()

        if route == "getsingledrivers":
            return GetSingleDrivers()
        

    def get(self, route):
        if route == "getalldrivers":
            return GetAllDrivers()
        

    def patch(self, route):
        if route == "updatedrivers":
            return UpdateDrivers()
        
        
    def delete(self, route):
        if route == "deletedrivers":
            return DeleteDrivers()

