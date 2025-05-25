from flask_restful import Resource
from flask import request
from helpers.payment_history import *


class PaymentHistoryApi(Resource):
    def post(self, route):
        if route == "registerpaymenthistory":
            return RegisterPaymentHistory()

    #     if route == "getsingledrivers":
    #         return GetSingleDrivers()
        

    def get(self, route):
        if route == "getallpaymenthistory":
            return GetAllPaymentHistory()
        

    # def patch(self, route):
    #     if route == "updatedrivers":
    #         return UpdateDrivers()
        
        
    # def delete(self, route):
    #     if route == "deletedrivers":
    #         return DeleteDrivers()

