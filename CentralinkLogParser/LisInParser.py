from datetime import *

from FilesFilter.FilesFilter import FilesFilter

from DBInterface.DBInterface import DBInterface

class LisInParser():
    """
    lis in log info parser.
    """
    def __init__(self):
        self.sample_order_map = {} # map sample id with its ordering timestamp

    def parse(self,log_file_list):
        self.sample_order_map = {}

        #print log_file_list
        for item in log_file_list:
            file_content_list = []
            if isinstance(item,str):
                try:
                    lis_in_file_handler = open(item)
                    file_content_list = lis_in_file_handler.readlines()
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
                        elif  -1 <> line.find(r'Rdl') and -1 <> line.find(r'O|1|'):#line.startswith(r'O|1|')
                            sample_id = line.split(r'|')[2]
                            #if not self.sample_order_map.has_key(sample_id):
                            self.sample_order_map[sample_id] = current_date_time


    def to_db(self):
        db_interface = DBInterface()
        db_interface.insert_sample_lis_order(self.sample_order_map)

    def work(self,log_file_list):
        self.parse(log_file_list)
        self.to_db()

    def __repr__(self):
        return 'sample ordering timestamp:\n' +\
            '\n'.join(str(sample_id)+':'+str(self.sample_order_map[sample_id]) \
                      for sample_id in self.sample_order_map.keys() )

def test():
    #print 'O|1|5400555276||^^^LAC|R||2015122105241401||||N||||||||||||||||IP'.startswith(r'O|1|')

    lis_in_log_folder = r'D:\01_Automation\23_Experiential_Conclusions_2016\19_Anhui_Provicial_Hospital\Log\trl\LIS_Translator_in'
    lis_in_log_file_list = FilesFilter.get_files_list(lis_in_log_folder)

    #print lis_in_log_file_list

    lis_in_parser = LisInParser()
    lis_in_parser.parse(lis_in_log_file_list)
    lis_in_parser.to_db()
    #print lis_in_parser

if __name__ == '__main__':
    test()