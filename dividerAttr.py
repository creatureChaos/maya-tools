###################################
#                                 #
#   Null Divider Attribute Tool   #
#     Created by Emile Menard     #
#               V1                #
#           2023-04-15            #
#                                 #
###################################


import maya.cmds as cmds
from functools import partial

def dividerAttr(attrName, niceName, enumName, *args):
    
    variableList = [attrName, niceName, enumName]
    
    i = 0
    for x in variableList:
        x = cmds.textField(x, q=True, tx=True)
        if x == '':
            x = ' '
        variableList[i] = x
        i = i+1
    print(variableList)
    
    sel = cmds.ls(sl=True)
    selName = sel[0]
    cmds.select(sel)
    
    cmds.addAttr(ln=variableList[0], at='enum', nn=variableList[1], en=variableList[2], k=False)
    cmds.setAttr('{}.{}'.format(selName, variableList[0]), cb=True)

#------------------------------------------
#------------------------------------------

window = cmds.window(title='Divider Attribute', widthHeight=(300, 100), s=True, mnb=False, mxb=False)

runLyt = cmds.columnLayout(adj=True)
txtLyt = cmds.columnLayout(adj=True)
guideLyt = cmds.columnLayout(adj=True)

#------------------------------------------

cmds.setParent(guideLyt)

cmds.separator(style='none', h=5)
cmds.text(l='Creates a non-keyable attribute for better channelBox organization', al='left', ww=True)
cmds.separator(style='in', h=20)

#------------------------------------------

cmds.setParent(txtLyt)

cmds.separator(style='none', h=5)
cmds.rowColumnLayout( adj=2, numberOfColumns=3, columnAlign=(1, 'left'), columnAttach=(2, 'left', 0), cs=(1,10))
cmds.text(l='Attribute Name:   ')
attrName = cmds.textField(tx='divider_01')
cmds.text(l='   ')
cmds.text(l='Nice Name:   ')
niceName = cmds.textField(tx='')
cmds.text(l='   ')
cmds.text(l='Enum Name:   ')
enumName = cmds.textField(tx='')
cmds.text(l='   ')
#------------------------------------------

cmds.setParent(runLyt)

cmds.separator(style='in', h=20)
cmds.button(l='Create Attribute', c=partial(dividerAttr, attrName, niceName, enumName))


#------------------------------------------

cmds.showWindow(window)
