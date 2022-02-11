import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io


# def plotPlaxisResults_Pile(result, title,r):

#     import matplotlib.pyplot as plt
#     x = result.x.values
#     y = result.y.values
#     d=result.Diameter.values
#     top=result.z.values
#     l=result.Length.values
#     N_text = result.Pile.values

#     colors=d
#     fig, ax = plt.subplots(figsize=(30, 10))
#     ax.scatter(x, y, s = d*.1, c =colors)

#     for i, txt in enumerate(d):
#         #print(txt)
#         ax.annotate('{}\n{:0.0f}mm\ntoe {:0.0f}mOD'.format(N_text[i],txt,(top[i]-l[i])),(x[i]+0.1, y[i]+0.1), color = 'red', rotation=45,fontsize = 5)
        

#     ax.set_xlim([min(x)-5, max(x)+5])
#     ax.set_ylim([min(y)-5, max(y)+5])    
#     ax.set_xlabel(r'$x$ in m', fontsize=15)
#     ax.set_ylabel(r'$y$ in m', fontsize=15)
#     ax.set_title(title)


#     ax.grid(True)
#     #fig.tight_layout()
#     plt.savefig(r".\Results/" + title + '{}.pdf'.format(r))
#     plt.show()
    
    
def plotplaxispilelayout(project_name,r,pile_name,pile_x,pile_y,result,title):
    import streamlit as st
    x = result["PLAXIS X (m)"].values
    y = result["PLAXIS Y (m)"].values
    d=result[" Pile Diameter (mm)"].values
    N_text = result["Pile Ref"].values
    d_unique=result[" Pile Diameter (mm)"].unique().tolist()
    d_colors={}
    list_colors=["k","r","b","g","m","y"]
    # st.write(d_unique)
    for i,j in enumerate(d_unique):
        d_colors.update({j:list_colors[i]})
    # st.write(d_colors)
    colors=result[" Pile Diameter (mm)"].apply(lambda x:d_colors[x])
    # st.write(colors)
    fig, ax = plt.subplots(figsize=(20,20))
    ax.scatter(x, y, s = d*.1, c =colors)

    # for i, txt in enumerate(d):
    #     #print(txt)
    #     ax.annotate('{}\n{:0.0f}mm'.format(N_text[i],txt),(x[i]+0.1, y[i]+0.1), color = 'red', rotation=45,fontsize = 6)
        

    ax.set_xlim([min(x)-5, max(x)+5])
    ax.set_ylim([min(y)-5, max(y)+5])    
    ax.set_xlabel('x in m', fontsize=15)
    ax.set_ylabel('y in m', fontsize=15)
    ax.set_title(title)
    rect = patches.Rectangle(((pile_x-1), (pile_y-1)),2,2, linewidth=5, edgecolor='r', facecolor='none')
    ax.add_patch(rect)                         

    ax.grid(True)
    # fig.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf)
    buf.seek(0)
    plt.savefig(r".\Results/" + title + '{}_{}_{}.pdf'.format(pile_name,project_name,r))
    plt.close()
    return(buf)
    

# def plotPlaxisResults_N(result, title,r,factor = 1.0):

#     import matplotlib.pyplot as plt
#     x = result.x.values
#     y = result.y.values
#     ref=result.Pile.values
#     N = abs(result.N.values*factor)
#     N_text = result.N.values*factor
#     print(factor)
#     colors = N
#     d=result.Diameter.values
#     fig, ax = plt.subplots(figsize=(30, 10))
#     ax.scatter(x, y, s = d*0.1, c =d)

#     for i, txt in enumerate(N_text):
#         #print(txt)
#         if txt < 0:
#             ax.annotate('{}\n{:0.0f}kN'.format(ref[i],txt),(x[i]+0.1, y[i]+0.1), color = 'red', rotation=45,fontsize = 5)
#         else:
#             ax.annotate('{}\n{:0.0f}kN'.format(ref[i],txt),(x[i]+0.1, y[i]+0.1), color = 'blue', rotation=45,fontsize = 5)

