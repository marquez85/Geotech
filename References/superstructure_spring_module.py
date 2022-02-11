import matplotlib.pyplot as plt
import time
import imp
import math
from scipy.interpolate import UnivariateSpline 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

start_time=time.time()

def superstructure_spring(s,g,s_output,g_output,project_name,rev,Phase):
    g.gotostructures()
    
    Name=[]
    Stage=[]
    uz=[]
    N=[]
    S=[]
    puz=[]
    c=[]
    b=[]
    v=[]

    for pha in Phase:
        r=getattr(g_output,pha)
        for a in g.PointLoads:
            print(a.Parent.Name.value,r.Name.value)
            x=a.Parent.x.value
            y=a.Parent.y.value
            z=a.Parent.z.value 
            disp=g_output.getsingleresult(r, g_output.ResultTypes.Plate.Uz,x,y,z)
            phase_disp=g_output.getsingleresult(r, g_output.ResultTypes.Plate.PUz,x,y,z)
            if disp =='not found':
                disp=g_output.getsingleresult(r, g_output.ResultTypes.Beam.Uz,x,y,z)
                phase_disp=g_output.getsingleresult(r, g_output.ResultTypes.Beam.PUz,x,y,z)
                
            Fz=g_output.getsingleresult(r, g_output.ResultTypes.PointLoad.Fz,x,y,z)
            if Fz =='not found':
                Fz=0
    
            Name.append(a.Name.value)
            Stage.append(r.Name.value)  
            uz.append(disp*1000)
            puz.append(phase_disp*1000)
            uz_m=float(disp)
            Fz_m=float(Fz)
            S.append(Fz_m/uz_m)
            c.append(x)
            v.append(y)
            b.append(z)
            N.append(Fz)
            
    data_dic={"Superstructure load Name":Name,
    "Stage":Stage,
    "Easting (m)":c,
    "Northing (m)":v,
    "Elevation (mOD))":b,
    "Settlement (mm)":uz,
    "Phase Settlement (mm)":puz,
    "Superstructure load (kN)":Fz,
    "Spring Stiffness (kN/m)":S}

    spring_df=pd.DataFrame(data=data_dic)
    write_spring=pd.ExcelWriter("Spring stiffness_superstructure {} {}.xlsx".format(project_name,rev))
    spring_df.to_excel(write_spring,sheet_name=("Summary"))
    write_spring.save()    

                                                                                        
    
    
               
    
            
    
    
