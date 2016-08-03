import pandas as pd
import ggplot as gp

tat_file_path = r'D:\01_Automation\23_Experiential_Conclusions_2016\21_LAS_Statistics\Zhongshan_TAT_Report_0.csv'

tat_data = pd.read_csv(tat_file_path)

data = tat_data[['TAT']].astype(int)

print data.describe()

gp.ggplot()

print gp.qplot(data=data)

