#To make this class to be able to interact with DB. 
import sqlite3
from flask_restful import Resource,Api,reqparse
class User:
    def __init__(self, uid,username,password):
        self.id=uid
        self.username=username
        self.password=password
    @classmethod
    def find_username(cls,username):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()

        query="SELECT * FROM users where username=?"
        #paramters always have to be in the form of a tuple.
        result=cursor.execute(query,(username,))
        row=result.fetchone()
        if row:
            user=cls(row[0],row[1],row[2])
            #user=cls(*row)  These both are same things
        else:
            user=None
        connection.close()

        return user 

    
    @classmethod
    def find_id(cls,uid):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()
        query="SELECT * FROM users where id=?"
        #paramters always have to be in the form of a tuple.
        result=cursor.execute(query,(uid,))
        row=result.fetchone()
        if row:
            user=cls(row[0],row[1],row[2])
            #user=cls(*row)  These both are same things
        else:
            user=None
        connection.close()

        return user 


class RegisterUser(Resource):

    parser=reqparse.RequestParser() # It can also be used to parse the html form and validate them.
    parser.add_argument('username',
        type=str,
        required=True,
        help="Username can not be left blank!")
    parser.add_argument('password',
    required=True,
    type=str,
    help="Password can not be left blank!"
    )
    def post(self):
        data=RegisterUser.parser.parse_args()

        # To check whether the user already exists.
        if User.find_username(data['username']):
            return {"message": "{} already exists.".format(data['username'])}


        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()

        query="INSERT INTO users values(NULL,?,?)"
        
        cursor.execute(query,(data['username'],data['password']))

        connection.commit()
        connection.close()

        return {"message": "User Created Successfully"},201