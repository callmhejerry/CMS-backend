from api import db
from api.shared.models.base_model import BaseModel
from enum import Enum
from werkzeug.security import check_password_hash, generate_password_hash


class Gender(Enum):
    """Class for representing gender"""
    FEMALE = 'F'
    MALE = 'M'
    
    @staticmethod
    def get_gender(gender):
        """convert from string to gender"""
        gender = gender.lower()
        if gender == 'female' or gender == 'f':
            return Gender.FEMALE
        if gender == 'male' or gender == 'm':
            return Gender.MALE

        return Gender.MALE
    
class RelationshipStatus(Enum):
    """class for representing relationship status"""
    MARRIED = 'Married'
    SINGLE = 'Single'
    DIVORSE = 'Divorse'
    
    @staticmethod
    def get_status(status):
        """convert to relationship status"""
        status = status.lower()
        if status == 'married':
            return RelationshipStatus.MARRIED
        if status == 'divorse':
            return RelationshipStatus.DIVORSE
        
        return RelationshipStatus.SINGLE

class MemberModel(BaseModel):
    """
    The memeber object class
    """
    __tablename__ = 'members'
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email_address = db.Column(db.String(60), unique=True, nullable=False)
    phone_number = db.Column(db.String(15))
    gender = db.Column(db.Enum(Gender), nullable=False)
    relationship_status = db.Column(db.Enum(RelationshipStatus), nullable=False)
    residential_address = db.Column(db.String(100))
    church_id = db.Column(db.String(60), db.ForeignKey('churches.id'))
    dob = db.Column(db.Date)
    password_hash = db.Column(db.String(128), nullable=False)
    
    
    def __init__(self, *args, **kwargs):
        """initializes the member"""
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
    
    def __str__(self):
        """String to print for the member object"""
        return "Member(id : {}, first_name : {})".format(self.id, self.first_name)


    def to_dict(self):
        """return the dictionary representation of the member"""
        new_dict = {}
        new_dict['id'] = self.id
        new_dict['first_name'] = self.first_name
        new_dict['last_name'] = self.last_name
        new_dict['email_address'] = self.email_address
        new_dict['phone_number'] = self.phone_number
        new_dict['residential_address'] = self.residential_address
        new_dict['gender'] = self.gender.value
        new_dict['relationship_status'] = self.relationship_status.value
        new_dict['dob'] = str(self.dob)
        return new_dict