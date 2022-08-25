
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.path as mplp
import os

import time
import imp
import math
from streamlit_tags import st_tags
from streamlit_tags import st_tags_sidebar

from scipy.interpolate import UnivariateSpline 
from scipy.interpolate import griddata

from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image,Frame
from reportlab.lib.styles import getSampleStyleSheet
from  reportlab.platypus import PageBreak
from reportlab.lib.units import inch,cm
from reportlab.lib import utils
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.enums import TA_LEFT
import io



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
import streamlit as st

from References.master_pile_schudule_module_streamlit_rev1 import masterpileschudule
from References.outline_to_mask_module import outline_to_mask
from References.countour_module import contour_mode
from References.plot_functions import plotplaxispilelayout


def add_text(text, style="Normal", fontsize=12):
    """ Adds text with some spacing around it to  PDF report 

    Parameters
    ----------
    text : str
        The string to print to PDF

    style : str
        The reportlab style

    fontsize : int
        The fontsize for the text
    """
    Story.append(Spacer(1, 12))
    ptext = "<font size={}>{}</font>".format(fontsize, text)
    Story.append(Paragraph(ptext, styles[style]))
    Story.append(Spacer(1, 12))
                        
def get_image(path, width=1*cm):
                        
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))




@st.cache
def load_summary(project_name,rev):
    try:
        data = pd.read_excel("Pile schedule excel {} {} - Part 1.xlsx".format(project_name,rev),sheet_name="Summary",header=0)
        data.drop("AKT Pile Ref",axis=1,inplace=True)
        data.rename(columns={"AKT Pile Ref.1":"Pile Ref"},inplace=True)
        s=1
        return data,s

    except FileNotFoundError: 
        data_error=0
        s=0
        return data_error,s

   
@st.cache
def load_pile_data(pile,index):
    multiple=1
    while index >= 25*multiple:
        multiple=multiple+1
    try:
        data=pd.read_excel("Pile schedule excel {} {} - Part {}.xlsx".format(project_name,rev,multiple),sheet_name="Pile{}".format(pile),header=0)
        s=1
        return data,s
    except FileNotFoundError: 
        data_error=0
        s=0
        return data_error,s
    
@st.cache(allow_output_mutation=True)
def load_pile_head(project_name,rev):
    try:
        data=pd.read_excel("Pile results {} {}.xlsx".format(project_name,rev),sheet_name="Summary",header=0)
        data.dropna(axis=0,how="any",inplace=True)
        s=1
        return data,s

    except FileNotFoundError: 
        data_error=0
        s=0
        return data_error,s
    
    
    
def plots (f,ax,df_pile,pile,phases,name_dic):
    for i in phases:
                name=name_dic[i]
                # st.write("Plotting {} in {}".format(i,pile))
                mask=df_pile["Phase"]==i
                df_i=df_pile[mask]
                # st.write(df_pile[mask])
                elev=df_i["Elevation (mOD)"].tolist()
                disp=df_i["Vertical displacement uz (mm)"].tolist()
                axial=df_i["N (kN)"]
                bending=df_i["M SLS resultant(kNm)"]
                shear=df_i["Q SLS resultant (kN)"]
                
            
                ax[0,0].plot(disp,elev,label=name)
                ax[0,1].plot(axial,elev,label=name)    
                ax[1,1].plot(bending,elev,label=name)
                ax[1,0].plot(shear,elev,label=name)
            
    ax[0,0].title.set_text('Vertical Displacement uz (mm)')
    ax[0,0].title.set_fontsize(13)
    ax[0,0].set_xlabel('Displacements (mm)',fontsize=10)
    ax[0,0].xaxis.set_label_position('top') 
    xmin,xmax=ax[0,0].get_xlim()
    # ax[0,0].set_xlim(0,xmax)
    ax[0,0].set_xlim(0,50)
    ax[0,0].set_ylabel('Elevation (mOD)',fontsize=10)
    ax[0,0].grid(color="grey",linestyle="--")
    ax[0,0].xaxis.tick_top()
    # ax[0,0].set_xticklabels() 
    # ax[0,0].legend(bbox_to_anchor=(0, 1),loc='upper left')
    
    ax[0,1].title.set_text('Axial Force N (kN)')
    ax[0,1].title.set_fontsize(13)
    ax[0,1].set_xlabel('Axial force (kN)',fontsize=10)
    ax[0,1].xaxis.set_label_position('top') 
    xmin,xmax=ax[0,1].get_xlim()
    # ax[0,1].set_xlim(0,xmax)
    ax[0,1].set_xlim(0,5000)
    ax[0,1].set_ylabel('Elevation (mOD)',fontsize=10)
    ax[0,1].grid(color="grey",linestyle="--")
    ax[0,1].xaxis.tick_top()
    ax[0,1].legend(bbox_to_anchor=(1.0, 1),loc='upper left')
    
    ax[1,0].title.set_text('Shear force V (kN)')
    ax[1,0].title.set_fontsize(13)
    ax[1,0].set_xlabel('Shear force (kN)',fontsize=10)
    ax[1,0].xaxis.set_label_position('top') 
    xmin,xmax=ax[1,0].get_xlim()
    # ax[1,0].set_xlim(0,xmax)
    ax[1,0].set_xlim(0,700)
    ax[1,0].set_ylabel('Elevation (mOD)',fontsize=10)
    ax[1,0].grid(color="grey",linestyle="--")
    ax[1,0].xaxis.tick_top()
    # ax[1,0].legend(bbox_to_anchor=(1.0, 1),loc='upper left')
    
    ax[1,1].title.set_text('Bending Moments M (kN.m)')
    ax[1,1].title.set_fontsize(13)
    ax[1,1].set_xlabel('Moments (kN.m)',fontsize=10)
    ax[1,1].xaxis.set_label_position('top') 
    xmin,xmax=ax[1,1].get_xlim()
    # ax[1,1].set_xlim(0,xmax)
    ax[1,1].set_xlim(0,2500)
    ax[1,1].set_ylabel('Elevation (mOD)',fontsize=10)
    ax[1,1].grid(color="grey",linestyle="--")
    ax[1,1].xaxis.tick_top()
    # ax[1,1].legend(bbox_to_anchor=(1.0, 1),loc='upper left')
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf)
    buf.seek(0)
    
    
    return(f,ax,buf)

