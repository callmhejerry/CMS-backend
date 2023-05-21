from app import db
from uuid import uuid4


class BaseModel(db.Model):
    """Base model for all models"""
    __abstract__ = True
    id = db.Column(db.String(60), primary_key=True)
    
    def __init__(self, *args, **kwargs):
        """Initializatoin function for the object"""
        if kwargs is not None:
            for key, value in kwargs.items():
                setattr(self, key, value)
        self.id = uuid4().hex
    
    def to_dict(self):
        """
        convert object to a dictionary
        representationn
        """
        new_dict = self.__dict__.copy()
        del new_dict['_sa_instance_state']
        return new_dict
    
    def __repr__(self):
        """String representation of the Member object"""
        return "<{}-{}>".format(self.__class__.__name__, self.id)
