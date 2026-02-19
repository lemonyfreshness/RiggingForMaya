import maya.cmds as cmds
import json
import os

controlType = 'Rotation_Control'
bodyRegion = 'custom'
fingerChain = 'thumb'
auxJointType = 'deform'
RLSideAbbreviation = None
FBSideAbbreviation = None
RLSideAbbreviationFingers = 'l'
namingConventionSwapDirection = 'JFM to Unreal'

defaultNamingConventionSwapData = { 
    "UNWEIGHTED_SKIN_COG": "COG",
    "UNWEIGHTED_SACRUM_SPINE_0": "pelvis",
    "UNWEIGHTED_SPINE_1": "spine_01",
    "UNWEIGHTED_SPINE_2": "spine_02",
    "UNWEIGHTED_SPINE_3": "spine_03",
    "UNWEIGHTED_SPINE_4": "spine_04",
    "UNWEIGHTED_NECK_0": "neck_00",
    "UNWEIGHTED_NECK_1": "neck_01",
    "UNWEIGHTED_NECK_2": "neck_02",
    "UNWEIGHTED_NECK_3": "neck_03",
    "UNWEIGHTED_NECK_3_HEAD": "head",
    "SKIN_SQUASH_STRETCH_SACRUM_SPINE_0": "stretchy_pelvis",
    "SKIN_SQUASH_STRETCH_SPINE_1": "stretchy_spine_01",
    "SKIN_SQUASH_STRETCH_SPINE_2": "stretchy_spine_02",
    "SKIN_SQUASH_STRETCH_SPINE_3": "stretchy_spine_03",
    "SKIN_SQUASH_STRETCH_SPINE_4": "stretchy_spine_04",
    "SKIN_SQUASH_STRETCH_NECK_0": "stretchy_neck_01",
    "SKIN_SQUASH_STRETCH_NECK_1": "stretchy_neck_02",
    "SKIN_SQUASH_STRETCH_NECK_2": "stretchy_neck_03",
    "SKIN_ARM_CLAVICLE_LEFT": "clavicle_l",
    "SKIN_ARM_CLAVICLE_RIGHT": "clavicle_r",
    "SKNCONTROL_ARM_SHOULDER_GIMBLE_LEFT": "deform_shoulder_gimble_l",
    "SKNCONTROL_ARM_SHOULDER_GIMBLE_RIGHT": "deform_shoulder_gimble_r",
    "SKIN_ARM_SHOULDER_LEFT": "upperarm_l",
    "SKIN_ARM_SHOULDER_RIGHT": "upperarm_r",
    "SKIN_ARM_ELBOW_LEFT": "lowerarm_l",
    "SKIN_ARM_ELBOW_RIGHT": "lowerarm_r",
    "SKNCONTROL_UPPER_ARM_TWIST_1_LEFT": "upperarm_twist_01_l",
    "SKNCONTROL_UPPER_ARM_TWIST_1_RIGHT": "upperarm_twist_01_r",
    "SKNCONTROL_UPPER_ARM_TWIST_2_LEFT": "upperarm_twist_02_l",
    "SKNCONTROL_UPPER_ARM_TWIST_2_RIGHT": "upperarm_twist_02_r",
    "SKNCONTROL_LOWER_ARM_TWIST_1_LEFT": "lowerarm_twist_01_l",
    "SKNCONTROL_LOWER_ARM_TWIST_1_RIGHT": "lowerarm_twist_01_r",
    "SKNCONTROL_LOWER_ARM_TWIST_2_LEFT": "lowerarm_twist_02_l",
    "SKNCONTROL_LOWER_ARM_TWIST_2_RIGHT": "lowerarm_twist_02_r",
    "SKNCONTROL_ARM_ELBOW_INNER_VOLUME_LEFT": "deform_elbow_fr_l",
    "SKNCONTROL_ARM_ELBOW_INNER_VOLUME_RIGHT": "deform_elbow_fr_r",
    "SKNCONTROL_ARM_ELBOW_OUTER_VOLUME_LEFT": "deform_elbow_bk_l",
    "SKNCONTROL_ARM_ELBOW_OUTER_VOLUME_RIGHT": "deform_elbow_bk_r",
    "SKNCONTROL_ARM_WRIST_GIMBLE_LEFT": "deform_wrist_gimble_l",
    "SKNCONTROL_ARM_WRIST_GIMBLE_RIGHT": "deform_wrist_gimble_r",
    "SKNCONTROL_ARM_WRIST_LEFT": "deform_wrist_l",
    "SKNCONTROL_ARM_WRIST_RIGHT": "deform_wrist_r",
    "SKIN_HAND_INDEX_METACARPAL_LEFT": "index_metacarpal_l",
    "SKIN_HAND_INDEX_METACARPAL_RIGHT": "index_metacarpal_r",
    "SKIN_HAND_INDEX_1_LEFT": "index_01_l",
    "SKIN_HAND_INDEX_1_RIGHT": "index_01_r",
    "SKIN_HAND_INDEX_2_LEFT": "index_02_l",
    "SKIN_HAND_INDEX_2_RIGHT": "index_02_r",
    "SKIN_HAND_INDEX_3_LEFT": "index_03_l",
    "SKIN_HAND_INDEX_3_RIGHT": "index_03_r",
    "SKIN_HAND_INDEX_END_LEFT": "index_03_l_end",
    "SKIN_HAND_INDEX_END_RIGHT": "index_03_r_end",
    "SKIN_HAND_MIDDLE_1_LEFT": "middle_01_l",
    "SKIN_HAND_MIDDLE_1_RIGHT": "middle_01_r",
    "SKIN_HAND_MIDDLE_2_LEFT": "middle_02_l",
    "SKIN_HAND_MIDDLE_2_RIGHT": "middle_02_r",
    "SKIN_HAND_MIDDLE_3_LEFT": "middle_03_l",
    "SKIN_HAND_MIDDLE_3_RIGHT": "middle_03_r",
    "SKIN_HAND_MIDDLE_END_LEFT": "middle_03_l_end",
    "SKIN_HAND_MIDDLE_END_RIGHT": "middle_03_r_end",
    "SKIN_HAND_RING_1_LEFT": "ring_01_l",
    "SKIN_HAND_RING_1_RIGHT": "ring_01_r",
    "SKIN_HAND_RING_2_LEFT": "ring_02_l",
    "SKIN_HAND_RING_2_RIGHT": "ring_02_r",
    "SKIN_HAND_RING_3_LEFT": "ring_03_l",
    "SKIN_HAND_RING_3_RIGHT": "ring_03_r",
    "SKIN_HAND_RING_END_LEFT": "ring_03_l_end",
    "SKIN_HAND_RING_END_RIGHT": "ring_03_r_end",
    "SKIN_HAND_PINKY_1_LEFT": "pinky_01_l",
    "SKIN_HAND_PINKY_1_RIGHT": "pinky_01_r",
    "SKIN_HAND_PINKY_2_LEFT": "pinky_02_l",
    "SKIN_HAND_PINKY_2_RIGHT": "pinky_02_r",
    "SKIN_HAND_PINKY_3_LEFT": "pinky_03_l",
    "SKIN_HAND_PINKY_3_RIGHT": "pinky_03_r",
    "SKIN_HAND_PINKY_END_LEFT": "pinky_03_l_end",
    "SKIN_HAND_PINKY_END_RIGHT": "pinky_03_r_end",
    "SKNCONTROL_LEG_HIP_ROOT_LEFT": "hip_root_l",
    "SKNCONTROL_LEG_HIP_ROOT_RIGHT": "hip_root_r",
    "UNWEIGHTED_LEG_HIP_GAP_LEFT": "hip_gap_l",
    "UNWEIGHTED_LEG_HIP_GAP_RIGHT": "hip_gap_r",
    "UNWEIGHTED_LEG_HIP_GIMBLE_LEFT": "hip_gimble_l",
    "UNWEIGHTED_LEG_HIP_GIMBLE_RIGHT": "hip_gimble_r",
    "SKIN_LEG_HIP_LEFT": "thigh_l",
    "SKIN_LEG_HIP_RIGHT": "thigh_r",
    "SKIN_LEG_KNEE_1_LEFT": "calf_l",
    "SKIN_LEG_KNEE_1_RIGHT": "calf_r",
    "SKIN_LEG_KNEE_2_LEFT": "calf_02_l",
    "SKIN_LEG_KNEE_2_RIGHT": "calf_02_r",
    "SKIN_LEG_ANKLE_LEFT": "foot_l",
    "SKIN_LEG_ANKLE_RIGHT": "foot_r",
    "SKIN_LEG_FOOT_METATARSAL_LEFT": "metatarsal_l",
    "SKIN_LEG_FOOT_METATARSAL_RIGHT": "metatarsal_r",
    "SKIN_LEG_FOOT_BALL_LEFT": "ball_l",
    "SKIN_LEG_FOOT_BALL_RIGHT": "ball_r",
    "SKIN_TOE_THUMB_1_LEFT": "thumbtoe_01_l",
    "SKIN_TOE_THUMB_1_RIGHT": "thumbtoe_01_r",
    "SKIN_TOE_THUMB_2_LEFT": "thumbtoe_02_l",
    "SKIN_TOE_THUMB_2_RIGHT": "thumbtoe_02_r",
    "SKIN_TOE_THUMB_3_LEFT": "thumbtoe_03_l",
    "SKIN_TOE_THUMB_3_RIGHT": "thumbtoe_03_r",
    "SKIN_TOE_THUMB_END_LEFT": "thumbtoe_03_l_end",
    "SKIN_TOE_THUMB_END_RIGHT": "thumbtoe_03_r_end",
    "SKIN_TOE_INDEX_1_LEFT": "toe_01_l",
    "SKIN_TOE_INDEX_1_RIGHT": "toe_01_r",
    "SKIN_TOE_INDEX_2_LEFT": "toe_02_l",
    "SKIN_TOE_INDEX_2_RIGHT": "toe_02_r",
    "SKIN_TOE_INDEX_3_LEFT": "toe_03_l",
    "SKIN_TOE_INDEX_3_RIGHT": "toe_03_r",
    "SKIN_TOE_INDEX_END_LEFT": "toe_03_l_end",
    "SKIN_TOE_INDEX_END_RIGHT": "toe_03_r_end",
    "SKIN_TOE_MIDDLE_1_LEFT": "middletoe_01_l",
    "SKIN_TOE_MIDDLE_1_RIGHT": "middletoe_01_r",
    "SKIN_TOE_MIDDLE_2_LEFT": "middletoe_02_l",
    "SKIN_TOE_MIDDLE_2_RIGHT": "middletoe_02_r",
    "SKIN_TOE_MIDDLE_3_LEFT": "middletoe_03_l",
    "SKIN_TOE_MIDDLE_3_RIGHT": "middletoe_03_r",
    "SKIN_TOE_MIDDLE_END_LEFT": "middletoe_03_l_end",
    "SKIN_TOE_MIDDLE_END_RIGHT": "middletoe_03_r_end",
    "SKIN_TOE_RING_1_LEFT": "ringtoe_01_l",
    "SKIN_TOE_RING_1_RIGHT": "ringtoe_01_r",
    "SKIN_TOE_RING_2_LEFT": "ringtoe_02_l",
    "SKIN_TOE_RING_2_RIGHT": "ringtoe_02_r",
    "SKIN_TOE_RING_3_LEFT": "ringtoe_03_l",
    "SKIN_TOE_RING_3_RIGHT": "ringtoe_03_r",
    "SKIN_TOE_RING_END_LEFT": "ringtoe_03_l_end",
    "SKIN_TOE_RING_END_RIGHT": "ringtoe_03_r_end",
    "SKIN_TOE_PINKY_1_LEFT": "pinkytoe_01_l",
    "SKIN_TOE_PINKY_1_RIGHT": "pinkytoe_01_r",
    "SKIN_TOE_PINKY_2_LEFT": "pinkytoe_02_l",
    "SKIN_TOE_PINKY_2_RIGHT": "pinkytoe_02_r",
    "SKIN_TOE_PINKY_3_LEFT": "pinkytoe_03_l",
    "SKIN_TOE_PINKY_3_RIGHT": "pinkytoe_03_r",
    "SKIN_TOE_PINKY_END_LEFT": "pinkytoe_03_l_end",
    "SKIN_TOE_PINKY_END_RIGHT": "pinkytoe_03_r_end",
    "UNWEIGHTED_LEG_FOOT_HEEL_POSITION_LEFT": "heel_l",
    "UNWEIGHTED_LEG_FOOT_HEEL_POSITION_RIGHT": "heel_r",
    "UNWEIGHTED_LEG_FOOT_TOE_POSITION_LEFT": "toe_l",
    "UNWEIGHTED_LEG_FOOT_TOE_POSITION_RIGHT": "toe_r",
    "SKNCONTROL_LOWER_LG_TWIST_1_LEFT": "lower_leg_twist_01_l",
    "SKNCONTROL_LOWER_LG_TWIST_1_RIGHT": "lower_leg_twist_01_r",
    "SKNCONTROL_LOWER_LG_TWIST_2_LEFT": "lower_leg_twist_02_l",
    "SKNCONTROL_LOWER_LG_TWIST_2_RIGHT": "lower_leg_twist_02_r",
    "SKNCONTROL_ARM_TRICEP_LEFT": "tricep_l",
    "SKNCONTROL_ARM_TRICEP_RIGHT": "tricep_r",
    "SKNCONTROL_ARM_BICEP_LEFT": "bicep_l",
    "SKNCONTROL_ARM_BICEP_RIGHT": "bicep_r",
    "SKNCONTROL_BUTT_CHEEK_LEFT": "butt_cheek_l",
    "SKNCONTROL_BUTT_CHEEK_RIGHT": "butt_cheek_r",
    "SKNCONTROL_KNEE_VOLUME_LEFT": "deform_knee_l",
    "SKNCONTROL_KNEE_VOLUME_RIGHT": "deform_knee_r",
    "SKNCONTROL_HAMSTRING_LEFT": "hamstring_l",
    "SKNCONTROL_HAMSTRING_RIGHT": "hamstring_r",
    "SKNCONTROL_QUAD_LEFT": "quad_l",
    "SKNCONTROL_QUAD_RIGHT": "quad_r",
    "SKNCONTROL_CALF_LEFT": "calf_l",
    "SKNCONTROL_CALF_RIGHT": "calf_r",
    "SKNCONTROL_BELLYBREATH": "belly_breath",
    "SKNCONTROL_CHESTBREATH": "chest_breath",
    "SKNCONTROL_BREAST_PIVOT_LEFT" : "breast_pivot_l",
    "SKNCONTROL_BREAST_PIVOT_RIGHT" : "breast_pivot_r",
    "SKNCONTROL_BREAST_LEFT" : "breast_l",
    "SKNCONTROL_BREAST_RIGHT" : "breast_r",
    "SKNCONTROL_AREOLA_LEFT" : "areola_l",
    "SKNCONTROL_AREOLA_RIGHT" : "areola_r",
    "SKNCONTROL_NIPPLE_LEFT" : "nipple_l",
    "SKNCONTROL_NIPPLE_RIGHT" : "nipple_r"
}


