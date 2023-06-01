from api import db
from api.shared.models.base_model import BaseModel
from sqlalchemy import DateTime

class EventModel(BaseModel):
    """Model for event object"""
    
    __tablename__ = 'events'
    title = db.Column(db.String(60), nullable=False)
    thumbnail = db.Column(db.String(100), nullable=False)
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
        new_dict = {}
        
        new_dict['start_date'] = str(self.start_date)
        new_dict['title'] = self.title
        new_dict["thumbnail"] = self.thumbnail
        new_dict["venue"] = self.venue
        new_dict["location"] = self.location
        new_dict['start_date'] = str(self.start_date)
        new_dict['end_date'] = str(self.end_date)
        new_dict['start_time'] = str(self.start_time)
        new_dict['end_time'] = str(self.end_time)
        new_dict['created_at'] = str(self.created_at)
        new_dict['end_date'] = str(self.end_date)
        new_dict['start_time'] = str(self.start_time)
        new_dict['end_time'] = str(self.end_time)
        new_dict['created_at'] = str(self.created_at)     
        new_dict["church"] = self.church.name   
        return new_dict
    