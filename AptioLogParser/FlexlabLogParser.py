from datetime import *
import zipfile
from zipfile import ZipFile
import os

from FilesFilter.FilesFilter import FilesFilter
from DBInterface.Tables import Payload_Table
from DBInterface.TAT_Interface import TAT_Interface,TAT_Update_Timestamp_Interface
from DBInterface.Payload_Interface import Payload_Interface

TABLE_UPDATE_TIMESTAMP_ID = r'Flaxlab'

class FlexlabControlParser():
    """
    advia 2400 log info parser
    """
    def __init__(self):
        self.last_file_modified_timestamp = 0   #last checked file modified time
        self.last_updated_record_timestamp = '' #timestamp of the last updated record.

        timestamp_table_interface = TAT_Update_Timestamp_Interface()
        self.last_file_modified_timestamp = timestamp_table_interface.get_log_file_last_update_timestamp(TABLE_UPDATE_TIMESTAMP_ID)
        self.last_updated_record_timestamp = timestamp_table_interface.get_record_last_update_timestamp(TABLE_UPDATE_TIMESTAMP_ID)

        self.centrifuge_in_map = {}
        self.centrifuge_out_map = {}
        self.decap_map = {}
        self.seal_map = {}
        self.store_map = {}

        self.payload_list = list()

    def parse(self,log_file_list):
        self.centrifuge_in_map = {}
        self.centrifuge_out_map = {}
        self.decap_map = {}
        self.seal_map = {}
        self.store_map = {}

        self.payload_list = []

        current_date_time = ''
        last_updated_record_timestamp = self.last_updated_record_timestamp

        if not log_file_list:
            print 'null log file list of Aptio Control'
            return

        #print log_file_list
        for item in log_file_list:
            file_content_list = []
            if isinstance(item,str) and os.path.isfile(item):
                if not zipfile.is_zipfile(item):
                    try:
                        flexlab_file_handler = open(item)
                        file_content_list = flexlab_file_handler.readlines()
                        file_content_list.reverse()
                    except Exception as e:
                        print 'file read failed!'
                        print 'exception:',e
                    finally:
                        flexlab_file_handler.close()
                else:
                    with ZipFile(item, 'r') as open_zip_file:
                        #print open_zip_file.namelist()
                        file_list = open_zip_file.namelist()
                        for log_file in file_list:
                            if isinstance(log_file,str):
                                if log_file.startswith(r'CONTROL'):
                                    with open_zip_file.open(log_file) as opened_control_log_file:
                                        file_content_list += opened_control_log_file.readlines()

            if file_content_list:
                for line in file_content_list:
                    if isinstance(line,str):
                        #parsing information for TAT statistic.
                        if -1 <> line.find(r' CM ADD ') and -1 <> line.find(r'timestamp='):
                            current_date_time = line.split(r'timestamp="')[1].split(r'"')[0]
                            if current_date_time >= self.last_updated_record_timestamp:
                                sample_id = line.split(r' CM ADD ')[1].split(r'|')[1]
                                if sample_id:
                                    if not self.centrifuge_in_map.has_key(sample_id):
                                        self.centrifuge_in_map[sample_id] = current_date_time
                                    elif self.centrifuge_in_map[sample_id] < current_date_time:
                                        self.centrifuge_in_map[sample_id] = current_date_time
                        elif -1 <> line.find(r' CM RETURNED ') and -1 <> line.find(r'timestamp='):
                            current_date_time = line.split(r'timestamp="')[1].split(r'"')[0]
                            if current_date_time >= self.last_updated_record_timestamp:
                                sample_id = line.split(r' CM RETURNED ')[1].split(r'^')[1]
                                if sample_id:
                                    if not self.centrifuge_out_map.has_key(sample_id):
                                        self.centrifuge_out_map[sample_id] = current_date_time
                                    elif self.centrifuge_out_map[sample_id] < current_date_time:
                                        self.centrifuge_out_map[sample_id] = current_date_time
                        elif -1 <> line.find(r' DCM RETURNED ') and -1 <> line.find(r'timestamp='):
                            current_date_time = line.split(r'timestamp="')[1].split(r'"')[0]
                            if current_date_time >= self.last_updated_record_timestamp:
                                sample_id = line.split(r' DCM RETURNED ')[1].split(r'^')[1]
                                if sample_id:
                                    if not self.decap_map.has_key(sample_id):
                                        self.decap_map[sample_id] = current_date_time
                                    elif self.decap_map[sample_id] < current_date_time:
                                        self.decap_map[sample_id] = current_date_time
                        elif -1 <> line.find(r' SM RETURNED ') and -1 <> line.find(r'timestamp='):
                            current_date_time = line.split(r'timestamp="')[1].split(r'"')[0]
                            if current_date_time >= self.last_updated_record_timestamp:
                                sample_id = line.split(r' SM RETURNED ')[1].split(r'^')[1]
                                if sample_id:
                                    if not self.seal_map.has_key(sample_id):
                                        self.seal_map[sample_id] = current_date_time
                                    elif self.seal_map[sample_id] < current_date_time:
                                        self.seal_map[sample_id] = current_date_time
                        #<SRM SAMPLE-LOCATION ^> as storage time stamp
                        elif -1 <> line.find(r' SAMPLE-LOCATION ^') and -1 <> line.find(r'timestamp='):
                            current_date_time = line.split(r'timestamp="')[1].split(r'"')[0]
                            if current_date_time >= self.last_updated_record_timestamp:
                                sample_id = line.split(r' SAMPLE-LOCATION ^')[1].split(r'^')[0]
                                if sample_id:
                                    if not self.store_map.has_key(sample_id):
                                        self.store_map[sample_id] = current_date_time
                                    elif self.store_map[sample_id] < current_date_time:
                                        self.store_map[sample_id] = current_date_time

                        #payload parsing.
                        if isinstance(line,str):
                            if -1 <> line.find(r' RETURNED ') and -1 <> line.find(r'timestamp='):
                                payload_timestamp = line.split(r'timestamp="')[1].split(r'"')[0]
                                payload_module_id = line.split(r'message="')[1].split()[0]
                                payload_module_type = line.split(r'message=')[1].split()[1]
                                payload_sample_id = line.split(r' RETURNED ')[1].split(r'^')[1]
                                if payload_sample_id:
                                    self.payload_list.append(Payload_Table(payload_sample_id,payload_module_id,payload_module_type,payload_timestamp))

                if last_updated_record_timestamp < current_date_time:
                    last_updated_record_timestamp = current_date_time

        if last_updated_record_timestamp > self.last_updated_record_timestamp:
            self.last_updated_record_timestamp = last_updated_record_timestamp
            #update to db
            timestamp_table_interface = TAT_Update_Timestamp_Interface()
            timestamp_table_interface.set_record_last_update_timestamp(TABLE_UPDATE_TIMESTAMP_ID,self.last_updated_record_timestamp)

    def to_db(self):
        db_interface = TAT_Interface()
        db_interface.insert_sample_centrifuge_in(self.centrifuge_in_map)
        db_interface.insert_sample_centrifuge_out(self.centrifuge_out_map)
        db_interface.insert_sample_decap(self.decap_map)
        db_interface.insert_sample_seal(self.seal_map)
        db_interface.insert_sample_store(self.store_map)

        db_payload_interrface = Payload_Interface()
        db_payload_interrface.add_new_records(self.payload_list)

    def pre_work(self,log_folder):
        #please keep this evaluate sequence...
        current_file_modified_timestamp = FilesFilter.get_latest_modified_timestamp(log_folder,r'CONTROL')
        log_file_list = FilesFilter.get_files_after_a_modified_timestamp(log_folder,self.last_file_modified_timestamp,r'CONTROL')
        log_file_list += FilesFilter.get_files_after_a_modified_timestamp(log_folder,self.last_file_modified_timestamp,r'Logs-')
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
        return 'sample in CM timestamp:\n' +\
            '\n'.join(str(sample_id)+':'+str(self.centrifuge_in_map[sample_id]) \
                      for sample_id in self.centrifuge_in_map.keys()) +'\n'\
            'sample out CM timestamp:\n'+\
                '\n'.join(str(sample_id)+':'+str(self.centrifuge_out_map[sample_id]) \
                      for sample_id in self.centrifuge_out_map.keys()) +'\n'\
            'sample DCM timestamp:\n'+\
                '\n'.join(str(sample_id)+':'+str(self.decap_map[sample_id]) \
                      for sample_id in self.decap_map.keys()) +'\n'\
            'sample SEAL timestamp:\n'+\
                '\n'.join(str(sample_id)+':'+str(self.seal_map[sample_id]) \
                      for sample_id in self.seal_map.keys()) +'\n'\
            'sample SRM timestamp:\n'+\
                '\n'.join(str(sample_id)+':'+str(self.store_map[sample_id]) \
                      for sample_id in self.store_map.keys())

def test():
    flexlab_parser = FlexlabControlParser()

    flexlab_log_folder = r'D:\01_Automation\20_Experiential_Conclusions_2015\53_Zhongshan_Aptio\01_Aptio\Log'

    flexlab_log_file_list = flexlab_parser.pre_work(flexlab_log_folder)
    print flexlab_log_file_list
    print len(flexlab_log_file_list)
    flexlab_parser.work(flexlab_log_file_list)
    print flexlab_parser

if __name__ == '__main__':
    test()