import sys,os,math,arcpy,time

def x_4(x1,y1,x2,y2,x3,y3):
    f_x = ((x1-x2)*x3)/(y1-y2)
    s_x = ((y1-y2)*x1)/(x1-x2)
    c_x = (((y1-y2)/(x1-x2))+((x1-x2)/(y1-y2)))
    r_x = y3-y1
    return (f_x+s_x+r_x)/c_x

def y_4(x1,y1,x2,y2,x3,y3):
    f_y = ((y1-y2)/(x1-x2))*x_4(x1,y1,x2,y2,x3,y3)
    s_y = ((y1-y2)*x1)/(x1-x2)
    r_y = y1
    return f_y-s_y+r_y

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


"Shape@"
xy1 = row1[0].firstPoint
startx = xy1.X  
starty = xy1.Y 
##########################################################################

desc = arcpy.Describe(feat)
sr_set = arcpy.SpatialReference('NAD 1983 UTM ZONE 17N') 
new = os.path.join(arcpy.env.workspace,str(desc.baseName)+'_Proj.shp')
arcpy.Project_management(feat, new, sr_set) 

arcpy.CopyFeatures_management(plot(geom),os.path.join(arcpy.env.workspace,str(desc.baseName)+str(count)+'_closestPoint.shp'))

arcpy.DefineProjection_management(n,arcpy.SpatialReference('NAD 1983 UTM ZONE 17N'))

##########################################################################

with arcpy.da.UpdateCursor(f_1,["ASSET_ID","StartStamp","EndStamp"]) as update:
    for row in update:
        with arcpy.da.SearchCursor(f_2,["ASSET_ID","Diststamp1","Diststamp2"]) as search:
            for row2 in search:
                if row[0]==row2[0]:
                    row[1]=row2[1]
                    row[2]=row2[2]
                    update.updateRow(row)