def getDataLocation(nameOfFile):
	filePath = cmds.file(sceneName = True, query = True)
	pathToFile = '%s/%s' % (filePath.rsplit('/', 2)[0], 'data/' + nameOfFile + '.json')#regroving that path to go to the assets folder
	print('The pathToFile is: ' + str(pathToFile))
	return pathToFile

def makeBufferJoint(*args):
    joint = cmds.ls(selection = True)[0]
    jointParent = cmds.listRelatives(parent = True)
    bufferJoint = cmds.duplicate(joint, parentOnly = True, name = joint + '_BufferJoint')
    cmds.parent(joint, bufferJoint)
    cmds.parent(bufferJoint, jointParent)


def orientJointForUnreal(*args):
    jointForOrient = cmds.ls(selection = True)[0]
    bufferJoint = setupReorientJoint()
    cmds.select(bufferJoint)
    setupReorientJoint()
    
    print('orientJointForUnreal(), jointForOrient is: ' + str(jointForOrient))
    reorientChildrenValue = cmds.checkBox(reorientChildren, query=True, value=True)
    reverseXValue = cmds.checkBox(reverseX, query=True, value=True)
    print('orientJointForUnreal(), reorientChildrenValue is: ' + str(reorientChildrenValue))
    print('orientJointForUnreal(), reverseXValue is: ' + str(reverseXValue))
    cmds.joint(jointForOrient, edit = True, orientJoint = 'xzy', secondaryAxisOrient = 'xdown', children = reorientChildrenValue, zeroScaleOrient = True) #
    
    if reverseXValue == True:
        print('orientJointForUnreal(), reverseXValue is running and that value is: ' + str(reverseXValue))
        cmds.joint(jointForOrient, edit = True, orientJoint = 'xzy', secondaryAxisOrient = 'ydown', children = reorientChildrenValue, zeroScaleOrient = True)#  
        bufferJoint = setupJointForReorient()
        cmds.rotate(0,180,0, bufferJoint)
        cleanupReorientedJoint()