#     ax.set_xlim([min(x)-5, max(x)+5])
#     ax.set_ylim([min(y)-5, max(y)+5])    
#     ax.set_xlabel(r'$x$ in m', fontsize=15)
#     ax.set_ylabel(r'$y$ in m', fontsize=15)
#     ax.set_title(title + ' - Pile SLS forces ( - for compression and + for tension)')


#     ax.grid(True)
#     #fig.tight_layout()
#     plt.savefig(r".\Results/" + title + ' - Pile SLS forces {}.pdf'.format(r))
#     plt.show()
    
    

# def plotPlaxisResults_U(result, title,r):

#     import matplotlib.pyplot as plt
#     #print(result)
#     x = result.x.values
#     #print(x)
#     y = result.y.values
#     #print(y)   
#     N_text = result.u.values
#     ref=result.Pile.values
#     stage=result.Stage.values
# #    colors = N
#     d=result.Diameter.values
#     fig, ax = plt.subplots(figsize=(30, 10))
#     ax.scatter(x, y, s = d*0.1, c =d)

#     for i, txt in enumerate(N_text):
#         print(stage[i],ref[i],txt)
#         if txt < 0:
#             ax.annotate('{}\n{:0.1f}mm'.format(ref[i],txt),(x[i]+0.1, y[i]+0.5), color = 'red', rotation=45,fontsize = 5)
#         else:
#             ax.annotate('{}\n{:0.1f}mm'.format(ref[i],txt),(x[i]+0.1, y[i]+0.5), color = 'blue', rotation=45,fontsize = 5)

#     ax.set_xlim([min(x)-5, max(x)+5])
#     ax.set_ylim([min(y)-5, max(y)+5])    
#     ax.set_xlabel(r'$x$ in m', fontsize=15)
#     ax.set_ylabel(r'$y$ in m', fontsize=15)
#     ax.set_title(title + ' - Pile Displacement ( - for settlement and + for heave) ')


#     ax.grid(True)
#     #fig.tight_layout()
#     plt.savefig(r".\Results/" + title + ' - Pile Displacement {}.pdf'.format(r))
#     plt.show()
    
    
# def plotPlaxisResults_Uphase(result, title,r):

#     import matplotlib.pyplot as plt
#     #print(result)
#     x = result.x.values
#     #print(x)
#     y = result.y.values
#     #print(y)   
#     N_text = result.u_phase.values
#     ref=result.Pile.values
#     stage=result.Stage.values
# #    colors = N
#     d=result.Diameter.values
#     fig, ax = plt.subplots(figsize=(30, 10))
#     ax.scatter(x, y, s = d*0.1, c =d)

#     for i, txt in enumerate(N_text):
#         print(stage[i],ref[i],txt)
#         if txt < 0:
#             ax.annotate('{}\n{:0.1f}mm'.format(ref[i],txt),(x[i]+0.1, y[i]+2), color = 'red', rotation=45,fontsize = 5)
#         else:
#             ax.annotate('{}\n{:0.1f}mm'.format(ref[i],txt),(x[i]+0.1, y[i]+2), color = 'blue', rotation=45,fontsize = 5)

#     ax.set_xlim([min(x)-5, max(x)+5])
#     ax.set_ylim([min(y)-5, max(y)+5])    
#     ax.set_xlabel(r'$x$ in m', fontsize=15)
#     ax.set_ylabel(r'$y$ in m', fontsize=15)
#     ax.set_title(title + r' - Pile Phase Displacement ( - for settlement and + for heave) ')


#     ax.grid(True)
#     #fig.tight_layout()
#     plt.savefig(r".\Results/" + title + r' - Pile Phase Displacement {}.pdf'.format(r))
#     plt.show()
    
    
    
# def plotPlaxisResults_SF(result, title,r,writer,factor = 1.0):
    
#     thanetsand_top_dic={"No Scour":-15.5,"Scour":-17.5}
#     result.reset_index(inplace=True,drop=True)
#     x = result.x.values
#     #print(x)
#     y = result.y.values
#     #print(y)
#     d=result.Diameter.values
    
#     # pd.Dataframe(data={"Pile":})
#     colors = d
#     fig, ax = plt.subplots(figsize=(30, 10))
#     ax.scatter(x, y, s = d*0.08, c =colors)
    
