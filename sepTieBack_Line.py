import sys,os,arcpy,time

'''
The first to Eight inputs have to be equivalent of each other, i.e. similar datasets
'''

from arcpy import env
env.workspace = r'G:\Lidar'

...
...
...

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
