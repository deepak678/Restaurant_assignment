from app import db
from passlib.apps import custom_app_context as pwd_context


class Restaurant(db.Model):
    __tablename__ = 'Restaurant'
    Restaurant_Id = db.Column(db.Integer, primary_key = True)
    Restaurant_Name = db.Column(db.String(32), index = True)
    Booth = db.Column(db.Integer)
    Couple = db.Column(db.Integer)
    Family = db.Column(db.Integer)

class User(db.Model):
    __tablename__ = 'users'
    User_Id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))

    #The hash_password() method takes a plain password as argument and stores a hash of it with the user. 
    # This method is called when a new user is added
    def hashPassword(self, password):
        self.password_hash = pwd_context.encrypt(password)

    #The verify_password() method takes a plain password as argument and returns True if the password is correct and false is not
    #This method is called whenever the user provides credentials and we need to verify them
    def verifyPassword(self, password):
        return pwd_context.verify(password, self.password_hash)


class Booking(db.Model):
    __tablename__ = 'Booking'
    Booking_Id = db.Column(db.Integer, primary_key = True)
    User_Id = db.Column(db.Integer, db.ForeignKey('users.User_Id'))
    user_table=db.relationship('User')
    Restaurant_Id = db.Column(db.Integer, db.ForeignKey('Restaurant.Restaurant_Id'))
    restaurant_table=db.relationship('Restaurant')
    Table_Type=db.Column(db.String(32))
    Booking_Date=db.Column(db.Text)

class Item(db.Model):
    __tablename__='Item'
    Item_Id=db.Column(db.Integer,primary_key=True)
    Restaurant_Id=db.Column(db.Integer,db.ForeignKey('Restaurant.Restaurant_Id'))
    restaurant_table=db.relationship('Restaurant')
    Item_Name=db.Column(db.Text)
    Price=db.Column(db.REAL)