def parentShapesUnderControl(controlJoint, importedShape):

    #print('parentShapesUnderControl(), the controlJoint is: ' + str(controlJoint))
    shapeSelection = cmds.listRelatives(importedShape, children = True, type = 'shape')
    #print('parentShapesUnderControl(), the shapeSelection is: ' + str(shapeSelection))
    i = 0
    for eachShape in shapeSelection:
        renamedShape = cmds.rename(eachShape, controlJoint + 'shape_' + str(i))
        cmds.parent(renamedShape, controlJoint, relative = True, shape = True)
        i = i+1
    #print('parentShapesUnderControl(), the controlJoint is: ' + str(controlJoint))
    
    importedShapeChildren = cmds.listRelatives(importedShape, allDescendents = True)
    #print('parentShapesUnderControl(), the importedShapeChildren is: ' + str(importedShapeChildren))
    if importedShapeChildren == None:
        cmds.delete(importedShape)
    return controlJoint


def renameBodyJoints(*args):
    global bodyRegion
    bodyRegion = cmds.optionMenu(bodyRegionOptionMenu,query = True, value = True)
    print('renameBodyJoints(), the bodyRegion is: ' + str(bodyRegion))
    if bodyRegion == 'custom':
        bodyRegion = cmds.textField('bodyRegionTextField', query = True, text = True)
    print('renameBodyJoints(), the FBSideAbbreviation is: ' + str(FBSideAbbreviation))
    print('renameBodyJoints(), the RLSideAbbreviation is: ' + str(RLSideAbbreviation)) 
    isStretchyJoint = cmds.checkBox(isStretchyJointCheckbox, query=True, value=True)
    isTwistJoint = cmds.checkBox(isTwistJointCheckbox, query=True, value=True)
    isDeformJoint = cmds.checkBox(isDeformJointCheckbox, query=True, value=True)
    isDynamicsJoint = cmds.checkBox(isDynamicJointCheckbox, query=True, value=True)
    isAttachJoint = cmds.checkBox(isAttachJointCheckbox, query=True, value=True)
    isEnumerated = cmds.checkBox(isEnumeratedCheckbox, query=True, value=True)
    isPositionJoint = cmds.checkBox(isPivotJointCheckbox, query=True, value=True)
    print('renameBodyJoints(), isTwistJoint is: ' + str(isTwistJoint))
    if isEnumerated == True:
        print('renameBodyJoints(), isEnumerated is ' + str(isEnumerated))
        startNumberSequence = cmds.intField("startNumberIntField", query = True, value = True)
        print('renameBodyJoints(), the startNumberSequence is: ' + str(startNumberSequence))
        i = startNumberSequence
    
    jointSelection = cmds.ls(selection = True)
    renameList = []
    if jointSelection:  
        for eachJoint in jointSelection:
            name = bodyRegion
            if isStretchyJoint:
                name = 'stretchy_' + name
            if isTwistJoint:
                name = name + '_twist'
            if isDeformJoint:
                name = 'deform_' + name 
            if isDynamicsJoint:
                name = 'dyn_' + name
            if isPositionJoint:
                name = name + '_pivot'
            if isAttachJoint:
                name = name + '_Attach'
            if isEnumerated == True:
                name = name + '_' + str(0) + str(i)
            if FBSideAbbreviation != None:
                name = name + '_' + FBSideAbbreviation
                i = i+1
            if RLSideAbbreviation != None:
                name = name + '_' + RLSideAbbreviation
            print('renameBodyJoints(), the name is :' + name)
            renameList.append(name)
        jointSelection.reverse()
        renameList.reverse()
        for eachJoint, eachName in zip(jointSelection, renameList):
            cmds.rename(eachJoint, eachName)
            print('renameBodyJoints(), the eachJoint is: ' + eachJoint + ' and the eachName is: ' + eachName)
        updateTextField(name, 'unrealName')
        
    else:
         print('renameBodyJoints(),you gotta select a joint bra')



