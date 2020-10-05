# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 13:26:38 2020

@author: sandra
"""
from shapes import circle,racecourse,line
import simplekml

def export_kml(data_shape,instructions):
    """
    

    Parameters
    ----------
    data_shape : shape to plot
    instructions : Instructions and parameters from website

    Returns
    -------
    kmls : kml objects

    """
    
    rp=list(instructions[0][0])
    rp = [float(x) for x in rp]
    
    params_dict = {}
    i = 0
    while i < len(data_shape):
        params_dict[data_shape[i]] = instructions[i+1][0]
        i+=1
        
        
    kmls = []
    
    #start plotting
    for j in params_dict.keys():
        if j == 'circle':
            radius = float(params_dict['circle'][0])
            start_bearing = float(params_dict['circle'][1])
            intervals = float(params_dict['circle'][2])
            span = float(params_dict['circle'][3])
            circle_wps=circle(rp,radius,start_bearing,intervals,span)
            i=0
            while i < len(circle_wps):
                circle_wps[i]=[circle_wps[i][1],circle_wps[i][0]]
                i+=1
            
            circle_wps.append(circle_wps[0])    
            circle_tuples=[tuple(k) for k in circle_wps]
            kml_circle = simplekml.Kml()
            polygon_kml = kml_circle.newpolygon(name = 'Racecourse',outerboundaryis=circle_tuples)

            polygon_kml.style.linestyle.color = simplekml.Color.blue
            polygon_kml.style.linestyle.width = 3
            polygon_kml.style.polystyle.color = simplekml.Color.changealphaint(0, simplekml.Color.green)
            kmls.append(kml_circle)
                
        elif j == 'racecourse':
            rc_nearest = float(params_dict['racecourse'][0])
            rc_furthest = float(params_dict['racecourse'][1])
            rc_span = float(params_dict['racecourse'][2])
            rc_bearing = float(params_dict['racecourse'][3])
            racecourse_wps=racecourse(rp,rc_nearest,rc_furthest,rc_span,rc_bearing)
            i=0
            while i < len(racecourse_wps):
                racecourse_wps[i]=[racecourse_wps[i][1],racecourse_wps[i][0]]
                i+=1
            
            racecourse_wps.append(racecourse_wps[0])    
            racecourse_tuples=[tuple(k) for k in racecourse_wps]
            kml_racecourse = simplekml.Kml()
            polygon_kml = kml_racecourse.newpolygon(name = 'Racecourse',outerboundaryis=racecourse_tuples)

            polygon_kml.style.linestyle.color = simplekml.Color.blue
            polygon_kml.style.linestyle.width = 3
            polygon_kml.style.polystyle.color = simplekml.Color.changealphaint(0, simplekml.Color.green)
            kmls.append(kml_racecourse)
            
        else:
            line_bearing = float(params_dict['line'][0])
            line_length = float(params_dict['line'][1])
            line_wp=line(rp,line_bearing,line_length)
            points=[rp,line_wp]
            i=0
            while i < len(points):
                points[i]=[points[i][1],points[i][0]]
                i+=1
            line_tuples=[tuple(k) for k in points]
            kml_line=simplekml.Kml()
            lines = kml_line.newlinestring(name='Path',coords=points)
            lines.style.linestyle.width=3
            lines.style.linestyle.color=simplekml.Color.blue
            kmls.append(kml_line)

    return kmls