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
from bokeh.layouts import row
from bokeh.layouts import gridplot
from bokeh.layouts import widgetbox

from bokeh.tile_providers import CARTODBPOSITRON

from bokeh.transform import dodge

from bokeh.core.properties import value

#set up data

df_cost = pd.read_csv('data/cost_trainee.csv')
df_time = pd.read_csv('data/time_trainee.csv')
df_bar = pd.read_csv('data/bar.csv')
df_bar_m = pd.read_csv('data/bar-multi.csv')

#############################################

PLOT_OPTS = dict(
    plot_height = 400,
    )

########################################Figure 1

source_bar = ColumnDataSource(data=dict(
    facility = df_bar_m[df_bar_m['year'] == 2011]['facility'],
    cost = df_bar_m[df_bar_m['year'] == 2011]['cost_per_trainee'],
    time = df_bar_m[df_bar_m['year'] == 2011]['time_per_trainee']
))

p = figure(x_range= list(df_bar['facility']), plot_height=400, title="Costs",
           toolbar_location=None, tools="")

p.vbar(x=dodge('facility', -0.1, range=p.x_range), top='cost', width=0.2, source=source_bar, legend=value("cost"))
p.yaxis.axis_label = "Costs"

p.y_range = Range1d(0, max(df_bar_m['cost_per_trainee']))

p.extra_y_ranges = {"foo": Range1d(start=0, end=max(df_bar_m['time_per_trainee']))}
p.add_layout(LinearAxis(y_range_name="foo", axis_label='Time Spent'), 'right')

p.vbar(x=dodge('facility', 0.1, range=p.x_range), top='time', width=.2, y_range_name='foo', source=source_bar, color='red', legend=value('time'))

p.x_range.range_padding = 0.0
p.xgrid.grid_line_color = None
p.xgrid.grid_line_color = None
p.y_range.start = 0
p.xaxis.axis_label = "facility"



def update_slider(attr, old, new):
    year = new
    new_data = dict(
        facility = df_bar_m[df_bar_m['year'] == year]['facility'],
        cost = df_bar_m[df_bar_m['year'] == year]['cost_per_trainee'],
        time = df_bar_m[df_bar_m['year'] == year]['time_per_trainee']
    )
    source_bar.data = new_data
    p.title.text = str(year)

slider = Slider(start=2010, end=2017, value=2017, step=1, title="Year")
slider.on_change('value', update_slider)

###############################################Figure 1

p1 = figure(
    title='Costs per Trainee',
    tools=[HoverTool(tooltips='@location', show_arrow=False)],
    **PLOT_OPTS)

for i, x in enumerate(df_cost[df_cost.columns[1:]]):
    
    source_cost = ColumnDataSource(data=dict(
    x = df_cost['year'],
    y = df_cost[x]
    ))
    
    colors = Spectral6
    p1.line(
        x='x',
        y='y',
        legend = x,
        color = colors[i],
        source=source_cost,
        line_width=3
    )

p1.xaxis.axis_label = "Year"
p1.yaxis.axis_label = "Costs"

###########################################################Figure 3

p2 = figure(
    title='Time Spent per Trainee',
    tools=[HoverTool(tooltips='@location', show_arrow=False)],
    **PLOT_OPTS)

for i, x in enumerate(df_time[df_time.columns[1:]]):
    
    source_time = ColumnDataSource(data=dict(
    x = df_time['year'],
    y = df_time[x]
    ))
    
    colors = Spectral6
    
    p2.line(
        x='x',
        y='y',
        legend = x,
        color = colors[i],
        source=source_time,
        line_width=3
    )

p2.xaxis.axis_label = "Year"
p2.yaxis.axis_label = "Time Spent"

#######################################################

layout = gridplot([ [p1, p2], [p, None], [slider, None]])
curdoc().add_root(layout)

#bokeh serve filename.py --show