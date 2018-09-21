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
from bokeh.models.widgets import RadioButtonGroup
from bokeh.models import GMapOptions
from bokeh.models import GMapPlot
from bokeh.models.ranges import Range1d
from bokeh.models import LinearAxis

from bokeh.plotting import figure
from bokeh.plotting import gmap

from bokeh.palettes import Spectral6

from bokeh.layouts import column
from bokeh.layouts import widgetbox

from bokeh.tile_providers import CARTODBPOSITRON

from bokeh.transform import dodge

from bokeh.core.properties import value

#set up data
df_ = pd.read_csv('data/random_data.csv')

df_cost = pd.read_csv('data/cost_trainee.csv')
df_time = pd.read_csv('data/time_trainee.csv')
df_bar = pd.read_csv('data/bar.csv')

del df_['Unnamed: 0']
del df_['index']
data = df_[['year', 'locationid', 'costs', 'trainees_total', 'trainees_pass', 'latitude', 'longitude']]
data = data.set_index('year')

#############################################


p1 = figure(
    title='costs per trainee',
    tools=[HoverTool(tooltips='@location', show_arrow=False)],
    **PLOT_OPTS)

for i, x in enumerate(df_cost[df_cost.columns[1:]]):
    colors = Spectral6
    p1.line(
        df_cost['year'],
        df_cost[x],
        legend = x,
        color = colors[i]
        
    )

p1.xaxis[0].formatter = NumeralTickFormatter()
p1.xaxis.axis_label = "year"
p1.yaxis.axis_label = "Costs"


###########Figure 2

source_bar = ColumnDataSource(data=dict(
    facility = df_bar['facility'],
    cost = df_bar['cost_per_trainee'],
    time = df_bar['time_per_trainee']
))

p2 = figure(x_range= list(df_bar['facility']), plot_height=250, title="Costs",
           toolbar_location=None, tools="")

p2.vbar(x=dodge('facility', -0.1, range=p.x_range), top='cost', width=0.2, source=source_bar, legend=value("cost"))

p2.y_range = Range1d(0, max(df_bar['cost_per_trainee']))

p2.extra_y_ranges = {"foo": Range1d(start=0, end=max(df_bar['time_per_trainee']))}
p2.add_layout(LinearAxis(y_range_name="foo"), 'right')

p2.vbar(x=dodge('facility', 0.1, range=p.x_range), top='time', width=.2, y_range_name='foo', source=source, color='red', legend=value('time'))
#p.circle(x=df_bar['facility'], y=df_bar['time_per_trainee'], y_range_name='foo')

p2.x_range.range_padding = 0.0
p2.xgrid.grid_line_color = None
p2.xgrid.grid_line_color = None
p2.y_range.start = 0

############################################


#slider = Slider(start=2000, end=2016, value=2000, step=1, title="Year")
#slider.on_change('value', update_slider)

#radio_button_group = RadioButtonGroup(labels=["trainees_total", "trainees_pass"], active=0)
#radio_button_group.on_change('active', update_buttons)

layout = column(p1, p2)
curdoc().add_root(layout)

#bokeh serve filename.py --show