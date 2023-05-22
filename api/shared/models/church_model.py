from api import db
from .base_model import BaseModel

class ChurchModel(BaseModel):
    """Model for the church object"""
    __tablename__ = 'churches'
    name = db.Column(db.String(80), unique=True)
    location = db.Column(db.String(100))
    members = db.relationship('MemberModel', backref='church', cascade='all, delete')
    admins = db.relationship('AdminModel', backref='church', cascade='all, delete')
    events = db.relationship('EventModel', backref='church', cascade='all, delete')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        """string representation of the Church"""
        return "Church(id : {}, name : {})".format(self.id, self.name)

    def to_dict(self):
        """return the dictionary representation of church"""
        new_dict = {}
        new_dict['name'] = self.name
        new_dict["location"] = self.location
        new_dict["id"] = self.id
        
        return new_dict
