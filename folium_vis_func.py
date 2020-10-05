# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 12:55:26 2020

@author: sandra
"""

import folium
from shapes import circle,racecourse,line

def folium_vis(data_shape,instructions):
    """
    

    Parameters
    ----------
    data_shape : shape to plot
    instructions : Instructions and parameters from website

    Returns
    -------
    m : folium Map Object

    """
    
    rp=list(instructions[0][0])
    rp = [float(x) for x in rp]
    
    #initialise map
    m = folium.Map(rp,zoom_start=14,tiles='http://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',attr='Coded and Produced by Sandra Ng Yi Ling, DSTA 2020 \u00a9') #google satellite

    #range rings
    folium.Circle(rp,500,color='purple',fill=False).add_to(m)
    folium.Circle(rp,1000,color='yellow',fill=False).add_to(m)
    folium.Circle(rp,2000,color='yellow',fill=False).add_to(m)
    folium.Circle(rp,3000,color='yellow',fill=False).add_to(m)
    folium.Circle(rp,4000,color='yellow',fill=False).add_to(m)
    folium.Circle(rp,5000,color='yellow',fill=False).add_to(m)
    folium.Circle(rp,6000,color='yellow',fill=False).add_to(m)
    folium.Circle(rp,7000,color='yellow',fill=False).add_to(m)
    
    #unpack
    params_dict = {}
    i = 0
    while i < len(data_shape):
        params_dict[data_shape[i]] = instructions[i+1][0]
        i+=1
    
    #start plotting
    for j in params_dict.keys():
        if j == 'circle':
            radius = float(params_dict['circle'][0])
            start_bearing = float(params_dict['circle'][1])
            intervals = float(params_dict['circle'][2])
            span = float(params_dict['circle'][3])
            folium.Circle(rp,radius).add_to(m)
            circle_wps=circle(rp,radius,start_bearing,intervals,span)
            for w in circle_wps:
                folium.Marker(w).add_to(m)
        elif j == 'racecourse':
            rc_nearest = float(params_dict['racecourse'][0])
            rc_furthest = float(params_dict['racecourse'][1])
            rc_span = float(params_dict['racecourse'][2])
            rc_bearing = float(params_dict['racecourse'][3])
            racecourse_wps=racecourse(rp,rc_nearest,rc_furthest,rc_span,rc_bearing)
            folium.Polygon(racecourse_wps).add_to(m)
            for r in racecourse_wps:
                folium.Marker(r).add_to(m)
            
        else:
            line_bearing = float(params_dict['line'][0])
            line_length = float(params_dict['line'][1])
            line_wp=line(rp,line_bearing,line_length)
            points=[tuple(rp),tuple(line_wp)]
            folium.PolyLine(points).add_to(m)
    
    return m
            
    
    