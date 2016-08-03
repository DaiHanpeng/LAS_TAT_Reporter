#%matplotlib inline
from ggplot import *

import pandas as pd
#import ggplot as gp

tat_file_path = r'D:\01_Automation\23_Experiential_Conclusions_2016\21_LAS_Statistics\Zhongshan_TAT_Report_0.csv'

tat_data = pd.read_csv(tat_file_path)

# datetime format: 5/31/2016 15:58
#05SEP2014:00:00:00.000 ==> format='%d%b%Y:%H:%M:%S.%f'
tat_data['las_inlab'] =  pd.to_datetime(tat_data['las_inlab'], format='%m/%d/%Y %H:%M')
data = tat_data[['TAT']].astype(int)
#data = data[['las_inlab']].astype(pd.DatetimeIndex)


print data.describe()

#print gp.ggplot(tat_data, gp.aes(x='TAT')) + gp.geom_histogram()
#print gp.qplot(tat_data)

'''
print (ggplot(tat_data, aes(x='TAT')) \
           #+ geom_histogram()) \
            + geom_density()
            + xlab("TAT Time in Minutes") \
            + ylab("# of Tubes") \
            + scale_x_continuous("TAT", breaks=range(0,500,50))\
            + theme_xkcd()
'''

geom_histogram()

print ggplot(data, aes(x='TAT')) + geom_density()