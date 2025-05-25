from flask_restful import Resource
from flask import request
from helpers.users import *


class UsersApi(Resource):
    def post(self, route):
        if route == "createuser": 
            return CreateUser()
        
        if route == "test_name": 
            return test_name()

        if route == "getalluserbycompany":
            return GetAllUserByCompany()
        
        if route == "getsingleuser":
            return GetSingleUser()
        
        if route == "loginuser":
            return LoginUsers()

    def get(self, route):
        if route == "getallusercompany":
            return GetAllUserCompany()
        
        if route == "getalladmincompany":
            return GetAllAdminCompany()
        

    def patch(self, route):
        if route == "updateuser":
            return UpdateUser()
        
        if route == "updateidentifier":
            return UpdateIdentifier()
        
    def delete(self, route):
        if route == "deleteuser":
            return DeleteUser() 
