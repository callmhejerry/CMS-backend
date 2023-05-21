from flask import Blueprint, jsonify

membership_blue_print = Blueprint('membership', __name__)

from .admins.routes import admin_route
# from .members.routes import member_route


@membership_blue_print.errorhandler(405)
def error_handler_for_405(error):
    """error handler for 405 error"""
    desc = error.description
    return jsonify({"error": desc}), 200
