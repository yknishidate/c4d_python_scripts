import c4d

def main():
    obj = doc.GetActiveObject()
    doc.AddUndo(c4d.UNDOTYPE_DELETE, obj)  # DELETEは変更の前に呼び出す必要がある
    obj.Remove()

if __name__ == '__main__':
    doc.StartUndo()
    main()
    doc.EndUndo()
    c4d.EventAdd()