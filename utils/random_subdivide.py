import c4d
import random

setting = c4d.BaseContainer()
setting.SetData(c4d.MDATA_DISCONNECT_PRESERVEGROUPS, True)

cube = doc.GetActiveObject()
c4d.utils.SendModelingCommand(c4d.MCOMMAND_DISCONNECT, [cube],
                              c4d.MODIFY_POINTSELECTION, setting, doc)

poly_cnt = cube.GetPolygonCount()
    
sel = cube.GetPolygonS()
sel.DeselectAll()

prob = 0.5

for index in xrange(poly_cnt):
    print index
    if random.random() < prob:
        sel.Select(index)
    
    
c4d.utils.SendModelingCommand(c4d.MCOMMAND_SUBDIVIDE, [cube],
                              c4d.MODELINGCOMMANDMODE_POLYGONSELECTION, doc=doc)
c4d.utils.SendModelingCommand(c4d.MCOMMAND_DISCONNECT, [cube],
                              c4d.MODIFY_POINTSELECTION, setting, doc)
c4d.EventAdd()