###################################
#                                 #
#          autoRig Asset          #
#     Created by Emile Menard     #
#               v1                #
#           2023-05-08            #
#                                 #
###################################

import maya.cmds as cmds
from functools import partial

# ------------------------------------------------------------------------------------------
# OUTINER COLOR 
def outlinerCol(target, R, G, B):
    target = cmds.ls(target)
    targetName = target[0]

    cmds.setAttr('{}.useOutlinerColor'.format(targetName), 1)
    cmds.setAttr('{}.outlinerColorR'.format(targetName), R)
    cmds.setAttr('{}.outlinerColorG'.format(targetName), G)
    cmds.setAttr('{}.outlinerColorB'.format(targetName), B)

# VIEWPORT COLOR
def viewportCol(target, R, G, B):
    target = cmds.ls(target)
    targetName = target[0]

    cmds.setAttr('{}.overrideEnabled'.format(targetName), 1)
    cmds.setAttr('{}.overrideRGBColors'.format(targetName), 1)
    cmds.setAttr('{}.overrideColorRGB'.format(targetName), R, G, B)
    
# MOVE
def offsetMove(target):
    target = cmds.ls(target)
    targetName = target[0]

    # get selected object's parent and store name
    targetParent = cmds.listRelatives(target, allParents=True)

    mov = cmds.group(n='{}_MOVE'.format(targetName), em=True)
    cmds.matchTransform(mov, targetName)
    cmds.parent(targetName, mov)
    
    if targetParent is None:
        print('none')
    else:
        cmds.parent(mov, targetParent)

    # set MOVE group Outliner color to mauve 
    outlinerCol(mov, 0.7, 0.6, 1)
    
# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
def fixHierarchy():
    
    # Get selected object and store name
    sel = cmds.ls(sl=True)
    name = sel[0]
    
    # create groups
    grpMast = cmds.group(n='{}_master'.format(name), em=True)
    grpGeo = cmds.group(n='{}_geo'.format(name), em=True, p=grpMast)
    grpRig = cmds.group(n='{}_rig'.format(name), em=True, p=grpMast)
    
    # put geo into hierarchy
    cmds.parent(sel, grpGeo)
    
    cmds.select(grpGeo)
    
# -------------------------------------------------------------------------------------------
def btnCheck(btn, *args):

    # set the color based on the button that was clicked
    if btn == 'red':
        col = (1.0, 0.0, 0.0)
    elif btn == 'ylw':
        col = (1.0, 1.0, 0.0)
    elif btn == 'grn':
        col = (0.0, 1.0, 0.0)
    elif btn == 'ind':
        col = (0.0, 1.0, 1.0)
    elif btn == 'blu':
        col = (0.0, 0.0, 1.0)
    elif btn == 'vlt':
        col = (1.0, 0.0, 1.0)
    else:
        col = (1.0, 1.0, 0.0)
        
    cmds.button(activeCol, e=True, bgc=(col[0], col[1], col[2]))

# -------------------------------------------------------------------------------------------
def bbox(*args):
    
    # Get selected object and store name
    sel = cmds.ls(sl=True)
    sel = sel[0]
    
    # get world space bounding box
    bbox = cmds.exactWorldBoundingBox(sel)
    bbox.pop(1)
    bbox.pop(3)
    maxVal = max(bbox)
    
    radius = maxVal * 1.4
    
    cmds.floatField(radOverride, e=True, v=radius)

# -------------------------------------------------------------------------------------------
def rig(ctrlCol, *args):
    
    rad = float(cmds.floatField(radOverride, q=True, v=True))
    
    # Get selected object and store name
    sel = cmds.ls(sl=True)
    sel = sel[0]
    name = sel[:-4]
    
    # create groups, controllers
    try:
        grpRig = cmds.group(n='{}_rig'.format(name), em=True, p='{}_master'.format(name))
    except:
        fixHierarchy()
        sel = cmds.ls(sl=True)
        sel = sel[0]
        name = sel[:-4]
        grpRig = '{}_rig'.format(name)
    ctrlMast = cmds.circle(n='ctrl_{}_master'.format(name), nr=(0,1,0), c=(0,0.05,0), r=rad, ch=False)
    ctrlMain = cmds.circle(n='ctrl_{}_main'.format(name), nr=(0,1,0), c=(0,0.1,0), r=rad * 0.9, ch=False)
    cmds.parent(ctrlMast[0], grpRig)
    cmds.parent(ctrlMain[0], ctrlMast)
    
    # Move group ctrls
    offsetMove(ctrlMast)
    offsetMove(ctrlMain)
    
    # create the necessary constraints
    cmds.parentConstraint(ctrlMain, sel)
    cmds.scaleConstraint(ctrlMain, sel)
    
    # Modify color of main ctrl
    col = cmds.button(activeCol, q=True, bgc=True)
    
    viewportCol(ctrlMast, 0.3, 0.3, 0.3)
    viewportCol(ctrlMain, col[0], col[1], col[2])
    

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
window = cmds.window(title='Asset Auto Rig', widthHeight=(200, 179), s=False, mnb=False, mxb=False)

runLayout = cmds.columnLayout(adj=True)
colLayout = cmds.columnLayout(adj=True)
radLayout = cmds.columnLayout(adj=True)

# --------------------
# Radius Override
cmds.setParent(radLayout)

cmds.separator(st='none', h=10)
cmds.rowColumnLayout(nc=2, co=[2, 'left', 10])
cmds.text('Radius:')
radOverride = cmds.floatField(v=0, w=50, pre=2)

cmds.setParent(radLayout)

cmds.separator(st='none', h=10)
cmds.rowColumnLayout(nc=1, adj=True)
cmds.button(l='Bounding Box', c=partial(bbox))

# --------------------
# Color Buttons
cmds.setParent(colLayout)

cmds.separator(st='in', h=20)
cmds.rowColumnLayout(nc=2, co=[(2, 'left', 10)])
cmds.text(l='Controller Color:')
activeCol = cmds.button(l='', w=80, h=10, bgc=(1.0, 1.0, 0.0), vis=False)
cmds.separator(st='none', h=10)

cmds.setParent(colLayout)
cmds.rowColumnLayout(nc=6, co=[(1, 'left', 7)])
redBtn = cmds.button(l='', w=30, h=15, bgc=(1.0, 0.0, 0.0), c=partial(btnCheck, 'red'))
ylwBtn = cmds.button(l='', w=30, h=15, bgc=(1.0, 1.0, 0.0), c=partial(btnCheck, 'ylw'))
grnBtn = cmds.button(l='', w=30, h=15, bgc=(0.0, 1.0, 0.0), c=partial(btnCheck, 'grn'))
indBtn = cmds.button(l='', w=30, h=15, bgc=(0.0, 1.0, 1.0), c=partial(btnCheck, 'ind'))
bluBtn = cmds.button(l='', w=30, h=15, bgc=(0.0, 0.0, 1.0), c=partial(btnCheck, 'blu'))
vltBtn = cmds.button(l='', w=30, h=15, bgc=(1.0, 0.0, 1.0), c=partial(btnCheck, 'vlt'))

# --------------------
# Execute
cmds.setParent(runLayout)

cmds.separator(st='in', h=20)
cmds.button(l='Execute', c=partial(rig))

# --------------------
cmds.showWindow(window)
# -------------------------------------------------------------------------------------------