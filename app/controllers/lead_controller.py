
from flask import request, current_app, jsonify
from app.exceptions.exceptions import InvalidInput, InvalidKey, InvalidPhonePattern
from app.models.lead_model import LeadModel
from sqlalchemy import exc, desc
from datetime import datetime
import pytz

from app.services.handler_leads_service import check_phone_pattern, sanitize, verify


def create_lead():
    data = request.get_json()

    try:
        verify(data)
        check_phone_pattern(data)
        clean_data = sanitize(data)

        new_lead = LeadModel(**clean_data)
        current_app.db.session.add(new_lead)
        current_app.db.session.commit()

        return jsonify(new_lead), 201

    except InvalidInput as error:
        return(*error.args, 400)

    except InvalidKey as error:
        return(*error.args, 400)

    except exc.IntegrityError:
        return {'error': 'Lead already exists on database.'}, 409

    except InvalidPhonePattern as error:
        return(*error.args, 400)


def get_all_by_visist_order():
    leads_list = current_app.db.session.query(LeadModel).order_by(desc(LeadModel.visits))

    serializer = [
        {
            "id": lead.id,
            "name": lead.name,
            "email": lead.email,
            "phone": lead.phone,
            "creation_date": lead.creation_date,
            "last_visit": lead.last_visit,
            "visits": lead.visits
        } for lead in leads_list
    ]

    if not serializer:
        return {'data': []}, 200

    return jsonify(serializer), 200


def update_lead():
    data = request.get_json()
    email = data['email']

    try:
        lead = current_app.db.session.query(LeadModel).filter_by(email=email)
        today = datetime.now(pytz.timezone('GMT'))

        serializer = [
                {
                    "visits": leads.visits
                } for leads in lead
            ]

        data = {
            "last_visit": today,
            "visits": serializer[0]['visits']+1
            }

        lead.update(data)
        current_app.db.session.commit()

        return '', 204

    except IndexError:
        return {'error': 'Lead not found, please check the email address'}, 404


def delete_lead():
    data = request.get_json()
    email = data['email']
    
    try:
        lead = current_app.db.session.query(LeadModel).filter_by(email=email).one()

        current_app.db.session.delete(lead)
        current_app.db.session.commit()

        return '', 204

    except IndexError:
        return {'error': 'Lead not found, please check the email address'}, 404
