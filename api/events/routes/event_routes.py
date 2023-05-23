from api.events import event_blue_print
from flask import request, abort, jsonify, send_from_directory
from api.events.services.event_service import EventService
from config import total_path
import os


event_service = EventService()


@event_blue_print.route("/admin/<admin_id>/event", strict_slashes=False,
                        methods=["POST"])
def create_event(admin_id):
    """ROUTE - creates an event"""
    # if not request.is_json:
    #     print("invalid json")
    #     abort(404, description="INVALID JSON")
    if "flier" not in request.files:
        abort(403, "UPLOAD A FLIER FOR THE EVENT")
    data = request.form
    flier = request.files['flier']
    
    event = event_service.create_event(admin_id, data, flier)
    
    return jsonify(event.to_dict()), 200


@event_blue_print.route('/admin/<admin_id>/event/<event_id>/',
                        strict_slashes=False,
                        methods=["DELETE"])
def delete_event(admin_id, event_id):
    """ROUTE - deletes an event"""
    event = event_service.delete_event(admin_id, event_id)
    return jsonify(event), 200


@event_blue_print.route('/admin/<admin_id>/event/<event_id>/',
                        strict_slashes=False,
                        methods=["put"])
def update_event(admin_id, event_id):
    """ROUTE - updates an event"""
    
    data = request.form.copy()
    file = request.files.copy()
    
    event = event_service.update_event(admin_id, event_id, data, file)
    return jsonify(event.to_dict()), 200


@event_blue_print.route("/admin/<admin_id>/events/",
                        strict_slashes=False,
                        methods=["GET"])
def all_events(admin_id):
    """ROUTE - gets all events created by admin"""
    base_url = request.host_url
    events = event_service.get_all_events_by_admin(admin_id, base_url)
    return jsonify(events), 200


@event_blue_print.route('/admin/<admin_id>/add-category/',
                        strict_slashes=False,
                        methods=["POST"])
def add_category(admin_id):
    """ROUTE - adds event category"""
    if not request.is_json:
        abort(404, description="INVALID JSON")
    
    data = request.get_json()
    event_category = event_service.add_event_category(admin_id, data)
    return jsonify(event_category.to_dict()), 200


@event_blue_print.route('/flier/<file_name>', strict_slashes=False)
def get_flier(file_name):
    """ROUTE - get a flier"""
    if os.path.exists(os.path.join(total_path, file_name)):
        return send_from_directory(total_path, file_name), 200
    abort(404, description="FLIER NOT FOUND")


@event_blue_print.route('/event-by-category/<event_category_name>', strict_slashes=False)
def get_events_by_category(event_category_name):
    """ROUTE - get events by category"""
    base_url = request.host_url
    events = event_service.events_by_category(event_category_name, base_url)
    return jsonify(events)


@event_blue_print.route('/today', strict_slashes=False)
def today_events():
    """ROUTE - get events by category"""
    base_url = request.host_url
    events = event_service.today_events(base_url)
    return jsonify(events), 200


@event_blue_print.route("/upcoming", strict_slashes=False)
def upcoming_events():
    """ROUTE - get upcoming events"""
    base_url = request.host_url
    events = event_service.upcoming_events(base_url)
    return jsonify(events), 200


@event_blue_print.route("/past", strict_slashes=False)
def past_event():
    """ROUTE - get past events"""
    base_url = request.host_url
    events = event_service.past_events(base_url)
    return jsonify(events), 200
