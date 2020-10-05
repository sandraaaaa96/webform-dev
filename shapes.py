# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 12:05:17 2020

@author: sandra
"""
import numpy as np
from geographiclib.geodesic import Geodesic
geod=Geodesic.WGS84

def circle(rp,radius,start_bearing,intervals,span):
    """
    Generates waypoints of a circle / sector centered around the reference point.

    Parameters
    ----------
    rp : reference point in a list [lat,long]
    radius : radius of circle in m
    start_bearing: which bearing to start counting from
    intervals : angular intervals in degrees
    span: range of angles

    Returns
    -------
    wp_ll : list of [lat,long] of all the waypoints

    """
    
    bearings=np.arange(start_bearing,start_bearing+span+intervals,intervals)%360
    wp_ll=[]
    for bearing in bearings:
        l_true = geod.Direct(rp[0],rp[1],bearing,radius)
        wp_ll.append([l_true['lat2'],l_true['lon2']])
    
    return wp_ll

def racecourse(rp,nearest,furthest,span,bearing):
    """
    Generates a racecourse profile directed at a nearest and furthest distance
    away from the reference point pointed in a defined bearing.

    Parameters
    ----------
    rp : reference point in a list [lat,long]
    nearest : nearest distance to rp (m)
    furthest : furthest distance to rp (m)
    span : width of racecourse (m)
    bearing : pointing of rc

    Returns
    -------
    wp_ll : list of [lat,long] of all the waypoints

    """
    
    l_near = geod.Direct(rp[0],rp[1],bearing,nearest)
    l_far = geod.Direct(rp[0],rp[1],bearing,furthest)
    perp_right=(bearing+90)%360
    perp_left=(bearing-90)%360
    l_right_bot=geod.Direct(l_near['lat2'],l_near['lon2'],perp_right,span/2)
    l_left_bot=geod.Direct(l_near['lat2'],l_near['lon2'],perp_left,span/2)
    l_right_top=geod.Direct(l_far['lat2'],l_far['lon2'],perp_right,span/2)
    l_left_top=geod.Direct(l_far['lat2'],l_far['lon2'],perp_left,span/2)
    wp_ll=[]
    wp_ll.append([l_right_bot['lat2'],l_right_bot['lon2']])
    wp_ll.append([l_left_bot['lat2'],l_left_bot['lon2']])
    wp_ll.append([l_left_top['lat2'],l_left_top['lon2']])
    wp_ll.append([l_right_top['lat2'],l_right_top['lon2']])
    
    return wp_ll

def line(rp,bearing,length):
    """
    Generates a line profile directed at a particular bearing from the reference
    point.

    Parameters
    ----------
    rp : reference point in a list [lat,long]
    bearing : bearing in degrees from true north
    length : distance in m

    Returns
    -------
    wp_ll : [lat,long] of endpoint

    """
    l_true = geod.Direct(rp[0],rp[1],bearing,length)
    wp_ll=[l_true['lat2'],l_true['lon2']]
    
    return wp_ll