def renameFingerJoints(*args):
    jointSelection = cmds.ls(selection = True)[0]
    jointChildren = cmds.listRelatives(jointSelection, allDescendents = True, type= 'joint')
    jointChildren.reverse()
    jointChildren.insert(0, jointSelection)  
    hasMetacarpalsValue = cmds.checkBox(hasMetacarpals, query=True, value=True)
    hasEndJointValue = cmds.checkBox(hasEndJoint, query=True, value=True)
    isToesValue = cmds.checkBox(isToes, query=True, value=True)

    print('renameFingerJoints(), the hasEndJointValue is : ' + str(hasEndJointValue))
    
    fingerChain
    if hasMetacarpalsValue == True:
        name = fingerChain
        metacarpal = jointChildren.pop(0)
        name = name + '_metacarpal'
        if RLSideAbbreviationFingers != None:
            name = name + '_' + RLSideAbbreviationFingers
        cmds.rename(metacarpal, name)

    jointChildrenLength = len(jointChildren)
    print('renameFingerJoints(), the jointChildrenLength are: ' + str(jointChildrenLength))
    i = 1
    ai = 1
    for eachChild in jointChildren:
        print('renameFingerJoints(), i is : ' + str(i))
        name = fingerChain
        if isToesValue == True:
            name = name + 'toe' 
        name = name + '_' + str(0) + str(i)
        if RLSideAbbreviationFingers != None:
            name = name + '_' + RLSideAbbreviationFingers
        if ai == jointChildrenLength and hasEndJointValue == True:
            name = name + '_end'
        cmds.rename(eachChild, name)
        if hasEndJointValue == True and i != jointChildrenLength -1:
            i = i+1
        elif hasEndJointValue == False:
            i = i+1
        ai = ai+1
     

