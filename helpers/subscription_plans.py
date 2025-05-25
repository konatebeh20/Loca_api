from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask import request, jsonify
from config.db import db
from config.constant import *
from model.flotys import *

def CreateSubscriptionPlans():
    response = {}
    plans = {}
    all_plans = []
    all_rs = []

    try:
        plans["Monthly"] = {
            'plan_name': 'Monthly',
            'maximum_of_cars': '1',
            'number_of_cars_chosen': '',
            'duration_in_month': '1',
            'price_per_vehicle_one_month': '5000',
            'price_total_before_discount': '5000',
            'discount': '0%',
            'total_cost_for_one_vehicle': '5000'
        }
        plans["Quarterly"] = {
            'plan_name': 'Quarterly',
            'maximum_of_cars': '3',
            'number_of_cars_chosen': '',
            'duration_in_month': '3',
            'price_per_vehicle_one_month': '5000',
            'price_total_before_discount': '15000',
            'discount': '5%',
            'total_cost_for_one_vehicle': '14250',
        }   
        plans["Semi-Annual"] = {
            'plan_name': 'Semi-Annual',
            'maximum_of_cars': '6',
            'number_of_cars_chosen': '',
            'duration_in_month': '6',
            'price_per_vehicle_one_month': '5000',
            'price_total_before_discount': '30000',
            'discount': '10%',
            'total_cost_for_one_vehicle': '27000'
        }
        plans["Annual"] = {
            'plan_name': 'Annual',
            'maximum_of_cars': '12',
            'number_of_cars_chosen': '',
            'duration_in_month': '12',
            'price_per_vehicle_one_month': '5000',
            'price_total_before_discount': '60000',
            'discount': '15%',
            'total_cost_for_one_vehicle': '51000'
        }
        all_plans.append(plans)
        
        for plans in all_plans:
            print('ok1')
            for plan_name in plans.keys():
                print('ok2')
                print("Nom du plan :", plans[plan_name]['plan_name'])

                new_subscription_plans = SubscriptionPlans()
                new_subscription_plans.plan_name = plans[plan_name]['plan_name']
                new_subscription_plans.maximum_of_cars = plans[plan_name]['maximum_of_cars']
                new_subscription_plans.duration_in_month = plans[plan_name]['duration_in_month']
                new_subscription_plans.price_per_vehicle_one_month = plans[plan_name]['price_per_vehicle_one_month']
                new_subscription_plans.price_total_before_discount = int(plans[plan_name]['price_per_vehicle_one_month']) * int(plans[plan_name]['duration_in_month'])
                new_subscription_plans.discount = plans[plan_name]['discount']
                discount_percentage = float(plans[plan_name]['discount'].strip('%')) / 100
                new_subscription_plans.total_cost_for_one_vehicle = (new_subscription_plans.price_total_before_discount * (1 - discount_percentage))

                db.session.add(new_subscription_plans)
                db.session.commit()

                rs = {}
                rs['plan_id'] = new_subscription_plans.plan_id
                rs['plan_name'] = new_subscription_plans.plan_name
                rs['maximum_of_cars'] = new_subscription_plans.maximum_of_cars
                rs['duration_in_month'] = new_subscription_plans.duration_in_month
                rs['price_per_vehicle_one_month'] = new_subscription_plans.price_per_vehicle_one_month
                rs['price_total_before_discount'] = new_subscription_plans.price_total_before_discount
                rs['discount'] = new_subscription_plans.discount
                rs['total_cost_for_one_vehicle'] = new_subscription_plans.total_cost_for_one_vehicle
                all_rs.append(rs)

        response['status'] = 'Success'
        response['subscription_plans_info'] = all_rs

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response


# Ajout des chiffres aléatoires à plan_name



def RegisterSubscriptionPlans():
    response = {}
    
    random_digits = random.randint(10, 99)
    number_of_cars_chosen =  int(request.json.get('number_of_cars_chosen'))
    plan_name =  request.json.get('plan_name')
    new_subscription_plans = SubscriptionPlans()
    new_subscription_plans.plan_name = f"{plan_name}{random_digits}"
    new_subscription_plans.maximum_of_cars = request.json.get('maximum_of_cars')
    # new_subscription_plans.number_of_cars_chosen = number_of_cars_chosen
    new_subscription_plans.duration_in_month = request.json.get('duration_in_month')
    new_subscription_plans.price_per_vehicle_one_month = request.json.get('price_per_vehicle_one_month')
    new_subscription_plans.price_total_before_discount = request.json.get('price_total_before_discount')
    new_subscription_plans.discount = request.json.get('discount')
    total_cost_for_one_vehicle =  request.json.get('total_cost_for_one_vehicle')
    if number_of_cars_chosen and number_of_cars_chosen > 0 :
        new_subscription_plans.total_cost_for_one_vehicle = int(total_cost_for_one_vehicle) * number_of_cars_chosen
    else:
        new_subscription_plans.total_cost_for_one_vehicle = total_cost_for_one_vehicle

    db.session.add(new_subscription_plans)
    db.session.commit()

    rs = {}
    rs['plan_id'] = new_subscription_plans.plan_id
    rs['plan_name'] = new_subscription_plans.plan_name
    rs['maximum_of_cars'] = new_subscription_plans.maximum_of_cars
    # rs['number_of_cars_chosen'] = new_subscription_plans.number_of_cars_chosen
    rs['duration_in_month'] = new_subscription_plans.duration_in_month
    rs['price_per_vehicle_one_month'] = new_subscription_plans.price_per_vehicle_one_month
    rs['price_total_before_discount'] = new_subscription_plans.price_total_before_discount
    rs['discount'] = new_subscription_plans.discount
    rs['total_cost_for_one_vehicle'] = new_subscription_plans.total_cost_for_one_vehicle

    response['status'] = 'Succes'
    response['subscription_plans_info'] = rs

    return response



