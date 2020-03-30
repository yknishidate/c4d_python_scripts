import c4d

def make_editable(obj, inserted=False):

    res = c4d.utils.SendModelingCommand(command=c4d.MCOMMAND_MAKEEDITABLE, list=[obj])
    if not res:
        print "failed"
        return False
    print "SUCCESS: ", "make_editable"
    return res[0]

def copy_coodinates(from_obj, to_obj):
    to_obj.SetMg(from_obj.GetMg())

def main():
    spline = doc.GetActiveObject()
    if not spline:
        print "ERROR  : select spline"
        return
    print "SUCCESS: ", "selected"


    if not spline.CheckType(c4d.Ospline):
        print "this is NOT Oline"
        return
    print "SUCCESS: ", "this  is Oline"

    count = spline.GetPointCount()
    print "SUCCESS: ", "count = ", count
    matrix = spline.GetMg()
    print "SUCCESS: ", "matrix = ", matrix
    spline.SetMg(c4d.Matrix())

    mospl = c4d.BaseObject(440000054) # MoSpline
    print "SUCCESS: ", "MoSpline = ", mospl

    mospl[c4d.MGMOSPLINEOBJECT_MODE] = 1 # spline
    mospl[c4d.MGMOSPLINEOBJECT_SPLINE_MODE] = 2 # even
    mospl[c4d.MGMOSPLINEOBJECT_SOURCE_SPLINE] = spline
    mospl[c4d.MGMOSPLINEOBJECT_SPLINE_COUNT] = count
    mospl.SetName(spline.GetName())
    mospl.SetMg(matrix)

    print "SUCCESS: ", "MoSpline = ", mospl

    doc.InsertObject(mospl)
    res = make_editable(mospl)
    res.InsertBefore(spline)

    c4d.EventAdd()


if __name__ == '__main__':
    main()
    c4d.EventAdd()