def setupController(*args):
    joint = cmds.ls(selection = True)[0]
    controllerShape = importObject(controlType)
    controllerScale = cmds.floatField('controllerScale', query=True, value=True)
    controller = parentShapesUnderControl(joint, controllerShape)


def setupReorientJoint(*args):
    selection = cmds.ls(selection = True)
    selection = selection[0]
    if '_ReorientJoint' not in selection:
        bufferJoint = setupJointForReorient()
        return bufferJoint
    else:
        cleanupReorientedJoint()


def setupJointForReorient():
    selection = cmds.ls(selection = True)
    if selection != None and len(selection) == 1:
        selection = selection[0]
        print('dupeJointForReorient(), the selection is: ' + selection)
        if cmds.objectType(selection) == 'joint':
            selectionParent = cmds.listRelatives(selection, parent = True)
            selectionChildren = cmds.listRelatives(selection, children = True)
            tempNull = cmds.group(empty = True, world = True, name = selection + '_TempNull')
            if selectionParent == None:
                cmds.parent(tempNull, world = True)
            else:
                cmds.parent(tempNull, selectionParent)
        if selectionChildren != None:
            cmds.select(clear = True)
            cmds.parent(selectionChildren, tempNull)
        dupedJoint = cmds.duplicate(selection, parentOnly = True, name = selection + '_ReorientJoint')
        cmds.parent(selection, dupedJoint)
        cmds.select(dupedJoint)
        return dupedJoint
    else:
        print('setupJointForReorient, Select a JOINT dumbass!')



def cleanupReorientedJoint():
    selection = cmds.ls(selection = True)
    if selection != None and len(selection) == 1:
        selection = selection[0]
        print('cleanupReorientedJoint(), The selection is: ' + selection)
        if '_ReorientJoint' in selection:
            jointForFreezeTransforms = cmds.listRelatives(selection, children = True)
            cmds.makeIdentity(jointForFreezeTransforms, apply = True, translate = True, rotate = True, scale = True, jointOrient = True)
            originalJoint = cmds.listRelatives(selection, children = True)[0]
            originalParent = cmds.listRelatives(originalJoint + '_TempNull', parent = True)
            reparentChildren = cmds.listRelatives(originalJoint + '_TempNull', children = True)
            if reparentChildren != None:
                    cmds.parent(reparentChildren, originalJoint)
            if originalParent != None:
                cmds.parent(originalJoint, originalParent)
            else:
                cmds.parent(originalJoint, world = True)
            cmds.delete(selection, originalJoint + '_TempNull')
        else:
            print('cleanupReorientedJoint(), Select the _ReorientJoint')



def importObject(nameOfFile):
    print('importObject(), the nameOfFile is : ' + nameOfFile)
    nameOfFile = 'JFM_' + nameOfFile
    scriptsUserDirectory = cmds.internalVar(usd=True) #getting this version of maya scripts directory which is in the same directory as the assets folder
    pathToFile = '%s/%s' % (scriptsUserDirectory.rsplit('/', 3)[0], 'assets/' + nameOfFile + '.ma')#regroving that path to go to the assets folder
    print('importObject(), the opath to the file is is : ' + pathToFile)
    cmds.file(pathToFile, i = True, groupReference = True, groupName = 'loadedShapeGroup', mergeNamespaceWithParent = True, ignoreVersion = True)
    importedObject = cmds.listRelatives('loadedShapeGroup', children = True)
    if len(importedObject) > 1:
        for eachImportedObject in importedObject:
            if 'transform' in eachImportedObject:
                importedObject.remove(eachImportedObject)
    print('importObject(), the importedObject is : ' + str(importedObject))
    importedObject = importedObject[0]
    print('importObject(), the importedObject is : ' + str(importedObject))
    cmds.parent(importedObject, world = True)
    cmds.delete('loadedShapeGroup')

    return importedObject


def listDuplicateJoints(*args):
    jointSelection = cmds.ls(selection = True)
    if jointSelection != None:
        jointSelection = jointSelection[0]
        jointChildren = cmds.listRelatives(jointSelection, allDescendents = True, type= 'joint')
        jointChildren.insert(0, jointSelection)  
        
        for eachJoint in jointChildren:
            duplicateJoints = []
            for eachJoint2 in jointChildren:
                if eachJoint == eachJoint2:
                    duplicateJoints.append(eachJoint)
                    if len(duplicateJoints) > 2:
                        print('listDuplicateJoints(), the joint ' + eachJoint + ' is duplicated')
                        return
                    else:
                        print('listDuplicateJoints(), no duplicates found')
                        duplicateJoints = []
        print('listDuplicateJoints(), the duplicateJoints are: ' + str(duplicateJoints))


