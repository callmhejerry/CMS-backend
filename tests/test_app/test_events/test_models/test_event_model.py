import unittest
from app import create_app, db
from app.events.models.event_category_model import EventCategoryModel
from app.events.models.event_model import EventModel
from app.membership.admins.models.admin_model import AdminModel
from app.shared.models.church_model import ChurchModel
from datetime import date, time, datetime

class TestEventModel(unittest.TestCase):
    """Tests for the event model"""
    
    def setUp(self) -> None:
        """initialization"""
        self.app = create_app('testing')
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        db.create_all()
        self.church_1 = ChurchModel(name='Lam', location='Anambra')
        self.admin_1 = AdminModel(first_name='Jeremiah', last_name="Chinedu",
                             email_address="test@test.gmail.com",
                             phone_number="09034535401", church=self.church_1)
        self.category_1 = EventCategoryModel(name="singles program")
        self.event_1 = EventModel(title="Singles night",
                                  start_date=date(2023, 5, 29),
                                  end_date=date(2023, 5, 30),
                                  start_time=time(hour=17, minute=30),
                                  end_time=time(hour=20),
                                  venue="LCC",
                                  location="Book foundation",
                                  event_category=self.category_1,
                                  admin=self.admin_1,
                                  church=self.church_1)
        
        
    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()
    
    
    def test_attributes(self):
        """test all the attribute of an event object"""
        self.assertIn('id', self.event_1, "id present")
        self.assertIn('title', self.event_1, "title present")
        self.assertIn('thumbnail', self.event_1, "thumbnail present")
        self.assertIn('start_date', self.event_1, "start date present")
        self.assertIn('end_date', self.event_1, "end date present")
        self.assertIn('start_time', self.event_1, "start time present")
        self.assertIn('end_time', self.event_1, "end time present")
        self.assertIn('created_at', self.event_1, "created at present")
        self.assertIn('venue', self.event_1, "venue present")
        self.assertIn('location', self.event_1, "start time present")
        self.assertIn('event_category', self.event_1, "event category present")
        self.assertIn('admin', self.event_1, "admin present")
        self.assertIn('church', self.event_1, "church present")
    
    
    def test_attributes_type(self):
        """test the attribute type of all the attributes of an event object"""
        self.assertIsInstance(self.event_1.id, str)
        self.assertIsInstance(self.event_1.title, str)
        self.assertIsNone(self.event_1.thumbnail)
        self.assertIsInstance(self.event_1.start_date, date)
        self.assertIsInstance(self.event_1.end_date, date)
        self.assertIsInstance(self.event_1.start_time, time)
        self.assertIsInstance(self.event_1.end_time, time)
        self.assertIsInstance(self.event_1.created_at, datetime)
        self.assertIsInstance(self.event_1.venue, str)
        self.assertIsInstance(self.event_1.location, str)
        self.assertIsInstance(self.event_1.category_id, str)
        self.assertIsInstance(self.event_1.created_by, str)
        self.assertIsInstance(self.event_1.church_id, str)
    
    def test_todict(self):
        """test the to dict function"""
        pass
    