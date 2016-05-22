from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import MetaData
from sqlalchemy import Table


from sqlalchemy import func, or_, not_

from Tables import TAT_Table,BaseModel


class DBInterface():
    """
    db interface for sql.
    """
    def __init__(self):
        DB_CONNECT_STRING = 'mysql+mysqldb://root:root@localhost/tat'

        #DB_CONNECT_STRING = 'sqlite:///tutorial.db'
        self.engine = create_engine(DB_CONNECT_STRING,echo=False)
        DB_Session = sessionmaker(bind=self.engine)
        self.session = DB_Session()

        self.init_database()


    def init_database(self):

        self.session.execute('create database if not exists tat')
        self.session.execute('use tat')

        self.init_tables()
        self.session.commit()

    def init_tables(self):
        BaseModel.metadata.create_all(self.engine)


    def insert_sample_lis_order(self,sample_order_map):
        if isinstance(sample_order_map,dict):
            for sample_id in sample_order_map.keys():
                self.touch_new_sample_record(sample_id)

                #print sample_id
                query = self.session.query(TAT_Table)

                query.filter(TAT_Table.sample_id == sample_id).update({TAT_Table.lis_order:sample_order_map[sample_id]})

            self.session.commit()

    def insert_sample_inlab(self,sample_inlab_map):
        if isinstance(sample_inlab_map,dict):
            for sample_id in sample_inlab_map.keys():
                self.touch_new_sample_record(sample_id)

                #print sample_id
                query = self.session.query(TAT_Table)

                query.filter(TAT_Table.sample_id == sample_id).update({TAT_Table.las_inlab:sample_inlab_map[sample_id]})

            self.session.commit()

    def insert_advia_query(self,advia_query_map):
        if isinstance(advia_query_map,dict):
            for sample_id in advia_query_map.keys():
                self.touch_new_sample_record(sample_id)

                #print sample_id
                query = self.session.query(TAT_Table)

                query.filter(TAT_Table.sample_id == sample_id).update({TAT_Table.advia_query:advia_query_map[sample_id]})

            self.session.commit()

    def insert_advia_result(self,advia_result_map):
        if isinstance(advia_result_map,dict):
            for sample_id in advia_result_map.keys():
                self.touch_new_sample_record(sample_id)

                #print sample_id
                query = self.session.query(TAT_Table)

                query.filter(TAT_Table.sample_id == sample_id).update({TAT_Table.advia_result:advia_result_map[sample_id]})

            self.session.commit()

    def insert_centaut_query(self,centaur_query_map):
        if isinstance(centaur_query_map,dict):
            for sample_id in centaur_query_map.keys():
                self.touch_new_sample_record(sample_id)

                #print sample_id
                query = self.session.query(TAT_Table)

                query.filter(TAT_Table.sample_id == sample_id).update({TAT_Table.centaur_query:centaur_query_map[sample_id]})

            self.session.commit()

    def insert_centaur_result(self,centaur_result_map):
        if isinstance(centaur_result_map,dict):
            for sample_id in centaur_result_map.keys():
                self.touch_new_sample_record(sample_id)

                #print sample_id
                query = self.session.query(TAT_Table)

                query.filter(TAT_Table.sample_id == sample_id).update({TAT_Table.centaur_result:centaur_result_map[sample_id]})

            self.session.commit()

    def  insert_lis_result(self,lis_result_map):
        if isinstance(lis_result_map,dict):
            for sample_id in lis_result_map.keys():
                self.touch_new_sample_record(sample_id)

                #print sample_id
                query = self.session.query(TAT_Table)

                query.filter(TAT_Table.sample_id == sample_id).update({TAT_Table.lis_upload:lis_result_map[sample_id]})

            self.session.commit()


    def check_if_sample_record_exist(self,sample_id):
        if isinstance(sample_id,str):
            query = self.session.query(TAT_Table)
            #print query.get(sample_id)#access by primay key.
            #print query.filter(TAT_Table.sample_id == sample_id)
            if query.get(sample_id):
                return True
            else:
                return False

    def touch_new_sample_record(self,sample_id):
        if isinstance(sample_id,str):
            if len(sample_id) > 40:
                sample_id = sample_id[:41]
            if not self.check_if_sample_record_exist(sample_id):
                self.session.add(TAT_Table(sample_id=sample_id))
                self.session.flush()
                #self.session.commit()

def test():

    db_interface = DBInterface()
    lis_order_map = {'1411042707':'2014-11-04 11:52:10',\
                    '1411130109':'2014-11-13 09:42:44',\
                    '9908014671':'2014-11-13 09:43:59',\
                    '1411120665':'2014-11-12 10:00:23'}

    db_interface.insert_sample_lis_order(lis_order_map)

if __name__ == '__main__':
    test()
