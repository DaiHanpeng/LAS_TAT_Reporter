
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt


class DataProcessor():
    """

    """
    def __init__(self):
        pass

    def process(self,file_path):
        data_frame = pd.read_csv(file_path)
        if isinstance(data_frame,DataFrame):
            print 'ploting'
            data_frame.plot()


        #print data_frame
        #data_frame.plot()

def test():
    csv_path = r'D:\01_Automation\23_Experiential_Conclusions_2016\19_Anhui_Provicial_Hospital\WenzhouTAT-meaningful.csv'
    data_processor = DataProcessor()
    data_processor.process(csv_path)

    plt.plot([1,2,3,4,5,6,7,8],[1,2,3,4,5,6,7,8])

    plt.savefig('plot01.png')

if __name__ == '__main__':
    test()

