from flask_restful import Resource,reqparse
from flask import request
from flask_jwt import JWT,jwt_required
import sqlite3

class Item(Resource):
    parser=reqparse.RequestParser() # It can also be used to parse the html form and validate them.
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field can not be left blank!"
        )

    @jwt_required()
    def get(self,name):
        #Following lines were used for in-memory database.
        """
        item=next(filter(lambda x: x['name']==name,items),None)
        return {'item':item},200 if item else 404
        """
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()
        query="SELECT * FROM items where name=?"
        connection.close() 
        # connection.commit() is not needed because we're just retrieving the data. No Edit/Delete/Add is done.
        result=cursor.execute(query,(name,))
        row=result.fetchone()
        if row:
            return {
                'item':{
                    'name':row[0],
                    'price':row[1]
                }
            }
        return {
            "message":"{} not found.".format(name)
        },404


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