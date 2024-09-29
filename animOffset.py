####################################
#                                  #
#      Animation Offset Tool       #
#     Created by Emile Menard      #
#               V1                 #
#           2023-03-28             #
#                                  #
####################################


import maya.cmds as cmds
from functools import partial

def animOffset(start, end, offset, *args):
    
    convertStart = float(cmds.intField(start, q=True, value=True))
    convertEnd = float(cmds.intField(end, q=True, value=True))
    convertOffset = float(cmds.intField(offset, q=True, value=True))

    ctrls = cmds.ls(sl=True)   
    lead = ctrls[0]
    ctrls.pop(0)
    print('lead: '.format(lead))
    print('ctrls: '.format(ctrls))
    
    cmds.copyKey(lead, time=(convertStart, convertEnd))
    
    i = convertOffset
    for x in ctrls:
        cmds.pasteKey(x, to=i)
        i = i+convertOffset
        

window = cmds.window(title='Animation Offset', widthHeight=(200, 185), s=True, mnb=False, mxb=False)

runLyt = cmds.columnLayout(adj=True)
offsetLyt = cmds.columnLayout(adj=False)
rangeLyt = cmds.columnLayout(adj=True)
introLyt = cmds.columnLayout(adj=True)

#--------

cmds.setParent(introLyt)

cmds.separator(style='none', h=5)
cmds.text(l='Select your animated controller, then continue down the chain.', al='left', w=200, ww=True)
cmds.separator(style='in', h=20)

#--------

cmds.setParent(offsetLyt)

cmds.separator(style='none', h=15)
cmds.rowColumnLayout( numberOfColumns=2, columnAlign=(1, 'right'), columnAttach=(2, 'left', 0))
cmds.text(label='Offset: ')
offset = cmds.intField(v=5, w=50)

#--------

cmds.setParent(rangeLyt)

cmds.text(l='Frame Range:', al='left')
cmds.separator(style='none', h=10)
cmds.rowColumnLayout(nc=4, cw=([1,30], [2,70], [3,30], [4,50]), columnAttach=(2, 'left', 0))
cmds.text(l='Start:')
start = cmds.intField(v=1, w=50)
cmds.text(l='End:')
end = cmds.intField(v=10, w=50)

#--------

cmds.setParent(runLyt)

cmds.separator(style='in', h=20)
cmds.button(l='execute', c=partial(animOffset, start, end, offset))



cmds.showWindow(window)