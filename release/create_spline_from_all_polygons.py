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
    # select polygon
    sel.DeselectAll()
    sel.Select(index)

    # convert selection (polygon -> edge)
    c4d.utils.SendModelingCommand(c4d.MCOMMAND_CONVERTSELECTION, [obj],
                                  c4d.MODELINGCOMMANDMODE_POLYGONSELECTION,
                                  setting, doc)
    # edge to spline
    c4d.utils.SendModelingCommand(c4d.MCOMMAND_EDGE_TO_SPLINE, [obj])
c4d.EventAdd()