from api.events.models.event_category_model import EventCategoryModel
from api import db

class EventCategoryDao():
    """Event category dao"""
    
    @staticmethod
    def create(data):
        """creates an event category"""
        event_category = EventCategoryModel(**data)
        db.session.add(event_category)
        db.session.commit()
        return event_category
    
    @staticmethod
    def get_event_category_by_name(name):
        """gets even category by name"""
        category = EventCategoryModel.query.filter_by(name=name).first()
        return category
