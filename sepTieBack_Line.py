import sys,os,arcpy,time

'''
The first to Eight inputs have to be equivalent of each other, i.e. similar datasets
'''

##############################################################################################################################
########################################## INPUTS INTO THE PROGRAM ###########################################################
##############################################################################################################################
GDB = raw_input(str('Please enter the name of your geodatabase.extension: '))
RES = raw_input(str('Please enter the name of your results folder: '))
print '\n'
fc1 = raw_input(str('Please enter the name of your first input from GDB: '))
fc2 = raw_input(str('Please enter the name of your second input from GDB: '))
fc3 = raw_input(str('Please enter the name of your third input from GDB: '))
fc4 = raw_input(str('Please enter the name of your fourth input from GDB: '))
fc5 = raw_input(str('Please enter the name of your fifth input from GDB: '))
fc6 = raw_input(str('Please enter the name of your sixth input from GDB: '))
fc7 = raw_input(str('Please enter the name of your seventh input from GDB: '))
fc8 = raw_input(str('Please enter the name of your eighth input from GDB: '))
print '\n'
fc9 = raw_input(str('Please enter the name of your first input from results: '))
fc10 = raw_input(str('Please enter the name of your second input from results: '))
fc11 = raw_input(str('Please enter the name of your third input from results: '))
fc12 = raw_input(str('Please enter the name of your fourth input from results: '))
fc13 = raw_input(str('Please enter the name of your fifth input from results: '))
fc14 = raw_input(str('Please enter the name of your sixth input from results: '))
fc15 = raw_input(str('Please enter the name of your seventh input from results: '))
fc16 = raw_input(str('Please enter the name of your eighth input from results: '))
##############################################################################################################################
##############################################################################################################################
from arcpy import env
env.workspace = r'G:\Lidar'

g1=[fc1,fc2,fc3,fc4,fc5,fc6,fc7,fc8]
g2=[fc9,fc10,fc11,fc12,fc13,fc14,fc15,fc16]
f1=[]
fcs=[]
for g in g1:
    if g=='':
        pass
    else:
        g=os.path.join(GDB,g)
        f1.append(g)

for g in g2:
    if g=='':
        pass
    else:
        g=os.path.join(RES,g,'_proj.shp')
        fcs.append(g)

ff = zip(f1,fcs)
num = 0
for f in ff:
    num+=1
    f_1 = str(f[0])
    f_2 = str(f[1])
    try:
        arcpy.DeleteField_management(f_1,"StartStamp")
        arcpy.DeleteField_management(f_1,"EndStamp")
    except:
        pass
    arcpy.AddField_management(f_1,"StartStamp", "DOUBLE",20,10,20)
    arcpy.AddField_management(f_1,"EndStamp", "DOUBLE",20,10,20)
    print "\nRequired fields are added to", f[0] 
    try:
        with arcpy.da.UpdateCursor(f_1,["ASSET_ID","StartStamp","EndStamp"]) as update:
            for row in update:
                with arcpy.da.SearchCursor(f_2,["ASSET_ID","Diststamp1","Diststamp2"]) as search:
                    for row2 in search:
                        if row[0]==row2[0]:
                            row[1]=row2[1]
                            row[2]=row2[2]
                            update.updateRow(row)
    except Exception as e:
        print e
