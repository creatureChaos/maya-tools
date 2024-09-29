import maya.cmds as cmds
import maya.mel as mel
from functools import partial

#---------------------------------------------------------------
def getCtrls():

    ctrls = cmds.ls(sl=True)
    hero_ctrl = ctrls[0]

    ctrls.pop(0)

    # Debug Log:
    print('------------------------------------')
    print(f'__Selected Controller: {hero_ctrl}')
    print(f'__Controllers: {ctrls}')

    return hero_ctrl, ctrls

#---------------------------------------------------------------
def getSelectedRange(): # Get the highlighted range on the timeline

    # Get scene timeline range
    scene_start_frame = cmds.playbackOptions(q=True, animationStartTime=True)
    scene_end_frame = cmds.playbackOptions(q=True, animationEndTime=True)

    # Get selected timeline range
    aTimeSlider = mel.eval('$tmpVar=$gPlayBackSlider') # Mel command to identify the timeline
    selected_range = cmds.timeControl(aTimeSlider, q=True, rangeArray=True) # Python command to check for the selected range 

    difference = selected_range[1] - selected_range[0] # Check to see if the timeline is highlighted by verifying that the diffrence between the start and end of the selected range is greater than 1

    # If timeline section not slected, set the selected range to the timeline length 
    if difference == 1:
        selected_range = [scene_start_frame, scene_end_frame]
    else:
        selected_range = selected_range

    # Debug Log:
    print(f'__Selected Range: {selected_range}')

    return selected_range # Publish the frame range

#---------------------------------------------------------------
def getFullAttributeName(hero_ctrl, short_names):

    long_names = [] # Create empty list to store attribute long names
    
    for attribute in short_names:
        long_name = cmds.attributeQuery(attribute, node=hero_ctrl, longName=True)
        long_names.append(long_name)
    
    return long_names # Publish list

#---------------------------------------------------------------
def getChannelBoxSelection(hero_ctrl):

    channel_box = 'mainChannelBox' # Get Maya's main channelBox
    selectedChannels = cmds.channelBox(channel_box, q=True, selectedMainAttributes=True) # Return the list of selected channels

    if selectedChannels:
        channels = getFullAttributeName(hero_ctrl, selectedChannels) # Convert short name attributes to long name attributes
        print(f'\n__Selected Channels: {channels}') # Debug Log:

        return channels # Publish selected channels
    else:
        curves = cmds.keyframe(hero_ctrl, q=True, n=True) # Get all channelBox curve names as a list
        channels = [item.rsplit('_', 1)[-1] for item in curves] # Isolate channels from long names
        print(f'\n__Channels: {channels}') # Debug Log:

        return channels # Publish channels list

#---------------------------------------------------------------
def copyAnimation(channels, hero_ctrl, ctrls, selected_range, *args):

    timeOffset = cmds.intField('timeOffsetField', q=True, v=True)

    cmds.copyKey(hero_ctrl, time=(selected_range[0], selected_range[-1]), attribute=channels)
    
    n = timeOffset
    for ctrl in ctrls:
        cmds.pasteKey(ctrl, timeOffset=n)
        n = n + timeOffset
6
#---------------------------------------------------------------
def execute(*args):

    hero_ctrl, ctrls = getCtrls()

    selected_range = getSelectedRange()

    channels = getChannelBoxSelection(hero_ctrl)

    copyAnimation(channels, hero_ctrl, ctrls, selected_range)

#------------------------------------------
# POP UP WINDOW
#------------------------------------------
def instructions(*args):
    
    instructionWindow = cmds.window(title='Instructions', widthHeight=(340, 200), s=True, mnb=False, mxb=False)
        
    instructionLayout = cmds.columnLayout(adj=True)
    
    cmds.setParent(instructionLayout)
    cmds.separator(style='none', h=10)
    cmds.rowColumnLayout(numberOfColumns=2, columnSpacing=(1,10))
    cmds.text(l='''
              1. Select the controller you would like to copy, then select in order all other controllers you would like to paste the animation to.<br><br>
              2. In the channelBox, select which channels you would like to copy. If you do not select specific channels, all channels will be copied.<br><br>
              3. Select the range on the timeline you would like to copy. If no specific range is selected, the entire timeline will be copied.<br><br>
              4. Adjust the Frame Offset to suit your needs.<br><br>
              5. Execute.
              ''', al='left', ww=True)
    cmds.text(l='')
    
    cmds.showWindow(instructionWindow)

#------------------------------------------
# UI WINDOW 
#------------------------------------------
window = cmds.window(title='Animation Offset', widthHeight=(200, 137), s=False, mnb=False, mxb=False)

autographLayout = cmds.columnLayout(adj=True)
executeLayout = cmds.columnLayout(adj=True)
optionLayout = cmds.columnLayout(adj=True)
helpLayout = cmds.columnLayout(adj=True)

#------------------------------------------
cmds.setParent(helpLayout)

cmds.separator(style='none', h=2)
helpButton = cmds.button(l='Instructions', c=(instructions))

#------------------------------------------
cmds.setParent(optionLayout)

cmds.separator(style='none', h=10)
cmds.rowColumnLayout(numberOfColumns=2, cs=(1, 10))
cmds.text(label='Frame Offset:    ')
cmds.intField('timeOffsetField', v=2, w=50)

#------------------------------------------
cmds.setParent(executeLayout)

cmds.separator(style='in', h=20)
cmds.button(l='execute', c=partial(execute))

#------------------------------------------
cmds.setParent(autographLayout)

cmds.text(l='Tool built by Emile Menard', font="smallFixedWidthFont", enable=False, h=20)

#------------------------------------------

cmds.showWindow(window)