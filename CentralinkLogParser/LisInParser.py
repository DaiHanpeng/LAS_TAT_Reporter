from datetime import *

from FilesFilter.FilesFilter import FilesFilter

from DBInterface.TAT_Interface import TAT_Interface,TAT_Update_Timestamp_Interface

TABLE_UPDATE_TIMESTAMP_ID = r'LIS_In'

class LisInParser():
    """
    lis in log info parser.
    """
    def __init__(self):
        self.last_file_modified_timestamp = 0   #last checked file modified time
        self.last_updated_record_timestamp = '' #timestamp of the last updated record.

        timestamp_table_interface = TAT_Update_Timestamp_Interface()
        self.last_file_modified_timestamp = timestamp_table_interface.get_log_file_last_update_timestamp(TABLE_UPDATE_TIMESTAMP_ID)
        self.last_updated_record_timestamp = timestamp_table_interface.get_record_last_update_timestamp(TABLE_UPDATE_TIMESTAMP_ID)

        self.sample_order_map = {} # map sample id with its ordering timestamp

    def parse(self,log_file_list):
        self.sample_order_map = {}

        current_date_time = ''
        last_updated_record_timestamp = self.last_updated_record_timestamp

        if not log_file_list:
            print 'null log file list of Lis In'
            return

        #print log_file_list
        for item in log_file_list:
            file_content_list = []
            if isinstance(item,str):
                try:
                    lis_in_file_handler = open(item)
                    file_content_list = lis_in_file_handler.readlines()
                    file_content_list.reverse()
                except Exception as e:
                    print 'file read failed!'
                    print 'exception:',e
                finally:
                    lis_in_file_handler.close()

            if file_content_list:
                for line in file_content_list:
                    if isinstance(line,str):
                        if -1 <> line.find(r'*** INFO [IO-RDL]'):
                            current_date_time =  (' ').join(line.split()[-2:])[:-3]
                            #log_date_time = datetime.strptime(current_date_time,r'%Y-%m-%d %H:%M:%S')
                            if current_date_time < self.last_updated_record_timestamp:
                                print current_date_time
                                break
                        elif  -1 <> line.find(r'Rdl') and -1 <> line.find(r'O|1|'):#line.startswith(r'O|1|')
                            sample_id = line.split(r'|')[2]
                            if not self.sample_order_map.has_key(sample_id):
                                self.sample_order_map[sample_id] = current_date_time
                            elif self.sample_order_map[sample_id] > current_date_time:
                                self.sample_order_map[sample_id] = current_date_time
                if last_updated_record_timestamp < current_date_time:
                    last_updated_record_timestamp = current_date_time

        if last_updated_record_timestamp > self.last_updated_record_timestamp:
            self.last_updated_record_timestamp = last_updated_record_timestamp
            #update to db
            timestamp_table_interface = TAT_Update_Timestamp_Interface()
            timestamp_table_interface.set_record_last_update_timestamp(TABLE_UPDATE_TIMESTAMP_ID,self.last_updated_record_timestamp)


    def to_db(self):
        db_interface = TAT_Interface()
        db_interface.insert_sample_lis_order(self.sample_order_map)

    def pre_work(self,log_folder):
        #please keep this evaluate sequence...
        current_file_modified_timestamp = FilesFilter.get_latest_modified_timestamp(log_folder)
        log_file_list = FilesFilter.get_files_after_a_modified_timestamp(log_folder,self.last_file_modified_timestamp)
        if str(current_file_modified_timestamp) > str(self.last_file_modified_timestamp):
            self.last_file_modified_timestamp = current_file_modified_timestamp
            #update to db
            timestamp_table_interface = TAT_Update_Timestamp_Interface()
            timestamp_table_interface.set_log_file_last_update_timestamp(TABLE_UPDATE_TIMESTAMP_ID,self.last_file_modified_timestamp)

        return log_file_list

    def work(self,log_file_list):
        self.parse(log_file_list)
        self.to_db()

    def __repr__(self):
        return 'sample ordering timestamp:\n' +\
            '\n'.join(str(sample_id)+':'+str(self.sample_order_map[sample_id]) \
                      for sample_id in self.sample_order_map.keys() )

def test():
    #print 'O|1|5400555276||^^^LAC|R||2015122105241401||||N||||||||||||||||IP'.startswith(r'O|1|')
    lis_in_parser = LisInParser()
    lis_in_log_folder = r'D:\01_Automation\23_Experiential_Conclusions_2016\19_Anhui_Provicial_Hospital\Log\trl\LIS_Translator_in'
    lis_in_log_file_list = lis_in_parser.pre_work(lis_in_log_folder)
    lis_in_parser.work(lis_in_log_file_list)
    print lis_in_parser

if __name__ == '__main__':
    test()