from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primery_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=True, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=True, nullable=False)
    store = db.relationship("StoreModel", back_populates="items")
    