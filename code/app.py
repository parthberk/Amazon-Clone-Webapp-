from flask import Flask,jsonify
from security import authentication,identity
from user import RegisterUser
from item import Item,ItemList
from flask_jwt import JWT,jwt_required
from flask_restful import Api


app=Flask(__name__)
app.secret_key="parth"
api=Api(app)

jwt=JWT(app,authentication,identity)  
api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(RegisterUser,'/register')

app.run(port=5000,debug=True)
