# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 13:18:41 2020

@author: sandra
"""

import folium
import simplekml
from dict_processing import processing
from folium_vis_func import folium_vis
from export_kml_func import export_kml

data = dict([('rp_lat', '1.370075'), ('rp_long', '103.983342'), ('rc_nearest', '1800'), ('rc_furthest', '3300'), ('rc_span', '200'), ('rc_bearing', '42'), ('circle_radius', ''), ('start_bearing', ''), ('intervals', ''), ('span', ''), ('line_bearing', ''), ('line_length', ''), ('folium_map', ''), ('kml_circle', ''), ('kml_racecourse', 'racecourse_test.kml'), ('kml_line', ''), ('button2', 'generate')])

data_shape, instructions = processing(data)
folium_map=data['folium_map']
shape_names={'circle':data['kml_circle'],'racecourse':data['kml_racecourse'],'line':data['kml_line']}
kml_names=[]
for s in data_shape:
    kml_names.append(shape_names[s])

if instructions[-1]=='visualise':    
    m = folium_vis(data_shape,instructions)
    m.save(folium_map)
elif instructions[-1]=='generate':
    output = export_kml(data_shape,instructions)
    z=0
    while z < len(output):
        output[z].save(kml_names[z])
        z+=1
