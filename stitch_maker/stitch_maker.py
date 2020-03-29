
import c4d

CLONER_OBJECT = 1018544
MOSPLINE_OBJECT = 440000054

def main():

    null  = c4d.BaseObject(c4d.Onull)


    # print test_num
    spline = None                     #Output none here in case we don't have a child object

    obj = op.GetDown()                #Get the child object
    if obj:
        source = obj.GetClone()       #Always work with clones in generators
        selected = source.GetEdgeS()
        count = selected.GetCount()
        if count < 1: return          #Error handling if no edges are selected

        #Note that SendModelingCommand expects a list []
        if c4d.utils.SendModelingCommand(c4d.MCOMMAND_EDGE_TO_SPLINE, [source]):
            spline = source.GetDown().GetClone() #Return a clone of the selected splines
            spline.InsertUnder(null)
        # children = source.GetChildren() #Splines are created as children of the source object
        # print children


    # get userdata
    count = op[c4d.ID_USERDATA,1]
    x = op[c4d.ID_USERDATA,3]
    arc_rad = op[c4d.ID_USERDATA,3]
    arc_rad = op[c4d.ID_USERDATA,4]
    cir_rad = op[c4d.ID_USERDATA,5]

    # circle
    circle = c4d.BaseObject(c4d.Osplinecircle)
    circle[c4d.PRIM_CIRCLE_RADIUS] = cir_rad
    circle[c4d.SPLINEOBJECT_SUB] = 2

    # arc
    arc = c4d.BaseObject(c4d.Osplinearc)
    arc[c4d.PRIM_ARC_RADIUS] = arc_rad
    arc[c4d.PRIM_ARC_START] = c4d.utils.DegToRad(90)
    arc[c4d.PRIM_ARC_END] = c4d.utils.DegToRad(270)
    arc[c4d.PRIM_PLANE] = 2
    arc[c4d.SPLINEOBJECT_SUB] = 2

    # insert
    sweep = c4d.BaseObject(c4d.Osweep)
    arc.InsertUnder(sweep)
    circle.InsertUnder(sweep)

    # cloner
    cloner  = c4d.BaseObject(CLONER_OBJECT)
    cloner[c4d.ID_MG_MOTIONGENERATOR_MODE] = 0              # object
    cloner[c4d.MG_SPLINE_MODE] = 1                          # step
    cloner[c4d.MG_SPLINE_COUNT] = count
    cloner[c4d.ID_MG_TRANSFORM_POSITION,c4d.VECTOR_X] = x
    cloner[c4d.MG_OBJECT_LINK] = spline

    # insert
    sweep.InsertUnder(cloner)
    cloner.InsertUnder(null)
    return null