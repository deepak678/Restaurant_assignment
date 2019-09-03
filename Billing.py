from app import app,db
from tables import Item,Booking,Transaction,Restaurant,User
from flask import request       
import smtplib

@app.route('/api/GetBill',methods=['POST'])
def generateBill():
    restaurant_name=request.json.get('restaurant_name')
    username=request.json.get('username')
    items=request.json.get('items')
    emailId=request.json.get('emailId')
    restaurant = Restaurant.query.filter_by(Restaurant_Name=restaurant_name).first()
    user = User.query.filter_by(username=username).first()
    Total_amount=restaurant.Base_Table_Charges
    item_details=""
    #calculating amount for all iteams and their names
    for item in items:
        item_data=Item.query.filter(Item.Item_Name==item,Item.Restaurant_Id==restaurant.Restaurant_Id).first()
        item_details=item_details + str(item_data.Item_Name) + ":" + str(item_data.Price) + "\n"
        Total_amount=Total_amount + item_data.Price
    
    transaction=Transaction(User_Id=user.User_Id,Restaurant_Id=restaurant.Restaurant_Id,Total=Total_amount)
    #updating booking table
    book_confirm=Booking.query.filter_by(User_Id=user.User_Id).order_by(Booking.Booking_Id.desc()).first()
    book_confirm.Booking_status=1
    db.session.commit()
    db.session.add(transaction)
    db.session.commit()
    result="base table charges: " + str(restaurant.Base_Table_Charges)+ "\n" + item_details + "\n"+" amount to be paid is " + str(Total_amount)
    #SENDING EMAIL to the user about the bill
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    # start TLS for security 
    s.starttls() 
    # Authentication 
    s.login("tstdpk@gmail.com", "mindtree@12") 
    # message to be sent 
    message = result
    # sending the mail 
    s.sendmail("tstdpk@gmail.com", emailId, message) 
    # terminating the session 
    s.quit()
    return result


if __name__ == "__main__":
    app.run(port=5004, debug=True)