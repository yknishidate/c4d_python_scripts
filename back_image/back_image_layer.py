import c4d
import os
from c4d import gui, bitmaps, storage


class MyDialogs(gui.GeDialog):
    baseDraw = doc.GetActiveBaseDraw()

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
        self.SetTitle("Test")

        self.GroupBegin(10000, c4d.BFH_CENTER, 2)
        self.linkBox_1 = self.AddLinkBox(1000, c4d.BFH_LEFT)
        self.AddButton(1001, c4d.BFH_CENTER, 0, 0, "...")
        self.GroupEnd()

        return True

    def Command(self, id, msg):
        if id == 1001: # ...
            # Set BackImage
            path = storage.LoadDialog(type=c4d.FILESELECTTYPE_IMAGES, title = 'Open Image')
            self.baseDraw[c4d.BASEDRAW_DATA_PICTURE] = path

            # Print Current LinkBox
            #mylink = self.linkBox_1.GetLink(doc)
            #print mylink

            # Get Bitmap from Path
            bmp = bitmaps.BaseBitmap()
            bmp.InitWith(path)
            #bitmaps.ShowBitmap(bmp)
            #self.linkBox_1.SetLink(bmp)

            # Shader
            #material = doc.GetFirstMaterial()
            #shader = material[c4d.MATERIAL_LUMINANCE_SHADER]
            #shader = c4d.BaseShader(c4d.Xbitmap)
            #shader_bmp = shader.GetBitmap()
            #bitmaps.ShowBitmap(shader_bmp)
            #print shader
            #print shader_bmp

            #self.linkBox_1.SetLink(shader)

            c4d.EventAdd()
        return True

def main():
    dlg = MyDialogs()
    script_open_async_dialog(dlg)





    c4d.EventAdd()

def script_open_async_dialog(dlg):
    dialogs = vars(os).setdefault('__c4d_dialogs', [])
    dialogs = [d for d in dialogs if d.IsOpen()]
    dialogs.append(dlg)
    os.__c4d_dialogs = dialogs
    return dlg.Open(c4d.DLG_TYPE_ASYNC, 0, -1, -1, 0, 0)

if __name__=='__main__':
    main()