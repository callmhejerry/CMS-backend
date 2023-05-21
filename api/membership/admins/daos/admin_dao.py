from api.membership.admins.models.admin_model import AdminModel
from api import db

class AdminDao():
    """Class to access admin object"""
    
    @staticmethod
    def get_by_id(id):
        """get admin by id"""
        admin = AdminModel.query.get(id)
        return admin
    
    @staticmethod
    def get_all():
        """get all admins"""
        admins = AdminModel.query.all()
        return admins
    
    @staticmethod
    def get_by_email(email):
        """get admin by email"""
        admin = AdminModel.query.filter_by(email_address=email).first()
        return admin

    @staticmethod
    def create(data):
        """creates an admin"""
        admin = AdminModel(**data)
        db.session.add(admin)
        db.session.commit()