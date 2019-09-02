from app import app,db
from tables import User,Restaurant,Booking
from flask import request

#to list all the restaurants available in our system
@app.route('/api/Restaurants')
def getRestaurant():
    a=Restaurant.query.all()
    result=""
    for i in a:
        result=result + "\n" + i.Restaurant_Name
    return result

#gives the Number of tables available for a particular restaurant
@app.route('/api/<restaurant_name>/tables',methods=['POST'])
def getTables(restaurant_name):
    #on which date you have to check no. of available tables 
    booking_date=request.json.get('booking_date')
    #taking out restaurant id from restaurant name
    restaurant=Restaurant.query.filter_by(Restaurant_Name=restaurant_name).first()
    restaurantId=restaurant.Restaurant_Id
    #calculating no. of booked tables on a particular date of particular table_type in a restaurant
    booking_couple=Booking.query.filter(Booking.Booking_Date==booking_date,Booking.Restaurant_Id==restaurantId,Booking.Table_Type=='Couple').all()
    booking_booth=Booking.query.filter(Booking.Booking_Date==booking_date,Booking.Restaurant_Id==restaurantId,Booking.Table_Type=='Booth').all()
    booking_family=Booking.query.filter(Booking.Booking_Date==booking_date,Booking.Restaurant_Id==restaurantId,Booking.Table_Type=='Family').all()
    tables_available= "Booth Tables:" + str(restaurant.Booth-len(booking_booth)) +'\n Couple Tables:' +str(restaurant.Couple-len(booking_couple)) +'\n Famile Tables:'+str(restaurant.Family-len(booking_family))
    return tables_available

#api to book a table
@app.route('/api/booking',methods=['POST'])
def book_a_table():
    username=request.json.get('username')
    restaurant_name=request.json.get('restaurant')
    table_type=request.json.get('table_type')
    booking_date=request.json.get('booking_date')
    user = User.query.filter_by(username=username).first()
    restaurant = Restaurant.query.filter_by(Restaurant_Name=restaurant_name).first()

    #cheching if input is received or not
    if username is None or restaurant_name is None or table_type is None or booking_date is None or user is None or restaurant is None:
        return "Some Value is missing or invalid"
      
    try:
        #checking if table is available on that day or not
        if (getattr(restaurant,table_type)-len(Booking.query.filter(Booking.Booking_Date==booking_date,Booking.Restaurant_Id==restaurant.Restaurant_Id,Booking.Table_Type==table_type).all()))==0:
            return "Table is not available"
    except:
        return "Invalid table name"
         
    #creating a object for booking table
    booking=Booking(User_Id=user.User_Id,Restaurant_Id=restaurant.Restaurant_Id,Table_Type=table_type,Booking_Date=booking_date)

    #adding new record and commiting it.
    db.session.add(booking)
    db.session.commit()
    return "Booking Confirmed"
if __name__ == "__main__":
    app.run(port=5001, debug=True)