##########################################################################################
st.title("PLAXIS 3D's Pile results extracter and post-processor")
st.markdown("**Creator**: FM")
st.markdown("*General version - Rev 1.0*")
st.markdown("*Extraction version - Rev 1*")
st.markdown("*Contour generator version - Rev 1*")

st.sidebar.title("Basic project information")
project_name=st.sidebar.text_input("Project name", key="name")
rev=st.sidebar.text_input("Revison name", key="name2")

st.sidebar.title("PLAXIS 3D's calculation and extraction options")
st.sidebar.markdown("*Note: PLAXIS Remote scripting connection is required for any of the options below*")          
#intro=st.image(r"References\AKT II logo.png")
#intro=st.image(r"https://github.com/marquez85/Geotech/blob/main/References/akt.PNG")

calculation_check=st.sidebar.checkbox('Calculate PLAXIS 3D model before')
extraction_mode=st.sidebar.checkbox("Extract PLAXIS 3D's Piles results")
pileplots_all=st.sidebar.checkbox("Create and save Plots for all piles")

if calculation_check or extraction_mode or pileplots_all:
    ip=st.sidebar.text_input("User IP address", key="ip_address")
    password=st.sidebar.text_input("PLAXIS password", key="password",type="password")
    
    
    Phase_name_extract = st_tags_sidebar(
        label='Enter the names of construction sequences to extract ( in order):',
        text='Press enter to add more names',
        maxtags =20,
        key='1')
    st.sidebar.write(Phase_name_extract)
    
    Phase_extract = st_tags_sidebar(
        label='Enter the Phases index number to extract ( in order):',
        text='Press enter to add more phases',
        maxtags =20,
        key='2')
    st.sidebar.write(Phase_extract)
    st.sidebar.write("From the list above,")
    
    
    
    
    boundary_box=st.sidebar.text_input("Input the index number that matches the phase when the piles start acting as pile group")
    if boundary_box=="":
        boundary_box=0
    # st.write(type(boundary_box))
    # st.write(boundary_box)
    boundary=1+int(boundary_box)
        
    
     
        
    if st.sidebar.button('Click here to start PLAXIS 3D calculation &/or Result extraction!'):
        with st.spinner("Script working....."):
            # intro.empty()
            # cat_working=st.image("https://media2.giphy.com/media/ule4vhcY1xEKQ/giphy.gif?cid=ecf05e47dgzvok7otah9w3yeatf8c55dnlacjq33s2y99zh4&rid=giphy.gif&ct=g")
            
            cat_working=st.image("https://media3.giphy.com/media/V4NSR1NG2p0KeJJyr5/giphy.gif?cid=ecf05e47rpfhe57v1yrc5zzhvzln14khmzsn7orgczj1mvw8&rid=giphy.gif&ct=g")
            if calculation_check or extraction_mode:
                
                from plxscripting.easy import *
                localhostport_input = 21403 
                localhostport_output = 10001
                s,g = new_server(ip, localhostport_input, password=password)
                s_o,g_o=new_server(ip, localhostport_output, password=password)
                
                g.gotostages()
            
                st.write("Connection to PLAXIS Remote Server sucessuful")
            
            if calculation_check:
                st.write("Running PLAXIS 3D model first as instructed...")
                g.gotostages()
                for pha in g.Phases:
                    pha.ShouldCalculate=True
                g.calculate()
                st.write("Calculation finished. Saving model...")
                g.save()
            
            
            if extraction_mode:
                st.write("Opening now PLAXIS OUTPUT")
                masterpileschudule(s,g,s_o,g_o,project_name,rev,Phase_extract,boundary)
                st.write("Pile results extracted and exported to excel file")
                cat_working.empty()
                st.image("https://c.tenor.com/TGH4D9JDwrAAAAAC/chuck-norris-thumbs-up.gif")
            
            if pileplots_all:
                
                dic_buf={}
                c=Canvas('Force Plots all piles_{}_{}.pdf'.format(project_name,rev),
                        pagesize=landscape(A4))

                st.write("Creating Force/displacement diagrams for all the piles/phases")
                df_summary_all,s_error=load_summary(project_name,rev)
                st.dataframe(df_summary_all)
                
                all_piles=df_summary_all["Pile Ref"].tolist()
                latest_iteration = st.empty()
                bar = st.progress(0)
                index=0
                for i in all_piles:
                # for i in all_piles[0:3]:    
                    index=index+1
                    percentage=(index/len(all_piles))
                    latest_iteration.text("Plotting {}".format(i))
                    bar.progress(percentage)
                    # st.write("Plotting {}".format(i))
                    index_pile=df_summary_all.index[df_summary_all['Pile Ref'] == i][0]
                    df_pile_all,s_error2=load_pile_data(i,index_pile)
                    # st.dataframe(df_pile_all)
                    available_phases_all=df_pile_all["Phase"].unique().tolist()
                    dic_name=dict(zip(Phase_extract, Phase_name_extract))
                    
                    f_all,ax_all= plt.subplots(2,2,figsize=(10,15))
                    # f_all.suptitle("Project: {} -- PLAXIS run: {} --Pile {}".format(project_name,rev,i), fontsize=15)
                    f_all,ax_all,buf=plots(f_all,ax_all,df_pile_all,i,Phase_extract,dic_name)
                    dic_buf.update({"Plot_{}".format(i):buf})
                    plt.savefig(r".\Results\Plots_{}_{}_{}.pdf".format(i,project_name,rev),dpi=100)
                    x_pile=df_summary_all.loc[index_pile,"PLAXIS X (m)"]
                    y_pile=df_summary_all.loc[index_pile,"PLAXIS Y (m)"]
                    diam=df_summary_all.loc[index_pile," Pile Diameter (mm)"]
                    cut=df_summary_all.loc[index_pile,"Cut-off Level (mOD)"]
                    toe=df_summary_all.loc[index_pile,"Pile Toe Level (mOD)"]
                    buf_layout=plotplaxispilelayout(project_name,rev,i,x_pile,y_pile,df_summary_all,title='Pile Layout')
                    dic_buf.update({"layout_{}".format(i):buf_layout})
                    
                    c.drawImage(r".\References\akt.PNG", x=26*cm,y=17*cm,width=3*cm, preserveAspectRatio=True)
                    story1=[]
                    image_buffer2 = buf
                    story1.append(get_image(image_buffer2, width=14*cm))
                    f1=Frame(2.5*cm,-23.7*cm,10*cm,45*cm,showBoundary=0)
                    f1.addFromList(story1,c)
                
                    story2=[]
                    #a.hAlign=("RIGHT")
                    image_buffer3 = buf_layout
                    story2.append(get_image(image_buffer3, width=16.5*cm))
                    f2=Frame(13*cm,-4.5*cm,15*cm,20*cm,showBoundary=0)
                    f2.addFromList(story2,c)
                    
                    
                    styles = getSampleStyleSheet()
                    headline_style_left=styles["Heading1"]
                    headline_style_left.alignment=TA_LEFT
                    story3=[Paragraph("Force/Displacement plots in Pile {}".format(i),headline_style_left),Spacer(1, 5),]
                    story3.append(Paragraph("Project Name: {}".format(project_name),getSampleStyleSheet()["Normal"]))
                    story3.append(Spacer(1, 5))
                #     story3.append(Paragraph("Title: Plate Load Test Analysis - {}".format(sd[i]),getSampleStyleSheet()["Normal"]))
                #     story3.append(Spacer(1, 5))
                    story3.append(Paragraph("PLAXIS Revison --{} ".format(rev),getSampleStyleSheet()["Normal"]))
                    story3.append(Spacer(1, 5))
                    story3.append(Paragraph("Made by FM",getSampleStyleSheet()["Normal"]))
                    story3.append(Spacer(1, 15))
                    
                    story3.append(Paragraph("<strong>Pile number:{}</strong>".format(i),getSampleStyleSheet()["Normal"]))
                    story3.append(Spacer(1, 5))
                    story3.append(Paragraph("<strong>Diameter:{} mm</strong>".format(diam),getSampleStyleSheet()["Normal"]))
                    story3.append(Spacer(1, 5))
                    story3.append(Paragraph("<strong>Cut-off level in PLAXIS:{} mOD</strong>".format(cut),getSampleStyleSheet()["Normal"]))
                    story3.append(Spacer(1, 5))
                    story3.append(Paragraph("<strong>Toe level in PLAXIS:{} mOD</strong>".format(toe),getSampleStyleSheet()["Normal"]))
                    story3.append(Spacer(1, 5))
                    f3=Frame(14.5*cm,10*cm,15*cm,11*cm,showBoundary=0)
                    f3.addFromList(story3,c)
                    c.showPage()
                    plt.close()
                    
                c.save()

    
                
            cat_working.empty()

