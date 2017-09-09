from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class ACMRequest(db.Model):
    __tablename__ = "acm_requests"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500))
    created_on = db.Column(db.DateTime, default=datetime.now, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    
    def __init__(self, body):
        self.body = body
    
    def to_dict(self):
        acm_request_dict = {
            'id' : self.id,
            'body' : self.body,
            'created_on' : self.created_on.isoformat(),
            'completed' : self.completed
        }

        return acm_request_dict
    
