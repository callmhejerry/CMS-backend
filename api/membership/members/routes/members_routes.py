from flask import request, abort, jsonify
from api.membership import membership_blue_print
from api.membership.members.services.members_services import MemberService

member_service = MemberService()

@membership_blue_print.route('/member/register', strict_slashes=False,
                             methods=["POST"])
def register_member():
    """ROUTES - creates a member in the database"""
    if not request.is_json:
        abort(404, description="INVALID JSON")
    data = request.get_json()
    member = member_service.register_member(data)
    return jsonify(member.to_dict()), 200


@membership_blue_print.route("/member/update-member/<member_id>/",
                             strict_slashes=False,
                             methods=["PUT"])
def update_member(member_id):
    """ROUTES - updates member record"""

    if not request.is_json:
        abort(404, description="INVALID JSON")
        
    data = request.get_json()
    member = member_service.update_member(member_id, data)
    return jsonify(member.to_dict()), 200
    

@membership_blue_print.route("/member/activate/", strict_slashes=False,
                             methods=["POST"])
def activate_member():
    if not request.is_json:
        abort(404, description="INVALID JSON")
    data = request.get_json()
    member = member_service.activate_member(data)
    member_json = member.to_dict()
    if member_json.get("password_hash", None) is not None:
        del member_json["password_hash"]
    return jsonify(member_json), 200
 