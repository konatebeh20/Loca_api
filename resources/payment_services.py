from flask_restful import Resource
from helpers.Payment_Services import *
from flask import request


class PaymentServicesApi(Resource):
    def post(self, route):
        if route == 'create_payment':
            return CreatePaymentPlan() 
        
        if route == 'read_single_payment':
            return ReadSinglePaymentPlan()
        
        if route == 'update_payment_status':
            return UpdatePaymentStatus()
        
        
        
    def get(self, route):
        if route == 'read_all_payment':
            return ReadAllPaymentPlan()