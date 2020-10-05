# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 15:51:58 2020

@author: sandra
"""

import os
import folium
import simplekml
from dict_processing import processing
from folium_vis_func import folium_vis
from export_kml_func import export_kml

from flask import Flask,render_template,request,redirect,url_for,send_from_directory,send_file,abort

app = Flask(__name__, template_folder='template')

@app.route('/test')

def hello():
    return 'Hello World'

@app.route('/form', methods=['GET','POST'])

def getvals():
    if request.method=="POST":
        data=request.form
        #print(data)
        data_shape, instructions = processing(data)
        global folium_map
        folium_map=data['folium_map']
        folium_map1='template/'+data['folium_map']
        shape_names={'circle':data['kml_circle'],'racecourse':data['kml_racecourse'],'line':data['kml_line']}
        global kml_names
        kml_names=[]
        for s in data_shape:
            kml_names.append(shape_names[s])
        
        if instructions[-1]=='visualise':    
            m = folium_vis(data_shape,instructions)
            m.save(folium_map1)
            return redirect(url_for('printmap'))
        
        elif instructions[-1]=='generate':
            output = export_kml(data_shape,instructions)
            z=0
            while z < len(output):
                output[z].save(kml_names[z])
                z+=1
            return redirect(url_for('downloadkml'))
    
    else:
        return render_template('form.html')
    
@app.route('/map')

def printmap():
    return render_template(folium_map)

@app.route('/download')

def downloadkml():
    try:
        for i in kml_names:
            return send_from_directory(directory=os.getcwd(),filename=i,as_attachment=True)
    except FileNotFoundError:
        abort(404)

if __name__ == "__main__":
    app.run()
    