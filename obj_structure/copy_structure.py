import c4d
from c4d import gui
# Welcome to the world of Python


# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True


# Main function
def main():
    obj = doc.GetActiveObject()
    points = obj.GetAllPoints()
    polygons = obj.GetAllPolygons()
    vert_cnt = obj.GetPointCount()
    poly_cnt = obj.GetPolygonCount()
    structure = "import c4d\ndef main():\n    obj = c4d.BaseObject(c4d.Opolygon)\n"
    structure += "    obj.ResizeObject(" + str(vert_cnt) + "," + str(poly_cnt) + ")"
    structure += "\n    # Vertex\n"
    for i in range(vert_cnt):
        structure += "    obj.SetPoint(" + str(i) + ",c4d."+ str(points[i]) +")\n"

    structure += "\n    # Polygon\n"
    for i in range(vert_cnt):
        p = (polygons[i].a, polygons[i].b, polygons[i].c, polygons[i].d)
        structure += "    obj.SetPolygon(" +str(i) + ",c4d.CPolygon" + str(p) +")\n"


    structure += "\n    return obj"
    print structure

    
    c4d.CallCommand(1023866, 1023866) # Python Generator
    generator = doc.GetActiveObject()
    generator[c4d.OPYTHON_CODE] = structure

# Execute main()
if __name__=='__main__':
    main()