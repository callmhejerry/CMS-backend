from app import db



class Gender():
    """Class for representing gender"""
    FEMALE = 'F'
    MALE = 'M'
    
    
class RelationshipStatus():
    """class for representing relationship status"""
    MARRIED = 'Married'
    SINGLE = 'Single'
    DIVORSE = 'Divorse'
    
    
class Member(db.Model):
    """
    The memeber object class
    """
    __tablename__ = 'members'
    id = db.Column(db.String(60), primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email_address = db.Column(db.String(60), unique=True)
    phone_number = db.Column(db.String(15))
    gender = db.Column(db.Enum(Gender))
    relationship_status = db.Column(db.Enum(RelationshipStatus))
    church = db.Column(db.String(60), db.Foreignkey('churchs.id'))
    dob = db.Column(db.Date)
    # TODO : implement the passeord and password hash feature


    def __repr__(self):
        """String representation of the Member object"""
        return "<Member-{}>".format(self.id)

    
    def __str__(self):
        """String to print for the member object"""
        return "Member(id : {}, first_name : {})".format(self.id, self.first_name)
