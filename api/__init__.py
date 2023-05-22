from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

from api.shared.daos.church_dao import ChurchDao
from api.shared.services.church_service import ChurchService
from .events.models.event_category_model import EventCategoryModel
from .events.models.event_model import EventModel
from .membership.admins.models.admin_model import AdminModel
from .membership.members.models.member_model import MemberModel
from .shared.models.base_model import BaseModel
from .shared.models.church_model import ChurchModel
from .membership import membership_blue_print

def create_app(configuration):
    """Factory function to create and return
    flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config[configuration])
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    app.register_blueprint(membership_blue_print, url_prefix="/api/membership")
    @app.shell_context_processor
    def make_shell():
        """return objects in the shell"""
        return dict(db=db,
                    ChurchModel=ChurchModel,
                    AdminModel=AdminModel,
                    app=app,
                    EventModel=EventModel,
                    EventCategoryModel=EventCategoryModel,
                    MemberModel=MemberModel)
    
    @app.route('/api/churches',strict_slashes=False)
    def all_churches():
        churches = ChurchService().get_all_churches()
        return jsonify(churches), 200
    
    
    return app
