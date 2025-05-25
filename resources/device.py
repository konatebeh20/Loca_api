from flask_restful import Resource
from flask import request
from helpers.device import *


class DeviceApi(Resource):
    def post(self, route):
        if route == "createdevice":
            return CreateDevice()

        if route == "getsingledevice":
            return GetSingleDevice()
        

    def get(self, route):
        if route == "getalldevice":
            return GetAllDevice()
        

    def patch(self, route):
        if route == "updatedevice":
            return UpdateDevice()
        
        
    def delete(self, route):
        if route == "deletedevice":
            return DeleteDevice()

