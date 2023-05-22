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
        if data.get('church_id', None) is not None:
            del data['church_id']
        
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
        if data.get("id", None) is not None:
            del data['id']
        
        member = MemberDao.update(member_id, data=data)
        if member is None:
            abort(404, description="INVALID MEMBER ID")
        return member


    def delete_member(self, admin_id, member_id):
        """deletes a memeber from the database"""
        admin = self.admin_dao.get_by_id(admin_id)
        
        if admin is None:
            abort(404, description="ONLY ADMINS CAN DELETE A MEMBER")
        member = MemberDao.delete(member_id)
        if member is None:
            abort(404, description="MEMBER NOT FOUND")
        return {}


    def get_members_of_a_church(self, admin_id):
        """gets all members of a church"""
        admin = self.admin_dao.get_by_id(admin_id)
        if admin is None:
            abort(404, description="ONLY ADMINS CAN GET MEMBERS")
        church = admin.church
        members = ChurchDao.get_all_members(church.id)
        if members is None:
            abort(404, description="INVALID CHURCH")
        members_list = list(map(lambda member: member.to_dict(), members))
        return members_list


    def filter_members(self, admin_id, church_id, data):
        """filters members of a church based on some fields"""
        admin = self.admin_dao.get_by_id(admin_id)
        if admin is None:
            abort(404, description="ONLY ADMINS CAN FILTER MEMBERS")
        members = ChurchDao.get_all_members(church_id)
        if members is None:
            abort(404, description="INVALID CHURCH")
        gender = data.get('gender', None)
        relationship_status = data.get('relationship_status', None)
        
        filter_list = []
        
        # filter by gender first
        if gender is not None:
            gender = Gender.get_gender(gender)
            for member in members:
                if member.gender == gender:
                    filter_list.append(member)
        
        # filter by relationship_status
        if relationship_status is not None:
            relationship_status = RelationshipStatus.get_status(relationship_status)
            for member in members:
                if member.relationship_status == relationship_status:
                    filter_list.append(member)
        
        members_list = list(map(lambda member: member.to_dict(), filter_list))
        return members_list


    def search_member_by_name(self, admin_id, data):
        """searches for a member by id"""
        admin = self.admin_dao.get_by_id(admin_id)
        if admin is None:
            abort(404, description="ONLY ADMINS CAN FILTER MEMBERS")
        church = admin.church
        members = ChurchDao.get_by_id(church.id)
        name = data.get('name', None)
        if name is None:
            abort(403, description="NAME MUST BE PRESENT")
        
        names = name.split(" ")
        filter_list = []
        
        for n in names:
            for member in members:
                if member.first_name == n or member.last_name == n:
                    filter_list.append(member)
        
        members_list = list(map(lambda member: member.to_dict(), filter_list))
        return members_list


    def sign_in(self, data):
        """signs in an admin"""
        email = data.get('email_address', None)
        password = data.get('password', None)
        
        if email is None or password is None:
            abort(404, description="EMAIL AND PASSWORD MUST BE PROVIDED")
        
        admin = self.admin_dao.get_by_email(email)
        
        if not admin.verify(password, admin.password_hash):
            abort(403, description="INVALID EMAIL OR PASSWORD")
        
        return admin


    def create_admin(self, admin_id, data):
        """creates an admin"""
        admin = self.admin_dao.get_by_id(admin_id)
        if admin is None:
            abort(404, description="ONLY ADMINS CAN CREATE ADMINS")
        
        if data.get("first_name", None) is None:
            abort(403, description="FIRST NAME MUST BE PRESENT")
        if data.get('last_name', None) is None:
            abort(403, description="LAST NAME MUST BE PRESENT")
        if data.get("email_address", None) is None:
            abort(403, description="EMAIL ADDRESS MUST BE PRESENT")
        if data.get("phone_number", None) is None:
            abort(403, description="PHONE NUMBER MUST BE PRESENT")
        if data.get("password", None) is None:
            abort(403, description="PASSWORD MUST BE PRESENT")
        if data.get("church_id", None) is None:
            abort(403, description="CHURCH ID MUST BE PRESENT")
        
        admin = self.admin_dao.get_by_email(data['email_address'])
        if admin is None:
            admin = self.admin_dao.create(data)
        else:
            abort(403, description="ADMIN ALREADY PRESENT WITH THE EMAIL {}".format(
                data['email_address']
            ))
        
        return admin


    def update_admin(self, admin_id, data):
        """update admin record"""
        if data.get('id', None) is not None:
            del data['id']
        if data.get("church_id", None) is not None:
            abort(403, description="CANNOT UPDATE CHURCH")
        
        admin = self.admin_dao.update(admin_id, data)
        if admin is None:
            abort(404, description="ADMIN NOT FOUND")
        return admin


    def create_church(self, admin_id, data):
        """creates a church in the database"""
        admin = self.admin_dao.get_by_id(admin_id)
        if admin is None:
            abort(404, description="ONLY ADMINS CAN CREATE A CHURCH")
        
        if data.get('name', None) is None:
            abort(403, description="NAME MUST BE PRESENT")
        if data.get('location', None) is None:
            abort(403, description="LOCATION MUST BE PRESENT")
        
        church = ChurchDao.get_by_name(data['name'])
        
        if church is not None:
            abort(403, description="CHURCH ALREADY EXIST")
        church = ChurchDao.create(data)
        
        return church


    def delete_church(self, admin_id, church_id):
        """deltetes a church from the database"""
        admin = self.admin_dao.get_by_id(admin_id)
        if admin is None:
            abort(404, description="ONLY ADMINS CAN DELETE A CHURCH")
        church = ChurchDao.delete(church_id)
        
        if church is None:
            abort(404, description="NO CHURCH FOUND")
        return {}

    def update_church(self, admin_id, church_id, data):
        """updates a church record"""
        admin = self.admin_dao.get_by_id(admin_id)
        if admin is None:
            abort(404, description="ONLY ADMINS CAN UPDATE A CHURCH")
        if data.get('id', None) is not None:
            del data['id']
        
        church = ChurchDao.update(church_id, data)
        if church is None:
            abort(404, "NO CHURCH FOUND")
        return church

        