def listSkinJoints(*args):
    jointRoot = cmds.textField('jointRootTextField', query = True, text = True)
    jointHierarchy = cmds.listRelatives(jointRoot, allDescendents = True, type = 'joint')
    skinJoints = []
    for eachJoint in jointHierarchy:
        if 'end' not in eachJoint:
            skinJoints.append(eachJoint)
    return skinJoints


def writeNewNamingConventionData(*args):
        
    selectionInList = False
    for eachEntry in data:
        if eachEntry == eachController:
            selectionInList = True	

    newData = {eachController : {"Attributes": characterizationList}}
    print('readWriteCharacterization(), newData is in data is: ' + str(newData))


    if selectionInList:
        print('readWriteCharacterization(), newData for update is: ' + str(newData))
        data.update(newData)
        print('readWriteCharacterization(), data after update is for update is: ' + str(data))

    else:
        data = data | newData
        
    with open(path, 'w') as writefile:
        json.dump(data, writefile, sort_keys=True, indent=4)



def namingConventionSwap(*args):
    dataFile = cmds.textField('nameSwapDataFile', query = True, text = True)
    path = getDataLocation(dataFile)
    fileExists = False
    from pathlib import Path
    print('readWriteCharacterization(), the path to data is: ' + path)
    if os.path.exists(path):
        print(f"The path {dataFile} exists.")
        fileExists = True
    else:
        print(f"The path {dataFile} does not exist.")
        fileExists = False

    from collections import OrderedDict
    data = OrderedDict()

    
    print('readWriteCharacterization(), namingConventionSwapDirection is: ' + str(namingConventionSwapDirection))

    if fileExists == True:
        rootJoint = cmds.textField('jointRootTextField', query = True, text = True)
        jointHierarchy = cmds.listRelatives(rootJoint, allDescendents = True, type = 'joint')
        
        with open(path, 'r') as loadedData:
            data = json.load(loadedData)
        
        print('readWriteCharacterization(), data in data is: ' + str(data))

        keytoValue = True
        if namingConventionSwapDirection == 'JFMToUnreal':
            print('namingConventionSwap(), swapping from JFM to Unreal naming convention')
            keytoValue = True
        elif namingConventionSwapDirection == 'UnrealToJFM':
            print('namingConventionSwap(), swapping from Unreal to JFM naming convention')
            keytoValue = False
        
        print('namingConventionSwap(), the jointHierarchy is: ' + str(jointHierarchy))
        for eachJoint in jointHierarchy:
            print('namingConventionSwap(), eachJoint in jointHierarchy is : ' + str(eachJoint))
            if keytoValue == True:
                if eachJoint in data:
                    print('namingConventionSwap(), eachJoint is: ' + eachJoint + ' and the new name is: ' + data[eachJoint])
                    cmds.rename(eachJoint, data[eachJoint])
            elif keytoValue == False:
                if eachJoint in data.values():
                    print('namingConventionSwap(), eachJoint is: ' + eachJoint + ' and the new name is: ' + list(data.keys())[list(data.values()).index(eachJoint)])
                    cmds.rename(eachJoint, list(data.keys())[list(data.values()).index(eachJoint)])
    else:
        print('readWriteCharacterization(), the data file ' + dataFile + ' does not exist.  Using default naming convention swap data.')
        data = defaultNamingConventionSwapData
        selectionInList = False
        with open(path, 'w') as writefile:
            json.dump(data, writefile, sort_keys=True, indent=4)



#imports a json file
def getDataFile(nameOfFile):
	filePath = cmds.file(sceneName = True, query = True)
	#print('The filePath is: ' + str(filePath))
	pathToFile = '%s/%s' % (filePath.rsplit('/', 2)[0], 'data/' + nameOfFile + '.json')#regroving that path to go to the assets folder
	
	#print('The splitFilePath is: ' + str(pathToFile))

	from collections import OrderedDict
	data = OrderedDict()
	
	with open(pathToFile) as nameOfFile:
		data = json.load(nameOfFile, object_pairs_hook=OrderedDict)
	#print('getDataFile(), The data as an ordered list is: ' + str(data))
	return data


def setNamingConvention(namingConventionDirection):
    global namingConventionSwapDirection
    namingConventionSwapDirectionValue = cmds.optionMenu(nameConventionSwapOptionsMenu, query = True, value = True)
    if namingConventionSwapDirectionValue == 'JFM to Unreal':
        namingConventionSwapDirection = 'JFMToUnreal'
    elif namingConventionSwapDirectionValue == 'Unreal to JFM':
        namingConventionSwapDirection = 'UnrealToJFM'
    print('setNamingConvention(), the namingConventionDirection is:' + namingConventionDirection)


def selectSkinJoints(*args):
    jointRoot = cmds.textField('jointRootTextField', query = True, text = True)
    jointHierarchy = cmds.listRelatives(jointRoot, allDescendents = True, type = 'joint')
    skinJoints = []
    for eachJoint in jointHierarchy:
        if 'end' not in eachJoint and 'UNWEIGHTED' not in eachJoint:
            cmds.select(eachJoint, add = True)
    return skinJoints

def setControlType(control):
    global controlType
    controlType = control
    print('setControlType(), the joint chain direction is:' + controlType)


def setBodyRegionName(name):
    global bodyRegion
    bodyRegion = name
    print('setBodyRegionName(), the bodyRegion is:' + name)


