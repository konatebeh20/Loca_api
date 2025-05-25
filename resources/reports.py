from flask_restful import Resource
from flask import request
from helpers.reports import *


class ReportsApi(Resource):
    def post(self, route):
        if route == "createreports":
            return CreateReports()

        if route == "getsinglereports":
            return GetSingleReports()
        

    def get(self, route):
        if route == "getallreports":
            return GetAllReports()
        
        if route == "get_vehicle_usage_report":
            return get_vehicle_usage_report()
        
        if route == "get_driver_performance_report":
            return get_driver_performance_report()
        
        if route == "get_route_optimization_report":
            return get_route_optimization_report()
        
        if route == "get_maintenance_health_report":
            return get_maintenance_health_report()
        
        if route == "get_financial_cost_analysis":
            return get_financial_cost_analysis()
        
        if route == "get_compliance_safety_report":
            return get_compliance_safety_report()
        
        if route == "get_geofencing_security_report":
            return get_geofencing_security_report()
        
        if route == "get_environmental_impact_report":
            return get_environmental_impact_report()

        if route == "get_historical_tracking_report":
            return get_historical_tracking_report()

        if route == "get_forecasting_report":
            return get_forecasting_report()
        

    def patch(self, route):
        if route == "updatereports":
            return UpdateReports()
        
        
    def delete(self, route):
        if route == "deletereports":
            return DeleteReports()

