import maya.cmds as cmds

controlType = 'Rotation_Control'
bodyRegion = 'spine'
fingerChain = 'thumb'
auxJointType = 'deform'
RLSideAbbreviation = None
FBSideAbbreviation = None
RLSideAbbreviationFingers = 'l'


def makeBufferJoint(*args):
    joint = cmds.ls(selection = True)[0]
    jointParent = cmds.listRelatives(parent = True)
    bufferJoint = cmds.duplicate(joint, parentOnly = True, name = joint + '_BufferJoint')
    cmds.parent(joint, bufferJoint)
    cmds.parent(bufferJoint, jointParent)


def orientJointForUnreal(*args):
    jointForOrient = cmds.ls(selection = True)[0]
    cmds.makeIdentity(jointForOrient, apply = True, translate = True, rotate = True, scale = True, jointOrient = True)
    print('orientJointForUnreal(), jointForOrient is: ' + str(jointForOrient))
    reorientChildrenValue = cmds.checkBox(reorientChildren, query=True, value=True)
    reverseXValue = cmds.checkBox(reverseX, query=True, value=True)
    print('orientJointForUnreal(), reorientChildrenValue is: ' + str(reorientChildrenValue))
    print('orientJointForUnreal(), reverseXValue is: ' + str(reverseXValue))
    cmds.joint(jointForOrient, edit = True, orientJoint = 'xzy', secondaryAxisOrient = 'xdown', children = reorientChildrenValue, zeroScaleOrient = True) #
    
    if reverseXValue == True:
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
    print('renameBodyJoints(), the FBSideAbbreviation is: ' + str(FBSideAbbreviation))
    print('renameBodyJoints(), the RLSideAbbreviation is: ' + str(RLSideAbbreviation))
    isTwistJoint = cmds.checkBox(isTwistJointCheckbox, query=True, value=True)
    isDeformJoint = cmds.checkBox(isDeformJointCheckbox, query=True, value=True)
    isDynamicsJoint = cmds.checkBox(isDynamicJointCheckbox, query=True, value=True)
    isAttachJoint = cmds.checkBox(isAttachJointCheckbox, query=True, value=True)
    isEnumerated = cmds.checkBox(isEnumeratedCheckbox, query=True, value=True)
    print('renameBodyJoints(), isTwistJoint is: ' + str(isTwistJoint))
    if isEnumerated == True:
        print('renameBodyJoints(), isEnumerated is ' + str(isEnumerated))
        startNumberSequence = cmds.intField("startNumberIntField", query = True, value = True)
        print('renameBodyJoints(), the startNumberSequence is: ' + str(startNumberSequence))
        i = startNumberSequence
    
    jointSelection = cmds.ls(selection = True)
    name = bodyRegion
    if jointSelection:
        for eachJoint in jointSelection:
            if isTwistJoint:
                name = name + '_twist'
            if isDeformJoint:
                name = 'deform_' + name 
            if isDynamicsJoint:
                name = 'dyn_' + name
            if isAttachJoint:
                name = name + '_Attach'
            if isEnumerated == True:
                name = name + '_' + str(0) + str(i)
            if FBSideAbbreviation != None:
                name = name + '_' + FBSideAbbreviation
            if RLSideAbbreviation != None:
                name = name + '_' + RLSideAbbreviation
            print('renameBodyJoints(), the name is :' + name)
            cmds.rename(eachJoint, name)
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
        setupJointForReorient()
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


def setControlType(control):
    global controlType
    controlType = control
    print('setControlType(), the joint chain direction is:' + controlType)


def setBodyRegionName(name):
    global bodyRegion
    bodyRegion = name
    print('setBodyRegionName(), the bodyRegoin is:' + name)


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
cmds.setParent('..')

cmds.setParent('..')
#___________________________________________End_Tab1___________________________________________
#___________________________________________Start_Tab2___________________________________________
#_________________________________________Controllers__________________________________________

tabChild2 = cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1,400), (2,400)], columnOffset=[(1,'both', 3)])
cmds.text('Controller Scale')
controllerScale = cmds.floatField('controllerScale', value=1.0)
controlTypeMenu = cmds.optionMenu(label='Joint Chain Direction, Medial', changeCommand=setControlType)
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

cmds.rowColumnLayout(numberOfColumns=4, columnWidth=[(1,200), (2,200), (3,200), (4,200)], columnOffset=[(1,'both', 3)])
rightLeftSide = cmds.optionMenu(label='Right/Left Side', changeCommand=setRLSide)
cmds.menuItem(label='none')
cmds.menuItem(label='left')
cmds.menuItem(label='right')

cmds.separator(w=10, style='none')
frontBackSide = cmds.optionMenu(label='Front/Back Side', changeCommand=setFBSide)
cmds.menuItem(label='none')
cmds.menuItem(label='front')
cmds.menuItem(label='back')
cmds.separator(w=10, style='none')
cmds.setParent('..')

cmds.separator(h=10, style='single')

cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1,265), (2,265), (3,265)], columnOffset=[(1,'both', 3)])
isEnumeratedCheckbox = cmds.checkBox(label='is enumerated', value=False)
cmds.text('start number:')
startNumberSequence = cmds.intField("startNumberIntField", value = 0)
cmds.setParent('..')

cmds.separator(h=10, style='single')

cmds.rowColumnLayout(numberOfColumns=4, columnWidth=[(1,200), (2,200), (3,200), (4,200)], columnOffset=[(1,'both', 3)])
isTwistJointCheckbox = cmds.checkBox(label='twist joint', value=False)
isDeformJointCheckbox = cmds.checkBox(label='deform joint', value=False)
isDynamicJointCheckbox = cmds.checkBox(label='dynamic joint', value=False)
isAttachJointCheckbox = cmds.checkBox(label='attach joint', value=False)
cmds.setParent('..')

cmds.separator(h=10, style='double')

cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1,400), (2,400)], columnOffset=[(1,'both', 3)])
bodyRegion = cmds.optionMenu(label='Body Region', changeCommand=setBodyRegionName)
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
cmds.button(label = 'Rename Joint', command = renameBodyJoints)
cmds.setParent('..')

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
cmds.setParent('..')


cmds.setParent('..')

#___________________________________________End_Tab3___________________________________________
#___________________________________________Start_Tab4___________________________________________

tabChild4 = cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1,800)], columnOffset=[(1,'both', 3)])


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

cmds.tabLayout(tabs, edit=True, tabLabel=((tabChild1, 'Joint Tools'), (tabChild2, 'Controls Setup'),  (tabChild3, 'Joint Naming Unreal'), (tabChild4, 'Select Joints'), (tabChild5, 'Unskin/Export'), (tabChild6, 'Other Tools')) )





cmds.showWindow()