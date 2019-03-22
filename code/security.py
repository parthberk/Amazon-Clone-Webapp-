
from user import User

"""
users=[
    User(1,"Parth","qwerty")
]

username_mapping={u.username: u for u in users}
userid_mapping={u.id: u for u in users}
"""


def authentication(username,password):
    #user=username_mapping.get(username,None)
    user=User.find_username(username)
    if user and user.password == password:
        return user

def identity(payload):
    user_id=payload['identity']
    #return userid_mapping.get(user_id,None)
    return User.find_id(user_id)
