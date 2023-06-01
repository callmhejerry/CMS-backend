from api.membership import membership_blue_print
from api.membership.admins.models.admin_model import AdminModel
from flask import abort, request, jsonify
from api.membership.admins.services.admin_service import AdminService

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


@membership_blue_print.route("/admin/<admin_id>/members/",
                             strict_slashes=False,
                             methods=["GET"])
def all_members_of_a_church(admin_id):
    """ROUTE - gets all members of a church"""
    members = admin_service.get_members_of_a_church(admin_id)
    return jsonify(members), 200


@membership_blue_print.route("/admin/<admin_id>/members/",
                             strict_slashes=False,
                             methods=["POST"])
def filter_members_of_a_church(admin_id):
    """ROUTE - filters member of a church"""
    if not request.is_json:
        abort(404, description="INVALID JSON")
    data = request.get_json()
    members = admin_service.filter_members(admin_id, data)
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
    admin_dict = admin.to_dict().copy()
    admin_dict["id"] = admin.id
    return jsonify(admin_dict), 200


@membership_blue_print.route('/admin/<admin_id>/create-admin/',
                             strict_slashes=False,
                             methods=["POST"])
def create_admin_by_admin(admin_id):
    """ROUTE - creates an admin"""
    if not request.is_json:
        abort(404, description="INVALID JSON")
    data = request.get_json()
    admin = admin_service.create_admin(admin_id, data)
    return jsonify(admin.to_dict()), 200


@membership_blue_print.route('/admin/<admin_id>/update',
                             strict_slashes=False,
                             methods=["PUT"])
def update_admin(admin_id):
    """ROUTE - updates admin"""
    if not request.is_json:
        abort(404, description="INVALID JSON")
    data = request.get_json()
    admin = admin_service.update_admin(admin_id, data)
    
    return jsonify(admin.to_dict()), 200


@membership_blue_print.route('/admin/<admin_id>/create-church',
                             strict_slashes=False,
                             methods=["POST"])
def create_church(admin_id):
    """ROUTE - create a church"""
    if not request.is_json:
        abort(404, description="INVALID JSON")
    data = request.get_json()
    church = admin_service.create_church(admin_id, data)
    
    return jsonify(church.to_dict()), 200


# @membership_blue_print.route('/admin/<admin_id>/delete-church/<church_id>',
#                              strict_slashes=False,
#                              methods=["DELETE"])
# def delete_church(admin_id, church_id):
#     """ROUTE - deletes a church record"""
#     church = admin_service.delete_church(admin_id, church_id)
#     return jsonify(church), 200


@membership_blue_print.route("/admin/<admin_id>/update-church/",
                             strict_slashes=False,
                             methods=["PUT"])
def update_church(admin_id):
    """ROUTE - update church"""
    if not request.is_json:
        abort(404, description="INVALID JSON")
    data =request.get_json()
    church = admin_service.update_church(admin_id, data)
    
    return jsonify(church.to_dict()), 200

@membership_blue_print.route("/admin/<admin_id>/count/", strict_slashes=False)
def count(admin_id):
    """Route - get count of various aspect of the church"""
    count = admin_service.count(admin_id)
    return jsonify(count), 200

@membership_blue_print.route("/admins/", strict_slashes=False)
def all_admins():
    """ROUTE - get all admins"""
    admins = admin_service.get_all_admins()
    return jsonify(admins), 200