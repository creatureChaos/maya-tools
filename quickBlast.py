import maya.cmds as cmds
import os

def quickBlast():
    
    # Save location
    filePath = os.path.expanduser("~/Desktop")
    
    # Get file name
    sceneName = cmds.file(query=True, sceneName=True)[:-3]
    sceneName = sceneName.rsplit('/', 1)[-1]

    if sceneName == "":
        cmds.inViewMessage(msg="<h0 style='color: #FF0000'>Please save file before playblasting</h0>", pos='topCenter', fade=True, fit=250, fst=1000, fot=500)
        return
    fileName = f'{filePath}/{sceneName}_blast'
    print(fileName)
    
    # Playblast
    cmds.playblast(fmt='qt', orn=True, v=True, compression='H.264', qlt=100, percent=100, w=2048, h=858, f=fileName, cc=True, os=True, fp=4, s=True)

quickBlast()