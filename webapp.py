# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 15:51:58 2020

@author: sandra
"""

import os
import folium
from folium.plugins import Draw
import simplekml
from zipfile import ZipFile
from dict_processing import processing
from folium_vis_func import folium_vis
from export_kml_func import export_kml

from flask import Flask,render_template,render_template_string,request,redirect,url_for,send_from_directory,send_file,abort

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
            #first delete previous map
            os.chdir('template')
            templates=os.listdir(os.getcwd())
            for item in templates:
                if item != 'form.html':
                    os.remove(item)
            os.chdir('..')
            m = folium_vis(data_shape,instructions)
            m.save(folium_map1)
            return redirect(url_for('printmap'))
        
        elif instructions[-1]=='generate':
            files_in_dir=os.listdir(os.getcwd())
            for item in files_in_dir:
                if item.endswith('.zip'):
                    os.remove(item)
                elif item.endswith('.kml'):
                    os.remove(item)
                else:
                    pass
            output = export_kml(data_shape,instructions)
            z=0
            while z < len(output):
                output[z].save(kml_names[z])
                z+=1
            return redirect(url_for('downloadkml'))
        
        else:
            rp=list(instructions[0][0])
            rp = [float(x) for x in rp]
            m_draw=folium.Map(rp,zoom_start=14,tiles='http://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',attr='Coded and Produced by Sandra Ng Yi Ling, DSTA 2020 \u00a9') #google satellite
            draw=Draw()
            draw.add_to(m_draw)
            folium.Marker(rp).add_to(m_draw)
            html_string = m_draw.get_root().render()
            return render_template_string(html_string)
    
    else:
        return render_template('form.html')

@app.route('/map')

def printmap():
    return render_template(folium_map)

@app.route('/download')

def downloadkml():
    try:
        with ZipFile('all_kmls.zip','w') as zip:
            for file in kml_names:
                zip.write(file)
        return send_from_directory(directory=os.getcwd(),filename='all_kmls.zip',as_attachment=True)
    except FileNotFoundError:
        abort(404)

if __name__ == "__main__":
    app.run()
    