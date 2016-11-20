from threading import Thread
import os
import time
import zipfile
from zipfile import ZipFile
from threading import Timer

from FlexlabLogParser import FlexlabControlParser

from DBInterface.TAT_Interface import TAT_Interface

from FilesFilter.FilesFilter import FilesFilter

FILE_SCAN_INTERVAL = 1*60  #1 minutes of scan interval.
CONTROL_LOG_FOLDER = r'F:\Zhongshan\log_aptio_20161110\Log'

class ParserManager():
    """
    manager of all parsers.
    """
    def __init__(self):
        self.flexlab_parser = FlexlabControlParser()

        self.timing_exec_func()
        #self.timer = Timer(FILE_SCAN_INTERVAL,self.timing_exec_func)
        #self.timer.start()

    def timing_exec_func(self):
        print 'excuting...'
        ISOTIMEFORMAT='%Y-%m-%d %X'
        print  time.strftime(ISOTIMEFORMAT,time.localtime())
        self.parser(CONTROL_LOG_FOLDER)
        db_interface = TAT_Interface()
        db_interface.update_all_fields()
        self.timer = Timer(FILE_SCAN_INTERVAL,self.timing_exec_func)
        self.timer.start()
        print  time.strftime(ISOTIMEFORMAT,time.localtime())
        print 'end of execut'

    def parser(self,control_log_folder_path,start_date=None,end_date=None):
        flexlab_log_file_list = []

        flexlab_log_file_list = self.flexlab_parser.pre_work(CONTROL_LOG_FOLDER)
        print flexlab_log_file_list
        print len(flexlab_log_file_list)
        self.flexlab_parser.work(flexlab_log_file_list)

def test():
    parser_manager = ParserManager()
    control_log_dir = r'D:\01_Automation\20_Experiential_Conclusions_2015\53_Zhongshan_Aptio\01_Aptio\Aptio_Log'
    parser_manager.parser(control_log_dir,None,None)

def test2():
    zip_file = r'F:\Zhongshan\log_aptio_20161110\Log\Logs-161018.zip'
    print os.path.isfile(zip_file)

    if zipfile.is_zipfile(zip_file):
        with ZipFile(zip_file, 'r') as open_zip_file:
            #print open_zip_file.filelist
            print
            print open_zip_file.namelist()
            with open_zip_file.open(r'CONTROL-1610180940.XML') as opened_file:
                for line in opened_file.readlines():
                    print line

if __name__ == '__main__':
    '''
    ISOTIMEFORMAT='%Y-%m-%d %X'
    print  time.strftime(ISOTIMEFORMAT,time.localtime())
    test2()
    print  time.strftime(ISOTIMEFORMAT,time.localtime())
    '''
    ParserManager()