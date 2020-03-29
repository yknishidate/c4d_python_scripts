
import c4d
import c4d.utils
from c4d import gui
import math

#These multi-line strings are going to be put into our rig's Python tag later
pythontagcode = """
import c4d
import math
from c4d import gui

def main():
    bend = op.GetObject()
    parent = bend.GetUp()
    enable = op[c4d.ID_USERDATA,2]
    subbend = op[c4d.ID_USERDATA,3]
    #bend[c4d.DEFORMOBJECT_STRENGTH]
    #parent.SetAbsRot(c4d.Vector(0, -bend[c4d.DEFORMOBJECT_STRENGTH]/2, c4d.utils.DegToRad(90)))

    if enable:
        subbend[c4d.DEFORMOBJECT_STRENGTH] = -bend[c4d.DEFORMOBJECT_STRENGTH]
        subbend[c4d.DEFORMOBJECT_ANGLE] = -bend[c4d.DEFORMOBJECT_ANGLE]


def message(id, data) :
    bend = op.GetObject()
    parent = bend.GetUp()
    orientation = op[c4d.ID_USERDATA,1]

    if id == c4d.MSG_DESCRIPTION_CHECKUPDATE:
        #print "Changed"
        enable = op[c4d.ID_USERDATA,2]
        print enable
        subbend = op[c4d.ID_USERDATA,3]
        print subbend

        # Arc Mode
        if enable:
            if   orientation == 0 or orientation == 1: # +X or -X
                print("+X")
                bend.SetAbsPos(c4d.Vector(parent.GetRad()[0]/2, 0, 0))
                bend.SetAbsRot(c4d.Vector(0, c4d.utils.DegToRad(-90), c4d.utils.DegToRad(90)))
                bend[c4d.DEFORMOBJECT_SIZE] = c4d.Vector(parent.GetRad()[2]*2, parent.GetRad()[0], parent.GetRad()[1]*2)

                subbend.SetAbsPos(c4d.Vector(-parent.GetRad()[0]/2, 0, 0))
                subbend.SetAbsRot(c4d.Vector(0, c4d.utils.DegToRad(-90), c4d.utils.DegToRad(-90)))
                subbend[c4d.DEFORMOBJECT_SIZE] = c4d.Vector(parent.GetRad()[2]*2, parent.GetRad()[0], parent.GetRad()[1]*2)

            elif orientation == 2 or orientation == 3: # +Y or -Y
                print("+Y")
                bend.SetAbsPos(c4d.Vector(0, parent.GetRad()[1]/2, 0))
                bend.SetAbsRot(c4d.Vector(0, 0, 0))
                bend[c4d.DEFORMOBJECT_SIZE] = c4d.Vector(parent.GetRad()[0]*2, parent.GetRad()[1], parent.GetRad()[2]*2)

                subbend.SetAbsPos(c4d.Vector(0, -parent.GetRad()[1]/2, 0))
                subbend.SetAbsRot(c4d.Vector(c4d.utils.DegToRad(180), c4d.utils.DegToRad(180), 0))
                subbend[c4d.DEFORMOBJECT_SIZE] = c4d.Vector(parent.GetRad()[0]*2, parent.GetRad()[1], parent.GetRad()[2]*2)

            elif orientation == 4 or orientation == 5: # +Z or -Z
                print("+Z")
                bend.SetAbsPos(c4d.Vector(0, 0, parent.GetRad()[2]/2))
                bend.SetAbsRot(c4d.Vector(0, c4d.utils.DegToRad(-90), 0))
                bend[c4d.DEFORMOBJECT_SIZE] = c4d.Vector(parent.GetRad()[0]*2, parent.GetRad()[2], parent.GetRad()[1]*2)

                subbend.SetAbsPos(c4d.Vector(0, 0, -parent.GetRad()[2]/2))
                subbend.SetAbsRot(c4d.Vector(0, c4d.utils.DegToRad(-90), c4d.utils.DegToRad(-180)))
                subbend[c4d.DEFORMOBJECT_SIZE] = c4d.Vector(parent.GetRad()[0]*2, parent.GetRad()[2], parent.GetRad()[1]*2)

        else:
            bend.SetAbsPos(c4d.Vector(0, 0, 0))
            # Normal Mode
            if   orientation == 0: # +X
                print("+X")
                bend.SetAbsRot(c4d.Vector(0, c4d.utils.DegToRad(-90), c4d.utils.DegToRad(90)))
                bend[c4d.DEFORMOBJECT_SIZE] = c4d.Vector(parent.GetRad()[2]*2, parent.GetRad()[0]*2, parent.GetRad()[1]*2)
            elif orientation == 1: # -X
                print("-X")
                bend.SetAbsRot(c4d.Vector(0, c4d.utils.DegToRad(-90), c4d.utils.DegToRad(-90)))
                bend[c4d.DEFORMOBJECT_SIZE] = c4d.Vector(parent.GetRad()[2]*2, parent.GetRad()[0]*2, parent.GetRad()[1]*2)
            elif orientation == 2: # +Y
                print("+Y")
                bend.SetAbsRot(c4d.Vector(0, 0, 0))
                bend[c4d.DEFORMOBJECT_SIZE] = parent.GetRad()*2
            elif orientation == 3: # -Y
                print("-Y")
                bend.SetAbsRot(c4d.Vector(c4d.utils.DegToRad(180), c4d.utils.DegToRad(180), 0))
                bend[c4d.DEFORMOBJECT_SIZE] = parent.GetRad()*2
            elif orientation == 4: # +Z
                print("+Z")
                bend.SetAbsRot(c4d.Vector(0, c4d.utils.DegToRad(-90), 0))
                bend[c4d.DEFORMOBJECT_SIZE] = c4d.Vector(parent.GetRad()[0]*2, parent.GetRad()[2]*2, parent.GetRad()[1]*2)
            elif orientation == 5: # -Z
                print("-Z")
                bend.SetAbsRot(c4d.Vector(0, c4d.utils.DegToRad(-90), c4d.utils.DegToRad(-180)))
                bend[c4d.DEFORMOBJECT_SIZE] = c4d.Vector(parent.GetRad()[0]*2, parent.GetRad()[2]*2, parent.GetRad()[1]*2)"""

