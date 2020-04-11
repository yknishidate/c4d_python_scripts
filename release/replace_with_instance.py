import c4d
import os
from c4d import gui

class MyDialogs(gui.GeDialog):

    def GetLink(self, param_id):
        gui = self.FindCustomGui(param_id, c4d.CUSTOMGUI_LINKBOX)
        if gui:
            return gui.GetLink()
        return None

    def AddLinkBox(self, param_id, flags, link=None):
        gui = self.AddCustomGui(param_id, c4d.CUSTOMGUI_LINKBOX, "", flags, 400, 0)
        gui.SetLink(link)
        return gui

    def CreateLayout(self):
        self.SetTitle("Replace with instance")
        self.GroupBegin(1, c4d.BFH_LEFT, 2)
        self.AddStaticText(1002, c4d.BFH_LEFT, 150, 0, "Reference Object", c4d.BORDER_NONE)
        self.AddLinkBox(1000, c4d.BFH_LEFT)
        self.AddStaticText(1003, c4d.BFH_LEFT, 150, 0, "Instance Mode", c4d.BORDER_NONE)
        self.AddComboBox(1004, c4d.BFH_LEFT, 357, 0)
        self.AddChild(1004, 0, "Instance")
        self.AddChild(1004, 1, "Render Instance")
        self.AddChild(1004, 2, "Multi-Instance")
        self.AddStaticText(1005, c4d.BFH_LEFT, 150, 0, "Position Source", c4d.BORDER_NONE)
        self.AddLinkBox(1006, c4d.BFH_LEFT)
        self.AddStaticText(1007, c4d.BFH_LEFT, 150, 0, "Viewport Mode", c4d.BORDER_NONE)
        self.AddComboBox(1008, c4d.BFH_LEFT, 357, 0)
        self.AddChild(1008, 0, "Off")
        self.AddChild(1008, 1, "Points")
        self.AddChild(1008, 3, "Matrix")
        self.AddChild(1008, 4, "Bounding Box")
        self.AddChild(1008, 2, "Object")
        self.SetInt32(1008, 2)
        self.HideElement(1005, True)
        self.HideElement(1006, True)
        self.HideElement(1007, True)
        self.HideElement(1008, True)
        self.GroupEnd()
        # Layer Setting
        self.GroupBegin(2, c4d.BFH_LEFT, 2)
        self.GroupBorder(c4d.BORDER_MASK)
        self.AddStaticText(1009, c4d.BFH_LEFT, 150, 0, "Layer", c4d.BORDER_NONE)
        self.AddComboBox(1010, c4d.BFH_LEFT, 357, 0)
        self.AddChild(1010, 0, "None")
        self.AddChild(1010, 1, "Keep Original Layer")
        self.AddChild(1010, 2, "Replace with Reference Layer")
        self.GroupEnd()
        # Replace
        self.GroupBegin(2, c4d.BFH_CENTER, 2)
        self.AddButton(1100, c4d.BFH_CENTER, 0, 0, "Replace")
        self.GroupEnd()
        return True

    def Command(self, id, msg):
        if id == 1100:
            base = self.GetLink(1000)
            if base != None:
                objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_NONE)
                doc.StartUndo()
                for i, obj in enumerate(objects):
                    # Create Instance
                    instance = c4d.BaseObject(c4d.Oinstance)
                    # Undo
                    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
                    doc.AddUndo(c4d.UNDOTYPE_NEW, instance)
                    # Instance Data
                    instance[c4d.INSTANCEOBJECT_LINK] = base
                    instance[c4d.ID_BASEOBJECT_REL_POSITION] = obj[c4d.ID_BASEOBJECT_REL_POSITION]
                    instance[c4d.ID_BASEOBJECT_REL_SCALE] = obj[c4d.ID_BASEOBJECT_REL_SCALE]
                    instance[c4d.ID_BASEOBJECT_REL_ROTATION] = obj[c4d.ID_BASEOBJECT_REL_ROTATION]
                    instance[c4d.INSTANCEOBJECT_RENDERINSTANCE_MODE] = self.GetInt32(1004)
                    instance[c4d.INSTANCEOBJECT_MULTIPOSITIONINPUT] = self.GetLink(1006)
                    instance[c4d.INSTANCEOBJECT_DRAW_MODE] = self.GetInt32(1008)
                    # Layer
                    layer = self.GetInt32(1010)
                    if layer == 1:
                        instance.SetLayerObject( obj.GetLayerObject(doc) )
                    if layer == 2:
                        instance.SetLayerObject( base.GetLayerObject(doc) )
                    instance.SetName(obj.GetName() + "_" + base.GetName() + "_" + str(i) )
                    instance.InsertBefore(obj)
                    # Replace Children
                    children = obj.GetChildren()
                    for child in reversed(children):
                        child.InsertUnder(instance)
                    # Copy Animation
                    tracks = obj.GetCTracks()
                    trackListToCopy = [c4d.ID_BASEOBJECT_POSITION, c4d.ID_BASEOBJECT_ROTATION, c4d.ID_BASEOBJECT_SCALE]
                    for track in tracks:
                        did = track.GetDescriptionID()
                        if not did[0].id in trackListToCopy:
                            continue
                        foundTrack = instance.FindCTrack(did)
                        if foundTrack:
                            foundTrack.Remove()
                        clone = track.GetClone()
                        instance.InsertTrackSorted(clone)
                    animateflag = c4d.ANIMATEFLAGS_NONE if c4d.GetC4DVersion() > 20000 else c4d.ANIMATEFLAGS_0
                    doc.AnimateObject(instance, doc.GetTime(), animateflag)
                    # Remove Obj
                    obj.Remove()
                doc.EndUndo()
                c4d.EventAdd()
        if id == 1004:
            mode = self.GetInt32(1004)
            if mode == 0:
                self.HideElement(1005, True)
                self.HideElement(1006, True)
                self.HideElement(1007, True)
                self.HideElement(1008, True)
                self.LayoutChanged(1)
            elif mode == 1:
                self.HideElement(1005, True)
                self.HideElement(1006, True)
                self.HideElement(1007, True)
                self.HideElement(1008, True)
                self.LayoutChanged(1)
            else:
                self.HideElement(1005, False)
                self.HideElement(1006, False)
                self.HideElement(1007, False)
                self.HideElement(1008, False)
                self.LayoutChanged(1)
        return True
    
def main():
    dlg = MyDialogs()
    script_open_async_dialog(dlg)
    
def script_open_async_dialog(dlg):
    dialogs = vars(os).setdefault('__c4d_dialogs', [])
    dialogs = [d for d in dialogs if d.IsOpen()]
    dialogs.append(dlg)
    os.__c4d_dialogs = dialogs
    return dlg.Open(c4d.DLG_TYPE_ASYNC, 0, -1, -1, 0, 0)

if __name__=='__main__':
    main()
    c4d.EventAdd()