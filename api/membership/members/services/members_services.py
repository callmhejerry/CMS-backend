
from datetime import date
from flask import abort
from api.membership.members.daos.member_dao import MemberDao
from api.membership.members.models.member_model import Gender, RelationshipStatus
from api.shared.daos.church_dao import ChurchDao


class MemberService():
    """Member service class"""
    
    def __init__(self) -> None:
        self.member_dao = MemberDao()
    
    def register_member(self, data):
        """registers a member"""

        if data.get('phone_number', None) is None:
            abort(403, "Phone number must be present")
        if data.get('email_address', None) is None:
            abort(403, "email address must be present")
        if data.get('password', None) is None:
            abort(403, "password must be present")
        if data.get('gender', None) is None:
            abort(403, 'gender must be present')
        if data.get('first_name', None) is None:
            abort(403, "first name must be present")
        if data.get('last_name', None) is None:
            abort(403, "last name must be present")
        if data.get('relationship_status', None) is None:
            abort(403, "relationship status must be present")
        if data.get('church_id', None) is None:
            abort(403, "CHURCH_ID MUST BE PRESENT")
        
        church = ChurchDao.get_by_id(data["church_id"])
        del data["church_id"]
        data['gender'] = Gender.get_gender(data['gender'])
        data['relationship_status'] = RelationshipStatus.get_status(data['relationship_status'])
        if data.get('dob', None) is not None:
            data['dob'] = date.fromisoformat(data['dob'])
        data["email_address"] = data["email_address"].lower()
        member = MemberDao.get_by_email(data['email_address'])

        if member is not None:
            abort(405, description="Member already exist with the email {}".format(data["email_address"]))

        member = self.member_dao.create(data, church)
        
        return member


    def update_member(self, member_id, data):
        """updates a member record"""
        if member_id is "":
            abort(404, description="INVALID MEMBER ID")
        if data.get('gender', None) is not None:
            data['gender'] = Gender.get_gender(data['gender'])
        if data.get('relationship_status', None) is not None:
            data['relationship_status'] = RelationshipStatus.get_status(data['relationship_status'])
        if data.get('dob', None) is not None:
            data['dob'] = date.fromisoformat(data['dob'])
        if data.get("id", None) is not None:
            del data['id']
        if data.get("church_id", None) is not None:
            church = ChurchDao.get_by_id(data["church_id"])
            del data["church_id"]
            data["church"] = church
        
        member = MemberDao.update(member_id, data=data)
        if member is None:
            abort(404, description="INVALID MEMBER ID")
        return member


    def activate_member(self, data):
        """activates a member"""
        if data.get("email_address", None) is None:
            abort(403, description="EMAIL ADDRESS MUST BE PRESENT")
        if data.get("password", None) is None:
            abort(403, description="PASSWORD MUST BE PRESENT")
        
        data["email_address"] = data["email_address"].lower()
        member = self.member_dao.get_by_email(data["email_address"])
        if member is None:
            abort(403, description="PLEASE REGISTER")
        if member.verify(data["password"]):
            return member
        else:
            abort(403, description="INVALID EMAIL OR PASSWORD")
