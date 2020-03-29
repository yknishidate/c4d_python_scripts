import c4d
from c4d import gui

def make_editable(obj, inserted=False):
    if not inserted:
        doc.InsertObject(obj)
    res = c4d.utils.SendModelingCommand(command=c4d.MCOMMAND_MAKEEDITABLE, list=[obj])
    if not res:
        print "failed"
        return False
    doc.InsertObject(res[0])
    c4d.EventAdd()

def main():
    cube = c4d.BaseObject(c4d.Ocube)
    make_editable(cube)

# Execute main()
if __name__=='__main__':
    main()
    c4d.EventAdd()