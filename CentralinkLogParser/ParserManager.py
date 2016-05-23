from threading import Thread
import os
import time
from Advia2400Parser import Advia2400Parser
from CentaurParser import CentaurParser
from LasReceiveParser import LasReceiveParser
from LisInParser import LisInParser
from LisOutParser import LisOutParser

from FilesFilter.FilesFilter import FilesFilter

class ParserManager():
    """
    manager of all parsers.
    """
    def __init__(self):
        self.advia_parser = Advia2400Parser()
        self.centuar_parser = CentaurParser()
        self.las_receive_parser = LasReceiveParser()
        self.lis_in_parser = LisInParser()
        self.lis_out_parser = LisOutParser()
        '''
        self.parser_list = []
        self.parser_list.append(Advia2400Parser())
        self.parser_list.append(CentaurParser())
        self.parser_list.append(LasReceiveParser())
        self.parser_list.append(LisInParser())
        self.parser_list.append(LisOutParser())
        '''

    def parser(self,trl_log_folder_path,start_date,end_date):
        advia_log_list = []
        centaur_log_list = []
        las_receive_log_list = []
        lis_in_log_list = []
        lis_out_log_list = []

        dir_list = os.listdir(trl_log_folder_path)
        for dir in dir_list:
            if isinstance(dir,str):
                if dir.startswith(r'Advia2400') or dir.startswith(r'Advia1800'):
                    advia_log_list += FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
                elif dir.startswith(r'CentaurXP'):
                    centaur_log_list += FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
                elif r'Auto_Receive' == dir:
                    las_receive_log_list = FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
                elif r'LIS_Translator_in' == dir:
                    lis_in_log_list = FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
                elif r'LIS_Translator_out' == dir:
                    lis_out_log_list = FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)

        parser_threads = []

        parser_threads.append(Thread(target=self.advia_parser.work,args=(advia_log_list,)))
        parser_threads.append(Thread(target=self.centuar_parser.work,args=(centaur_log_list,)))
        parser_threads.append(Thread(target=self.las_receive_parser.work,args=(las_receive_log_list,)))
        parser_threads.append(Thread(target=self.lis_in_parser.work,args=(lis_in_log_list,)))
        parser_threads.append(Thread(target=self.lis_out_parser.work,args=(lis_out_log_list,)))

        for t in parser_threads:
            #t.setDaemon(True)
            t.start()

def test():
    parser_manager = ParserManager()
    trl_log_dir = r'D:\01_Automation\23_Experiential_Conclusions_2016\19_Anhui_Provicial_Hospital\Log\trl'
    parser_manager.parser(trl_log_dir,None,None)


def test2():
    #trl_log_folder_path = r'D:\01_Automation\23_Experiential_Conclusions_2016\19_Anhui_Provicial_Hospital\Log\trl'
    trl_log_folder_path=r'D:\01_Automation\05_Experiential_Conclusions\37_Wenzhou\20141117_Backup\trl\trl'
    start_date = None
    end_date = None

    advia_log_list = []
    centaur_log_list = []
    las_receive_log_list = []
    lis_in_log_list = []
    lis_out_log_list = []

    dir_list = os.listdir(trl_log_folder_path)
    for dir in dir_list:
        if isinstance(dir,str):
            if dir.startswith(r'Advia2400') or dir.startswith(r'Advia1800'):
                advia_log_list += FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
            elif dir.startswith(r'CentaurXP'):
                centaur_log_list += FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
            elif r'Auto_Receive' == dir:
                las_receive_log_list = FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
            elif -1 <> dir.find(r'LIS_') and dir[-2:].lower() == r'in':
                lis_in_log_list = FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
                print 'lis in:',lis_in_log_list
            elif -1 <> dir.find(r'LIS_') and dir[-3:].lower() == r'out':
                lis_out_log_list = FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
                print 'lis out:',lis_out_log_list

    advia_parser = Advia2400Parser()
    centaur_parser = CentaurParser()
    las_receive_parser = LasReceiveParser()
    lis_in_parser = LisInParser()
    lis_out_parser = LisOutParser()

    advia_parser.work(advia_log_list)
    centaur_parser.work(centaur_log_list)
    las_receive_parser.work(las_receive_log_list)
    lis_in_parser.work(lis_in_log_list)
    lis_out_parser.work(lis_out_log_list)


if __name__ == '__main__':
    ISOTIMEFORMAT='%Y-%m-%d %X'
    print  time.strftime(ISOTIMEFORMAT,time.localtime())
    test2()
    print  time.strftime(ISOTIMEFORMAT,time.localtime())