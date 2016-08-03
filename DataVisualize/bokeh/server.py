from bokeh.plotting import figure, output_file, output_notebook, show,save
from bokeh.charts import *
import pandas as pd

tat_file_path = r'D:\01_Automation\23_Experiential_Conclusions_2016\21_LAS_Statistics\Zhongshan_TAT_Report_0.csv'

tat_data = pd.read_csv(tat_file_path)

#print tat_data
#tat_data.columns=['sample_id','lis_order','las_inlab','advia_query','advia_result','centaur_query','centaur_result','lis_upload','TAT']

data = tat_data[['TAT']].astype(int)

#output_notebook()

print data.describe()

#p = Histogram(data,xgrid=True,ygrid=True,color='navy',label='TAT',values=None,agg='count')
p = Histogram(data)

p = Bar(data)
p = BoxPlot(data)
p = Area(data)
p = Line(data,x='tat')
save(p,'tat.png',resources.INLINE,'tat report')

#p = Bar(data,label='TAT',values=None,color='navy',stack=None,group='TAT',agg='count')
#p = BoxPlot(data, width=400, height=400)

#show(p)