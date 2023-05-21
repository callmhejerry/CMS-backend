from api.shared.models.church_model import ChurchModel


class ChurchDao():
    """Church data access object"""
    
    @staticmethod
    def get_by_id(church_id):
        """get church by id"""
        church = ChurchModel.query.get(church_id)
        return church
    
    @staticmethod
    def get_by_name(name):
        """get church by name"""
        church = ChurchModel.query.filter_by(name=name).first()
        return church
    
    @staticmethod
    def get_all():
        """get all churches"""
        churches = ChurchModel.query.all()
        return churches
    