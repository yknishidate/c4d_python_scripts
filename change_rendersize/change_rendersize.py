import c4d
from c4d import gui
import math


def main():
    #print "RenderSize: ", rd[c4d.RDATA_XRES], rd[c4d.RDATA_YRES]
    #print "FoV(H)    : ", 360/(2*math.pi)*cameraObject[c4d.CAMERAOBJECT_FOV]
    #print "FoV(V)    : ", 360/(2*math.pi)*cameraObject[c4d.CAMERAOBJECT_FOV_VERTICAL]

    rd = doc.GetActiveRenderData() 
    rbd = doc.GetRenderBaseDraw()
    cameraObject = rbd.GetSceneCamera(doc)
    
    fov = cameraObject[c4d.CAMERAOBJECT_FOV]
    
    # swap image size
    tmp = rd[c4d.RDATA_XRES]
    rd.SetParameter(c4d.RDATA_XRES_VIRTUAL, rd[c4d.RDATA_YRES], c4d.DESCFLAGS_SET_USERINTERACTION)
    rd.SetParameter(c4d.RDATA_YRES_VIRTUAL, tmp, c4d.DESCFLAGS_SET_USERINTERACTION)
    
    cameraObject[c4d.CAMERAOBJECT_FOV_VERTICAL] = fov
    c4d.EventAdd()
    
    #rd[c4d.RDATA_XRES] = 720
    #rd[c4d.RDATA_YRES] = 1280
    #rd[c4d.RDATA_XRES], rd[c4d.RDATA_YRES] = rd[c4d.RDATA_YRES], rd[c4d.RDATA_XRES]
    #cameraObject[c4d.CAMERAOBJECT_FOV_VERTICAL] = 53.13/(360/(2*math.pi))
    
if __name__=='__main__':
    main()