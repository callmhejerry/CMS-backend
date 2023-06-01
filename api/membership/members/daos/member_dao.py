from api.membership.members.models.member_model import MemberModel
from api import db


class MemberDao():
    """Member data access object"""

    @staticmethod
    def get_by_id(member_id):
        """Get member by id"""
        member = MemberModel.query.get(member_id)
        return member
    
    @staticmethod
    def get_by_email(email):
        """get member by email"""
        member = MemberModel.query.filter_by(email_address=email).first()
        return member
    
    @staticmethod
    def get_all():
        """get all members"""
        member = MemberModel.query.limit(10).all()
        return member
    
    @staticmethod
    def create(data, church):
        """creates a member in the database"""
        member = MemberModel(**data)
        member.church = church
        db.session.add(member)
        db.session.commit()
        
        return member

    @staticmethod
    def update(member_id, data):
        """update a member record"""
        member = MemberDao.get_by_id(member_id)
        if member is None:
            return None
        for key, value in data.items():
            setattr(member, key, value)
        db.session.commit()
        return member
    
    @staticmethod
    def delete(member_id):
        """deletes a member from database"""
        member = MemberDao.get_by_id(member_id=member_id)
        if member is None:
            return None
        db.session.delete(member)
        db.session.commit()
        return member

            