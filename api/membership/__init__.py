from flask import Blueprint, jsonify

membership_blue_print = Blueprint('membership', __name__)

from .admins.routes import admin_route
from .members.routes import members_routes


@membership_blue_print.errorhandler(405)
def error_handler_for_405(error):
    """error handler for 405 error"""
    desc = error.description
    return jsonify({"error": desc}), 405

@membership_blue_print.errorhandler(404)
def error_handler_for_404(error):
    """error handler for 404 error"""
    desc = error.description
    return jsonify({"error": desc}), 404

@membership_blue_print.errorhandler(403)
def error_handler_for_403(error):
    """error handler for 403 error"""
    desc = error.description
    return jsonify({"error": desc}), 403