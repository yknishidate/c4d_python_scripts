import c4d
from c4d import gui

def main():
    obj = doc.GetActiveObject()
    points = obj.GetAllPoints()
    polygons = obj.GetAllPolygons()
    print "# Vertex"
    for i in range(obj.GetPointCount()):
        print "obj.SetPoint(" + str(i) + ",c4d."+ str(points[i]) +")"
        
    print "\n# Polygon"
    for i in range(obj.GetPointCount()):
        p = (polygons[i].a, polygons[i].b, polygons[i].c, polygons[i].d)
        print "obj.SetPolygon(" +str(i) + ",c4d.CPolygon" + str(p) +")"

if __name__=='__main__':
    main()