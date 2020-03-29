import c4d
from c4d import gui

class MyDialogs(gui.GeDialog):
    def findSketchAndToon(self, renderData):
        curEffect = renderData.GetFirstVideoPost()
        while curEffect is not None:
            if curEffect.GetType() == 1011015: # 'Sketch and Toon'
                return curEffect
            curEffect = curEffect.GetNext()
        return 0

    def CreateLayout(self):
        self.SetTitle("Easy Isoparm Render")

        self.GroupBegin(1, c4d.BFH_LEFT, 2) # |-|-|

        self.AddStaticText(1000, c4d.BFH_LEFT, 150, 0, "Background", c4d.BORDER_NONE)
        self.AddColorField(1001, c4d.BFH_LEFT, 115, 0)
        self.SetColorField(1001, c4d.Vector(0.1, 0.1, 0.1), 1, 1, c4d.DR_COLORFIELD_NO_BRIGHTNESS)

        self.AddStaticText(1010, c4d.BFH_LEFT, 150, 0, "Line Color", c4d.BORDER_NONE)
        self.AddColorField(1011, c4d.BFH_LEFT, 115, 0,)
        self.SetColorField(1011, c4d.Vector(1, 1, 1), 1, 1, c4d.DR_COLORFIELD_NO_BRIGHTNESS)

        self.AddStaticText(1020, c4d.BFH_LEFT, 150, 0, "Line Thickness", c4d.BORDER_NONE)
        self.AddEditNumberArrows(1021, c4d.BFH_LEFT, 82, 0)
        self.SetFloat(1021, 2)

        self.GroupEnd()

        self.AddButton(1100, c4d.BFH_CENTER, 0, 0, "OK")

        return True

    def Command(self, id, msg):
        if id == 1100:
            doc.StartUndo()
            #doc.AddUndo(c4d.UNDOTYPE_CHANGE, None)

            renderData = doc.GetActiveRenderData()

            # Add Material
            sketchMat = c4d.BaseMaterial(1011014)
            sketchMat[c4d.OUTLINEMAT_COLOR] = self.GetColorField(1011)['color']
            sketchMat[c4d.OUTLINEMAT_THICKNESS] = self.GetFloat(1021)
            doc.InsertMaterial(sketchMat)

            # Add Sketch and Toon
            sketchEffect = self.findSketchAndToon(renderData)
            if(sketchEffect != 0):
                sketchEffect[c4d.OUTLINEMAT_LINE_DEFAULT_MAT_V] = sketchMat
                sketchEffect[c4d.OUTLINEMAT_LINE_CREASE]        = False
                sketchEffect[c4d.OUTLINEMAT_LINE_BORDER]        = False
                sketchEffect[c4d.OUTLINEMAT_LINE_ISOPARMS]      = True
                sketchEffect[c4d.OUTLINEMAT_LINE_OUTLINE]       = True
                sketchEffect[c4d.OUTLINEMAT_SHADING_BACK_COL]   = self.GetColorField(1001)['color']
                sketchEffect[c4d.OUTLINEMAT_SHADING_OBJECT]     = 4         # Object->Background
            else:
                newSketchEffect = c4d.documents.BaseVideoPost(1011015)
                newSketchEffect[c4d.OUTLINEMAT_LINE_DEFAULT_MAT_V] = sketchMat
                newSketchEffect[c4d.OUTLINEMAT_LINE_CREASE]        = False
                newSketchEffect[c4d.OUTLINEMAT_LINE_BORDER]        = False
                newSketchEffect[c4d.OUTLINEMAT_LINE_ISOPARMS]      = True
                newSketchEffect[c4d.OUTLINEMAT_LINE_OUTLINE]       = True
                newSketchEffect[c4d.OUTLINEMAT_SHADING_BACK_COL]   = self.GetColorField(1001)['color']
                newSketchEffect[c4d.OUTLINEMAT_SHADING_OBJECT]     = 4         # Object->Background
                renderData.InsertVideoPostLast(newSketchEffect)

            ##########
            doc.EndUndo()
            c4d.EventAdd()
            self.Close()

        return True

def main():
    dlg = MyDialogs()
    dlg.Open(c4d.DLG_TYPE_MODAL)

    print "Execute"
    c4d.EventAdd()


if __name__=='__main__':
    main()