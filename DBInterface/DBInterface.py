from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_,or_

from sqlalchemy import MetaData
from sqlalchemy import Table


from sqlalchemy import func, or_, not_

from Tables import TAT_Table,BaseModel,TAT_Update_Timestamp_Table


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

        #self.session.execute('create database if not exists tat')
        self.session.execute('use tat')

        self.init_tables()
        self.session.commit()

    def init_tables(self):
        BaseModel.metadata.create_all(self.engine)

    def update_all_fields(self):
        #update inlab_cat
        self.session.execute(r"UPDATE tat.tat SET inlab_cat = 'morning'  WHERE HOUR(las_inlab) < 11")
        self.session.execute(r"UPDATE tat.tat SET inlab_cat = 'noon'  WHERE HOUR(las_inlab) >= 11 AND HOUR(las_inlab) < 14")
        self.session.execute(r"UPDATE tat.tat SET inlab_cat = 'afternoon'  WHERE HOUR(las_inlab) >= 14")
        #update TAT
        self.session.execute(r"UPDATE tat.tat SET TAT = TIMESTAMPDIFF(MINUTE,las_inlab,lis_upload) WHERE las_inlab is not NULL and lis_upload is not NULL")
        #update analyzer_type
        self.session.execute(r"UPDATE tat.tat SET analyzer_type = 'advia2400'  WHERE advia_result is not NULL And centaur_result is NULL")
        self.session.execute(r"UPDATE tat.tat SET analyzer_type = 'centaur'  WHERE advia_result is NULL And centaur_result is not NULL")
        self.session.execute(r"UPDATE tat.tat SET analyzer_type = 'both'  WHERE advia_result is not NULL And centaur_result is not NULL")

        #update CM_TAT
        self.session.execute(r'UPDATE tat.tat SET CM_TAT = TIMESTAMPDIFF(MINUTE,centrifuge_in,centrifuge_out) WHERE centrifuge_in is not NULL and centrifuge_out is not NULL')
        #update Chem_TAT
        self.session.execute(r'UPDATE tat.tat SET Chem_TAT = TIMESTAMPDIFF(MINUTE,advia_query,advia_result) WHERE advia_query is not NULL and advia_result is not NULL')
        #update Immu_TAT
        self.session.execute(r'UPDATE tat.tat SET Immu_TAT = TIMESTAMPDIFF(MINUTE,centaur_query,centaur_result) WHERE centaur_query is not NULL and centaur_result is not NULL')
        #update Track_TAT
        self.session.execute(r'UPDATE tat.tat SET Track_TAT = TIMESTAMPDIFF(MINUTE,las_inlab,store) WHERE las_inlab is not NULL and store is not NULL')

        self.session.commit()

    def insert_sample_lis_order(self,sample_order_map):
        if isinstance(sample_order_map,dict):
            for sample_id in sample_order_map.keys():
                self.touch_new_sample_record(sample_id)

                #print sample_id
                query = self.session.query(TAT_Table)
                condition = and_((TAT_Table.sample_id == sample_id),or_((TAT_Table.lis_order < sample_order_map[sample_id]),(TAT_Table.lis_order == None)))
                query.filter(condition).update({TAT_Table.lis_order:sample_order_map[sample_id]})

            self.session.commit()

    def insert_sample_inlab(self,sample_inlab_map):
        if isinstance(sample_inlab_map,dict):
            for sample_id in sample_inlab_map.keys():
                self.touch_new_sample_record(sample_id)

                #print sample_id
                query = self.session.query(TAT_Table)
                condition = and_((TAT_Table.sample_id == sample_id),or_((TAT_Table.las_inlab < sample_inlab_map[sample_id]),(TAT_Table.las_inlab == None)))
                query.filter(condition).update({TAT_Table.las_inlab:sample_inlab_map[sample_id]})

            self.session.commit()


    def insert_sample_centrifuge_in(self,sample_centrifuge_in_map):
        if isinstance(sample_centrifuge_in_map,dict):
            for sample_id in sample_centrifuge_in_map.keys():
                self.touch_new_sample_record(sample_id)

                #print sample_id
                query = self.session.query(TAT_Table)
                condition = and_((TAT_Table.sample_id == sample_id),or_((TAT_Table.centrifuge_in < sample_centrifuge_in_map[sample_id]),(TAT_Table.centrifuge_in == None)))
                query.filter(condition).update({TAT_Table.centrifuge_in:sample_centrifuge_in_map[sample_id]})

            self.session.commit()

    def insert_sample_centrifuge_out(self,sample_centrifuge_out_map):
        if isinstance(sample_centrifuge_out_map,dict):
            for sample_id in sample_centrifuge_out_map.keys():
                self.touch_new_sample_record(sample_id)

                #print sample_id
                query = self.session.query(TAT_Table)
                condition = and_((TAT_Table.sample_id == sample_id),or_((TAT_Table.centrifuge_out < sample_centrifuge_out_map[sample_id]),(TAT_Table.centrifuge_out == None)))
                query.filter(condition).update({TAT_Table.centrifuge_out:sample_centrifuge_out_map[sample_id]})

            self.session.commit()

    def insert_sample_decap(self,sample_decap_map):
        if isinstance(sample_decap_map,dict):
            for sample_id in sample_decap_map.keys():
                self.touch_new_sample_record(sample_id)

                #print sample_id
                query = self.session.query(TAT_Table)
                condition = and_((TAT_Table.sample_id == sample_id),or_((TAT_Table.decap < sample_decap_map[sample_id]),(TAT_Table.decap == None)))
                query.filter(condition).update({TAT_Table.decap:sample_decap_map[sample_id]})

            self.session.commit()

    def insert_advia_query(self,advia_query_map):
        if isinstance(advia_query_map,dict):
            for sample_id in advia_query_map.keys():
                self.touch_new_sample_record(sample_id)

                #print sample_id
                query = self.session.query(TAT_Table)
                condition = and_((TAT_Table.sample_id == sample_id),or_((TAT_Table.advia_query < advia_query_map[sample_id]),(TAT_Table.advia_query == None)))
                query.filter(condition).update({TAT_Table.advia_query:advia_query_map[sample_id]})

            self.session.commit()

    def insert_advia_result(self,advia_result_map):
        if isinstance(advia_result_map,dict):
            for sample_id in advia_result_map.keys():
                self.touch_new_sample_record(sample_id)

                #print sample_id
                query = self.session.query(TAT_Table)
                condition = and_((TAT_Table.sample_id == sample_id),or_((TAT_Table.advia_result < advia_result_map[sample_id]),(TAT_Table.advia_result == None)))
                query.filter(condition).update({TAT_Table.advia_result:advia_result_map[sample_id]})

            self.session.commit()

    def insert_centaut_query(self,centaur_query_map):
        if isinstance(centaur_query_map,dict):
            for sample_id in centaur_query_map.keys():
                self.touch_new_sample_record(sample_id)

                #print sample_id
                query = self.session.query(TAT_Table)
                condition = and_((TAT_Table.sample_id == sample_id),or_((TAT_Table.centaur_query < centaur_query_map[sample_id]),(TAT_Table.centaur_query == None)))
                query.filter(condition).update({TAT_Table.centaur_query:centaur_query_map[sample_id]})

            self.session.commit()

    def insert_centaur_result(self,centaur_result_map):
        if isinstance(centaur_result_map,dict):
            for sample_id in centaur_result_map.keys():
                self.touch_new_sample_record(sample_id)

                #print sample_id
                query = self.session.query(TAT_Table)
                condition = and_((TAT_Table.sample_id == sample_id),or_((TAT_Table.centaur_result < centaur_result_map[sample_id]),(TAT_Table.centaur_result == None)))
                query.filter(condition).update({TAT_Table.centaur_result:centaur_result_map[sample_id]})

            self.session.commit()

    def insert_sample_seal(self,sample_seal_map):
        if isinstance(sample_seal_map,dict):
            for sample_id in sample_seal_map.keys():
                self.touch_new_sample_record(sample_id)

                #print sample_id
                query = self.session.query(TAT_Table)
                condition = and_((TAT_Table.sample_id == sample_id),or_((TAT_Table.seal < sample_seal_map[sample_id]),(TAT_Table.seal == None)))
                query.filter(condition).update({TAT_Table.seal:sample_seal_map[sample_id]})

            self.session.commit()

    def insert_sample_store(self,sample_store_map):
        if isinstance(sample_store_map,dict):
            for sample_id in sample_store_map.keys():
                self.touch_new_sample_record(sample_id)

                #print sample_id
                query = self.session.query(TAT_Table)
                condition = and_((TAT_Table.sample_id == sample_id),or_((TAT_Table.store < sample_store_map[sample_id]),(TAT_Table.store == None)))
                query.filter(condition).update({TAT_Table.store:sample_store_map[sample_id]})

            self.session.commit()

    def  insert_lis_result(self,lis_result_map):
        if isinstance(lis_result_map,dict):
            for sample_id in lis_result_map.keys():
                self.touch_new_sample_record(sample_id)

                #print sample_id
                query = self.session.query(TAT_Table)
                condition = and_((TAT_Table.sample_id == sample_id),or_((TAT_Table.lis_upload < lis_result_map[sample_id]),(TAT_Table.lis_upload == None)))
                query.filter(condition).update({TAT_Table.lis_upload:lis_result_map[sample_id]})

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
                self.session.commit()
                self.session.flush()
                #self.session.commit()


