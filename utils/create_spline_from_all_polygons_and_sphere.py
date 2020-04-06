import c4d
import random

# setting of "convert selection" command
setting = c4d.BaseContainer()
setting[c4d.MDATA_CONVERTSELECTION_LEFT] = 2  # polygon
setting[c4d.MDATA_CONVERTSELECTION_RIGHT] = 1  # edge

# get object
obj = doc.GetActiveObject()
poly_cnt = obj.GetPolygonCount()

# initialize polygon selection
sel = obj.GetPolygonS()
sel.DeselectAll()

for index in xrange(poly_cnt):
    # select one polygon
    sel.DeselectAll()
    sel.Select(index)

    # convert selection (polygon -> edge)
    c4d.utils.SendModelingCommand(c4d.MCOMMAND_CONVERTSELECTION, [obj],
                                  c4d.MODELINGCOMMANDMODE_POLYGONSELECTION,
                                  setting, doc)
    # edge to spline
    c4d.utils.SendModelingCommand(c4d.MCOMMAND_EDGE_TO_SPLINE, [obj])
    
splines = obj.GetChildren()
for spline in splines:
    # create sphere
    sphere = c4d.BaseObject(c4d.Osphere)
    sphere[c4d.PRIM_SPHERE_RAD] = 1
    sphere[c4d.PRIM_SPHERE_SUB] = 4
    
    # create "align to spline" tag
    tag = c4d.BaseTag(c4d.Taligntospline)
    tag[c4d.ALIGNTOSPLINETAG_LINK] = spline
    
    # attach tag to sphere
    sphere.InsertTag(tag)
    
    # insert sphere to doc
    doc.InsertObject(sphere)

c4d.EventAdd()