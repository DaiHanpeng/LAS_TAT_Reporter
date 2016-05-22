import os
from datetime import *

class FilesFilter():
    """
    filter to get file list in a folder, which file modification time between[start_date,end_date]
    """
    @staticmethod
    def get_files_list(path_to_folder,start_date=None,end_date=None):
        file_list = []
        if start_date and end_date:
            if isinstance(start_date,date) and isinstance(end_date,date):
                folder_file_list = os.listdir(path_to_folder)
                for f in folder_file_list:
                    #print os.path.getmtime(f)
                    file_mtime = date.fromtimestamp(os.path.getmtime(f))
                    if start_date <= file_mtime <= end_date:
                        file_list.append(os.path.join(path_to_folder,f))
            else:
                print 'start or end datetime format error!'
        else:
            folder_file_list = os.listdir(path_to_folder)
            for f in folder_file_list:
                file_list.append(os.path.join(path_to_folder,f))
        return file_list


def test():

    #files_filter = FilesFilter()

    start = '2016-05-19'
    end = '2016-05-21'
    start_date = datetime.strptime(start,'%Y-%m-%d').date()
    end_date = datetime.strptime(end,'%Y-%m-%d').date()

    #print end_date < start_date

    print FilesFilter.get_files_list('.',start_date,end_date)

    lis_in_log_folder = r'D:\01_Automation\23_Experiential_Conclusions_2016\19_Anhui_Provicial_Hospital\Log\trl\LIS_Translator_in'
    lis_in_log_file_list = FilesFilter.get_files_list(lis_in_log_folder)

    print lis_in_log_file_list


    '''
    # datetime and string conversion...
    start = '2016-05-20'
    end = '2016-05-21'

    start_date = datetime.strptime(start,'%Y-%m-%d').date()
    end_date = datetime.strptime(end,'%Y-%m-%d').date()

    print start_date,end_date
    '''

if __name__ == '__main__':
    #test()
    print os.listdir(r'D:\01_Automation\23_Experiential_Conclusions_2016\19_Anhui_Provicial_Hospital\Log\trl')

