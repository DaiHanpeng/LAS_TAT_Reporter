from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Tables import BaseModel,Exception_Table


class Exception_Interface():
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

    def add_new_record(self,timestamp,module_id,module_type,sample_id,err_code):
        self.session.add(Exception_Table(timestamp,module_id,module_type,sample_id,err_code))

    def add_new_records(self,err_list):
        if isinstance(err_list,list):
            for item in err_list:
                if isinstance(item,Exception_Table):
                    self.add_new_record(item.timestamp,item.module_id,item.module_type,item.sample_id,item.err_code)
            self.write_to_db()

    def write_to_db(self):
        self.session.flush()
        self.session.commit()