#     for i in range(0, len(result)):
#         pile_i=result.loc[i,"Pile"]
#         pile_i=pile_i.replace('_Line',"")
#         x_i=result.loc[i,"x"]
#         y_i=result.loc[i,"y"]
#         base=result.loc[i,"Base Resistance (kN)"]
#         shaft=result.loc[i,"Shaft Resistance (kN)"]
#         effects=result.loc[i,"Apply pile group effects?"]
#         toe=result.loc[i,"Toe level(mOD)"]
#         zone=result.loc[i,"Zone"]
#         thanet_sand_top=thanetsand_top_dic[zone]
#         sls=abs(result.loc[i,"N"])
#         usf_sf=(shaft/sls)
#         usf_ueb_sf=(base+shaft)/sls
#         print(pile_i)
#         print("UEB:{:0.2f} kN".format(base))
#         print("USF:{:0.2f} kN".format(shaft))
#         print("SLS load:{:0.2f} kN".format(sls))
#         print("(USF+UEB)/SLS :{:0.2f}".format(usf_ueb_sf))
#         print("(USF)/SLS:{:0.2f}".format(usf_sf))
#         print("\n \n")
        
#         if (usf_ueb_sf<1.95 or usf_sf<0.95) and toe>thanet_sand_top:
#             c="red"
#             f=4
#             status="NOT OK,PLEASE CHANGE"
#             ax.annotate('{}\nPile group effects={}\nSF shaft={:0.2f}\nSF Base+Shaft={:0.2f}\nSF not OK and Pile Toe above Thanet sand\nCHANGE DESIGN'.format(pile_i,effects,usf_sf,usf_ueb_sf),(x_i, y_i), color = c, rotation=45,fontsize = f)
        
#         if (usf_ueb_sf<1.95 or usf_sf<0.95) and toe<=thanet_sand_top:
#             c="blue"
#             f=4
#             status="OK-ish"
#             ax.annotate('{}\nPile group effects={}\nSF shaft={:0.2f}\nSF Base+Shaft={:0.2f}\nSF not OK but Pile inside of Thanet sand \n OK-ish....!'.format(pile_i,effects,usf_sf,usf_ueb_sf),(x_i, y_i), color = c, rotation=45,fontsize = f)

#         if usf_ueb_sf>=1.95 and usf_sf>=0.95:
#             c="black"
#             f=4
#             status="OK"
#             ax.annotate('{}\nPile group effects={}\nSF shaft={:0.2f}\nSF Base+Shaft={:0.2f}'.format(pile_i,effects,usf_sf,usf_ueb_sf),(x_i, y_i), color = c, rotation=45,fontsize = f)
        
#         result.loc[i,"(USF+UEB)/SLS"]=usf_ueb_sf
#         result.loc[i,"(USF)/SLS"]=usf_sf
#         result.loc[i,"Status"]=status
#         print(status)
#         print(c)
        
#     new_result = result[['Pile', 'Diameter', 'Stage','x','y','z','u','Zone','Toe level(mOD)','Apply pile group effects?','Base Resistance (kN)',	
#                             'Shaft Resistance (kN)','N','(USF+UEB)/SLS','(USF)/SLS','Status']].copy()
#     new_result["Pile"]=new_result["Pile"].apply(lambda x:x.replace('_Line',""))
#     new_result["N"]=new_result["N"].apply(lambda x:float("{:0.2f}".format(-x)))
#     new_result.to_excel(writer,sheet_name=title)
        
    
#     # for i, txt in enumerate(N):
#     #     print(i,txt)
#     #     ax.annotate('{}\nSF shaft={:0.2f}'.format(ref[i],pile_capacities[d[i],comp]/txt),(x[i]-1, y[i]+3), color = 'blue', rotation=45,fontsize = 5)
    
    
#     ax.set_xlim([min(x)-5, max(x)+5])
#     ax.set_ylim([min(y)-5, max(y)+5])    
#     ax.set_xlabel(r'$x$ in m', fontsize=15)
#     ax.set_ylabel(r'$y$ in m', fontsize=15)
#     ax.set_title(title + ' - Safety factor checks')
    
    
#     ax.grid(True)
#     #fig.tight_layout()
#     plt.savefig(r".\Results/" + title + ' - Safety factor {}.pdf'.format(r))
    
#     plt.show()
