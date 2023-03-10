import numpy as np
import pandas as pd
from bokeh.layouts import column, gridplot
from bokeh.models import ColorBar, ColumnDataSource, LinearColorMapper, LogColorMapper
from bokeh.plotting import figure, show
from bokeh.transform import transform

#read csv files (tyep: 'pandas.core.frame.DataFrame')
a = pd.read_csv('x.csv')
b = pd.read_csv('y.csv')
print(type(a))
print(type(b))

#Converts CSVs to NumPy Array
x = np.loadtxt('x.csv', delimiter=',')
y = np.loadtxt('y.csv', delimiter=',')
print(type(x))
print(type(y))
print(x)
print(y)

source = ColumnDataSource(dict(x=x, y=y))

def make_plot(mapper_type, palette):
    cls = LogColorMapper if mapper_type == "log" else LinearColorMapper
    mapper = cls(palette=palette, low=1, high=1000)

    p = figure(x_range=(1, 1000), title=f"{palette} with {mapper_type} mapping",
               toolbar_location=None, tools="", x_axis_type=mapper_type)
    p.scatter('x', 'y', alpha=0.8, source=source, color=transform('x', mapper))

    color_bar = ColorBar(color_mapper=mapper, padding=0,
                         ticker=p.xaxis.ticker, formatter=p.xaxis.formatter)
    p.add_layout(color_bar, 'below')

    return p

p1 = make_plot("linear", "Viridis256")
p2 = make_plot("log", "Viridis256")
p3 = make_plot("linear", "Viridis6")
p4 = make_plot("log", "Viridis6")

p5 = figure(x_range=(1, 1000), width=800, height=300, toolbar_location=None, tools="",
            title="Viridis256 with linear mapping, low/high = 200/800 = pink/grey")
mapper = LinearColorMapper(palette="Viridis256", low=200, high=800,
                           low_color="pink", high_color="darkgrey")
p5.scatter(x='x', y='y', alpha=0.8, source=source, color=transform('x', mapper))

grid =  gridplot([[p1, p2], [p3, p4]], width=400, height=300, toolbar_location=None)
show(column(grid, p5))
