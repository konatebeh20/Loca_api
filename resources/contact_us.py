from flask_restful import Resource
from flask import request
from helpers.contact_us import *


class ContactUsApi(Resource):
    def post(self, route):
        if route == "save_contact_us": 
            return SaveContactUs()

        if route == "get_single_contact_us":
            return GetSingleContactUs()


    def get(self, route):
        if route == "get_all_contact_us":
            return GetAllContactUs()


    def delete(self, route):
        if route == "delete_contact_us":
            return DeleteContactUs()
