from flask_restful import Resource
from flask import request
from helpers.trips import *


class TripsApi(Resource):
    def post(self, route):
        if route == "createtrips":
            return CreateTrips()

        if route == "getsingletrips":
            return GetSingleTrips()
        

    def get(self, route):
        if route == "getalltrips":
            return GetAllTrips()
        

    def patch(self, route):
        if route == "updatetrips":
            return UpdateTrips()
        
        
    def delete(self, route):
        if route == "deletetrips":
            return DeleteTrips()

