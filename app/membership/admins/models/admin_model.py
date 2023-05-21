from app.shared.models.base_model import BaseModel
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class AdminModel(BaseModel):
    """
    Admin model for the Admin
    """
    __tablename__ = 'admins'
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email_address = db.Column(db.String(60), unique=True, nullable=False)
    phone_number = db.Column(db.String(15))
    church_id = db.Column(db.String(60), db.ForeignKey('churches.id'))
    events = db.relationship('EventModel', backref='admin')
    password_hash = db.Column(db.String(128), nullable=False)
    
    def __init__(self, *args, **kwargs):
        """initializes the object for the Admin"""
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        raise AttributeError("Password cannot be read")
    
    @password.setter
    def password(self, password):
        """generate password hash for password"""
        self.password_hash = generate_password_hash(password)
    
    def verify(self, password_hash, password)->bool:
        """check the password stored if it matches"""
        return check_password_hash(password_hash, password)

    def to_dict(self):
        """dictionary representation of the admin object"""
        new_dict = self.__dict__.copy()
        del new_dict['_sa_instance_state']
        del new_dict['password_hash']
        
        return new_dict
