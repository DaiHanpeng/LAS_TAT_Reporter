from bokeh.models.widgets import Button
from bokeh.models.widgets import CheckboxButtonGroup
from bokeh.models.widgets import CheckboxGroup
from bokeh.models.widgets import CheckboxGroup
from datetime import date
from random import randint

from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn

from bokeh.io import output_file, show, vform


output_file("BokehInteractive00.html")

button = Button(label="Foo", type="success")
#show(vform(button))


checkbox_button_group = CheckboxButtonGroup(
        labels=["Option 1", "Option 2", "Option 3"], active=[0, 1])
#show(vform(checkbox_button_group))

checkbox_group = CheckboxGroup(
        labels=["Option 1", "Option 2", "Option 3"], active=[0, 1])
#show(vform(checkbox_group))

data = dict(
        dates=[date(2014, 3, i+1) for i in range(10)],
        downloads=[randint(0, 100) for i in range(10)],
    )
source = ColumnDataSource(data)
columns = [
        TableColumn(field="dates", title="Date", formatter=DateFormatter()),
        TableColumn(field="downloads", title="Downloads"),
    ]
data_table = DataTable(source=source, columns=columns, width=400, height=280)

show(vform(button,checkbox_button_group,checkbox_group,data_table))