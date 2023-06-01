from api.events.models.event_model import EventModel
from api.events.models.event_category_model import EventCategoryModel
from api import db

class EventDao():
    """Events data access object"""
    
    @staticmethod
    def create_event(data):
        """Creates an event"""
        event = EventModel(**data)
        db.session.add(event)
        db.session.commit()
        return event

    @staticmethod
    def get_event_by_id(event_id):
        """gets event by ID"""
        event  = EventModel.query.get(event_id)
        return event
    
    @staticmethod
    def delete_event(event_id):
        """deletes event from the database"""
        event = EventDao.get_event_by_id(event_id)
        if event:
            db.session.delete(event)
            db.session.commit()
        return event

    @staticmethod
    def update_event(event_id, data):
        """update an event in the database"""
        event = EventDao.get_event_by_id(event_id)
        
        if event is not None:
            for key , value in data.items():
                setattr(event, key, value)
            db.session.commit()
        return event


    @staticmethod
    def get_event_by_admin(admin_id):
        """gets events created by admins"""
        events = EventModel.query.filter_by(created_by=admin_id)
        return events


    @staticmethod
    def events_by_category(event_category_name):
        """gets events by category name"""
        event_category = EventCategoryModel.query.filter_by(name=event_category_name).first()
        
        if event_category:
            events = event_category.events
            return events
        
        return event_category

    @staticmethod
    def today_events(today):
        """returns events for today"""
        events = EventModel.query.filter_by(start_date=today).all()
        return events

    @staticmethod
    def get_all_events(limit=None):
        """gets all events"""
        if limit:
            events = EventModel.query.limit(limit).all()
        else:
            events = EventModel.query.all()
        return events

    @staticmethod
    def get_past_events(today, limit=None):
        """get past events"""
        if limit:
            events = EventModel.query.filter(EventModel.end_date < today).limit(limit)
        else:
            events = EventModel.query.filter(EventModel.end_date < today).all()
        return events
