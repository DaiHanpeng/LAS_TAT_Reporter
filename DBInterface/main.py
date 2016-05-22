from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from user import User,Base
from sqlalchemy.ext.declarative import declarative_base
#Base = declarative_base()

if __name__ == '__main__':
  engine = create_engine('mysql://root:root@127.0.0.1:3306/test',echo=True)
  Base.metadata.create_all(engine, checkfirst=True)
  Session = sessionmaker(bind=engine)
  session = Session()
  ed_user = User('ed', 'Ed Jones', 'edspassword')
  session.add(ed_user)

  session.commit()