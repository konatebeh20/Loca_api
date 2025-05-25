from flask_restful import Resource
from flask import request
from helpers.tracking_device import *


class TrackingDeviceApi(Resource):
    def post(self, route):
        if route == "registertrackingdevice":
            return RegisterTrackingDevice()

        if route == "getsingletrackingdevice":
            return GetSingleTrackingDevice()
        

    def get(self, route):
        if route == "getalltrackingdevice":
            return GetAllTrackingDevice()
        

    def patch(self, route):
        if route == "updatetrackingdevice":
            return UpdateTrackingDevice()
        
        
    def delete(self, route):
        if route == "deletetrackingdevice":
            return DeleteTrackingDevice()

