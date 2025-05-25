import logging
from flask import request, jsonify
from config.db import db
from model.flotys import *
from werkzeug.security import check_password_hash


def SaveContactUs():
    response = {}

    new_contact = ContactUs()
    new_contact.fullname = request.json.get('fullname')
    new_contact.email = request.json.get('email')
    new_contact.subject = request.json.get('subject')
    new_contact.message = request.json.get('message')

    db.session.add(new_contact)
    db.session.commit()

    rs = {
        'uid': new_contact.uid,
        'fullname': new_contact.fullname,
        'email': new_contact.email,
        'subject': new_contact.subject,
        'message': new_contact.message
    }

    response['status'] = 'Success'
    response['contact_info'] = rs

    logger.info(f"Contact saved: {new_contact.fullname}")

    return response


def GetAllContactUs():
    response = {}
    try:
        all_contacts = ContactUs.query.all()
        contact_info = []
        for contact in all_contacts:
            info_contact = {
                'uid': contact.uid,
                'fullname': contact.fullname,
                'email': contact.email,
                'subject': contact.subject,
                'message': contact.message
            }
            contact_info.append(info_contact)

        response['status'] = 'success'
        response['contacts'] = contact_info

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response


def GetSingleContactUs():
    response = {}

    try:
        contact_id = request.json.get('uid')
        single_contact = ContactUs.query.filter_by(uid=contact_id).first()
        if single_contact:
            info_contact = {
                'uid': single_contact.uid,
                'fullname': single_contact.fullname,
                'email': single_contact.email,
                'subject': single_contact.subject,
                'message': single_contact.message
            }
            response['status'] = 'success'
            response['contact'] = info_contact
        else:
            response['status'] = 'error'
            response['error_description'] = 'Contact not found'

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response



def DeleteContactUs():
    response = {}
    try:
        contact_id = request.json.get('uid')
        contact_to_delete = ContactUs.query.filter_by(uid=contact_id).first()
        if contact_to_delete:
            db.session.delete(contact_to_delete)
            db.session.commit()
            response['status'] = 'success'
        else:
            response['status'] = 'error'
            response['error_description'] = 'Contact not found'

    except Exception as e:
        response['error_description'] = str(e)
        response['status'] = 'error'

    return response
