#!/usr/bin/env python
# coding: utf-8

# ## Reformat NetCDF4 File for Function Call

# In[583]:


import opedia
import math
import common as com
from opedia import plotRegional as REG
import netCDF4
import xarray as xr
import numpy as np
from datetime import datetime
from dateutil.parser import parse
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column
from bokeh.palettes import all_palettes
from bokeh.models import HoverTool, LinearColorMapper, BasicTicker, ColorBar, DatetimeTickFormatter
from bokeh.models.annotations import Title
from bokeh.embed import components
from tqdm import tqdm_notebook as tqdm
from netCDF4 import num2date, date2num

tFile = netCDF4.Dataset('http://engaging-opendap.mit.edu:8080/thredds/dodsC/las/id-a1d60eba44/data_usr_local_tomcat_content_cbiomes_20190510_20_darwin_v0.2_cs510_darwin_v0.2_cs510_nutrients.nc.jnl')


# In[582]:


tables = [tFile]
variables = ['O2']
startDate = '1969-12-31'
endDate = '1969-12-31'
lat1, lat2 = -89, 80
lon1, lon2 = -179, 179
depth1, depth2 = tFile.variables['DEP_C'][:][0], tFile.variables['DEP_C'][:][len(tFile.variables['DEP_C'][:]) - 1]
fname = 'regional'
exportDataFlag = False

regionalMap(tables, variables, startDate, endDate, lat1, lat2, lon1, lon2, depth1, depth2, fname, exportDataFlag)


# ### RegionalMap Method (Takes NetCDF4 Files) ###

# In[581]:


def regionalMap(tables, variabels, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2, fname, exportDataFlag):
    for i in tqdm(range(len(tables)), desc='overall'):
        subTime = dt1
        
        #testing goin' on here-----------------------
       # df = xr.open_dataset(tables[i])
        
        #testing------------------------------------
        
        dt1 = date2num(datetime.combine(datetime.strptime(dt1, '%Y-%m-%d'), datetime.min.time()), units = (tables[i].variables['TIME'].units))
        dt2 = date2num(datetime.combine(datetime.strptime(dt2, '%Y-%m-%d'), datetime.min.time()), units = (tables[i].variables['TIME'].units))
        times = tables[i].variables['TIME'][:]
        minTimeIndex = findClosestIndex(times, dt1)
        maxTimeIndex = (np.abs(times[::-1] - dt2)).argmin() + 1
        
        lats = tables[i].variables['LAT_C'][:]
        lons = tables[i].variables['LON_C'][:]
        
        minLatDex = findClosestIndex(lats, lat1)
        maxLatDex = findClosestIndex(lats, lat2) + 1
        minLonDex = findClosestIndex(lons, lon1)
        maxLonDex = findClosestIndex(lons, lon2) + 1
        
        lats = lats[minLatDex : maxLatDex]
        lons = lons[minLonDex : maxLonDex]
        varData = tables[i].variables[variables[i]][0, 0, minLatDex : maxLatDex, minLonDex : maxLonDex]
        
        unit = '[' + variables[i] + ' [' + tables[i].variables[variables[i]].units + '], time: ' + str(subTime) + ']'
        
        shape = (len(lats), len(lons))
        varData.reshape(shape)
        
        lats = [np.asarray(lats)]
        lons = [np.asarray(lons)]
        varData[varData < 0] = float('NaN')
        varData = [np.asarray(varData)]
        
        bokehMap(varData, unit, 'regional', lats, lons, unit, 'OTHER', variables[i])


# In[406]:


def bokehMap(data, subject, fname, lat, lon, units, tables, variabels):
    TOOLS="crosshair,pan,zoom_in,wheel_zoom,zoom_out,box_zoom,reset,save,"
    p = []
    for ind in range(len(data)):
        w, h = com.canvasRect(dw=np.max(lon[ind])-np.min(lon[ind]), dh=np.max(lat[ind])-np.min(lat[ind]))
        p1 = figure(tools=TOOLS, toolbar_location="right", title=subject[ind], plot_width=w, plot_height=h, x_range=(np.min(lon[ind]), np.max(lon[ind])), y_range=(np.min(lat[ind]), np.max(lat[ind])))
        p1.xaxis.axis_label = 'Longitude'
        p1.yaxis.axis_label = 'Latitude'
    
        unit = units
        
        bounds = com.getBounds(variabels[ind])
        
        paletteName = com.getPalette(variabels[ind])
        low, high = bounds[0], bounds[1]
        
        if low == None:
            low, high = np.nanmin(data[ind].flatten()), np.nanmax(data[ind].flatten())
        color_mapper = LinearColorMapper(palette=paletteName, low=low, high=high)
        p1.image(image=[data[ind]], color_mapper=color_mapper, x=np.min(lon[ind]), y=np.min(lat[ind]), dw=np.max(lon[ind])-np.min(lon[ind]), dh=np.max(lat[ind])-np.min(lat[ind]))
        p1.add_tools(HoverTool(
            tooltips=[
                ('longitude', '$x'),
                ('latitude', '$y'),
                (variabels[ind]+unit, '@image'),
            ],
            mode='mouse'
        ))
        color_bar = ColorBar(color_mapper=color_mapper, ticker=BasicTicker(),
                        label_standoff=12, border_line_color=None, location=(0,0))
        p1.add_layout(color_bar, 'right')
        p.append(p1)
    if len(p) > 0:
       # if not inline:      ## if jupyter is not the caller
       #     dirPath = 'embed/'
       #     if not os.path.exists(dirPath):
       #         os.makedirs(dirPath)        
       #     output_file(dirPath + fname + ".html", title="Regional Map")
        show(column(p))
    return


# In[356]:


def findClosestIndex(list, value):
    array = np.asarray(list)
    index = (np.abs(list - value)).argmin()
    return index


# In[ ]:



