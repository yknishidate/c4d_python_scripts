import c4d
from c4d import gui
from c4d import storage

def main():

    baseDraw = doc.GetActiveBaseDraw()
    if baseDraw is None:
       raise RuntimeError()

    # Get Picture
    back_image_path = baseDraw.GetParameter(c4d.BASEDRAW_DATA_PICTURE, c4d.DESCFLAGS_GET_NO_GEDATADEFAULTVALUE)
    if back_image_path == '':
        print 'No Active BaseDraw Picture'
        return
    print back_image_path

    c4d.EventAdd()

if __name__=='__main__':
    main()