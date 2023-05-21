from datetime import date
from flask import abort
from api.membership.admins.daos.admin_dao import AdminDao
from api.membership.members.daos.member_dao import MemberDao
from api.membership.members.models.member_model import Gender, MemberModel, RelationshipStatus
from api.shared.daos.church_dao import ChurchDao


class AdminService():
    """Admin service"""
    
    def __init__(self) -> None:
        """initializes the admin services"""
        self.admin_dao = AdminDao()
    
    def create_member(self, data, admin_id):
        """creates and return a member"""
        admin = self.admin_dao.get_by_id(admin_id)
        church = admin.church
        
        if admin is None:
            abort(404, 'ONLY ADMINS CAN CREATE A MEMBER')

        if data.get('phone_number', None) is None:
            abort(403, "Phone number must be present")
        if data.get('email_address', None) is None:
            abort(403, "email address must be present")
        if data.get('password', None) is None:
            abort(403, "passeord must be present")
        if data.get('gender', None) is None:
            abort(403, 'gender must be present')
        if data.get('first_name', None) is None:
            abort(403, "first name must be present")
        if data.get('last_name', None) is None:
            abort(403, "last name must be present")
        if data.get('relationship_status', None) is None:
            abort(403, "relationship status must be present")
        
        data['gender'] = Gender.get_gender(data['gender'])
        data['relationship_status'] = RelationshipStatus.get_status(data['relationship_status'])
        if data.get('dob', None) is not None:
            data['dob'] = date.fromisoformat(data['dob'])
        member = MemberDao.get_by_email(data['email_address'])

        if member is not None:
            abort(405, description="Member already exist with the email {}".format(data["email_address"]))
        member = MemberDao.create(data, church)
        
        return member


    def update_member(self, data, admin_id, member_id):
        """updates a member record"""
        #check for valid admin
        admin = self.admin_dao.get_by_id(admin_id)
        if admin is None:
            abort(404, description="ONLY ADMINS CAN UPDATE A MEMBER")
        
        if member_id is "":
            abort(404, description="INVALID MEMBER ID")
        if data.get('password', None) is not None:
            abort(403, description="ADMIN CANNOT UPDATE PASSWORD FIELD FOR MEMBERS")
        if data.get('gender', None) is not None:
            data['gender'] = Gender.get_gender(data['gender'])
        if data.get('relationship_status', None) is not None:
            data['relationship_status'] = RelationshipStatus.get_status(data['relationship_status'])
        if data.get('dob', None) is not None:
            data['dob'] = date.fromisoformat(data['dob'])
        if data.get('church_id') is not None:
            abort(403, description="ADMIN CANNOT UPDATE CHURCH")
        
        member = MemberDao.update(member_id, data=data)
        if member is None:
            abort(404, description="INVALID MEMBER ID")
        return member

    def delete_member(self, admin_id, member_id):
        admin = self.admin_dao.get_by_id(admin_id)
        
        if admin is None:
            abort(404, description="ONLY ADMINS CAN DELETE A MEMBER")
        member = MemberDao.delete(member_id)
        if member is None:
            abort(404, description="MEMBER NOT FOUND")
        return member
