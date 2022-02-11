import matplotlib.pyplot as plt
import time
import imp
import math
from scipy.interpolate import UnivariateSpline 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from shapely.geometry import Point
from shapely.geometry import Polygon
import random
import sys



def masterpileschudule(s,g,s_output,g_output,project_name,m_n,Phase_extract,boundary):

    start_time=time.time()
    ################################################################################################################################################# 
    #############Grab a individual MN curve
    def Pilebehaviour_control(Phase_name,boundary):
        
        Pile_behavior="Single Pile"
        
        if dic_index_Phase[Phase_name]<boundary:
            return(Pile_behavior)
        
        Pile_behavior="Pile Group/Pile-raft"
        return(Pile_behavior)
    
    ###################################
    def getMNcurve(dia):
        x_MN = pd.read_excel('References\TypicalMNcurves_{}mm.xlsx'.format(int(dia*1000)), sheet_name='C28_35',header=None)
        
        row=len(x_MN.index)
        
        nominal=[]
        p1=[]
        p2=[]
        maxs=[]
        
        nominal=pd.DataFrame(x_MN,index=range(4,row),columns=[0,1])
        nominal=nominal.values.tolist()
        
        p1=pd.DataFrame(x_MN,index=range(4,row),columns=[3,4])
        p1=p1.values.tolist()
        
        p2=pd.DataFrame(x_MN,index=range(4,row),columns=[6,7])
        p2= p2.values.tolist()
        
        maxs=pd.DataFrame(x_MN,index=range(4,row),columns=[9,10])
        maxs = maxs.values.tolist()
        
        x_MN = pd.read_excel('References\TypicalMNcurves_{}mm.xlsx'.format(int(dia*1000)), sheet_name='C40',header=None)
        
        row=len(x_MN.index)
        
        nominal_40=[]
        p1_40=[]
        p2_40=[]
        maxs_40=[]
        
        nominal_40=pd.DataFrame(x_MN,index=range(4,row),columns=[0,1])
        nominal_40= nominal_40.values.tolist()
        
        p1_40=pd.DataFrame(x_MN,index=range(4,row),columns=[3,4])
        p1_40= p1_40.values.tolist()
        
        p2_40=pd.DataFrame(x_MN,index=range(4,row),columns=[6,7])
        p2_40= p2_40.values.tolist()
        
        maxs_40=pd.DataFrame(x_MN,index=range(4,row),columns=[9,10])
        maxs_40 = maxs_40.values.tolist()
        
        return nominal, p1,p2,maxs, nominal_40,p1_40,p2_40,maxs_40
    #################################################################################################################################################
    def CheckMNfailure(Name,Phase,dia,ULS_c):
        nom,p1,p2,maxs,n_40,p1_40,p2_40,maxs_40=getMNcurve(dia)
        poly = Polygon(maxs)
        poly_40=Polygon(maxs_40)
        size=len(ULS_c)
    
        
        logic=0
        for rt in range(0,size-1):
            point1=Point(ULS_c[rt][1],ULS_c[rt][0])
            if point1.within(poly)==False and point1.within(poly_40)==True :
                logic=1
            if point1.within(poly)==False and point1.within(poly_40)==False :
                logic=2
            if point1.within(poly)==True and point1.within(poly_40)==False :
                logic=3
    
        
        alerts={
                1:"WARNING!!! CHECK {} IN {}, PILE FALLING OUTSIDE THE M-N DIAGRAM WHEN C28/35",
                2:"WARNING!!! CHECK {} IN {}, PILE FALLING OUTSIDE ALL M-N DIAGRAM - C28/35 AND C40",
                3:"WARNING!!! CHECK {} IN {}, PILE FALLING OUTSIDE THE M-N DIAGRAM WHEN C28/35"}
        print(logic)
        if logic!=0:
    
            print(alerts[logic].format(Name,Phase))
            log_a=[Name,Phase,alerts[logic].format(Name,Phase)]
            log.append(log_a)
    #################################################################################################################
    def Createsummary_excel(writer):
        df_summary=pd.DataFrame(index=None)
        data = pd.DataFrame({"A": range(len(g.Embeddedbeams))},index=None)
        df_summary=df_summary.append(data)
        
        col=["AKT Pile Ref"," Pile Diameter (mm)",
             "Cut-off Level (mOD)","Pile Toe Level (mOD)",
             "PLAXIS local x (m)","PLAXIS local y (m)",
             "PLAXIS X (m)","PLAXIS Y (m)",
             "SLS N max Single pile (kN)","SLS N  Single pile min (kN)",
             "SLS N max Piled-raft (kN)","SLS N  Piled-raft min (kN)",
             "SLS M max (kNm)","SLS V max (kN)",
             "Vertical displacement uz min (mm)","Vertical displacement uz max (mm)",
             "ULS N max (kN)","ULS N min (kN)",
             "ULS M max (kNm)","ULS V max (kN)"]
        
        
        df_summary=df_summary.reindex(columns = col)   
        print(df_summary)
        i=0
        for Pile in g.Embeddedbeams:
            data_pile=pd.DataFrame.from_records(Pile_data[Pile.Parent.Name.value])
            data_pile.columns=["Elevation (mOD)","Diameter (m)","Phase",
                               "Vertical displacement uz (mm)","N (kN)","Q SLS resultant (kN)",
                               "M SLS resultant(kNm)","N ULS (kN)","M ULS resultant (kNm)",
                               "Q ULS resultant (kN)","Pile behaviour"]
            
            Pile_Name=Pile.Parent.Name.value
            d=Pile.Material.Diameter.value*1000
            Cutoff=Pile.Parent.First.z.value
            Toelevel=Pile.Parent.Second.z.value
            Pilex=Pile.Parent.First.x.value
            Piley=Pile.Parent.First.y.value
            PileNorth=Piley
            PileEast=Pilex
            SLSNmax_sp=max(data_pile["N (kN)"].loc[data_pile["Pile behaviour"]=="Single Pile"])
            SLSNmin_sp=min(data_pile["N (kN)"].loc[data_pile["Pile behaviour"]=="Single Pile"])
        
            SLSNmax_pg=max(data_pile["N (kN)"].loc[data_pile["Pile behaviour"]=="Pile Group/Pile-raft"])
            SLSNmin_pg=min(data_pile["N (kN)"].loc[data_pile["Pile behaviour"]=="Pile Group/Pile-raft"])
            
            SLSMresultmax=max(data_pile["M SLS resultant(kNm)"])
            SLSVresultmax=max(data_pile["Q SLS resultant (kN)"])
        
            SLSuzmax=max(data_pile["Vertical displacement uz (mm)"])
            SLSuzmin=min(data_pile["Vertical displacement uz (mm)"])
        
            ULSNmax=max(data_pile["N ULS (kN)"])
            ULSNmin=min(data_pile["N ULS (kN)"])
        
            ULSMresultmax=max(data_pile["M ULS resultant (kNm)"])
            ULSVresultmax=max(data_pile["Q ULS resultant (kN)"])
            
            df_summary.iloc[i,0]=Pile_Name
            df_summary.iloc[i,1]=d
            df_summary.iloc[i,2]=Cutoff
            df_summary.iloc[i,3]=Toelevel
            df_summary.iloc[i,4]=PileNorth
            df_summary.iloc[i,5]=PileEast
            df_summary.iloc[i,6]=Pilex
            df_summary.iloc[i,7]=Piley
            df_summary.iloc[i,8]=SLSNmax_sp
            df_summary.iloc[i,9]=SLSNmin_sp
            df_summary.iloc[i,10]=SLSNmax_pg
            df_summary.iloc[i,11]=SLSNmin_pg
            
            df_summary.iloc[i,12]=SLSMresultmax
            df_summary.iloc[i,13]=SLSVresultmax
            df_summary.iloc[i,14]=SLSuzmax
            df_summary.iloc[i,15]=SLSuzmin
            df_summary.iloc[i,16]=ULSNmax
            df_summary.iloc[i,17]=ULSNmin
            df_summary.iloc[i,18]=ULSMresultmax
            df_summary.iloc[i,19]=ULSVresultmax
            
            i=i+1
            
        df_summary=df_summary.round(2)  
        df_summary.set_index("AKT Pile Ref")
        df_summary.to_excel(writer,sheet_name=("Summary"),startrow=1,header=False,index="AKT Pile Ref")
        workbook = writer.book
        worksheet = writer.sheets["Summary"]
        
        cell_format = workbook.add_format()
        cell_format.set_font_name('Eras Medium ITC')
        cell_format.set_bg_color('#FFFFCC')
        cell_format.set_align('center')
        cell_format.set_align('vcenter')
        cell_format.set_text_wrap()
                             
        worksheet.set_column('A:U', 20, cell_format)
        header_format = workbook.add_format({
        'bold': True,
        'font_name':'Eras Medium ITC',
        'text_wrap': True,
        'valign': 'top',
        'align':'center',
        'fg_color': '#D7E4BC',
        'border': 1})
        
        for col_num, value in enumerate(df_summary.columns.values):
            worksheet.write(0, col_num + 1, value, header_format)
            
        worksheet.write(0,0,"AKT Pile Ref",header_format)  
        worksheet.set_column('A:A', 35,  cell_format, {'hidden': 1})
        return(df_summary)       
    #################################################################################################################
    def CreateTabular_excel(writer,Pile,diameter):
    #    Pile_data[Pile]
    
        data_pile=pd.DataFrame.from_records(Pile_data[Pile],index=None)
        data_pile.columns=["Elevation (mOD)","Diameter (m)","Phase","Vertical displacement uz (mm)","N (kN)","Q SLS resultant (kN)","M SLS resultant(kNm)","N ULS (kN)","M ULS resultant (kNm)", "Q ULS resultant (kN)","Pile behaviour"]
        data_pile=data_pile.round(2)
    #    new_col=range(len(data_pile.index))
    #    data_pile.insert(0,column="Sort No.",value=new_col)
        data_pile.to_excel(writer,sheet_name=("Pile{}".format(Pile)),startrow=1,header=False,index_label="Sort No.")
        
        
        
        sample_size_plots=len(data_pile[data_pile["Phase"]==data_pile["Phase"].iloc[0]])
        
        workbook = writer.book
        worksheet = writer.sheets["Pile{}".format(Pile)]
        
        header_format = workbook.add_format({
        'bold': True,
        'font_name':'Eras Medium ITC',
        'text_wrap': True,
        'valign': 'top',
        'align':'center',
        'fg_color': '#D7E4BC',
        'border': 1})
        
        for col_num, value in enumerate(data_pile.columns.values):
            worksheet.write(0, col_num + 1, value, header_format)
        worksheet.write(0,0,"Sort No.",header_format)
        
            
        
        ################################# TABULE VALUES FOR M-N DIAGRAMS ENVOLOPES
        d=diameter
        nom,p1,p2,maxs,n_40,p1_40,p2_40,maxs_40=getMNcurve(d)
        
    
    #    headerMN_format = workbook.add_format({
    #    'font_color': 'white'
    #    })
        
        
        ##FOR C35
        d_nominal=pd.DataFrame.from_records(nom)
        d_nominal.columns=["Moment nominal [kNm]- {} mm pile [kN] and Concrete type C28/35".format(int(d*1000)),"Axial Force nominal [kN]- {} mm pile [kN] and Concrete type C28/35".format(int(d*1000))]
        
        d_1p=pd.DataFrame.from_records(p1)
        d_1p.columns=["Moment 1% [kNm]- {} mm pile [kN] and Concrete type C28/35".format(int(d*1000)),"Axial Force 1% - {} mm pile [kN] and Concrete type C28/35".format(int(d*1000))]
        
        
        d_2p=pd.DataFrame.from_records(p2)
        d_2p.columns=["Moment 2% [kNm]- {} mm pile [kN] and Concrete type C28/35".format(int(d*1000)),"Axial Force 2% [kN]- {} mm pile [kN] and Concrete type C28/35".format(int(d*1000))]
        
        d_max=pd.DataFrame.from_records(maxs)
        d_max.columns=["Moment max [kNm]- {} mm pile [kN] and Concrete type C28/35".format(int(d*1000)),"Axial Force max [kN]- {} mm pile [kN] and Concrete type C28/35".format(int(d*1000))]
        
        d_nominal.to_excel(writer,sheet_name=("Pile{}".format(Pile)),startcol=13,startrow=1,index=None,header=False)
        d_1p.to_excel(writer,sheet_name=("Pile{}".format(Pile)),startcol=16,startrow=1,index=None,header=False)
        d_2p.to_excel(writer,sheet_name=("Pile{}".format(Pile)),startcol=19,startrow=1,index=None,header=False)
        d_max.to_excel(writer,sheet_name=("Pile{}".format(Pile)),startcol=22,startrow=1,index=None,header=False)
        
    #    for col_num, value in enumerate(d_nominal.columns.values):
    #        worksheet.write(13, 13+col_num + 1, value, headerMN_format)
    #    for col_num, value in enumerate(d_1p.columns.values):
    #        worksheet.write(16, 28+col_num + 1, value, headerMN_format) 
    #    for col_num, value in enumerate(d_2p.columns.values):
    #        worksheet.write(19, 31+col_num + 1, value, headerMN_format)
    #    for col_num, value in enumerate(d_max.columns.values):
    #        worksheet.write(34, 34+col_num + 1, value, headerMN_format)   
        
        ##FOR C40
        d_nominal_40=pd.DataFrame.from_records(n_40)
        d_nominal_40.columns=["Moment nominal [kNm]- {} mm pile [kN] and Concrete type C40".format(int(d*1000)),"Axial Force nominal [kN]- {} mm pile [kN] and Concrete type C40".format(int(d*1000))]
        
        d_1p_40=pd.DataFrame.from_records(p1_40)
        d_1p_40.columns=["Moment 1% [kNm]- {} mm pile [kN] and Concrete type C40".format(int(d*1000)),"Axial Force 1% - {} mm pile [kN] and Concrete type C40".format(int(d*1000))]
        
        d_2p_40=pd.DataFrame.from_records(p2_40)
        d_2p_40.columns=["Moment 2% [kNm]- {} mm pile [kN] and Concrete type C40".format(int(d*1000)),"Axial Force 2% [kN]- {} mm pile [kN] and Concrete type C40".format(int(d*1000))]
        
        d_max_40=pd.DataFrame.from_records(maxs_40)
        d_max_40.columns=["Moment max [kNm]- {} mm pile [kN] and Concrete type C40".format(int(d*1000)),"Axial Force max [kN]- {} mm pile [kN] and Concrete type C40".format(int(d*1000))]
        
        d_nominal_40.to_excel(writer,sheet_name=("Pile{}".format(Pile)),startcol=25,startrow=1,index=None,header=False)
        d_1p_40.to_excel(writer,sheet_name=("Pile{}".format(Pile)),startcol=28,startrow=1,index=None,header=False)
        d_2p_40.to_excel(writer,sheet_name=("Pile{}".format(Pile)),startcol=31,startrow=1,index=None,header=False)
        d_max_40.to_excel(writer,sheet_name=("Pile{}".format(Pile)),startcol=34,startrow=1,index=None,header=False)
        
    
        
        #Generation of plots in Excel Tab
        Plotgeneration(writer,sample_size_plots,Pile,p2,maxs,p2_40,maxs_40,worksheet,workbook,d)          
    #########################################################################################################################           
    def Plotgeneration(writer,length,Pile,p2,maxs,p2_40,maxs_40,worksheet,workbook,d):
    
        
        chartNSLS = workbook.add_chart({'type': 'scatter',
                                                'subtype': 'straight'})
                
        chartMSLS = workbook.add_chart({'type': 'scatter',
                                                'subtype': 'straight'})
    
        chartQSLS = workbook.add_chart({'type': 'scatter',
                                                'subtype': 'straight'})
                
        chartUZ = workbook.add_chart({'type': 'scatter',
                                                'subtype': 'straight'})
        
        
                
        chartNSLS.set_title ({'name': 'Axial force Distribution SLS - Pile{} '.format(Pile),
                                      'name_font':  {'name': 'Arial', 'size': 9,'italic':True,},
                                       'overlay': False,
                                           'layout': {
                                                   'x': 0.01,
                                                   'y': 0.01,}
                                       })
        chartNSLS.set_x_axis({'name': 'Axial force N SLS (kN)',
                                                          'name_layout': {
                                                'x': 0.25,
                                                'y': 0.05,},
                                      'name_font':  {'name': 'Arial', 'size': 8},
                                      'label_position':'high',
                                      'crossing': 'max',
                                      'major_tick_mark': 'inside',
                                      'minor_tick_mark': 'inside',
                                      })
        chartNSLS.set_y_axis({'name': 'Elevation (mOD)',
                                      'num_font':  {'name': 'Arial', 'size': 8},
                                      'major_tick_mark': 'outside',
                                      'minor_tick_mark': 'outside',
                                      })
                
        chartMSLS.set_title ({'name': 'Bending Moment  Distribution SLS  - Pile{} '.format(Pile),
                                   'name_font':  {'name': 'Arial', 'size': 9,'italic':True,},
                                   'overlay': False,
                                       'layout': {
                                               'x': 0.01,
                                               'y': 0.01,}
                                   })
        chartMSLS.set_x_axis({'name': 'Bending Moment SLS (kN.m)',
                                    'name_layout': {
                                            'x': 0.25,
                                            'y': 0.05,},
                                   'num_font':  {'name': 'Arial', 'size': 8,},
                                   'label_position':'high',
                                   'crossing': 'max',
                                   'major_tick_mark': 'inside',
                                   'minor_tick_mark': 'inside',
                                   })
              
                
        chartQSLS.set_title ({'name': 'Shear Force   Distribution SLS - Pile{} '.format(Pile),
                                   'name_font':  {'name': 'Arial', 'size': 9,'italic':True,},
                                   'overlay': False,
                                       'layout': {
                                               'x': 0.01,
                                               'y': 0.01,}
                                         })
        chartQSLS.set_x_axis({'name': 'Shear Force (kN)',
                                                       'name_layout': {
                                            'x': 0.25,
                                            'y': 0.05,},
                                   'num_font':  {'name': 'Arial', 'size': 8},
                                   'label_position':'high',
                                   'crossing': 'max',
                                   'major_tick_mark': 'inside',
                                   'minor_tick_mark': 'inside',
                                   })
        chartQSLS.set_y_axis({'name': 'Elevation (mOD)',
                                   'num_font':  {'name': 'Arial', 'size': 8},
                                   'major_tick_mark': 'outside',
                                   'minor_tick_mark': 'outside',
                                   })
                
        chartUZ.set_title ({'name': 'Vertical movements along the pile - Pile{} '.format(Pile),
                                      'name_font':  {'name': 'Arial', 'size': 9,'italic':True,},
                                       'overlay': False,
                                           'layout': {
                                                   'x': 0.01,
                                                   'y': 0.01,}
                                       })
        chartUZ.set_x_axis({'name': 'Displacements (mm)',
                                                          'name_layout': {
                                                'x': 0.25,
                                                'y': 0.05,},
                                      'name_font':  {'name': 'Arial', 'size': 8},
                                      'label_position':'high',
                                      'crossing': 'max',
                                      'major_tick_mark': 'inside',
                                      'minor_tick_mark': 'inside',
                                      })
        chartUZ.set_y_axis({'name': 'Elevation (mOD)',
                                      'num_font':  {'name': 'Arial', 'size': 8},
                                      'major_tick_mark': 'outside',
                                      'minor_tick_mark': 'outside',
                                      })        
                
        multi=0
        
    
    
        for b,c in zip(Phases_name,color): 
            size=length*multi
            start=2+size
            end=length+size+1
            chartNSLS.add_series({
                        'name': '{}'.format(b),
                            'categories': '=Pile{}!F${}:$F${}'.format(Pile,start,end),
                            'values': '=Pile{}!$B${}:$B${}'.format(Pile,start,end),
                        'line': {'color':c,'width': 3.25}
                        })
            chartMSLS.add_series({
                'name': '{}'.format(b),
                        'categories': '=Pile{}!$H${}:$H${}'.format(Pile,start,end),
                        'values': '=Pile{}!$B${}:$B${}'.format(Pile,start,end),
                    'line': {'color':c,'width': 3.25}
                    })
                
                
            chartQSLS.add_series({
                'name': '{}'.format(b),
                        'categories': '=Pile{}!$G${}:$G${}'.format(Pile,start,end),
                        'values': '=Pile{}!$B${}:$B${}'.format(Pile,start,end),
                    'line': {'color':c,'width': 3.25}
                    })
            chartUZ.add_series({
                'name': '{}'.format(b),
                        'categories': '=Pile{}!$E${}:$E${}'.format(Pile,start,end),
                        'values': '=Pile{}!$B${}:$B${}'.format(Pile,start,end),
                    'line': {'color':c,'width': 3.25}
                    })
            
            
    
            multi=multi+1
            
        
            
        Plot_MN_c35 = workbook.add_chart({'type': 'scatter',
                                            'subtype': 'straight'})
        Plot_MN_c35.add_series({
            'name': 'ULS Loads',
                'categories': '=Pile{}!$J$2:$J$10000'.format(Pile),
                'values': '=Pile{}!$I$2:$I$10000'.format(Pile),
            'marker': {'type':'diamond',
                       'size':7,
                       'color':'green',
                       'border': {'color': 'black'},
                       'fill':{'color': 'red'}},
            'line':{'none': True},
                    })
        
        Plot_MN_c35.add_series({
            'name': 'Nominal Cage',
                'categories': '=Pile{}!$N$2:$N$10000'.format(Pile),
                'values': '=Pile{}!$O$2:$O$10000'.format(Pile),
            'line': {'color':'green','width': 3.25}
            })
        
        Plot_MN_c35.add_series({
            'name': 'As = 1% Ac',
                'categories': '=Pile{}!$Q$2:$Q$10000'.format(Pile),
                'values': '=Pile{}!$R$2:$R$10000'.format(Pile),
            'line': {'color':'blue','width': 3.25}
            })
        if p2!=maxs:
            Plot_MN_c35.add_series({
                'name': 'As = 2% Ac',
                    'categories': '=Pile{}!$T$2:$T$10000'.format(Pile),
                    'values': '=Pile{}!$U$2:$U$10000'.format(Pile),
                'line': {'color':'red','width': 3.25}
                })
            
        Plot_MN_c35.add_series({
            'name': 'Maximum reinforcement cage',
                'categories': '=Pile{}!$W$2:$W$10000'.format(Pile),
                'values': '=Pile{}!$X$2:$X$10000'.format(Pile),
            'line': {'color':'black','width': 3.25}
            })
        
        Plot_MN_c35.set_title ({'name': 'M-N diagram - Pile{}  Diameter= {} mm, Concrete type={}'.format(Pile,int(d*1000),"C28/35"),
                          'name_font':  {'name': 'Arial', 'size': 9,'italic':True,},
                           'overlay': False,
                               'layout': {
                                       'x': 0.01,
                                       'y': 0.01,}
                           })
        Plot_MN_c35.set_x_axis({'name': 'Moment [kNm]',
                          'name_layout': {
                                    'x': 0.3,
                                    'y': 1,},
                          'name_font':  {'name': 'Arial', 'size': 8},
                          'label_position':'next_to',
                          'crossing': '0',
                          'major_tick_mark': 'inside',
                          'minor_tick_mark': 'inside',
                          })
        Plot_MN_c35.set_y_axis({'name': 'Axial force [kN]',
                          'num_font':  {'name': 'Arial', 'size': 8},
                          'major_tick_mark': 'outside',
                          'minor_tick_mark': 'outside',
                          })
        
        
    
                
        Plot_MN_c40 = workbook.add_chart({'type': 'scatter',
                                            'subtype': 'straight'})
        Plot_MN_c40.add_series({
            'name': 'ULS Loads',
                'categories': '=Pile{}!$J$2:$J$10000'.format(Pile),
                'values': '=Pile{}!$I$2:$I$10000'.format(Pile),
            'marker': {'type':'diamond',
                       'size':7,
                       'color':'green',
                       'border': {'color': 'black'},
                       'fill':{'color': 'red'}},
            'line':{'none': True},
                    })
    #            
        Plot_MN_c40.add_series({
            'name': 'Nominal Cage',
                'categories': '=Pile{}!$Z$2:$Z$10000'.format(Pile),
                'values': '=Pile{}!$AA$2:$AA$10000'.format(Pile),
            'line': {'color':'green','width': 3.25}
            })
        
        Plot_MN_c40.add_series({
            'name': 'As = 1% Ac',
                'categories': '=Pile{}!$AC$2:$AC$10000'.format(Pile),
                'values': '=Pile{}!$AD$2:$AD$10000'.format(Pile),
            'line': {'color':'blue','width': 3.25}
            })
    
        if p2_40!=maxs_40:   
            Plot_MN_c40.add_series({
                'name': 'As = 2% Ac',
                    'categories': '=Pile{}!$AF$2:$AF$10000'.format(Pile),
                    'values': '=Pile{}!$AG$2:$AG$10000'.format(Pile),
                'line': {'color':'red','width': 3.25}
                })
        
        Plot_MN_c40.add_series({
            'name': 'Maximum reinforcement cage',
                'categories': '=Pile{}!$AI$2:$AI$10000'.format(Pile),
                'values': '=Pile{}!$AJ$2:$AJ$10000'.format(Pile),
            'line': {'color':'black','width': 3.25}
            })
    #            
        Plot_MN_c40.set_title ({'name': 'M-N diagram - Pile{}, Diameter= {} mm, Concrete type={}'.format(Pile,int(d*1000),"C40"),
                          'name_font':  {'name': 'Arial', 'size': 9,'italic':True,},
                           'overlay': False,
                               'layout': {
                                       'x': 0.01,
                                       'y': 0.01,}
                           })
        Plot_MN_c40.set_x_axis({'name': 'Moment [kNm]',
                          'name_layout': {
                                    'x': 0.3,
                                    'y': 1,},
                          'name_font':  {'name': 'Arial', 'size': 8},
                          'label_position':'next_to',
                          'crossing': '0',
                          'major_tick_mark': 'inside',
                          'minor_tick_mark': 'inside',
                          })
        Plot_MN_c40.set_y_axis({'name': 'Axial force [kN]',
                          'num_font':  {'name': 'Arial', 'size': 8},
                          'major_tick_mark': 'outside',
                          'minor_tick_mark': 'outside',
                          })
        
        
        cell_format = workbook.add_format()
        cell_format.set_font_color('white')
        cell_format.set_align('center')
        cell_format.set_align('vcenter')
        cell_format.set_text_wrap()
                                       
        worksheet.set_column('N:BZ', 20, cell_format) 
        
        cell_format2 = workbook.add_format()
        cell_format2.set_font_name('Eras Medium ITC')
        cell_format2.set_font_color('black')
        cell_format2.set_bg_color('#FFFFCC')
        cell_format2.set_align('center')
        cell_format2.set_align('vcenter')
        cell_format2.set_text_wrap()
        worksheet.set_column('A:L', 20, cell_format2)                           
    
    
        worksheet.insert_chart('M1', chartNSLS)
        worksheet.insert_chart('Q1', chartMSLS)
        worksheet.insert_chart('U1', chartQSLS)
        worksheet.insert_chart('M18', chartUZ)
        worksheet.insert_chart('Q18', Plot_MN_c40)
        worksheet.insert_chart('U18', Plot_MN_c35)     
     ####################           
    def Pileheadresults(phase):
        Name_h_i=[]
        Stage_h_i=[]
        uz_h_i=[]
        n_i=[]
        S_h_i=[]
        puz_h_i=[]
        c_h_i=[]
        b_h_i=[]
        v_h_i=[]
        m1_i=[] 
        m2_i=[]
        m1min_i=[]
        m2min_i=[]
        nmin_i=[]
        nmax_i=[]
        m1max_i=[]
        m2max_i=[]
        diameter_h_i=[]
        length_h_i=[]
        for a in g.EmbeddedBeams:
            
            print(a.Parent.Name.value,phase.Name.value)
            x_h=a.Parent.First.x.value
            y_h=a.Parent.First.y.value
            z_h=a.Parent.First.z.value 
            d_h=(a.Material.Diameter.value)*1000
            l_h=(a.Parent.Length.value)
            disp=g_output.getsingleresult(phase, g_output.ResultTypes.EmbeddedBeam.Uz,x_h,y_h,z_h)
            phase_disp=g_output.getsingleresult(phase, g_output.ResultTypes.EmbeddedBeam.PUz,x_h,y_h,z_h)
            Fz=g_output.getsingleresult(phase, g_output.ResultTypes.EmbeddedBeam.N,x_h,y_h,z_h)
            M2_h=g_output.getsingleresult(phase, g_output.ResultTypes.EmbeddedBeam.M2,x_h,y_h,z_h)
            M3_h=g_output.getsingleresult(phase, g_output.ResultTypes.EmbeddedBeam.M3,x_h,y_h,z_h)
            M2_envmax=g_output.getsingleresult(phase, g_output.ResultTypes.EmbeddedBeam.M2_EnvelopeMax,x_h,y_h,z_h)
            M2_envmin=g_output.getsingleresult(phase, g_output.ResultTypes.EmbeddedBeam.M2_EnvelopeMin,x_h,y_h,z_h)
            M3_envmax=g_output.getsingleresult(phase, g_output.ResultTypes.EmbeddedBeam.M3_EnvelopeMax,x_h,y_h,z_h)
            M3_envmin=g_output.getsingleresult(phase, g_output.ResultTypes.EmbeddedBeam.M3_EnvelopeMin,x_h,y_h,z_h)
            N_envmax=g_output.getsingleresult(phase, g_output.ResultTypes.EmbeddedBeam.N_EnvelopeMax,x_h,y_h,z_h)
            N_envmin=g_output.getsingleresult(phase, g_output.ResultTypes.EmbeddedBeam.N_EnvelopeMin,x_h,y_h,z_h)
            Name_h_i.append(a.Parent.Name.value)
            Stage_h_i.append(phase.Name.value)  
            uz_h_i.append(disp*1000)
            puz_h_i.append(phase_disp*1000)
            n_i.append(Fz)
            m1_i.append(M2_h)
            m2_i.append(M3_h)
            m1min_i.append(M2_envmin)
            m1max_i.append(M2_envmax)
            m2min_i.append(M3_envmin)
            m2max_i.append(M3_envmax)
            nmax_i.append(N_envmax)
            nmin_i.append(N_envmin)
            uz_m=float(disp)
            Fz_m=float(Fz)
            S_h_i.append(Fz_m/uz_m)
            diameter_h_i.append(d_h)
            c_h_i.append(x_h)
            v_h_i.append(y_h)
            b_h_i.append(z_h)
            length_h_i.append(l_h)            
            # return(Name_h,diameter_h,length_h,Stage_h,c_h,v_h,b_h,uz_h,puz_h,n,nmin,nmax,m1,m1min,m1max,m2,m2min,m2max,S_h)
        return(Name_h_i,diameter_h_i,length_h_i,Stage_h_i,c_h_i,v_h_i,b_h_i,uz_h_i,puz_h_i,n_i,nmin_i,nmax_i,m1_i,m1min_i,m1max_i,m2_i,m2min_i,m2max_i,S_h_i)
        
    #########################################################################################################################     

    
    project=[1]
    
    model_name=[m_n]
    for proj,modelname in zip(project,model_name):
        
        g.gotostages()
        # g.calculate()
        # g.save()
        g.view(g.Phase_3)
       
        g.gotostructures()
        
        
        Name_h=[]
        Stage_h=[]
        uz_h=[]
        n=[]
        S_h=[]
        puz_h=[]
        c_h=[]
        b_h=[]
        v_h=[]
        m1=[] 
        m2=[]
        m1min=[]
        m2min=[]
        nmin=[]
        nmax=[]
        m1max=[]
        m2max=[]
        diameter_h=[]
        length_h=[]
    
    
        
        log=[]
  
        Phases_name=[]
    
        Pile_data={}
        for a in g.EmbeddedBeams: 
            Pile_data[a.Parent.Name.value]= [] # Create an empty list associated to a key in the Pile_MN dic .Key is the Pile name.
        # Phase_extract=[
        #              g_output.Phase_3
        #             ,g_output.Phase_7
        #             ,g_output.Phase_4
        #             ,g_output.Phase_6
        #             ,g_output.Phase_5
        #             ,g_output.Phase_9
        #             ,g_output.Phase_11]
        
    
            
            
    #    Phase_extract=[g_output.Phase_10]        
        
        dic_index_Phase={}
        increment=1
        for ind in Phase_extract:
            dic_index_Phase.update({ind:increment})
            increment=increment+1            
        
        
    
        g.gotostructures()
        for pha in Phase_extract:
            
            phase=getattr(g_output,pha)
            # Name_h,diameter_h,length_h,Stage_h,c_h,v_h,b_h,uz_h,puz_h,n,nmin,nmax,m1,m1min,m1max,m2,m2min,m2max,S_h=Pileheadresults(phase)
            Name_h_p,diameter_h_p,length_h_p,Stage_h_p,c_h_p,v_h_p,b_h_p,uz_h_p,puz_h_p,n_p,nmin_p,nmax_p,m1_p,m1min_p,m1max_p,m2_p,m2min_p,m2max_p,S_h_p=Pileheadresults(phase)
    
            Name_h=Name_h+Name_h_p
            diameter_h=diameter_h+diameter_h_p
            length_h=length_h+length_h_p
            Stage_h=Stage_h+Stage_h_p
            c_h=c_h+c_h_p
            v_h=v_h+v_h_p
            b_h=b_h+b_h_p
            uz_h=uz_h+uz_h_p
            puz_h=puz_h+puz_h_p
            n_p=n+n_p
            nmin=nmin+nmin_p
            nmax=nmax+nmax_p
            m1=m1+m1_p
            m1min=m1min+m1min_p
            m1max=m1max+m1max_p
            m2=m2+m2_p
            m2min=m2min+m2min_p
            m2max=m2max+m2max_p
            S_h=S_h+S_h_p
            
            Phases_name.append(phase.Name.value)
            # obtain result tables for Phase [i]
            PileX = g_output.getresults(phase, g_output.ResultTypes.EmbeddedBeam.X, 'node') 
            PileY = g_output.getresults(phase, g_output.ResultTypes.EmbeddedBeam.Y, 'node')
            PileZ = g_output.getresults(phase, g_output.ResultTypes.EmbeddedBeam.Z, 'node')  
            
            PileM2 = g_output.getresults(phase, g_output.ResultTypes.EmbeddedBeam.M2, 'node')
            PileM2min = g_output.getresults(phase, g_output.ResultTypes.EmbeddedBeam.M2_EnvelopeMin, 'node')
            PileM2max = g_output.getresults(phase, g_output.ResultTypes.EmbeddedBeam.M2_EnvelopeMax, 'node')
          
            PileM3 = g_output.getresults(phase, g_output.ResultTypes.EmbeddedBeam.M3, 'node')
            PileM3min = g_output.getresults(phase, g_output.ResultTypes.EmbeddedBeam.M3_EnvelopeMin, 'node')
            PileM3max = g_output.getresults(phase, g_output.ResultTypes.EmbeddedBeam.M3_EnvelopeMax, 'node')
            
            PileQ12 = g_output.getresults(phase, g_output.ResultTypes.EmbeddedBeam.Q12, 'node') 
            PileQ12min = g_output.getresults(phase, g_output.ResultTypes.EmbeddedBeam.Q12_EnvelopeMin, 'node')
            PileQ12max = g_output.getresults(phase, g_output.ResultTypes.EmbeddedBeam.Q12_EnvelopeMax, 'node')
            
            PileQ13 = g_output.getresults(phase, g_output.ResultTypes.EmbeddedBeam.Q13, 'node')
            PileQ13min = g_output.getresults(phase, g_output.ResultTypes.EmbeddedBeam.Q13_EnvelopeMin, 'node')
            PileQ13max = g_output.getresults(phase, g_output.ResultTypes.EmbeddedBeam.Q13_EnvelopeMax, 'node')
            
            PileN = g_output.getresults(phase, g_output.ResultTypes.EmbeddedBeam.N, 'node')
            PileNmin = g_output.getresults(phase, g_output.ResultTypes.EmbeddedBeam.N_EnvelopeMin, 'node')
            PileNmax = g_output.getresults(phase, g_output.ResultTypes.EmbeddedBeam.N_EnvelopeMax, 'node')
            Pile_uz=g_output.getresults(phase, g_output.ResultTypes.EmbeddedBeam.Uz, 'node')
            
            for a in g.EmbeddedBeams:
                print(a.Parent.Name.value,phase.Name.value)
                x_p=a.Parent.First.x.value
                y_p=a.Parent.First.y.value
 
                d=a.Material.Diameter.value
                #initialize defaults: 
                ULS=[]
                Combined_data=Pile_data[a.Parent.Name.value]
                
                # determine minimum and maximum bending moment for each pile: 
                for x, y,z, M2,M3,Q12,Q13,N,M2min,M2max,M3min,M3max,Q12min,Q12max,Q13min,Q13max,Nmin,Nmax,vertical in zip(PileX, PileY,PileZ, PileM2,PileM3, PileQ12,PileQ13, PileN,
                                                                                                  PileM2min,PileM2max,PileM3min,PileM3max,PileQ12min,PileQ12max,PileQ13min,PileQ13max,PileNmin,PileNmax,Pile_uz): 
                    #is it on the left wall (with small numerical tolerance)? 
                    if abs(x_p-x)<1e-5 and abs(y_p - y)<1e-5:
                        Settlement=-vertical*1000
                        M_SLS=math.sqrt(M2**2+M3**2)
                        Q_SLS=math.sqrt(Q12**2+Q13**2)
                        if N<0:
                            N_uls=-1.4*N
                        else:
                            N_uls=-1.35*N
                        M_ULS=1.4*math.sqrt(M2**2+M3**2)
                        Q_ULS=1.4*math.sqrt(Q12**2+Q13**2)
                        Mn=[N_uls,M_ULS]
                        PB=Pilebehaviour_control(phase.Name.value,boundary)
                        P_s=[z,d,phase.Name.value,Settlement,-N,Q_SLS,M_SLS,N_uls,M_ULS,Q_ULS,PB]
                        ULS.append(Mn)
                        Combined_data.append(P_s)
                        
                    
                print("Updating the Pile_data dict")            
                Pile_data.update({a.Parent.Name.value:Combined_data})
     ##############################################
    
                CheckMNfailure(a.Parent.Name.value,phase.Name.value,d,ULS)
    ##############################################################################    

        data_dic={"Pile Name":Name_h,
        "Diamter(mm)":diameter_h,
        "Length(m)":length_h,
        "Stage":Stage_h,
        "X (m)":c_h,
        "Y (m)":v_h,
        "Z (m)":b_h,
        "Settlement (mm)":uz_h,
        "Phase Settlement (mm)":puz_h,
        "Axial Force (kN)":n,
        "Axial Force Envelope min (kN)":nmin,
        "Axial Force Envelope max (kN)":nmax,
        "Bedding Moment M1 (kN.m)":m1,
        "Bedding Moment M1 Envelope min(kN.m)":m1min,
        "Bedding Moment M1 Envelope max(kN.m)":m1max,
        "Bedding Momement M2 (kN.m)":m2,
        "Bedding Moment M2 Envelope min(kN.m)":m2min,
        "Bedding Moment M2 Envelope max(kN.m)":m2max,
        "Spring Stiffness (kN/m)":S_h}

        pilehead_df=pd.DataFrame(data=data_dic)
        write_pilehead=pd.ExcelWriter("Pile results {} {}.xlsx".format(project_name,modelname))
        pilehead_df.to_excel(write_pilehead,sheet_name=("Summary"))
        write_pilehead.save()    

            
        # filename= "Pile results Canada Water Plot F {}.csv".format(modelname)              
        # with open(filename, "w") as file:
        #         file.writelines("Pile Name\tDiamter(mm)\tLength(m)\tStage\tX (m)\tY (m)\tZ (m)\tSettlement (m)\tPhase Settlement (m)\tAxial Force (kN)\tAxial Force Envelope min (kN)\tAxial Force Envelope max (kN)\tBedding Moment M2 (kN.m)\tBedding Moment M2 Envelope min(kN.m)\tBedding Moment M2 Envelope max(kN.m)\tBedding Momement M3 (kN.m)\tBedding Moment M2 Envelope min(kN.m)\tBedding Moment M2 Envelope max(kN.m)\tSpring Stiffness (kN/m)\n")
        #         file.writelines( ['{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format( P,dw ,comp, Ph,l,k,j, set,Pset, axial,amin,amax,b1,b1min,b1max,b2,b2min,b2max,f)
        #                         for P,dw,comp,Ph,l,k,j, set,Pset, axial,amin,amax,b1,b1min,b1max,b2,b2min,b2max,f  in zip( Name_h,diameter_h,length_h,Stage_h,c_h,v_h,b_h,uz_h,puz_h,n,nmin,nmax,m1,m1min,m1max,m2,m2min,m2max,S_h)])
                            
         
        print("Pile schedule excel creation will now commence... Stand by")
        
        multipler=1
        current_number=0
        s_1=pd.ExcelWriter("Pile schedule excel {} {} - Part {}.xlsx".format(project_name,modelname,multipler))
        if log==[]:
            print("Success! All Point are inside the M-N diagrams!")
            log=[0,0,0]
            summary=pd.DataFrame(log).T
        else:
            print("Success! All Point are inside the M-N diagrams!")
            log=[0,0,0]
            summary=pd.DataFrame(log).T
    #        summary=pd.DataFrame.from_records(log)
            
        summary.columns=["Pile","Phase","Alert"]
        summary.to_excel(s_1,sheet_name=("Alert log"))
        number_of_colors = len(Phases_name)
    
        color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                 for i in range(number_of_colors)]
        
        er=Createsummary_excel(s_1)
    
        for a in g.EmbeddedBeams:
            print(current_number,multipler)
            if current_number<25*multipler:
                CreateTabular_excel(s_1,a.Parent.Name.value,a.Material.Diameter.value)
                current_number=current_number+1
            else:
               multipler=multipler+1
               s_1.save()
               s_1=[]
               s_1=pd.ExcelWriter("Pile schedule excel {} {} - Part {}.xlsx".format(project_name,modelname,multipler))
    
               if log==[]:
                    print("Success! All Point are inside the M-N diagrams!")
                    log=[0,0,0]
                    summary=pd.DataFrame(log).T
               else:
                    print("Success! All Point are inside the M-N diagrams!")
                    log=[0,0,0]
                    summary=pd.DataFrame(log).T
    #                summary=pd.DataFrame.from_records(log)
               summary.columns=["Pile","Phase","Alert"]
               summary.to_excel(s_1,sheet_name=("Alert log"))
               er=Createsummary_excel(s_1)
               CreateTabular_excel(s_1,a.Parent.Name.value,a.Material.Diameter.value)
               current_number=current_number+1
               
    
        s_1.save()    
    
        
    print("Script finished at %s seconds----" % (time.time() - start_time))
    
    ############### END########################################################
    
    


           

        