def new_rig(object):
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, object)

    #create a Python tag and attach it to the first joint
    pythontag = c4d.BaseTag(c4d.Tpython)
    object.InsertTag(pythontag)
    doc.AddUndo(c4d.UNDOTYPE_NEW, pythontag)
    #set the Python code inside the tag
    pythontag[c4d.TPYTHON_CODE] = pythontagcode

    CycleItems = c4d.BaseContainer()
    CycleItems.SetString( 0, "+X" )
    CycleItems.SetString( 1, "-X" )
    CycleItems.SetString( 2, "+Y" )
    CycleItems.SetString( 3, "-Y" )
    CycleItems.SetString( 4, "+Z" )
    CycleItems.SetString( 5, "-Z" )

    #add an Orientation field to the user data
    userdata_Orientation = c4d.GetCustomDataTypeDefault(c4d.DTYPE_LONG)
    userdata_Orientation[c4d.DESC_NAME] = "Orientation"
    userdata_Orientation[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_CYCLE
    userdata_Orientation.SetContainer(c4d.DESC_CYCLE, CycleItems)
    pythontag.AddUserData(userdata_Orientation)

    #add an Orientation field to the user data
    userdata_Orientation = c4d.GetCustomDataTypeDefault(c4d.DTYPE_BOOL)
    userdata_Orientation[c4d.DESC_NAME] = "Enable Arc Bend"
    userdata_Orientation[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_BOOL
    pythontag.AddUserData(userdata_Orientation)

    #add a 'link' field to the python tag's user data -
    #this link will determine which previous bend to attach to
    userdata_link = c4d.GetCustomDataTypeDefault(c4d.DTYPE_BASELISTLINK)
    userdata_link[c4d.DESC_NAME] = "Sub Bend"
    pythontag.AddUserData(userdata_link)

    return pythontag

def getTagsByType(tags, tagtype):
    newtags = []
    for tag in tags:
        if tag.GetType() == tagtype:
            newtags.append(tag)
    return newtags

#returns a list with objects of only the selected type
def filterlist(originallist, objecttype):
    newlist = []
    for op in originallist:
        if op.GetType() == objecttype:
            newlist.append(op)
    return newlist

def main():
    #c4d.CallCommand(5128) # Bend

    oplist = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)

    oplist = filterlist(oplist, c4d.Obend)

    rigtag = new_rig(op)

    c4d.EventAdd()

if __name__=='__main__':
    main()