st.sidebar.title("Iteractive Pile Results Inspection Options")   
st.sidebar.markdown("*Note: if any of the option below is run in isolation, then make sure that pile results have been exported first and saved in the folder*")          
    
inspect_mode=st.sidebar.checkbox("Interactive Pile results's Plots")        
if len(project_name) !=0 and len(rev) !=0 and inspect_mode:
    st.markdown("# Pile results plots inspection mode")
    df_results,s_error=load_summary(project_name,rev)
    st.write(s_error)
    if s_error ==1:
        st.dataframe(df_results)
        add_selectbox= st.selectbox('Which Pile number who wish to generate plots?',df_results['Pile Ref'])
        index_pile=df_results.index[df_results['Pile Ref'] == add_selectbox][0]
        # st.write(index_pile)
        df_pile,s_error2=load_pile_data(add_selectbox,index_pile)
        # st.dataframe(df_pile)
        
        available_phases=df_pile["Phase"].unique().tolist()
        selection=st.multiselect('Generate plots in which phases?', available_phases)
        f,ax= plt.subplots(2,2,figsize=(10,15))
        f.suptitle("Project: {} -- PLAXIS run: {} --Pile {}".format(project_name,rev,add_selectbox), fontsize=15)
        f,ax=plots(f,ax,df_pile,add_selectbox,available_phases)
        
        plt.savefig(r'temp\x.png')

        st.image(r'temp\x.png')
        # os.remove('x.png')
        with open("x.png", "rb") as file:
            st.download_button(
                label="Download Plots",
                data=file,
                file_name=r"{}_{}_{} plots.png".format(project_name,add_selectbox,rev),
                mime="image/png")
    else:
             st.error("Please input basic data or extract first the pile results from PLAXIS 3D model ")
             