class DBInterface_TAT_Update_Timestamp():
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
        #self.session.execute('use tat')

        self.init_tables()
        self.session.commit()

    def init_tables(self):
        BaseModel.metadata.create_all(self.engine)

    def get_log_file_last_update_timestamp(self,type_id):
        if isinstance(type_id,str):
            self.touch_new_record(type_id)
            for last_file_update_timestamp, in self.session.query(TAT_Update_Timestamp_Table.last_file_update_timestamp).filter_by(type_id=type_id):
                print 'type id: ', type_id, '; get last file updated timestamp: ', last_file_update_timestamp
                return last_file_update_timestamp

    def set_log_file_last_update_timestamp(self,type_id,timestamp):
        if isinstance(type_id,str):
            query = self.session.query(TAT_Update_Timestamp_Table)
            query.filter(TAT_Update_Timestamp_Table.type_id == type_id).update({TAT_Update_Timestamp_Table.last_file_update_timestamp:str(timestamp)})
            self.session.commit()
            print 'type id = ', type_id, '; last_file_update_timestamp set to => ', timestamp

    def get_record_last_update_timestamp(self,type_id):
        if isinstance(type_id,str):
            self.touch_new_record(type_id)
            for last_record_update_timestamp, in self.session.query(TAT_Update_Timestamp_Table.last_record_update_timestamp).filter_by(type_id=type_id):
                print 'type id: ', type_id, '; get last record updated timestamp: ', last_record_update_timestamp
                return last_record_update_timestamp

    def set_record_last_update_timestamp(self,type_id,timestamp):
        if isinstance(type_id,str):
            query = self.session.query(TAT_Update_Timestamp_Table)
            query.filter(TAT_Update_Timestamp_Table.type_id == type_id).update({TAT_Update_Timestamp_Table.last_record_update_timestamp:str(timestamp)})
            self.session.commit()
            print 'type id = ', type_id, 'last_record_update_timestamp set to => ', timestamp

    def touch_new_record(self,type_id):
        if isinstance(type_id,str):
            if len(type_id) > 16:
                type_id = type_id[:16]
            if not self.check_if_record_exist(type_id):
                self.session.add(TAT_Update_Timestamp_Table(type_id=type_id))
                self.session.commit()
                self.session.flush()
                print 'new record created in Timestamp table, id = ', type_id

    def check_if_record_exist(self,type_id):
        if isinstance(type_id,str):
            query = self.session.query(TAT_Update_Timestamp_Table)

            if query.get(type_id):
                return True
            else:
                return False


def test():

    db_interface = DBInterface()
    '''
    lis_order_map = {'1411042707':'2014-11-04 11:52:10',\
                    '1411130109':'2014-11-13 09:42:44',\
                    '9908014671':'2014-11-13 09:43:59',\
                    '1411120665':'2014-11-12 10:00:23'}

    db_interface.insert_sample_lis_order(lis_order_map)
    '''
    db_interface.update_all_fields()

def test2():
    interface = DBInterface_TAT_Update_Timestamp()
    #interface.check_if_record_exist(r'helll')
    #interface.check_if_record_exist(r'Advia2400')

    #interface.get_log_file_last_update_timestamp(r'Advia2400')
    #interface.get_record_last_update_timestamp(r'Advia2400')
    id = r'las_out'
    value = r'1988-09-02 12:34:56'

    interface.get_log_file_last_update_timestamp(id)
    #interface.set_log_file_last_update_timestamp(id,value)
    #interface.get_log_file_last_update_timestamp(id)

if __name__ == '__main__':
    test2()
