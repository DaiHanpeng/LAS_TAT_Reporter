#%matplotlib inline
from ggplot import *

import pandas as pd

tat_file_path = r'D:\01_Automation\23_Experiential_Conclusions_2016\21_LAS_Statistics\Zhongshan_TAT_GT_0.csv'

tat_data = pd.read_csv(tat_file_path)

tat_data[['TAT']] = tat_data[['TAT']].astype(int)

data = tat_data #[['TAT']].astype(int) + tat_data[['inlab_cat']]

print data.describe()
print '/////////////////////////////////////'

for i, group in data.groupby("analyzer_type"):
    print '////////////////////////////////////'
    print 'cat name:' + str(i)
    print group.describe()


#p = ggplot(group, aes(x='TAT'))
for name, group in data.groupby("analyzer_type"):
    p = ggplot(group, aes(x='TAT'))  + geom_density() + xlim(0,300) + ggtitle(name)
    print(p)