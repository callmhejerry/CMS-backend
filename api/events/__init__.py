from flask import Blueprint

event_blue_print = Blueprint('events', __name__)

from .routes import event_routes