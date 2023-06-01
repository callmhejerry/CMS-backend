from api.shared.models.church_model import ChurchModel
from api import db


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
    
    @staticmethod
    def get_all_members(church_id):
        """get all members of a church"""
        church = ChurchDao.get_by_id(church_id)
        if church is not None:
            members = church.members
            return members
        return church

    @staticmethod
    def create(data):
        """create a church in the database"""
        church = ChurchModel(**data)
        db.session.add(church)
        db.session.commit()
        return church
    
    @staticmethod
    def delete(church_id):
        """deletes a church"""
        church = ChurchDao.get_by_id(church_id)
        
        if church is None:
            db.session.delete(church)
            db.session.commit()
        return church

    @staticmethod
    def update(church_id, data):
        """updates a church record in the database"""
        church = ChurchDao.get_by_id(church_id)
        
        if church is not None:
            for key, value in data.items():
                setattr(church, key, value)
            db.session.commit()
        return church

