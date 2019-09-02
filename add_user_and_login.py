from app import app,db
from tables import User
from flask import request,abort,jsonify,url_for

#to register a new user
@app.route('/api/users', methods = ['POST'])
def newUser():
    username = request.json.get('username')
    password = request.json.get('password')
    #checking validity of entered username
    if username is None or password is None:
        return "Username or password is Null" # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        return "Username exists"
    user = User(username = username)
    user.hashPassword(password) 
    #making changes in the Database
    db.session.add(user)
    db.session.commit()
    return "User Added Successfully"


#login and check username and password
@app.route('/api/login', methods = ['POST'])
def checkLoginDetails():
    username = request.json.get('username')
    password = request.json.get('password')
    #checking validity of entered username
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        user = User.query.filter_by(username=username).first()
        pass_entered=user.verifyPassword(password)
        if pass_entered==True:
            return "Login Successful"
        else:
            return "Wrong Password"
    else:
        return "user not found"

if __name__ == "__main__":
    app.run(port=5000, debug=True)

