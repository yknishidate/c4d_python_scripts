import c4d
import os
from c4d import gui
from c4d import storage

def main():
    baseDraw = doc.GetActiveBaseDraw()
    if baseDraw is None:
       raise RuntimeError()

    # Set Image
    path = storage.LoadDialog(type=c4d.FILESELECTTYPE_IMAGES, title = 'Open Image')
    print "Image Path: ", path
    baseDraw[c4d.BASEDRAW_DATA_PICTURE] = path

    c4d.EventAdd()


if __name__=='__main__':
    main()