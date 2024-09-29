###################################
#                                 #
#           OFFSET MOVE           #
#     Created by Emile Menard     #
#               V1                #
#           2023-05-06            #
#                                 #
###################################

import maya.cmds as cmds

# -------------------------------------------------------------------------------------------

def outlinerCol(target, R, G, B):
    target = cmds.ls(target)
    target = target[0]

    cmds.setAttr('{}.useOutlinerColor'.format(target), 1)
    cmds.setAttr('{}.outlinerColorR'.format(target), R)
    cmds.setAttr('{}.outlinerColorG'.format(target), G)
    cmds.setAttr('{}.outlinerColorB'.format(target), B)
   
# -------------------------------------------------------------------------------------------

def checkState(*args):
    
    # get target
    object = cmds.ls(sl=True)
    objectParent = cmds.listRelatives(object, allParents=True)
    if not object:
        print('Please select an object.')
        return
    else:
        object = object[0]
        print('Object: {}'.format(object))
    
    # check checkBox state
    checkOffset = cmds.checkBox(offsetBox, q=True, v=True)
    checkHook = cmds.checkBox(hookBox, q=True, v=True)
    checkMove = cmds.checkBox(moveBox, q=True, v=True)
    print('OFFSET: {}\n  HOOK: {}\n  MOVE: {}'.format(checkOffset, checkHook, checkMove))
    
    grpList = []
        
    if checkMove == True:
        grpList.append('MOVE')
    if checkHook == True:
        grpList.append('HOOK')
    if checkOffset == True:
        grpList.append('OFFSET')
    else:
        pass
        
    print('Groups to create: {}'.format(grpList))
    lastInd = len(grpList) -1
    print('Last list Index: {}'.format(lastInd))
    
    # Create Groups
    i = 0
    for x in grpList:
        if i == 0:
            active = cmds.group(n='{}_{}'.format(object, x), em=True)
            grpList[i] = active
        else:
            active = cmds.group(n='{}_{}'.format(object, x))
            grpList[i] = active
        i = i+1
    
    print(grpList)
    
    # Parenting and Hierarchy
    cmds.matchTransform(grpList[-1], object)
    
    if objectParent is None:
        print('Object is child of world')
    else:
        cmds.parent(grpList[-1], objectParent)
        
    cmds.parent(object, grpList[0])
    
    # Add Outliner Color
    for x in grpList:
        if 'OFFSET' in x:
            outlinerCol(x, 0.9, 0.3, 0.6)
        if 'MOVE' in x:
            outlinerCol(x, 0.7, 0.6, 1.0)
        if 'HOOK' in x:
            outlinerCol(x, 1.0, 0.6, 0.1)
        
# -------------------------------------------------------------------------------------------

window = cmds.window(title='OFFSET MOVE', widthHeight=(150, 100), s=True, mnb=False, mxb=False)

runLayout = cmds.columnLayout(adj=True)
checkBoxLayout = cmds.columnLayout(adj=False)

# --------------------

cmds.setParent(checkBoxLayout)

cmds.separator(style='none', h=10)
cmds.rowColumnLayout(numberOfRows=3)
offsetBox = cmds.checkBox(l='Offset', v=True)
hookBox = cmds.checkBox(l='Hook', v=False)
moveBox = cmds.checkBox(l='Move', v=True)

# --------------------

cmds.setParent(runLayout)

cmds.separator(style='in', h=20)
cmds.button(l='Group', c=(checkState))


cmds.showWindow(window)