
'''
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table, ForeignKey
from sqlalchemy import Integer, String

engine = create_engine('sqlite:///tutorial.db',
                       echo=True)

metadata = MetaData(bind=engine)

users_table = Table('users', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('name', String(40)),
                    Column('age', Integer),
                    Column('password', String),
                    )

addresses_table = Table('addresses', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('user_id', None, ForeignKey('users.id')),
                        Column('email_address', String, nullable=False)
                        )

# create tables in database
metadata.create_all()
'''


from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, mapper, relation, sessionmaker

Base = declarative_base()

########################################################################
class User(Base):
    """"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    #----------------------------------------------------------------------
    def __init__(self, name, fullname, password):
        """Constructor"""
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)

########################################################################
class Address(Base):
    """
    Address Class

    Create some class properties before initilization
    """
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    # creates a bidirectional relationship
    # from Address to User it's Many-to-One
    # from User to Address it's One-to-Many
    user = relation(User, backref=backref('addresses', order_by=id))

    #----------------------------------------------------------------------
    def __init__(self, email_address):
        """Constructor"""
        self.email_address = email_address

    def __repr__(self):
        return "<Address('%s')>" % self.email_address


# create a connection to a sqlite database
# turn echo on to see the auto-generated SQL
engine = create_engine("sqlite:///tutorial.db", echo=True)

# get a handle on the table object
users_table = User.__table__
# get a handle on the metadata
metadata = Base.metadata
metadata.create_all(engine)