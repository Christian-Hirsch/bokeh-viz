import pandas as pd
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Select, PreText

from holoHelper import get_dataset, make_plot, select_top_base, update_text, update_plot

#file names and considered stats
DATA_PATH = "../data/EAGE2018/"
wld_fname = "{}well_log_data.txt".format(DATA_PATH)

###Set up the statistics text fields
STAT_NAMES = ['Max ', 'Min ', 'Mean ', 'Std ']
stats = [PreText(text=prop, width=500, height=1) for prop in STAT_NAMES]


###Set up drop-down menus
#Titles and initial valuesfor drop-downs
TITLES = ['Curve', 'Group', 'Well']
INITS = ['Gamma', 'AA', 'A']

#Options to choose from
CURVE_OPTIONS = ['Gamma', 'Res']
GROUP_OPTIONS = ['HH', 'GG', 'FF', 'EE', 'DD', 'CC', 'BB', 'AA', 'All']
WELL_OPTIONS = ['X-27', 'I_A', 'D', 'B', 'B_AT2', 'B_A', 'AA', 'A']
OPTIONS = [CURVE_OPTIONS, GROUP_OPTIONS, WELL_OPTIONS]

#Define drop-down menus
selects = [Select(value=init, title=title, options= option) for init, title, option in zip(INITS, TITLES, OPTIONS)]


def update_plot_text(attrname, old, new):
    curve, group, well = [select.value for select in selects]

    top,base = select_top_base(group, well)

    update_text(curve, well, top, base, stats)
    update_plot(curve, well, top, base, source)

for select in selects:
    select.on_change('value', update_plot_text)

source = get_dataset(INITS[0], INITS[2])
plot = make_plot(source, INITS[0])
controls = column(*selects, *stats)

curdoc().add_root(row(plot, controls))
curdoc().title = "Log quality visualisation"
