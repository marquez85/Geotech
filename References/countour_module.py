import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.path as mplp

import time
import imp
import math

from scipy.interpolate import UnivariateSpline 
from scipy.interpolate import griddata


import numpy as np
import numpy.ma as ma
import numpy.matlib as npm

import pandas as pd
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry import MultiPoint


import random
import sys
from fractions import Fraction
from References.outline_to_mask_module import outline_to_mask
import streamlit as st

def contour_mode(project_name,rev,df,Phase,ref_poly_a,countour_name,intr_disp,intr_load):
    
    list_poly_a=[]
    ref_poly_path=r"References/"+ref_poly_a+r".xlsx"
    ad=pd.ExcelFile(ref_poly_path)
    for i in ad.sheet_names:
        pd_b=pd.read_excel(ref_poly_path,sheet_name=i,header=0)
        bound=pd_b.values.tolist()
        poly=Polygon(bound)
        list_poly_a.append(poly)
        

    
    
    mask=df["Stage"]==Phase
    df.dropna(axis=0,how="any",inplace=True)

    df["Settlement (m)"]=df["Settlement (mm)"]/1000
    df["Axial Force Envelope min (kN)"]=df["Axial Force Envelope min (kN)"]

    h=df[mask]
    targetname=h["Pile Name"].tolist()
    targetx=h["X (m)"].tolist()
    targety=h["Y (m)"].tolist()
    targetz_load=h["Axial Force Envelope min (kN)"].tolist()
    targetz_displacements=h["Settlement (mm)"].tolist()
    targetz_gradient=h["Settlement (m)"].tolist()
    ## Mesh Grid generation
    n=200
    xip=np.linspace(min(targetx)-5,max(targetx)+5,n);
    yip=np.linspace(min(targety)-5,max(targety)+5,n);
    dx,dy=np.meshgrid(xip,yip)
    
    ## Data interpolation for contours
    pix=np.array(targetx)
    piy=np.array(targety)
    piz_disp=np.array(targetz_displacements)
    piz_load=np.array(targetz_load)

    Spi_disp=griddata((pix,piy),piz_disp,(dx,dy))
    Spi_load=griddata((pix,piy),piz_load,(dx,dy))
    
    ev_string=""
    mask_list=[]
    inc=0
    for i in list_poly_a:
        mask_i=outline_to_mask(i.boundary, xip, yip)
        mask_list.append(mask_i)
        if inc==0:
            ev_string=ev_string+"mask_list[{}]".format(inc)
        else:
    
            ev_string=ev_string+"| mask_list[{}]".format(inc)
        inc=inc+1
    
    mask_total=eval(ev_string)
#     mask_total=np.any(mask_list)


    Spi_disp_new=ma.masked_array(Spi_disp,~mask_total)
    Spi_load_new=ma.masked_array(Spi_load,~mask_total)
    
    plt.close()

    intr=0.0003
    vgrad=np.gradient(Spi_disp_new/1000)
    mag = np.sqrt(vgrad[0]**2 + vgrad[1]**2)

    def fmt(x, pos):
        ine=1/x
        a = "{:.0f}".format(ine)
        return '1/{}'.format(a)

    f,(ax1,ax2,ax3)=plt.subplots(3,1,figsize=(20,40))

    plt.suptitle('{} \n PLAXIS 3D Contour Plots ({}) \n {}'.format(project_name,countour_name,rev),fontsize=25)

    plot_ax1=ax1.contourf(dx,dy,Spi_disp_new,levels=list(np.arange(int(np.amin(targetz_displacements))-0,int(np.amax(targetz_displacements))+1,intr_disp)),cmap='jet_r',extend='both')
    ax1.title.set_text('Vertical displacement (mm)')
    ax1.title.set_fontsize(20)
    cbr=f.colorbar(plot_ax1,extendfrac='auto',ax=ax1)
    cbr.ax.tick_params(labelsize=14)
    test=ax1.contour(dx,dy,Spi_disp_new,levels=list(np.arange(int(np.amin(targetz_displacements))-0,int(np.amax(targetz_displacements))+1,intr_disp)),colors=('k',),linewidths=(2,))
    ax1.clabel(test, fmt='%.0f', colors='black', fontsize=14)
    ax1.plot(targetx,targety,'o',color='black',markerfacecolor="white",markersize=5)
    ax1.grid(color="grey",linestyle="--")
    ax1.set_xlabel('X (m)',fontsize=16)
    ax1.set_ylabel('Y (m)',fontsize=16)
    ax1.tick_params(labelsize=14)
    ax1.axis('equal')


    plot_ax2=ax2.contourf(dx,dy,mag,levels=list(np.arange(0,(0.0022),intr)),cmap='jet',extend='both')
    ax2.title.set_text('Differential movements ratio - Gradient')
    ax2.title.set_fontsize(20)
    cbr=f.colorbar(plot_ax2,extendfrac='auto',ax=ax2,format=ticker.FuncFormatter(fmt))
    cbr.ax.tick_params(labelsize=14)
    test=ax2.contour(dx,dy,mag,levels=list(np.arange(0,0.0022,intr)),colors=('k',),linewidths=(2,))
    ax2.clabel(test, fmt=ticker.FuncFormatter(fmt), colors='white', fontsize=14)
    ax2.plot(targetx,targety,'o',color='black',markerfacecolor="white",markersize=5)
    ax2.grid(color="grey",linestyle="--")
    ax2.set_xlabel('X (m)',fontsize=16)
    ax2.set_ylabel('Y (m)',fontsize=16)
    ax2.tick_params(labelsize=14)
    ax2.axis('equal')






    ax3.title.set_text('Vertical Load (kN)') 
    ax3.title.set_fontsize(20)
    plot_ax3=ax3.contourf(dx,dy,Spi_load_new,levels=list(np.arange(int(np.amin(targetz_load))-0,int(np.amax(targetz_load))+1,intr_load)),cmap='jet_r',extend='both')
    cbr=f.colorbar(plot_ax3,extendfrac='auto',ax=ax3)
    cbr.ax.tick_params(labelsize=14)
    test=ax3.contour(dx,dy,Spi_load_new,levels=list(np.arange(int(np.amin(targetz_load))-0,int(np.amax(targetz_load))+1,intr_load)),colors=('k',),linewidths=(2,))
    ax3.clabel(test, fmt='%.0f', colors='black', fontsize=14)
    ax3.plot(targetx,targety,'o',color='black',markerfacecolor="white",markersize=5)
    ax3.grid(color="grey",linestyle="--")
    ax3.set_xlabel('X (m)',fontsize=16)
    ax3.set_ylabel('Y (m)',fontsize=16)
    ax3.tick_params(labelsize=14)
    ax3.axis('equal')

    plt.tight_layout(pad=4)
    
    
    # plt.draw()

    # plt.pause(1)
    
    return f,(ax1,ax2,ax3),h
    

        
        