contours_mode=st.sidebar.checkbox("Generate contour Plots")
if contours_mode:
    poly_ref=st.sidebar.text_input("File name for polygon boundaries", key="polylist")
    intr_disp=st.sidebar.text_input("Countour intervals for displacements (mm)", key="intra_disp")
    intr_load=st.sidebar.text_input("Countour intervals for loads (kN)", key="intra_disp2")          
    df_pile_head,s_error_c=load_pile_head(project_name,rev)
    df_pilehead_cont=df_pile_head
    if len(project_name) !=0 and len(rev) !=0 and contours_mode and len(poly_ref)!=0 and len(intr_disp)!=0 and len(intr_load)!=0 :
        st.markdown("# Countour Plots creation mode")

        if s_error_c==1:
            # st.dataframe(df_pilehead_cont)
            add_selectbox_phase= st.selectbox('Which Phase who wish to generate plots?',df_pilehead_cont['Stage'].unique())
            intr_disp_float=float(intr_disp)
            intr_load_float=float(intr_load)
            
            countour_name=st.text_input("What is the name this construction phase?",key="name_phase_cont")
            
            if len(countour_name)!=0 and len(add_selectbox_phase)!=0:
                f_c,(ax1,ax2,ax3),h=contour_mode(project_name,rev,df_pilehead_cont,add_selectbox_phase,poly_ref,countour_name,intr_disp_float,intr_load_float)
                
                plt.savefig(r'temp\{} Contour All {} {}.png'.format(project_name,countour_name,rev))
      
                st.image(r'temp\{} Contour All {} {}.png'.format(project_name,countour_name,rev))
                st.dataframe(h)
                
                with open(r'temp\{} Contour All {} {}.png'.format(project_name,countour_name,rev), "rb") as file:
                    st.download_button(
                        label="Download Plots",
                        data=file,
                        file_name='{} Contour All {} {}.png'.format(project_name,countour_name,rev),
                    mime="image/png")
          
        else:
                 st.error("Please input basic data or extract first the pile results from PLAXIS 3D model ")    
        
      
