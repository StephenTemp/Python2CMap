#!/usr/bin/env python
# coding: utf-8

# ## Reformat netCDF4 File for a Function Call

# In[8]:


import opedia
import sys
import os
import numpy as np
import pandas as pd
import xarray as xr
import db
import subset
import common as com
from datetime import datetime, timedelta
import time
from bokeh.io import output_notebook
from math import pi
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column
from bokeh.models import DatetimeTickFormatter
from bokeh.palettes import all_palettes
from bokeh.models import HoverTool
from bokeh.embed import components
import jupyterInline as jup
if jup.jupytered():
    from tqdm import tqdm_notebook as tqdm
else:
    from tqdm import tqdm


# ### Testing Function 

# In[6]:



tables = ['tblSST_AVHRR_OI_NRT', 'tblArgoMerge_REP', 'tblArgoMerge_REP']           # see catalog.csv  for the complete list of tables and variable names
variables = ['sst', 'argo_merge_temperature_adj', 'argo_merge_salinity_adj']       # see catalog.csv  for the complete list of tables and variable names
startDate = '2016-04-30'
endDate = '2016-04-30'
lat1, lat2 = 20, 24
lon1, lon2 = -170, 150
depth1, depth2 = 0, 20
fname = 'DEP'
exportDataFlag = False      # True if you you want to download data

plotDist(tables, variables, startDate, endDate, lat1, lat2, lon1, lon2, depth1, depth2, fname, exportDataFlag)


# In[11]:


xFile = xr.open_dataset('http://engaging-opendap.mit.edu:8080/thredds/dodsC/las/id-a1d60eba44/data_usr_local_tomcat_content_cbiomes_20190510_20_darwin_v0.2_cs510_darwin_v0.2_cs510_nutrients.nc.jnl')

tables = [xFile]           # see catalog.csv  for the complete list of tables and variable names
variables = ['O2']       # see catalog.csv  for the complete list of tables and variable names
startDate = '2010-04-30'
endDate = '2010-04-30'
lat1, lat2 = -80, 80
lon1, lon2 = -80, 80
depth1, depth2 = 0, 10
fname = 'DEP'
exportDataFlag = False      # True if you you want to download data

xarrayPlotDist(tables, variables, startDate, endDate, lat1, lat2, lon1, lon2, depth1, depth2, fname, exportDataFlag)


# ### Original Function

# In[3]:


def plotDist(tables, variables, startDate, endDate, lat1, lat2, lon1, lon2, depth1, depth2, fname, exportDataFlag, marker='-', msize=30, clr='purple'):
    p = []
    lw = 2
    w = 800
    h = 400
    TOOLS = 'pan,wheel_zoom,zoom_in,zoom_out,box_zoom, undo,redo,reset,tap,save,box_select,poly_select,lasso_select'
    for i in tqdm(range(len(tables)), desc='overall'):
        y = subset.spaceTime(tables[i], variables[i], startDate, endDate, lat1, lat2, lon1, lon2, depth1, depth2) 
        if len(y) < 1:
            com.printTQDM('%d: No matching entry found: Table: %s, Variable: %s ' % (i+1, tables[i], variables[i]), err=True )
            continue
        com.printTQDM('%d: %s retrieved (%s).' % (i+1, variables[i], tables[i]), err=False)
        y = y[variables[i]]
        
        if exportDataFlag:
            exportData(y, tables[i], variables[i], startDate, endDate, lat1, lat2, lon1, lon2, depth1, depth2)
        try:    
            y = y[~np.isnan(y)]     # remove nans
        except Exception as e:
            continue    
        hist, edges = np.histogram(y, density=True, bins=50)
        p1 = figure(tools=TOOLS, toolbar_location="above", plot_width=w, plot_height=h)
        p1.yaxis.axis_label = 'Density'
        p1.xaxis.axis_label = variables[i] + ' [' + db.getVar(tables[i], variables[i]).iloc[0]['Unit'] + ']'
        leg = variables[i]
        fill_alpha = 0.4   
        cr = p1.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color="dodgerblue", line_color=None, hover_fill_color="firebrick", fill_alpha=fill_alpha, hover_alpha=0.7, hover_line_color="white", legend=leg)
        p1.add_tools(HoverTool(tooltips=None, renderers=[cr], mode='mouse'))
        p.append(p1)
    dirPath = 'embed/'
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)        
   # if not inline:      ## if jupyter is not the caller
   #     output_file(dirPath + fname + ".html", title="Histogram")
    show(column(p))
    return


# ### NetCDF4-Compatible Function

# In[10]:


def xarrayPlotDist(tables, variables, startDate, endDate, lat1, lat2, lon1, lon2, depth1, depth2, fname, exportDataFlag, marker='-', msize=30, clr='purple'):
    p = []
    lw = 2
    w = 800
    h = 400
    TOOLS = 'pan,wheel_zoom,zoom_in,zoom_out,box_zoom, undo,redo,reset,tap,save,box_select,poly_select,lasso_select'
    for i in tqdm(range(len(tables)), desc='overall'):
        
        unit = tables[i].variables[variables[i]].attrs['units']
        
        varData = tables[i].sel(TIME = slice(startDate, endDate), LAT_C = slice(lat1, lat2), LON_C = slice(lon1, lon2), DEP_C = slice(depth1, depth2))
        varData = varData.variables[variables[i]][:].values
        varData[varData < 0] = float('NaN')
        
        varData = varData.tolist()[0][0]
        elems = []
        for list in varData:
            for item in list:
                elems.append(item)
        varData = pd.Series(elems).dropna()

        if exportDataFlag:
            exportData(y, tables[i], variables[i], startDate, endDate, lat1, lat2, lon1, lon2, depth1, depth2)
        try:    
            carData = varData[~np.isnan(varData)]     # remove nans
        except Exception as e:
            continue   
            
        hist, edges = np.histogram(varData, density=True, bins=50)
        
        output_notebook()
        
        p1 = figure(tools=TOOLS, toolbar_location="above", plot_width=w, plot_height=h)
        p1.yaxis.axis_label = 'Density'
        p1.xaxis.axis_label = variables[i] + ' (' +str(unit) + ')'
        leg = variables[i]
        fill_alpha = 0.4   
        cr = p1.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color="dodgerblue", line_color=None, hover_fill_color="firebrick", fill_alpha=fill_alpha, hover_alpha=0.7, hover_line_color="white", legend=leg)
        p1.add_tools(HoverTool(tooltips=None, renderers=[cr], mode='mouse'))
        p.append(p1)
    dirPath = 'embed/'
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)        
    
    #if not inline:      ## if jupyter is not the caller
    #    output_file(dirPath + fname + ".html", title="Histogram")
    #    print('test')
    show(column(p))
    return


# In[ ]:




