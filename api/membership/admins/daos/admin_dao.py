from api.membership.admins.models.admin_model import AdminModel

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
    