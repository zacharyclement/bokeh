import pandas as pd

from bokeh.io import curdoc
from bokeh.io import output_notebook
from bokeh.io import show
from bokeh.io import push_notebook

from bokeh.models import NumeralTickFormatter
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool
from bokeh.models import LinearInterpolator
from bokeh.models import CategoricalColorMapper
from bokeh.models import Slider

from bokeh.plotting import figure

from bokeh.palettes import Spectral6

from bokeh.layouts import column

#set up data
df = pd.read_csv('trainee_costs.csv')
del df['Unnamed: 0']
del df['index']
data = df[['year', 'locationid', 'costs', 'trainees_total', 'trainees_pass', 'latitude', 'longitude']]
data = data.set_index('year')

source = ColumnDataSource(dict(
    x = data.loc[2000].trainees_total,
    y = data.loc[2000].costs,    
    location=data.loc[2000].locationid,
))

PLOT_OPTS = dict(
    plot_height = 400,
    x_range = (data['trainees_total'].min(), data['trainees_total'].max()),
    y_range = (data['costs'].min(), data['costs'].max()),
    )

p = figure(
    title='costs per trainee',
    tools=[HoverTool(tooltips='@location', show_arrow=False)],
    **PLOT_OPTS)

p.circle(
    x='x',
    y='y',
    source=source,
)

p.xaxis[0].formatter = NumeralTickFormatter()
p.xaxis.axis_label = "# of Total Trainees"
p.yaxis.axis_label = "Costs"

def update(attr, old, new):
    year = new
    new_data = dict(
        x = data.loc[year].trainees_total,
        y = data.loc[year].costs,    
        location=data.loc[year].locationid,
    )
    source.data = new_data
    p.title.text = str(year)


slider = Slider(start=2000, end=2016, value=2000, step=1, title="Year")
slider.on_change('value', update)

layout = column(p, slider)
curdoc().add_root(layout)

#bokeh serve filename.py --show