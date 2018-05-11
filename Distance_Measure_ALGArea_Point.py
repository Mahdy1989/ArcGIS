'''
    Author: Seyed-Mahdy Sadraddini
    Contact: msadraddini@gmail.com
'''
import sys,os,math,arcpy,time

def x_4(x1,y1,x2,y2,x3,y3):
    f_x = ((x1-x2)*x3)/(y1-y2)
    s_x = ((y1-y2)*x1)/(x1-x2)
    c_x = (((y1-y2)/(x1-x2))+((x1-x2)/(y1-y2)))
    r_x = y3-y1
    return (f_x+s_x+r_x)/c_x

def y_4(x1,y1,x2,y2,x3,y3):
    f_y = ((y1-y2)/(x1-x2)) * x_4(x1,y1,x2,y2,x3,y3)
    s_y = ((y1-y2)*x1)/(x1-x2)
    r_y = y1
    return f_y - s_y + r_y

def area(dist1,dist2,dist3):
    s = (dist1+dist2+dist3)/2
    return math.sqrt((s*(s-dist1)*(s-dist2)*(s-dist3)))

def distance_2D(x1,x2,y1,y2):
    return math.sqrt(((x1-x2)**2+(y1-y2)**2))

def DIR():
    return os.getcwd() 

def point(x,y):
    P = arcpy.Point()
    P.X = x
    P.Y = y
    return P

def plot(alist):
    pGeom=[]
    for p in alist:
        pGeom.append(arcpy.PointGeometry(p))
    return pGeom

##############################################################################################################################
########################################## INPUTS INTO THE PROGRAM ###########################################################
##############################################################################################################################
fc1 = raw_input(str('Please enter the name of your first input: '))
fc2 = raw_input(str('Please enter the name of your second input: '))
fc3 = raw_input(str('Please enter the name of your third input: '))
fc4 = raw_input(str('Please enter the name of your fourth input: '))
fc5 = raw_input(str('Please enter the name of your fifth input: '))
fc6 = raw_input(str('Please enter the name of your sixth input: '))
fc7 = raw_input(str('Please enter the name of your seventh input: '))
fc8 = raw_input(str('Please enter the name of your eighth input: '))
fc9 = raw_input(str('Please enter the name of your nineth input: '))
fc10 = raw_input(str('Please enter the name of your tenth input: '))
fc11 = raw_input(str('Please enter the name of your eleventh input: '))
fc12 = raw_input(str('Please enter the name of your twelvth input: '))
fc13 = raw_input(str('Please enter the name of your thirteenth input: '))
fc14 = raw_input(str('Please enter the name of your fourteenth input: '))
fc15 = raw_input(str('Please enter the name of your fifteenth input: '))
fc16 = raw_input(str('Please enter the name of your comparison layer input from which results will be extrapolated: '))# This must be of Point type geometry, have the distancestamp field --> ARAN Data
##############################################################################################################################

print '\n'
arcpy.env.workspace = os.path.join(str(DIR()),'results')
arcpy.env.overwriteOutput = True
feats = [fc1,fc2,fc3,fc4,fc5,fc6,fc7,fc8,fc9,fc10,fc11,fc12,fc13,fc14,fc15,fc16]
f1 = [] # used to tie back info at this level
fcs = list()

for feat in feats:
    if feat == '':
        pass
    elif not arcpy.Exists(feat):
        print "I/O ERROR..."
        print feat,': Your entry is wrong...\nIt either does not exist or it does not follow correct naming convention...\n'
        time.sleep(0.5)
        pass
    else:
        f1.append(feat)
        desc = arcpy.Describe(feat)
        sr_set = arcpy.SpatialReference('NAD 1983 UTM ZONE 14N') 
        new = os.path.join(arcpy.env.workspace,str(desc.baseName)+'_Proj.shp')
        arcpy.Project_management(feat, new, sr_set) 
        dataStrings = new.split('\\')
        fcs.append(str(dataStrings[-1]))
        print str(dataStrings[-1]),'has been created with NAD 1983 UTM ZONE 14N as spatial reference.\n'

for fc in fcs:
    if fc != fcs[-1]:
        try:
            arcpy.AddField_management(fc,"DIST1METR", "DOUBLE",8,5,12) # store the shortest distance to start of line
            arcpy.AddField_management(fc,"CLOSE1X", "DOUBLE",20,10,20) # x1 start 
            arcpy.AddField_management(fc,"CLOSE1Y", "DOUBLE",20,10,20) # y1 start 
            arcpy.AddField_management(fc,"DistStamp1", "DOUBLE",20,10,20) # distance stamp in meter for start
        except:
            pass
        
srch = fcs[-1]

for fc in fcs:
    if fc != fcs[-1]:
        geom1 = [] 
        desc = arcpy.Describe(fc)
        stamp = list()

        with arcpy.da.UpdateCursor(fc, ["Shape@","OBJECTID","DIST1METR","CLOSE1X","CLOSE1Y","DistStamp1"]) as update:    
            for row1 in update:
                xy1 = row1[0].firstPoint
                startx = xy1.X  
                starty = xy1.Y  

                distanceList1 = []
                
                with arcpy.da.SearchCursor(srch, ['Shape@','distancest']) as search: 
                    for row2 in search:
                        xy3 = row2[0].firstPoint
                        xT = xy3.X
                        yT = xy3.Y

                        distance1 = distance_2D(startx,xT,starty,yT)

                        distanceList1.append([distance1,xT,yT,row2[1]])

                        distanceList1.sort() 

                dist11 = distance_2D(distanceList1[0][1],distanceList1[1][1],distanceList1[0][2],distanceList1[1][2])
                dist12 = distanceList1[0][0]
                dist13 = distanceList1[1][0] 

                row1[2] = (2*area(dist11,dist12,dist13))/dist11  
              
                row1[3] = x_4(distanceList1[0][1],distanceList1[0][2],distanceList1[1][1],distanceList1[1][2],startx,starty)
                row1[4] = y_4(distanceList1[0][1],distanceList1[0][2],distanceList1[1][1],distanceList1[1][2],startx,starty)
                ration1 = distance_2D(distanceList1[0][1],float(str(row1[3])), 
                                      distanceList1[0][2],float(str(row1[4]))) 
                ratio1 = ration1/dist11 
                if float(str(distanceList1[0][3]))>float(str(distanceList1[1][3])): 
                    ratio1 = 1 - ratio1 
                row1[5] = (ratio1 * (max(distanceList1[0][3],distanceList1[1][3])-min(distanceList1[0][3],distanceList1[1][3]))
                                                        + min(float(str(distanceList1[0][3])),float(str(distanceList1[1][3]))))  
                geom1.append(point(row1[3],row1[4]))
                
                update.updateRow(row1)

                print 'OBJECTID',row1[1],desc.baseName,'is processed'

                del distanceList1
                del ration1
                del ratio1
                
        geomList =[geom1]
        name2 = []
        count = 1
        for geom in geomList:
            if geom!=[]:
                arcpy.CopyFeatures_management(plot(geom),os.path.join(arcpy.env.workspace,str(desc.baseName)+str(count)+'_closestPoint.shp'))
                name2.append(os.path.join(arcpy.env.workspace,str(desc.baseName)+str(count)+'_closestPoint.shp'))
                count+=1
        print '\n'
        for n in name2:
            arcpy.DefineProjection_management(n,arcpy.SpatialReference('NAD 1983 UTM ZONE 14N'))
            print n, "point file has been compiled"
        print '\n'
                    
        del geom1
        del name2
        del count
