# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 11:53:04 2020

@author: sandra
"""

import pandas as pd

def processing(data_dict):
    #filter out shape and parameters
    data_shape=[]
    instructions=[]
    df=pd.DataFrame.from_dict(data_dict,orient='index')
    rp=df.iloc[[0,1],:]
    instructions.append(rp)
    rc=df.iloc[[2,3,4,5],:]
    circle=df.iloc[[6,7,8,9],:]
    line=df.iloc[[10,11],:]
    shapes={'circle':circle,'racecourse':rc,'line':line}
    #check if first line is empty
    for key, value in shapes.items():
        if value[0][0] is not '':
            data_shape.append(key)
        
    for s in shapes.keys():
        if s in data_shape:
            instructions.append(shapes[s])
    
    #distinguish whether it is visualise or it is generate
    if 'button1' in data_dict.keys():  #visualise
        instructions.append('visualise')    
    else:    #generate
        instructions.append('generate')
    
    return data_shape,instructions
        
    