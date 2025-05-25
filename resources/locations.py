from flask_restful import Resource
from flask import request
from helpers.locations import *

class LocationsApi(Resource):
    def post(self, route):
        if route == "createlocation":
            return CreateLocation()

        if route == "getsinglelocation":
            return GetSingleLocation()

    def get(self, route):
        if route == "getalllocations":
            return GetAllLocations()

    def patch(self, route):
        if route == "updatelocation":
            return UpdateLocation()
        
    def delete(self, route):
        if route == "deletelocation":
            return DeleteLocation()
