from db.db import db

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(255), nullable=False)
    userEmail = db.Column(db.String(255), nullable=False)
    products = db.Column(db.JSON, nullable=False)  
