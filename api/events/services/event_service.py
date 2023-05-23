from flask_uploads import UploadSet, IMAGES
from datetime import date, time
from flask import abort
from api.events.daos.event_category_dao import EventCategoryDao
from api.events.daos.event_dao import EventDao
from uuid import uuid4
import os
from config import total_path

from api.membership.admins.daos.admin_dao import AdminDao

fliers = UploadSet('fliers', IMAGES)


class EventService():
    """Event service"""
    
    def __init__(self) -> None:
        """Initializes the Event service"""
        self.event_dao = EventDao()
    
    def create_event(self, admin_id, data, flier):
        """creates an event"""
        admin = AdminDao.get_by_id(admin_id)
        new_data = data.copy()
        
        if admin is None:
            abort(404, description="INVALID ADMIN")
    
        
        if "title" not in new_data:
            abort(403, decription="TITLE MUST BE PRESENT")
        if "start_date" not in new_data:
            abort(403, description="START DATE MUST BE PRESENT")
        if "end_date" not in new_data:
            abort(403, description="END DATE MUST BE PRESENT")
        if "start_time" not in new_data:
            abort(403, description="START TIME MUST BE PRESENT")
        if "end_time" not in new_data:
            abort(403, description="START TIME MUST BE PRESENT")
        if "venue" not in new_data:
            abort(403, description="VENUE MUST BE PRESENT")
        if "location" not in new_data:
            abort(403, description="LOCATION MUST BE PRESENT")
        if "event_category" not in new_data:
            abort(403, description="EVENT CATEGORY MUST BE PRESENT")
        
        
        new_data["church"] = admin.church
        new_data["admin"] = admin
        
        event_category = EventCategoryDao.get_event_category_by_name(new_data["event_category"])
        if event_category is None:
            abort(403, description="INVALID EVENTS")
        new_data["event_category"] = event_category
        new_data["start_date"] = date.fromisoformat(new_data["start_date"])
        new_data["end_date"] = date.fromisoformat(new_data["end_date"])
        new_data["start_time"] = time.fromisoformat(new_data["start_time"])
        new_data["end_time"] = time.fromisoformat(new_data["end_time"])
        name = uuid4().hex + '.'
        file_name = fliers.save(flier, name=name)
        new_data["thumbnail"] = file_name
        
        event = self.event_dao.create_event(new_data)
        if event is None:
            #delete the saved picture
            file_path = os.path.join(total_path, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        return event

    def delete_event(self, admin_id, event_id):
        """deletes the event from the database"""
        admin = AdminDao.get_by_id(admin_id)
        
        if admin is None:
            abort(403, description="INVALID ADMIN")
        
        event = self.event_dao.delete_event(event_id)
        
        if event is None:
            abort(403, description="INVALID EVENT")
        file_name = event.thumbnail
        file_path = os.path.join(total_path, file_name)
        
        print(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return {}
    

    def update_event(self, admin_id, event_id, data, file):
        """update event post"""
        admin = AdminDao.get_by_id(admin_id)
        
        if admin is None:
            abort(403, description="INVALID ADMIN")
        
        if "start_date" in data:
            data["start_date"] = date.fromisoformat(data["start_date"])
        if "end_date" in data:
            data["end_date"] = date.fromisoformat(data["end_date"])
        if "end_time" in data:
            data["end_time"] = date.fromisoformat(data["end_time"])
        if "start_time" in data:
            data["start_time"] = date.fromisoformat(data["start_time"])
        if "flier" in file:
            event = EventDao.get_event_by_id(event_id)
            flier = file["flier"]
            if event is None:
                abort(404, description="EVENT NOT FOUND")
            previous_file_name = event.thumbnail
            previous_file_path = os.path.join(total_path, previous_file_name)
            if os.path.exists(previous_file_path):
                os.remove(previous_file_path)
            name = uuid4().hex + "."
            file_name = fliers.save(flier, name=name)
            data["thumbnail"] = file_name
        if "created_by" in data:
            del data["created_by"]
        if "church_id" in data:
            del data["church_id"]
        if "event_category" in data:
            event_category = EventCategoryDao.get_event_category_by_name(data["event_category"])
            if event_category:
                data["event_category"] = event_category
            else:
                abort(404, description="EVENT NOT FOUND")
        
        event = self.event_dao.update_event(event_id, data)
        return event


    def get_all_events_by_admin(self, admin_id, base_url):
        """Gets all events created by admin"""
        admin = AdminDao.get_by_id(admin_id)
        if admin is None:
            abort(404, description="INVALID ADMIN")
        
        events = self.event_dao.get_event_by_admin(admin_id)
        events_list = list(map(lambda event: event.to_dict(), events))

        return self.get_events_with_flier(events_list, base_url)


    def add_event_category(self, admim_id, data):
        """Adds event category to the database"""
        admin = AdminDao.get_by_id(admim_id)
        
        if admin is None:
            abort(404, description="INVALID ADMIN")
        if "name" not in data:
            abort(403, description="NAME MUST BE PRESNT")
        
        event = EventCategoryDao.get_event_category_by_name(data["name"])
        if event:
            abort(403, description="EVENT CATEGORY ALREADY PRESENT")
        event = EventCategoryDao.create(data)
        
        return event

    def events_by_category(self, event_category_name, base_url):
        """gets events by category"""
        events = self.event_dao.events_by_category(event_category_name)
        if events is None:
            abort(404, description="INVALID EVENT CATEGORY")
        if events == []:
            abort(404, description="NO EVENTS FOUND")
        
        event_list = list(map(lambda event: event.to_dict(), events))
        
        return self.get_events_with_flier(event_list, base_url)
        
    def get_events_with_flier(self, events_list, base_url):
        """returns a list of events with the correct flier link"""
        new_list = []
        for event in events_list:
            event["thumbnail"] = base_url + "api/events/flier/" + event["thumbnail"]
            new_list.append(event)
        return new_list
    

    def today_events(self, base_url):
        """Get todays event"""
        today = date.today()
        events = self.event_dao.today_events(today)
        events_list = list(map(lambda event: event.to_dict(), events))
        return self.get_events_with_flier(events_list, base_url)

    def upcoming_events(self, base_url):
        """Get upcoming events"""
        today = date.today()
        all_events = self.event_dao.get_all_events()
        upcoming_events = []
        if all_events:
            for event in all_events:
                if event.start_date > today or event.end_date > today:
                    upcoming_events.append(event.to_dict())
        return self.get_events_with_flier(upcoming_events, base_url)


    def past_events(self, base_url):
        """Get past events"""
        today = date.today()
        all_events = self.event_dao.get_past_events(today)
        past_events = list(map(lambda event: event.to_dict(), all_events))
        return self.get_events_with_flier(past_events, base_url)
    
