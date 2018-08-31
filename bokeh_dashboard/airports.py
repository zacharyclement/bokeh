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

from bokeh.plotting import figure
from bokeh.plotting import gmap

from bokeh.palettes import Spectral6

from bokeh.layouts import column
from bokeh.layouts import widgetbox

from bokeh.tile_providers import CARTODBPOSITRON

#set up data
df = pd.read_csv('trainee_costs.csv')
del df['Unnamed: 0']
del df['index']
data = df[['year', 'locationid', 'costs', 'trainees_total', 'trainees_pass', 'latitude', 'longitude']]
data = data.set_index('year')

source1 = ColumnDataSource(dict(
    x = data.loc[2000].trainees_total,
    y = data.loc[2000].costs,
    location=data.loc[2000].locationid,
))

source2 = ColumnDataSource(dict(
    x = data.trainees_total,
    y = data.costs,
    location=data.locationid,
))

#map data
df_map = pd.read_csv('major_airports.csv')

map_source = ColumnDataSource(
    data=dict(
        lat = df_map['latitude_deg'],
        lon = df_map['longitude_deg']
        #lat = data.loc[2010].latitude,
        #lon = data.loc[2010].longitude,
        #location = data.loc[2010].locationid
#       lat=[ 30.29,  30.20,  30.29],
#       lon=[-97.70, -97.74, -97.78]
    )
)

######Figure 1

PLOT_OPTS = dict(
    plot_height = 400,
    x_range = (data['trainees_total'].min(), data['trainees_total'].max()),
    y_range = (data['costs'].min(), data['costs'].max()),
    )

p1 = figure(
    title='costs per trainee',
    tools=[HoverTool(tooltips='@location', show_arrow=False)],
    **PLOT_OPTS)

p1.circle(
    x='x',
    y='y',
    source=source1,
)

p1.xaxis[0].formatter = NumeralTickFormatter()
p1.xaxis.axis_label = "# of Total Trainees"
p1.yaxis.axis_label = "Costs"

###########Figure 2

p2 = figure(
    title='costs per trainee',
    #tools=[HoverTool(tooltips='@location', show_arrow=False)],
    **PLOT_OPTS)

p2.circle(
    x='x',
    y='y',
    source=source2,
)

p2.xaxis[0].formatter = NumeralTickFormatter()
p2.xaxis.axis_label = "# of Total Trainees"
p2.yaxis.axis_label = "Costs"

#############Figure 3 - map

googleAPI= 'AIzaSyBaL6-f-crVqoA88nnRsF0FtDhu6JvcVZU'
map_options = GMapOptions(lat=37.0902, lng=-95.7129, map_type="roadmap", zoom=3)
    #map_options = GMapOptions(lat=30.2861, lng=-97.7394, map_type="roadmap", zoom=11)

map_ = gmap(googleAPI, map_options)

map_.circle(
    x="lon",
    y="lat",
    size=5,
    fill_color="blue",
    fill_alpha=0.8,
    source=map_source,

)

def update_slider(attr, old, new):
    year = new
    new_data = dict(
        x = data.loc[year].trainees_total,
        y = data.loc[year].costs,
        location=data.loc[year].locationid,
    )
    source1.data = new_data
    p1.title.text = str(year)

def update_buttons(attr, old, new):

    # print('test_list', radio_button_group.labels[new])
    # print('type', type(radio_button_group.labels[new]))
    # print('dataframe ', data.head())
    # print('-------------')
    # print('selected column', selected_column)
    # print('type selected_column', type(data[selected_column]))

    selected_column = str(radio_button_group.labels[new])
    new_data = dict(
        x = data[selected_column],
        y = data.costs,
        location=data.locationid,
    )
    source2.data = new_data
    p2.xaxis.axis_label = str(selected_column)

slider = Slider(start=2000, end=2016, value=2000, step=1, title="Year")
slider.on_change('value', update_slider)

radio_button_group = RadioButtonGroup(labels=["trainees_total", "trainees_pass"], active=0)
radio_button_group.on_change('active', update_buttons)

layout = column(p1, slider, p2, widgetbox(radio_button_group), map_)
curdoc().add_root(layout)

#bokeh serve filename.py --show
