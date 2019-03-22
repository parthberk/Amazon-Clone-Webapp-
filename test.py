import sqlite3

connection=sqlite3.connect('data.db')


#Required to run the commands
cursor=connection.cursor()

create_table= "CREATE TABLE users(id int, username text,password text)"

cursor.execute(create_table)
"""
user=(1,'parth','asdf')
cursor.execute(insert_query,user)
"""
insert_query="INSERT INTO users values(?,?,?)"
users=[
    (1,'parth','asdf'),
    (2,'smit','abc'),
    (3,"peru","cde")
]

cursor.executemany(insert_query,users)

select_query="SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

#To save the data onto the disk
connection.commit()

# To close the database connection
connection.close()
