from flask_restful import Resource
from flask import request
from helpers.assignments import *


class AssignmentsApi(Resource):
    def post(self, route):
        if route == "craeteassignments":
            return CreateAssignments()

        if route == "getsingleassignments":
            return GetSingleAssignments()
        

    def get(self, route):
        if route == "getallassignments":
            return GetAllAssignments()
        

    def patch(self, route):
        if route == "updateassignments":
            return UpdateAssignments()
        
        
    def delete(self, route):
        if route == "deleteassignments":
            return DeleteAssignments()

