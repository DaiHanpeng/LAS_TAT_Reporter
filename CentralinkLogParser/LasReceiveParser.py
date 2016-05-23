from datetime import *

from FilesFilter.FilesFilter import FilesFilter

from DBInterface.DBInterface import DBInterface

class LasReceiveParser():
    """
    las receive log info parser.
    """
    def __init__(self):
        self.sample_inlab_map = {} # map sample id with its in-labbing timestamp

    def parse(self,log_file_list):
        self.sample_inlab_map = {}

        #print log_file_list
        for item in log_file_list:
            file_content_list = []
            if isinstance(item,str):
                try:
                    las_receive_file_handler = open(item)
                    file_content_list = las_receive_file_handler.readlines()
                except Exception as e:
                    print 'file read failed!'
                    print 'exception:',e
                finally:
                    las_receive_file_handler.close()

            if file_content_list:
                for line in file_content_list:
                    if isinstance(line,str):
                        if -1 <> line.find(r'*** INFO [IO-TCP]'):
                            current_date_time =  (' ').join(line.split()[-2:])[:-3]
                            #log_date_time = datetime.strptime(current_date_time,r'%Y-%m-%d %H:%M:%S')
                        elif  -1 <> line.find(r'|I|L001^'):
                            sample_id = line.split(r'|I|L001^')[1].split('\\')[0]
                            if not self.sample_inlab_map.has_key(sample_id):
                                self.sample_inlab_map[sample_id] = current_date_time
                            elif self.sample_inlab_map[sample_id] > current_date_time:
                                elf.sample_inlab_map[sample_id] = current_date_time

    def to_db(self):
        db_interface = DBInterface()
        db_interface.insert_sample_inlab(self.sample_inlab_map)

    def work(self,log_file_list):
        self.parse(log_file_list)
        self.to_db()

    def __repr__(self):
        return 'sample in-labbing timestamp:\n' +\
            '\n'.join(str(sample_id)+':'+str(self.sample_inlab_map[sample_id]) \
                      for sample_id in self.sample_inlab_map.keys() )

def test():
    #print 'O|1|5400555276||^^^LAC|R||2015122105241401||||N||||||||||||||||IP'.startswith(r'O|1|')

    las_receive_log_folder = r'D:\01_Automation\05_Experiential_Conclusions\37_Wenzhou\20141117_Backup\trl\trl\Auto_Receive'
    las_receive_log_file_list = FilesFilter.get_files_list(las_receive_log_folder)

    #print las_receive_log_file_list

    las_receive_parser = LasReceiveParser()
    las_receive_parser.parse(las_receive_log_file_list)
    las_receive_parser.to_db()
    #print las_receive_parser

if __name__ == '__main__':
    test()