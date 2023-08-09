from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index
from datetime import datetime

db = SQLAlchemy()

class Mj(db.Model):
    __tablename__ = 'mj'
    __table_args__ = (
        Index('idx_customer_id_mj', 'customer_id'),
        Index('idx_customer_email_mj', 'customer_email'),  # 添加了对customer_email字段的索引
        Index('idx_message_id_mj', 'messageId'),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.String(255), index=True)
    customer_name = db.Column(db.String(255), index=True)
    customer_email = db.Column(db.String(255), index=True)  # 添加了对customer_email字段的索引
    prompt = db.Column(db.Text)
    imageUrl = db.Column(db.String(255))
    imageUrls = db.Column(db.ARRAY(db.String))
    type = db.Column(db.String(255))
    messageId = db.Column(db.String(255), index=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    responseAt = db.Column(db.DateTime)
    updateAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Product(db.Model):
    __tablename__ = 'products'
    __table_args__ = (
        Index('idx_customer_id_product', 'customer_id'),
        Index('idx_customer_email_product', 'customer_email'),  # 添加了对customer_email字段的索引
        Index('idx_message_id_product', 'messageId'),
        Index('idx_variants_id_product', 'variantsId'),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    variantsId = db.Column(db.String(255), index=True)
    customer_id = db.Column(db.String(255), index=True)
    customer_name = db.Column(db.String(255), index=True)
    customer_email = db.Column(db.String(255), index=True)  # 添加了对customer_email字段的索引
    messageId = db.Column(db.String(255), index=True)
    selectedSize = db.Column(db.String(255))
    prompt = db.Column(db.String(255))
    imageUrl = db.Column(db.String(255))
    printImageUrl = db.Column(db.String(255))
    prodImageUrl = db.Column(db.String(255))
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    responseAt = db.Column(db.DateTime)
    updateAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
