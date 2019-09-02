from app import app,db
from flask import request
from tables import Restaurant,Item

@app.route('/api/additem',methods=['POST'])
def addItem():
    restaurant_name=request.json.get('restaurant_name')
    item_name=request.json.get('item_name')
    price=request.json.get('price')
    restaurant = Restaurant.query.filter_by(Restaurant_Name=restaurant_name).first()

    item=Item(Restaurant_Id=restaurant.Restaurant_Id,Item_Name=item_name,Price=price)
    db.session.add(item)
    db.session.commit()
    return "Item added" 

if __name__ == "__main__":
    app.run(port=5003, debug=True)