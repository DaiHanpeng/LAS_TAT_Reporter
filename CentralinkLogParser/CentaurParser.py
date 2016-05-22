from datetime import *

from FilesFilter.FilesFilter import FilesFilter

from DBInterface.DBInterface import DBInterface

class CentaurParser():
    """
    centaur log info parser
    """
    def __init__(self):
        self.sample_query_map = {}
        self.sample_result_map = {}

    def parse(self,log_file_list):
        self.sample_query_map = {}
        self.sample_result_map = {}

        #print log_file_list
        for item in log_file_list:
            file_content_list = []
            if isinstance(item,str):
                try:
                    centaur_file_handler = open(item)
                    file_content_list = centaur_file_handler.readlines()
                except Exception as e:
                    print 'file read failed!'
                    print 'exception:',e
                finally:
                    centaur_file_handler.close()

            if file_content_list:
                for line in file_content_list:
                    if isinstance(line,str):
                        if -1 <> line.find(r'*** INFO [IO-TCP]'):
                            current_date_time =  (' ').join(line.split()[-2:])[:-3]
                            #log_date_time = datetime.strptime(current_date_time,r'%Y-%m-%d %H:%M:%S')
                        elif -1 <> line.find(r'Q|1|^') and -1 <> line.find(r'OrderQuestion\OrderReportInfo'):
                            sample_id = line.split(r'Q|1|^')[1].split(r'|')[0]
                            self.sample_query_map[sample_id] = current_date_time
                        elif -1 <> line.find(r'|R||||||||||||||||||||') and -1 <> line.find(r'O|1|'):
                            sample_id = line.split(r'O|1|')[1].split(r'|')[0]
                            self.sample_result_map[sample_id] = current_date_time

    def to_db(self):
        db_interface = DBInterface()
        db_interface.insert_centaut_query(self.sample_query_map)
        db_interface.insert_centaur_result(self.sample_result_map)

    def work(self,log_file_list):
        self.parse(log_file_list)
        self.to_db()

    def __repr__(self):
        return 'sample quring timestamp:\n' +\
            '\n'.join(str(sample_id)+':'+str(self.sample_query_map[sample_id]) \
                      for sample_id in self.sample_query_map.keys()) +'\n'\
            'sample resuting timestamp:\n'+\
                '\n'.join(str(sample_id)+':'+str(self.sample_result_map[sample_id]) \
                      for sample_id in self.sample_result_map.keys())

def test():
    centaur_log_folder = r'D:\01_Automation\05_Experiential_Conclusions\37_Wenzhou\20141117_Backup\trl\trl\CentaurXP_2_Translator'
    centaur_log_file_list = FilesFilter.get_files_list(centaur_log_folder)

    #print lis_in_log_file_list

    centaur_parser = CentaurParser()
    centaur_parser.parse(centaur_log_file_list)
    #centaur_parser.to_db()
    print centaur_parser

if __name__ == '__main__':
    test()