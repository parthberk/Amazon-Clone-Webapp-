from flask import Flask,jsonify,request
from flask_restful import Resource,Api,reqparse

from flask_jwt import JWT,jwt_required

from security import authentication,identity


from user import RegisterUser


app=Flask(__name__)
app.secret_key="parth"
api=Api(app)

jwt=JWT(app,authentication,identity)  

items=[]


class Item(Resource):
    parser=reqparse.RequestParser() # It can also be used to parse the html form and validate them.
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field can not be left blank!"
        )

    @jwt_required()
    def get(self,name):
        item=next(filter(lambda x: x['name']==name,items),None)
        return {'item':item},200 if item else 404

    @jwt_required()
    def post(self,name):
        if next(filter(lambda x:x['name']==name,items),None):
            return {'message':"An item with name {} already exists.".format(name)},400

        data=Item.parser.parse_args()
        
        item= {'name':name,'price':data['price']}
        items.append(item)
        return item,201

    def delete(self,name):
        global items
        items=list(filter(lambda x: x['name']!=name,items))
        return {"message":"{} is deleted.".format(name)}

    def put(self,name):
        data=Item.parser.parse_args()
        item = next(filter(lambda x: x['name']==name,items),None)
        if item:
            item.update(data)
        else:
            item={'name':name,'price':data['price']}
            items.append(item)
        return item


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {"items":items}
     

api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(RegisterUser,'/register')

app.run(port=5000,debug=True)
