import maya.cmds as cmds

def rotate_order_attribute():
    
    sel = cmds.ls(sl=True)
    selName = sel[0]
    
    cmds.setAttr(f'{selName}.ro', cb=True)
    
    string = f'setAttr -keyable true "{selName}.ro";'
    mel.eval(string)
    
rotate_order_attribute()