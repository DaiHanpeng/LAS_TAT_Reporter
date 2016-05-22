
from sqlalchemy.sql import select
from sqlalchemy.sql import and_

from Tables import *




#inserting
''''
# create an Insert object
ins = users_table.insert()
# add values to the Insert object
new_user = ins.values(name="Joe", age=20, password="pass")

# create a database connection
conn = engine.connect()
# add user to database by executing SQL
conn.execute(new_user)
'''


'''
# a connectionless way to Insert a user
ins = users_table.insert()
result = engine.execute(ins, name="Shinji", age=15, password="nihongo")

# another connectionless Insert
result = users_table.insert().execute(name="Martha", age=45, password="dingbat")
'''

'''
# create a database connection
conn = engine.connect()

conn.execute(users_table.insert(), [
    {"name": "Ted", "age":10, "password":"dink"},
    {"name": "Asahina", "age":25, "password":"nippon"},
    {"name": "Evan", "age":40, "password":"macaca"}
])
'''

#quering

'''
s = select([users_table])
result = s.execute()

for row in result:
    print row

# The following is the equivalent to
# SELECT * FROM users WHERE id > 3
s = select([users_table], users_table.c.id > 3)

# You can use the "and_" module to AND multiple fields together
s = select(and_(users_table.c.name=="Martha", users_table.c.age < 25))
'''

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

mike_user = User("mike", "Mike Driscoll", "password")
session.add(mike_user)

session.add_all([
     User('Mary', 'Mary Wonka', 'foobar'),
     User('Sue', 'Sue Lawhead', 'xxg527'),
     User('Fay', 'Fay Ray', 'blah')])

session.commit()

# do a Select all
all_users = session.query(User).all()

# Select just one user by the name of "mike"
our_user = session.query(User).filter_by(name='mike').first()
print our_user

# select users that match "Mary" or "Fay"
users = session.query(User).filter(User.name.in_(['Mary', 'Fay'])).all()
print users

# select all and print out all the results sorted by id
for instance in session.query(User).order_by(User.id):
    print instance.name, instance.fullname
