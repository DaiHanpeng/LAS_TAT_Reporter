from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_,or_

from sqlalchemy import MetaData
from sqlalchemy import Table


from sqlalchemy import func, or_, not_

from Tables import BaseModel,Payload_Table


class Payload_Interface():
    """
    db interface for payload table.
    """
    def __init__(self):
        DB_CONNECT_STRING = 'mysql+mysqldb://root:root@localhost/tat'

        #DB_CONNECT_STRING = 'sqlite:///tutorial.db'
        self.engine = create_engine(DB_CONNECT_STRING,echo=False)
        DB_Session = sessionmaker(bind=self.engine)
        self.session = DB_Session()

        self.init_database()


    def init_database(self):
        #self.session.execute('use tat')

        self.init_tables()
        self.session.commit()

    def init_tables(self):
        BaseModel.metadata.create_all(self.engine)

    def add_new_record(self,sample_id,module_id,module_type,timestamp):
        self.session.add(Payload_Table(sample_id,module_id,module_type,timestamp))

    def add_new_records(self,payload_list):
        if isinstance(payload_list,list):
            for item in payload_list:
                if isinstance(item,Payload_Table):
                    self.add_new_record(item.sample_id,item.module_id,item.module_type,item.timestamp)
            self.write_to_db()

    def write_to_db(self):
        self.session.flush()
        self.session.commit()



