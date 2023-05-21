from app import db
from app.shared.models.base_model import BaseModel



class EventCategoryModel(BaseModel):
    """Model for event category"""
    
    __tablename__ = 'event_categories'
    name = db.Column(db.String(30), nullable=False)
    events = db.relationship('EventModel', backref='event_category', cascade='all, delete')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        """string representation for EventCategory"""
        return "EventCategoryModel(id : {} , name : {})".format(self.id, self.name)
