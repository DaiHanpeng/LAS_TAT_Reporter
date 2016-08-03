from sklearn.datasets import load_iris
import pandas as pd
iris = load_iris()
df=pd.DataFrame(iris.data)
df.columns=['petal_width','petal_length','sepal_width','sepal_length']

from bokeh.charts import BoxPlot, output_notebook, show
data=df[['petal_length','sepal_length']]

output_notebook()

p = BoxPlot(data, width=400, height=400)

#show(p)