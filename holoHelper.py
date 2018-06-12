from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.palettes import Blues4

import pandas as pd
import numpy as np
import json

#File path
DATA_PATH = "../data/EAGE2018/"
wld_fname = "{}well_log_data.txt".format(DATA_PATH)
group_fname = "{}EAGE_Hackathon_2018_Well_".format(DATA_PATH)

#considered statistics
STAT_NAMES = ['Max ', 'Min ', 'Mean ', 'Std ']

#Fix the maximum possible depth
MAX_DEPTH=5000

#convert json data into pandas
with open(wld_fname, 'r') as f:
    j_data = json.load(f)

for i, item in enumerate(j_data):
    if i == 0:
        p_data = pd.DataFrame(item)
    else:
        p_data = p_data.append(pd.DataFrame(item))



def get_dataset(curve, well, top=0, base=MAX_DEPTH):
    """Prepare dataset for plotting

    Select curve data from a well in a group bounded by a specified top and base
    # Arguments
        curve: curve to be considered
        well: well to be considered
        top: top coordinates of the group to be considered
        base: base coordinates of the group to be considered
    # Returns
        A bokeh Source object containing the pandas data
    """
    src = p_data[(p_data['Depth']>top) & (p_data['Depth']<base)]
    cur_df = (src[src['Well'] == well])[['Depth', curve]]
    cur_df=cur_df.set_index('Depth').copy()
    cur_df.columns = ['val']

    #reverse depth direction for drawing
    cur_df=cur_df.sort_index()
    cur_df.index = -cur_df.index

    return ColumnDataSource(data=cur_df)

def make_plot(current, curve, plot_width=800, plot_height=1000, alpha=.3, font_style="bold"):
    """Show plot of current data 

    Compute plot of current data 
    # Arguments
        current: bokeh Source object containing the current data
        curve: curve to be plotted
        plot_width: width of plot
        plot_heigth: height of plot
        alpha: alpha-value of plot
        font_style: font style for plot
    # Returns
        A plot object for the current data
    """

    #plot the figure
    plot = figure( plot_width=plot_width, plot_height=plot_height, tools="", toolbar_location=None)
    plot.line(y='Depth', x='val', source=current, color=Blues4[1])

    #set plot meta_data
    plot.yaxis.axis_label = "Depth"
    plot.axis.axis_label_text_font_style = font_style
    plot.grid.grid_line_alpha = alpha

    return plot


def select_top_base(group, well):
    """Extract top and base coordinates
    
    Extract top and base coordinates for a specified group and well
    # Arguments
        group: group for which top and base coords are to be queried
        well: well to be considered
    # Returns
        A pair consisting of the top and base coordinate of the specified group
    """

    group_file = "{}EAGE_Hackathon_2018_{}{}{}".format(DATA_PATH,"Well_", well,".csv")
    group_df = pd.read_csv(group_file)

    base = MAX_DEPTH
    top = 0
    if group!='All':
         base_top = group_df[(group_df['name'] == group) & (group_df['Surface'] == 'group')]
         top_sel = base_top[base_top['Obs#'] == 'Top']['MD']
         base_sel = base_top[base_top['Obs#'] == 'Base']['MD']
         if len(top_sel)>0:
             top = top_sel.values[0]
         if len(base_sel)>0:
            base = base_sel.values[0]
    return top, base 

    
def update_plot(curve, well, top, base, source):
    """Updates the plot

    Updates the plotted curve after user interaction
    # Arguments
        curve: curve to be considered
        well: well to be considered
        top: top coordinates of the group to be considered
        base: base coordinates of the group to be considered
        source: source object to be modified
    """
    new_source = get_dataset(curve, well, top, base)
    source.data.update(new_source.data)


def update_text(curve, well, top, base, stats):
    """Updates the plot

    Updates the displayed statistics after user interaction
    # Arguments
        curve: curve to be considered
        well: well to be considered
        top: top coordinates of the group to be considered
        base: base coordinates of the group to be considered
        stats: text fields to be modified
    """
    src = p_data[(p_data['Depth']>top) & (p_data['Depth']<base)]
    df = src[src['Well'] == well]
    df = df[curve]

    stat_vals = [df.max(), df.min(), df.mean(), df.std()]
    for stat, name, stat_val in zip(stats, STAT_NAMES, stat_vals):
        stat.text = "{0}{1:.2f}".format(name, stat_val)
