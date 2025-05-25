from flask_restful import Resource
from flask import request
from helpers.payment import *


class PaymentApi(Resource):
    def post(self, route):
        if route == "createpayment": 
            return CreatePayment()
    
        if route == "confirmpayment": 
            return ConfirmPayment()
        
        if route == "getsinglepayment":
            return GetSinglePayment()
        

    def get(self, route):
        if route == "getallpayment":
            return GetAllPayment()
        
        
    def delete(self, route):
        if route == "deletepayment":
            return DeletePayment() 