def setFingerChainName(name):
    global fingerChain
    fingerChain = name
    print('setBodyRegionName(), the fingerChain is:' + fingerChain)


def setFBSide(FBsideOfBody):
    global FBSideAbbreviation
    if FBsideOfBody == 'front':
         FBSideAbbreviation = 'fr'
    if FBsideOfBody == 'back':
         FBSideAbbreviation = 'bk'
    if FBsideOfBody == 'none':
         FBSideAbbreviation = None
    print('setRLSide(), the RLsideOfBody is:' + FBsideOfBody)
    print('setRLSide(), the FBSideAbbreviation is:' + str(FBSideAbbreviation))


def setRLSide(RLsideOfBody):
    global RLSideAbbreviation
    if RLsideOfBody == 'left':
         RLSideAbbreviation = 'l'
    if RLsideOfBody == 'right':
         RLSideAbbreviation = 'r'
    if RLsideOfBody == 'none':
         RLSideAbbreviation = None
    print('setRLSide(), the RLsideOfBody is:' + RLsideOfBody)
    print('setRLSide(), the sideAbbriviation is:' + str(RLSideAbbreviation))


def setRLSideFinger(RLsideOfBody):
    global RLSideAbbreviationFingers
    if RLsideOfBody == 'left':
         RLSideAbbreviationFingers = 'l'
    if RLsideOfBody == 'right':
         RLSideAbbreviationFingers = 'r'
    if RLsideOfBody == 'none':
         RLSideAbbreviationFingers = None
    print('setRLSide(), the RLsideOfBody is:' + RLsideOfBody)
    print('setRLSide(), the RLSideAbbreviationFingers is:' + str(RLSideAbbreviationFingers))


def skinSelectedMeshes(*args):
    selectedMeshes = cmds.ls(selection = True)
    skinJoints = []
    skinJoints = listSkinJoints()
    cmds.select(skinJoints, replace = True)
    for eachMesh in selectedMeshes:
        cmds.skinCluster(skinJoints,eachMesh, toSelectedBones=True)

def updateTextField(newText, textFieldName):
    cmds.textField(textFieldName, edit=True, text=newText)


#___________________________________________Start GUI___________________________________________

windowID = 'RiggingTools'

if cmds.window(windowID, exists=True):
    cmds.deleteUI(windowID)

cmds.window(windowID, title='Rigging Tools', sizeable=True, width = 800)

#___________________________________________Tab1___________________________________________
#___________________________________________JointTools____________________________________


tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)

tabChild1 = cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1,800)], columnOffset=[(1,'both', 3)])
cmds.button(label = 'Make Buffer Joint', command = makeBufferJoint)
cmds.button(label = 'Setup/Clean Joint For Reorient', command = setupReorientJoint)

cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1,400), (2,400)], columnOffset=[(1,'both', 3)])
reorientChildren = cmds.checkBox(label='Reorient Children', value=False)
reverseX = cmds.checkBox(label='reverseX (leg left)', value=False)
cmds.button(label = 'Orient Joint for Unreal (Left)', command = orientJointForUnreal)

cmds.button(label = 'List Duplicate Joints', command = listDuplicateJoints)
cmds.setParent('..')

cmds.setParent('..')
#___________________________________________End_Tab1___________________________________________
#___________________________________________Start_Tab2___________________________________________
#_________________________________________Controllers__________________________________________

tabChild2 = cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1,400), (2,400)], columnOffset=[(1,'both', 3)])
cmds.text('Controller Scale')
controllerScale = cmds.floatField('controllerScale', value=1.0)
controlTypeMenu = cmds.optionMenu(label='Control Type', changeCommand=setControlType)
cmds.menuItem(label='Rotation_Control')

#cmds.button(label = 'Create Medial Joint Chain', command = createMedialJoints)

cmds.button(label = 'Setup Controller', command = setupController)
cmds.setParent('..')

#___________________________________________End_Tab2___________________________________________
#___________________________________________Start_Tab3___________________________________________
#_______________________________________Unreal Joint Naming_________________________________________

tabChild3 = cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1,800)], columnOffset=[(1,'both', 3)])

cmds.separator(h=10, style='none')
cmds.text('Rename Unreal Body joints for, Select the joint(s) in order, set region and hit button')
cmds.separator(h=10, style='single')

cmds.rowColumnLayout(numberOfColumns=4, columnWidth=[(1,180), (2,180), (3,180), (4,180)], columnSpacing=[(1, 10), (2, 10), (3, 10), (4, 10)], columnOffset=[(1,'both', 3)])
bodyRegionOptionMenu = cmds.optionMenu(label='Body Region', changeCommand=setBodyRegionName)
cmds.menuItem(label='custom')
cmds.menuItem(label='pelvis')
cmds.menuItem(label='spine')
cmds.menuItem(label='neck')
cmds.menuItem(label='head')
cmds.menuItem(label='clavicle')
cmds.menuItem(label='upperarm')
cmds.menuItem(label='lowerarm')
cmds.menuItem(label='hand')
cmds.menuItem(label='pectoral')
cmds.menuItem(label='deltoid')
cmds.menuItem(label='elbow')
cmds.menuItem(label='thigh')
cmds.menuItem(label='knee')
cmds.menuItem(label='calf')
cmds.menuItem(label='foot')
cmds.menuItem(label='ball')
cmds.menuItem(label='toe')
cmds.menuItem(label='heel')

cmds.textField('bodyRegionTextField', editable = True, text = 'custom name')

