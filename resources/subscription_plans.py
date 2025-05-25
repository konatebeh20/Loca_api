from flask_restful import Resource
from flask import request
from helpers.subscription_plans import *


class SubscriptionPlansApi(Resource):
    def post(self, route):
        if route == "createsubscriptionplans": 
            return CreateSubscriptionPlans()
        
        if route == "registersubscriptionplans": 
            return RegisterSubscriptionPlans()
        
        if route == "getsinglesubscriptionplans":
            return GetSingleSubscriptionPlans()
        

    def get(self, route):
        if route == "getallsubscriptionlans":
            return GetAllSubscriptionPlans()
        

    def patch(self, route):
        if route == "updatesubscriptionplans":
            return UpdateSubscriptionPlans()
        
        
    def delete(self, route):
        if route == "deletesubscriptionplans":
            return DeleteSubscriptionPlans() 
