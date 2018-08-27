import pandas as pd
from bokeh.io import curdoc

from bokeh.io import output_notebook
from bokeh.io import show
from bokeh.plotting import figure
from bokeh.models import NumeralTickFormatter
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool
from bokeh.models import LinearInterpolator
from bokeh.palettes import Spectral6
from bokeh.models import CategoricalColorMapper
from bokeh.models import Slider
from bokeh.layouts import column

data = pd.read_csv('gapminder.csv', thousands=',', index_col='Year')

source = ColumnDataSource(dict(
    x=data.loc[2010].income,
    y=data.loc[2010].life,
    country=data.loc[2010].Country,
    population =data.loc[2010].population,
    region=data.loc[2010].region
))

PLOT_OPTS = dict(
    height=400, x_axis_type='log',
    x_range = (100, 100000), 
    y_range = (0,100), 
    )

regions = list(data.region.unique())

size_mapper = LinearInterpolator(
    x=[data.population.min(), data.population.max()],
    y=[5,50]
)

color_mapper = CategoricalColorMapper(
    factors=regions,
    palette=Spectral6)

p = figure(
    title='2010',
    toolbar_location='above',
    tools=[HoverTool(tooltips='@country', show_arrow=False)], 
    **PLOT_OPTS)

p.circle(x='x', y='y', 
         size={'field': 'population', 'transform': size_mapper}, 
         color={'field': 'region', 'transform': color_mapper},
         alpha=.6, 
         source=source,
        legend='region')

p.legend.border_line_color = None
p.legend.location = (0, 100)
p.right.append(p.legend[0])

def update(attr, old, new):
    # new = year
    year = new
    new_data = dict(
        x=data.loc[year].income,
        y=data.loc[year].life,
        country=data.loc[year].Country,
        region=data.loc[year].region,
        population=data.loc[year].population,
    )
    source.data = new_data
    p.title.text = str(year)

slider = Slider(start=1800, end=2010, step=1, title='Year')
slider.on_change('value', update)

layout = column(p, slider)
curdoc().add_root(layout)