from flask_restful import Resource
from helpers.company import *
from flask import request


class CompanyApi(Resource):
    def post(self, route):
        if route == "create":
            return CreateCompany() 
        
        if route == "getsingle":
            return GetSingleCompany() 
        
        if route == "autoupdatecompany":
            return AutoUpdateCompany() 
        
        
    def get(self, route):
        if route == "getall":
            return GetAllCompany()
        
        if route == "getsingle":
            return GetSingleCompany()

        
    def delete(self, route):
         if route == "delete":
            return DeleteCompany()
         
    def patch(self, route):
        if route == "update":
            return UpdateCompany()

        if route == "subscriptionrenewal":
            return SubscriptionRenewal()