def GetAllSubscriptionPlans():
    response = {}
    try:
        all_subscription_plans = SubscriptionPlans.query.all()
        subscription_plans_info = []
        for subscription_plans in all_subscription_plans:
            info_subscription_plans = {
                'plan_id': subscription_plans.plan_id,
                'plan_name': subscription_plans.plan_name,
                'maximum_of_cars': subscription_plans.maximum_of_cars,
                # 'number_of_cars_chosen': subscription_plans.number_of_cars_chosen,
                'duration_in_month': subscription_plans.duration_in_month,
                'price_per_vehicle_one_month': subscription_plans.price_per_vehicle_one_month,
                'price_total_before_discount': subscription_plans.price_total_before_discount,
                'discount': subscription_plans.discount,
                'total_cost_for_one_vehicle': subscription_plans.total_cost_for_one_vehicle,
            }
            subscription_plans_info.append(info_subscription_plans)
        response['status'] = 'success'
        response['subscription_plans_info'] = subscription_plans_info

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response



def GetSingleSubscriptionPlans():
    response = {}
    try:
        plan_id = request.json.get('plan_id')
        single_subscription_plans = SubscriptionPlans.query.filter_by(plan_id=plan_id).first()
        if single_subscription_plans:
            info_subscription_plans = {
                'plan_id': single_subscription_plans.plan_id,
                'plan_name': single_subscription_plans.plan_name,
                'maximum_of_cars': single_subscription_plans.maximum_of_cars,
                # 'number_of_cars_chosen': single_subscription_plans.number_of_cars_chosen,
                'duration_in_month': single_subscription_plans.duration_in_month,
                'price_per_vehicle_one_month': single_subscription_plans.price_per_vehicle_one_month,
                'price_total_before_discount': single_subscription_plans.price_total_before_discount,
                'discount': single_subscription_plans.discount,
                'total_cost_for_one_vehicle': single_subscription_plans.total_cost_for_one_vehicle,
            }
            response['status'] = 'success'
            response['subscription_plans'] = info_subscription_plans
        else:
            response['status'] = 'error'
            response['error_description'] = 'Subscription plans not found'

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response



def UpdateSubscriptionPlans():
    response = {}
    plan_id = request.json.get('plan_id')
    subscription_plans_to_update = SubscriptionPlans.query.filter_by(plan_id=plan_id).first()
    if subscription_plans_to_update:
        subscription_plans_to_update.maximum_of_cars = request.json.get('maximum_of_cars', subscription_plans_to_update.maximum_of_cars)
        # subscription_plans_to_update.number_of_cars_chosen = request.json.get('number_of_cars_chosen', subscription_plans_to_update.number_of_cars_chosen)
        subscription_plans_to_update.duration_in_month = request.json.get('duration_in_month', subscription_plans_to_update.duration_in_month)
        subscription_plans_to_update.price_per_vehicle_one_month = request.json.get('price_per_vehicle_one_month', subscription_plans_to_update.price_per_vehicle_one_month)
        subscription_plans_to_update.price_total_before_discount = request.json.get('price_total_before_discount', subscription_plans_to_update.price_total_before_discount)
        subscription_plans_to_update.discount = request.json.get('discount', subscription_plans_to_update.discount)
        subscription_plans_to_update.total_cost_for_one_vehicle = request.json.get('total_cost_for_one_vehicle', subscription_plans_to_update.total_cost_for_one_vehicle)

        db.session.commit()

        rs = {}
        rs['plan_id'] = subscription_plans_to_update.plan_id
        rs['plan_name'] = subscription_plans_to_update.plan_name
        rs['maximum_of_cars'] = subscription_plans_to_update.maximum_of_cars
        # rs['number_of_cars_chosen'] = subscription_plans_to_update.number_of_cars_chosen
        rs['duration_in_month'] = subscription_plans_to_update.duration_in_month
        rs['price_per_vehicle_one_month'] = subscription_plans_to_update.price_per_vehicle_one_month
        rs['price_total_before_discount'] = subscription_plans_to_update.price_total_before_discount
        rs['discount'] = subscription_plans_to_update.discount
        rs['total_cost_for_one_vehicle'] = subscription_plans_to_update.total_cost_for_one_vehicle

        response['status'] = 'Success'
        response['plan_id'] = rs
    else:
        response['status'] = 'error'
        response['error_description'] = 'Subscription plans not found'

    return response



def DeleteSubscriptionPlans():
    response = {}
    try:
        plan_id = request.json.get('plan_id')
        payment_to_delete = SubscriptionPlans.query.filter_by(plan_id=plan_id).first()
        if payment_to_delete:
            db.session.delete(payment_to_delete)
            db.session.commit()
            response['status'] = 'success'
        else:
            response['status'] = 'error'
            response['error_description'] = 'Subscription plans not found'

    except Exception as e:
        response['error_description'] = str(e)
        response['status'] = 'error'

    return response