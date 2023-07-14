from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index
from datetime import datetime

db = SQLAlchemy()

class Mj(db.Model):
    __tablename__ = 'mj'
    __table_args__ = (
        Index('idx_customer_id', 'customer_id'),
        Index('idx_message_id', 'messageId'),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.String(255), index=True)
    prompt = db.Column(db.Text)
    imageUrl = db.Column(db.String(255))
    imageUrls = db.Column(db.ARRAY(db.String))
    type = db.Column(db.String(255))
    messageId = db.Column(db.String(255), index=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    responseAt = db.Column(db.DateTime)
    updateAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
