import c4d

def main():
    objects = doc.GetActiveObjects(1)

    for obj in objects:
        name = obj.GetName()
        name = name.replace('.', '_')
        if(not name[-1].isdigit()):
            name += "_0"
        doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL, obj)
        obj.SetName(name)


if __name__ == '__main__':
    main()
    c4d.EventAdd()