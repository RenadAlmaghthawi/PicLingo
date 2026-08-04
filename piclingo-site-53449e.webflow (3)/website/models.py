from . import db
from flask_login import UserMixin 



# Database schema 

#Favorites table (id, mentor_id, image_id)
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'))
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))


#Mentor table (id,FullName,email,password)
class Mentor(db.Model, UserMixin):
    fullName = db.Column(db.String(255))
    email = db.Column(db.String(255),unique=True)
    password =  db.Column(db.String(250))
    id = db.Column(db.Integer, primary_key=True)
    favorites = db.relationship('Favorite', backref='mentor', lazy=True)


#Image table (id , category , caption , faviorite tag)
class Image(db.Model):
    #image = db.Column(db.LargeBinary, nullable=False)
    image = db.Column(db.Text, unique=True, nullable=False)
    category = db.Column(db.Text, nullable=False)
    caption = db.Column(db.Text, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    favorites = db.relationship('Favorite', backref='image', lazy=True)

