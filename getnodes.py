'''
    This script is meant to capture the nodes from the polylines in a shapefile
    and reconstruct another line by connecting all the coordinates together.
'''


import arcpy, os, csv
from arcpy import env
arcpy.env.overwriteOutput = True

root = os.getcwd()
xory = raw_input(str('Do you want to sort in "x" direction or "y" direction: '))
shape = '2B_Changed.shp'
shpf = os.path.join(root,shape)
xl = open(os.path.join(root,'check.csv'))

name = 'Sort_recno_ASC.shp'
if arcpy.Exists(os.path.join(root,name)):
    shp = os.path.join(root,name)
else:
    shp = arcpy.Sort_management(shpf, os.path.join(root,name), [['Record_Number', 'ASCENDING']])

b = 0
rw_list = []
for row in xl:
    if b > 0:
        rw_list.append(str(row[:6]))
    b+=1
xl.close()

def naming(name):
    if name == 'x':
        name = 'Sorted_Xdir.shp'
    else:
        name = 'Sorted_Ydir.shp'
    return name

############################################################################################################

c=0
recordList = []
for rw in rw_list:
    chg = []
#---
    with arcpy.da.SearchCursor(shp, ["SHAPE@WKT",'section','Record_Number']) as cur:
#---#---
        for row in cur:
#---#---#---
            if str(row[1]) == str(rw):
#---#---#---#---
                op = str(cur[0]).find('(')
                cp = str(cur[0]).find(')')
                unlisted = str(cur[0][op+2:cp])
                listed = unlisted.split(" ")
                d = 0
                newList = []
                innerList = []
                for item in listed:
#---#---#---#---#---
                    d+=1
                    e = d//3
                    if not (d-e == e*2):
#---#---#---#---#---#---
                        innerList.append(float(item))
                    else:
                        newList.append(innerList)
                        innerList = []
#---#---#---#---
                c+=1
                recordList.append([int(str(row[1])), newList]) 


print c, " records were read"

############################################################################################################

d = dict()
x = 0

for rec in recordList:
    k = rec[0]
    v = rec[1]
    if k not in d:
        d[k] = list()
    for n in v:
        d[k].append((n[0],n[1]))

############################################################################################################
        
lines = []

if not os.path.exists(os.path.join(root,'results')):
    os.makedirs(os.path.join(root,'results'))

name = naming(xory)

for k, v in d.iteritems():
    v.sort(key = lambda node: (node[0], node[1])) # not a very clean sorting method!!! It's not a spatial sort.
    # One weay to do a spatial sort is to track which node is coming from which feature.
    # This means more code that's not implemented here.
    lines.append(arcpy.Polyline(arcpy.Array([arcpy.Point(*coords) for coords in v]),'WGS 1984'))


arcpy.CopyFeatures_management(lines, os.path.join(root,os.path.join('results',name)))