rightLeftSide = cmds.optionMenu(label='Right/Left Side', changeCommand=setRLSide)
cmds.menuItem(label='none')
cmds.menuItem(label='left')
cmds.menuItem(label='right')

frontBackSide = cmds.optionMenu(label='Front/Back Side', changeCommand=setFBSide)
cmds.menuItem(label='none')
cmds.menuItem(label='front')
cmds.menuItem(label='back')
cmds.setParent('..')

cmds.separator(h=10, style='single')

cmds.rowColumnLayout(numberOfColumns=4, columnWidth=[(1,200), (2,200), (3,200), (4,200)], columnOffset=[(1,'both', 3)])
isEnumeratedCheckbox = cmds.checkBox(label='is enumerated', value=False)
cmds.text('start number:')
startNumberSequence = cmds.intField("startNumberIntField", value = 0)
cmds.separator(h=10, style='none')
cmds.setParent('..')

cmds.separator(h=10, style='single')

cmds.rowColumnLayout(numberOfColumns=6, columnWidth=[(1,130), (2,130), (3,130), (4,130), (5,130), (6,130)], columnOffset=[(1,'both', 3)])
isStretchyJointCheckbox = cmds.checkBox(label='stretchy joint', value=False)
isTwistJointCheckbox = cmds.checkBox(label='twist joint', value=False)
isDeformJointCheckbox = cmds.checkBox(label='deform joint', value=False)
isDynamicJointCheckbox = cmds.checkBox(label='dynamic joint', value=False)
isAttachJointCheckbox = cmds.checkBox(label='attach joint', value=False)
isPivotJointCheckbox = cmds.checkBox(label='pivot joint', value=False)
cmds.setParent('..')

cmds.separator(h=10, style='single')

cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1,800)], columnOffset=[(1,'both', 3)])
cmds.button(label = 'Rename Joint', command = renameBodyJoints)
cmds.setParent('..')

cmds.separator(h=10, style='double')
cmds.separator(h=10, style='double')

cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1,800)], columnOffset=[(1,'both', 3)])
cmds.text('Rename for Unreal hand joints, select the first joint in the chain, check whether it has metacarpals and end joints and hit button')
cmds.setParent('..')

cmds.rowColumnLayout(numberOfColumns=5, columnWidth=[(1,140), (2,140), (3,140), (4,140), (5,140)], 
                     columnSpacing=[(1, 10), (2, 10), (3, 10), (4, 10), (5, 10)], columnOffset=[(1,'both', 3)])
fingerChain = cmds.optionMenu(label='Finger Chain', changeCommand=setFingerChainName)
cmds.menuItem(label='thumb')
cmds.menuItem(label='index')
cmds.menuItem(label='middle')
cmds.menuItem(label='ring')
cmds.menuItem(label='pinky')

rightLeftSideFingers = cmds.optionMenu(label='Right/Left Side', changeCommand=setRLSideFinger)
cmds.menuItem(label='left')
cmds.menuItem(label='right')
cmds.menuItem(label='none')
hasMetacarpals = cmds.checkBox(label='Has Metacarpals', value=True)
hasEndJoint = cmds.checkBox(label='Has End Jont', value=True)
isToes = cmds.checkBox(label='Are Toes', value=True)
cmds.setParent('..')

cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1,800)], columnOffset=[(1,'both', 3)])
cmds.button(label = 'Rename Finger Joints', command = renameFingerJoints)
cmds.textField('unrealName', editable = True, text = 'new name')
cmds.setParent('..')

cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1,400), (2,400)])
cmds.textField('jointRootTextField', text = 'root')
cmds.textField('nameSwapDataFile', text = 'JFM-Unreal_SkeletalNamingConvention_Dict')
nameConventionSwapOptionsMenu = cmds.optionMenu(label='Name Convention Swap', changeCommand=setNamingConvention)
cmds.menuItem(label='JFM to Unreal')
cmds.menuItem(label='Unreal to JFM')
cmds.button(label = 'Run Name Convention Swap', command = namingConventionSwap)
cmds.setParent('..')

cmds.setParent('..')

#___________________________________________End_Tab3___________________________________________
#___________________________________________Start_Tab4___________________________________________

tabChild4 = cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1,800)], columnOffset=[(1,'both', 3)])
cmds.textField('jointRootTextField', text = 'root')
cmds.button(label = 'Select Skin Joints', command = selectSkinJoints)
cmds.button(label = 'Skin Selected Meshes', command = skinSelectedMeshes)

cmds.setParent('..')

#___________________________________________End_Tab4___________________________________________
#___________________________________________Start_Tab5___________________________________________

tabChild5 = cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1,400), (2,400)], columnOffset=[(1,'both', 3)])


cmds.setParent('..')

#___________________________________________End_Tab5___________________________________________
#___________________________________________Start_Tab6___________________________________________

tabChild6 = cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1,400)], columnOffset=[(1,'both', 3)])

cmds.text('Select the root of the joint chain, enter body part key, set the down axis and run Align Joint Chain')
cmds.rowColumnLayout(numberOfColumns=5, columnWidth=[(1,200), (2,50), (3,50), (4,50), (5,150)], columnOffset=[(1,'both', 3)])

cmds.tabLayout(tabs, edit=True, tabLabel=((tabChild1, 'Joint Tools'), (tabChild2, 'Controls Setup'),  (tabChild3, 'Joint Naming Unreal'), (tabChild4, 'Skinning'), (tabChild5, 'Unskin/Export'), (tabChild6, 'Other Tools')) )





cmds.showWindow()