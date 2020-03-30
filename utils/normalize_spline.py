import c4d

def make_editable(obj, inserted=False):

    res = c4d.utils.SendModelingCommand(command=c4d.MCOMMAND_MAKEEDITABLE, list=[obj])
    if not res:
        print "failed"
        return False
    return res[0]

def copy_coodinates(from_obj, to_obj):
    to_obj.SetMg(from_obj.GetMg())

def main():
    splines = doc.GetActiveObjects(1)

    doc.StartUndo()

    for spline in splines:
        if not spline.CheckType(c4d.Ospline):
            print "this is NOT Oline"
            continue

        count = spline.GetPointCount()
        matrix = spline.GetMg()
        spline.SetMg(c4d.Matrix())

        mospl = c4d.BaseObject(440000054) # MoSpline
        mospl[c4d.MGMOSPLINEOBJECT_MODE] = 1 # spline
        mospl[c4d.MGMOSPLINEOBJECT_SPLINE_MODE] = 2 # even
        mospl[c4d.MGMOSPLINEOBJECT_SOURCE_SPLINE] = spline
        mospl[c4d.MGMOSPLINEOBJECT_SPLINE_COUNT] = count
        mospl.SetName(spline.GetName())
        mospl.SetMg(matrix)

        doc.InsertObject(mospl)
        res = make_editable(mospl)
        res.InsertAfter(spline)

        c4d.EventAdd()
        doc.AddUndo(c4d.UNDOTYPE_NEW, mospl)

        doc.AddUndo(c4d.UNDOTYPE_DELETE, spline)
        spline.Remove()

        doc.SetActiveObject(mospl,1)

    doc.EndUndo()

if __name__ == '__main__':
    main()
    c4d.EventAdd()