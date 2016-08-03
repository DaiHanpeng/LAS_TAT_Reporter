import pandas as pd
import ggplot as gp

tat_file_path = r'D:\01_Automation\23_Experiential_Conclusions_2016\21_LAS_Statistics\Zhongshan_TAT_Report_0.csv'

tat_data = pd.read_csv(tat_file_path)

data = tat_data[['TAT']].astype(int)

#tat_data['las_inlab'] =  pd.to_datetime(tat_data['las_inlab'], format='%m/%d/%Y %H:%M')
print data.describe()


#print gp.ggplot(tat_data, gp.aes(x='TAT')) + gp.geom_histogram()
#print gp.qplot(tat_data)



#print (ggplot(tat_data, aes(x='TAT')) + geom_histogram()) + xlab("TAT Time in Minutes") + ylab("# of Tubes")
