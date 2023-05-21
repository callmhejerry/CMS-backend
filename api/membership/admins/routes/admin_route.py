from api.membership import membership_blue_print
from api import db
from api.membership.admins.models.admin_model import AdminModel
from flask import abort, request, jsonify
from api.membership.admins.services.AdminService import AdminService

from api.membership.members.models.member_model import Gender, MemberModel, RelationshipStatus
from api.shared.models.church_model import ChurchModel

admin_service = AdminService()

@membership_blue_print.route('/admin/<admin_id>/create-member',
                             strict_slashes=False,
                             methods=["POST"])
def create_member_by_admin(admin_id):
    """ROUTE - creates a member in the record"""
    if not request.is_json:
        abort(403, descriotion="INVALID JSON")
    data = request.get_json()
    member = admin_service.create_member(data, admin_id)
    
    return jsonify(member.to_dict()), 200


@membership_blue_print.route('/admin/<admin_id>/update-member/<member_id>',
                             strict_slashes=False,
                             methods=["PUT"])
def update_member_by_admin(admin_id, member_id):
    """ROUTE - Updates a member in the database"""
    if not request.is_json:
        abort(404, description="INVALID JSON")
    data = request.get_json()
    member = admin_service.update_member(data, admin_id=admin_id,
                                         member_id=member_id)
    
    return jsonify(member.to_dict()), 200


@membership_blue_print.route('/admin/<admin_id>/delete-member/<member_id>',
                             strict_slashes=False,
                             methods=["DELETE"])
def delete_member_by_admin(admin_id, member_id):
    """ROUTE - Deletes a member from the database"""
    member = admin_service.delete_member(admin_id, member_id)
    return jsonify(member), 200


@membership_blue_print.route("/admin/<admin_id>/members/<church_id>/",
                             strict_slashes=False,
                             methods=["GET"])
def all_members_of_a_church(admin_id, church_id):
    """ROUTE - gets all members of a church"""
    members = admin_service.get_members_of_a_church(admin_id, church_id)
    return jsonify(members), 200


@membership_blue_print.route("/admin/<admin_id>/members/<church_id>/",
                             strict_slashes=False,
                             methods=["POST"])
def filter_members_of_a_church(admin_id, church_id):
    """ROUTE - filters member of a church"""
    if not request.is_json:
        abort(404, description="INVALID JSON")
    data = request.get_json()
    members = admin_service.filer_members(admin_id, church_id, data)
    return jsonify(members), 200


@membership_blue_print.route('/admin/<admin_id>/members/search-by-name/',
                             strict_slashes=False,
                             methods=["POST"])
def search_by_name(admin_id):
    """ROUTE - searches for a member"""
    if not request.is_json:
        abort(404, description="INVALID JSON")
    data = request.get_json()
    members = admin_service.search_member_by_name(admin_id, data)
    return jsonify(members), 200


@membership_blue_print.route('/admin/sign-in', strict_slashes=False,
                             methods=["POST"])
def sign_in_admin():
    """ROUTE - admin sign in"""
    if not request.is_json:
        abort(404, description="INVALID JSON")
    data = request.get_json()
    admin = admin_service.sign_in(data)
    
    return jsonify(admin.to_dict()), 200
