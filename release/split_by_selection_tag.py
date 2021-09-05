import c4d
from c4d import utils
from c4d import gui

def deselect_all():
    c4d.CallCommand(100004767, 100004767)
    
def activate(obj):
    deselect_all()
    obj.SetBit(c4d.BIT_ACTIVE)

def activate_prev_obj():
    obj = doc.GetActiveObject().GetPred()
    activate(obj)

def split():
    c4d.CallCommand(14046)
    activate_prev_obj()

def get_empty_polygons():
    polys = op.GetPolygonS()
    polys.DeselectAll()
    return polys

def split_by_selection_tag(selection_tag):
    polys = get_empty_polygons()
    count = op.GetPolygonCount()
    selection = selection_tag.GetBaseSelect()
    for i in range(count):
        if selection.IsSelected(i):
            polys.Select(i)
    split()

def main():
    tags = op.GetTags()
    for tag in tags:
        if type(tag) is c4d.SelectionTag:
            split_by_selection_tag(tag)

    op.Message(c4d.MSG_UPDATE)  
    c4d.EventAdd()  

if __name__=='__main__':
    main()
