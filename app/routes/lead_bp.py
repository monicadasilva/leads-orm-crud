from flask import Blueprint

from app.controllers.lead_controller import create_lead, delete_lead, get_all_by_visist_order, update_lead

bp_leads = Blueprint('bp_leads', __name__, url_prefix='/leads')


bp_leads.post('')(create_lead)
bp_leads.get('')(get_all_by_visist_order)
bp_leads.patch('')(update_lead)
bp_leads.delete('')(delete_lead)
