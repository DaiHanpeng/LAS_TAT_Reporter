from sqlalchemy import Column,Integer,Sequence, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer,Sequence('user_seq'),primary_key=True)
  username   = Column(String(50),unique=True)
  fullname = Column(String(150))
  password  = Column(String(50))
  def __init__(self,name,fullname,password):
    self.name = name
    self.fullname = fullname
    self.password = password