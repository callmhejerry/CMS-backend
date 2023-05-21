from api import db
from api.shared.models.base_model import BaseModel
from sqlalchemy import DateTime

class EventModel(BaseModel):
    """Model for event object"""
    
    __tablename__ = 'events'
    title = db.Column(db.String(60), nullable=False)
    thumbnail = db.Column(db.String(100))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    created_at = db.Column(DateTime, default=db.func.current_timestamp())
    venue = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(80), nullable=False)
    category_id = db.Column(db.String(60), db.ForeignKey('event_categories.id'))
    created_by = db.Column(db.String(60), db.ForeignKey('admins.id'))
    church_id = db.Column(db.String(60), db.ForeignKey('churches.id'))
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def __str__(self):
        """String representation for Event"""
        return "Event(id : {}, title: {})".format(self.id, self.title)
    
    def to_dict(self):
        new_dict = self.__dict__.copy()
        del new_dict['_sa_instance_state']
        new_dict['start_date'] = str(new_dict['start_date'])
        new_dict['end_date'] = str(new_dict['end_date'])
        new_dict['start_time'] = str(new_dict['start_time'])
        new_dict['end_time'] = str(new_dict['end_time'])
        new_dict['created_at'] = str(new_dict['created_at'])
        
        return new_dict
    