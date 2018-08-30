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

source = ColumnDataSource(dict(
    x = data.loc[2000].trainees_total,
    y = data.loc[2000].costs,    
    location=data.loc[2000].locationid,
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


p.xaxis[0].formatter = NumeralTickFormatter()
p.xaxis.axis_label = "# of Total Trainees"
p.yaxis.axis_label = "Costs"


googleAPI= 'AIzaSyBaL6-f-crVqoA88nnRsF0FtDhu6JvcVZU'
map_options = GMapOptions(lat=37.0902, lng=-95.7129, map_type="roadmap", zoom=3)
#map_options = GMapOptions(lat=30.2861, lng=-97.7394, map_type="roadmap", zoom=11)
map = gmap(googleAPI, map_options)

map.circle(
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
    source.data = new_data
    p.title.text = str(year)

def update_buttons(attr, old, new):
    
    print('test_list', radio_button_group.labels[new])
    print('type', type(radio_button_group.labels[new]))
    #print('dataframe ', data.head())
    print('-------------')

    selected_column = str(radio_button_group.labels[new])
    print('selected column', selected_column)
    print('type selected_column', type(data[selected_column]))
    new_data = dict(
        x = data[selected_column],
        y = data.costs,
        location=data.locationid,
    )
    source.data = new_data
    p.xaxis.axis_label = str(selected_column)

slider = Slider(start=2000, end=2016, value=2000, step=1, title="Year")
slider.on_change('value', update_slider)

radio_button_group = RadioButtonGroup(
        labels=["trainees_total", "trainees_pass"], active=0)
radio_button_group.on_change('active', update_buttons)

layout = column(p, slider, widgetbox(radio_button_group), map)
curdoc().add_root(layout)

#bokeh serve filename.py --show