from datetime import *

from FilesFilter.FilesFilter import FilesFilter

from DBInterface.DBInterface import DBInterface

class LisOutParser():
    """
    lis out log info parser.
    """
    def __init__(self):
        self.sample_result_map = {}# map sample id with it's resulting timestamp.

    def parse(self,log_file_list):
        self.sample_result_map = {}

        for item in log_file_list:
            file_content_list = []
            if isinstance(item,str):
                try:
                    lis_out_file_handler = open(item)
                    file_content_list = lis_out_file_handler.readlines()
                except Exception as e:
                    print 'file read failed!'
                    print 'exception:',e
                finally:
                    lis_out_file_handler.close()

            if file_content_list:
                for line in file_content_list:
                    if isinstance(line,str):
                        if -1 <> line.find(r'*** INFO [IO-RDL]'):
                            current_date_time =  (' ').join(line.split()[-2:])[:-3]
                            #log_date_time = datetime.strptime(current_date_time,r'%Y-%m-%d %H:%M:%S')
                        elif  -1 <> line.find(r'Xmt') and -1 <> line.find(r'O|1|'):#line.startswith(r'O|1|')
                            sample_id = line.split(r'|')[2]
                            #if not self.sample_order_map.has_key(sample_id):
                            self.sample_result_map[sample_id] = current_date_time

    def to_db(self):
        db_interface = DBInterface()
        db_interface.insert_lis_result(self.sample_result_map)

    def work(self,log_file_list):
        self.parse(log_file_list)
        self.to_db()

    def __repr__(self):
        return 'sample resulting timestamp:\n' +\
            '\n'.join(str(sample_id)+':'+str(self.sample_result_map[sample_id]) \
                      for sample_id in self.sample_result_map.keys())


def test():
    lis_out_log_folder = r'D:\01_Automation\23_Experiential_Conclusions_2016\19_Anhui_Provicial_Hospital\Log\trl\LIS_Translator_out'
    lis_out_log_file_list = FilesFilter.get_files_list(lis_out_log_folder)

    #print lis_in_log_file_list

    lis_out_parser = LisOutParser()
    lis_out_parser.parse(lis_out_log_file_list)
    lis_out_parser.to_db()
    #print lis_out_parser

if __name__ == '__main__':
    test()