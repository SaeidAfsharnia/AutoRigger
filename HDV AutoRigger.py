###################################
###     IMPORT LIBRARY          ###
###################################
import maya.cmds as cmds
import urllib.request

"""
FW_ Function related to Windows         F_AR > Function Arm Rigger
F_WM > Function Wheel Set Maker         F_TM > Function Tread Maker
F_HR > Function Hydraulic Rigger        FU   > General Utility Functions 

"""
###################################
###    GLOBAL VARIABLES         ###
###################################
#colors Variables
brightColor=[0.25, 0.4, 0.4];   enabledColor=[0.1, 0.2, 0.2]
disabledColor=[0.3,0.3,0.3]   
#Variable for treadmaker
updateCopyNum=35
#variable for Arm Rigger
locList=[]; JointList=[]
#variable for Hydraulics Rigger
rigType=""; controlerDistance=0.5; controlerScale=0.3
#Windows Names Variable 
FW_RMName="RiggingMenu";  treadWinName="TreadBuilder"
wheelWinName="WheelRigger"; armRigWinName="ArmRigger"
hydWinName="HydraulicMaker"
#Geral Variables
UIWidth=420

######################################
###  FUNCTIONS for ARM RIGGER      ###
######################################  

def F_AR_makeJoints():#this func create joints where the locators are
    cmds.select(cl=True)
    global JointList
    JointList=[]
    for i in locList:
        TheJoint=cmds.joint(n='%s_Jnt' %i)
        JointList.append(TheJoint)
        Thelocator=i
        cmds.matchTransform(TheJoint,Thelocator,pos=True)
    jointScrolSel=(cmds.intSliderGrp(FW_RM.jointsQ,q=True,v=True))-1
    cmds.textScrollList(FW_RM.locListScrAR, e=True, ra=True)          #here I will remove th eitens from the textscroll and refresh with updated list
    cmds.textScrollList(FW_RM.locListScrAR,e=True,append=(locList))
    jntScrolLS=[FW_RM.jntsAR,FW_RM.jntsAR1]
    for item in jntScrolLS:
        cmds.textScrollList(item, e=True, ra=True)          #here I will remove the itens from the textscroll and refresh with updated list
        cmds.textScrollList(item,e=True,append=(JointList))      
    cmds.textScrollList(FW_RM.jntsAR, e=True, sii=1)
    cmds.textScrollList(FW_RM.jntsAR1, e=True, sii=jointScrolSel)     
    #cmds.button(FW_RM.ikBtnAR,edit=True,enable=True)
    FUI_endis([FW_RM.ikBtnAR],"button",True)
    FUI_endis([FW_RM.jointsBtnAR],"button",False)
    FUI_endis([FW_RM.sjAR,FW_RM.eeAR],"text",True)

def F_AR_ikHandle():
    sjJnt=cmds.textScrollList(FW_RM.jntsAR,q=True,si=True)[0] #fetch the joint the user choose
    eeJnt=cmds.textScrollList(FW_RM.jntsAR1,q=True,si=True)[0]
    F_AR_ikHandle=cmds.ikHandle(sj=sjJnt,ee=eeJnt)[0]
    FUI_endis([FW_RM.jntsAR,FW_RM.jntsAR1],"textScrollList",False)
    FUI_endis([FW_RM.sjAR,FW_RM.eeAR],"text",False)
    F_AR_resetLoc()
    
def F_AR_makeLoc():  #this func create as many locators as user choose
    FW_RM.jointsQValue=cmds.intSliderGrp(FW_RM.jointsQ,q=True,v=True)
    for i in range(1,FW_RM.jointsQValue+1):
        newLoc=cmds.spaceLocator(n="ArmLocator%s"%i,p=(0,0,-i*5))
        cmds.CenterPivot()
        locXYZ=cmds.getAttr(newLoc[0]+".wp")
        locList.append(newLoc[0])
    #disabling the make locators button and slider // reset button enable
    FUI_endis([FW_RM.makeBtnAR],"button",False)
    FUI_endis([FW_RM.resetBtnAR,FW_RM.jointsBtnAR],"button",True)
    FUI_endis([FW_RM.jointsQ],"intSliderGrp",False)
    FUI_endis([FW_RM.msg001AR,FW_RM.msg002AR],"vis_text",True)
    #this func is to save the location of the locators    
    global locLocation
    locLocation=[]
    for i in (locList):
        locXYZ=cmds.getAttr(i+'.wp')
        locLocation.append(locXYZ[0])
    return 
    
def F_AR_resetLoc(): #this function delete the last locators created 
    global locList
    cmds.select(locList)
    cmds.delete()
    locList=[]
    #enabling the make locators button and slider // reset button disable
    FUI_endis([FW_RM.makeBtnAR],"button",True)
    FUI_endis([FW_RM.resetBtnAR,FW_RM.jointsBtnAR,FW_RM.ikBtnAR],"button",False)#,FW_RM.ikBtnAR
    FUI_endis([FW_RM.jointsQ],"intSliderGrp",True)
    FUI_endis([FW_RM.msg001AR,FW_RM.msg002AR],"vis_text",False)

def F_AR_locNumber(): #this func pass new slider numer
    FW_RM.jointsQValue=cmds.intSliderGrp(FW_RM.jointsQ,q=True,v=True)
    namelist=[]
    for i in range(1,FW_RM.jointsQValue+1):
        namelist.append(i)

######################################
###  FUNCTIONS for WHEELMAKER      ###
######################################    

def F_WM_wheelSel():
    F_WM_wheelSel.selWheels=cmds.ls(sl=True)
    cmds.group(n="WheelGrp")
    cmds.select(clear=True)
    cmds.select("WheelCTRL");   cmds.select("WheelGrp",add=True)
    cmds.align(x="mid",z="mid",y="max",atl=True)
    cmds.select("WheelCTRL")
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    wheelRadius=cmds.floatSliderGrp(FW_RM.wheelRad,q=True,v=True)
    Primeter=(3.1415*2*wheelRadius)
    if radioSelection==1:
        for wheel in F_WM_wheelSel.selWheels:
            cmds.expression(n="rotator",string=wheel+".rz=(WheelCTRL.tx/%s)*-360"%Primeter)
    if radioSelection==2:
        for wheel in F_WM_wheelSel.selWheels:
            cmds.expression(n="rotator",string=wheel+".rz=(WheelCTRL.ty/%s)*360"%Primeter) 
    else:    
        for wheel in F_WM_wheelSel.selWheels:
            cmds.expression(n="rotator",string=wheel+".rx=(WheelCTRL.tz/%s)*360"%Primeter)
    cmds.parentConstraint("WheelCTRL","WheelGrp",mo=True)
    
def F_WM_FrontWheel():
    wheelRadius=cmds.floatSliderGrp(FW_RM.wheelRad,q=True,v=True)
    cmds.group(n="Front_Grp")
    cmds.circle(n="Rotation_Ctrl",radius = (wheelRadius*2.5),nrx=0,nry=1,nrz=0)
    cmds.select("Rotation_Ctrl");   cmds.select("Front_Grp",add=True)
    cmds.align(x="mid",z="mid",y="max",atl=True)
    cmds.ungroup("Front_Grp")
    F_WM_FrontWheel.selection=cmds.ls(sl=True)
    for i in F_WM_FrontWheel.selection:
        if radioSelection==1:
            curveCtrl=cmds.circle(n="Front_Wheel_Rot_Ctrl",radius = (wheelRadius*1.2),nrx=0,nry=0,nrz=1)
        if radioSelection==2:
            curveCtrl=cmds.circle(n="Front_Wheel_Rot_Ctrl",radius = (wheelRadius*1.2),nrx=1,nry=0,nrz=0)    
        else:    
            curveCtrl=cmds.circle(n="Front_Wheel_Rot_Ctrl",radius = (wheelRadius*1.2),nrx=1,nry=0,nrz=0)
        cmds.select(curveCtrl)
        cmds.matchTransform(curveCtrl[0],i)
        cmds.select(clear=True)
        cmds.select('Rotation_Ctrl')
        cmds.select(curveCtrl[0],add = True)
        cmds.parentConstraint(mo = True,  st=["x","y","z"],sr=["x","z"])
        cmds.select(curveCtrl[0])
        cmds.select(i,add = True)
        cmds.parentConstraint(mo = True, st=["x","y","z"],sr=["x","z"])
    cmds.group("Front_Wheel_Rot_Ctrl","Front_Wheel_Rot_Ctrl1",n="FrWheels")
    cmds.select(cl=True)
    cmds.select('Rotation_Ctrl',"FrWheels")
    cmds.parentConstraint(mo = True,  sr=["x","y","z"])
    cmds.select('WheelCTRL','Rotation_Ctrl')
    cmds.parentConstraint(mo = True,  sr=["x","y","z"])

def F_WM_resetAll():
    if cmds.objExists('WheelCTRL'):
        cmds.delete("WheelCTRL")
    if cmds.objExists("Rotation_Ctrl"):
        cmds.delete("Rotation_Ctrl")
    if cmds.objExists("Front_Wheel_Rot_Ctrl"):
        cmds.delete("Front_Wheel_Rot_Ctrl")
    if cmds.objExists("Front_Wheel_Rot_Ctrl1"):
        cmds.delete("Front_Wheel_Rot_Ctrl1")
    if cmds.objExists("WheelGrp"):
        cmds.ungroup("WheelGrp")
        cmds.delete("WheelGrp")
    if cmds.objExists("FrWheels"):
        cmds.delete("FrWheels")

def F_WM_renaming():
    cmds.rename("WheelCTRL","WheelCTRL1");  cmds.rename("WheelGrp","WheelGrp1")

def F_WM_arrowDrop():
    cmds.curve(n="WheelCTRL", d=1, p=[(-20,0,0),(-27.5,0,-7.5),(-22.5,0,-7.5),(-22.5,0,-17.5),(-27.5,0,-17.5),(-20,0,-25),(-12.5,0,-17.5),
                        (-17.5,0,-17.5),(-17.5,0,-7.5),(-12.5,0,-7.5),(-20,0,0)],k=[0,1,2,3,4,5,6,7,8,9,10])
    global radioSelection
    radioSelection=cmds.radioButtonGrp(FW_RM.radioSel,q=True,sl=True)
    cmds.CenterPivot("WheelCTRL")
    if radioSelection==1:
        cmds.rotate(0,90,0)
    if radioSelection==2:
        cmds.rotate(90,0,0)
    cmds.closeCurve(rpo=True)
    
######################################
###  FUNCTIONS for TREADMAKER      ###
######################################

def F_TM_confirmAxis(): #confirms the model is Z-axis aligned
    cmds.deleteUI(FW_RM.msgOrientTM,FW_RM.confirmBtnTM,control=True)
    F_TM_OnOff("enInit")

def F_TM_initFunc(): #initializes treadmaker by creating two locators
    F_TM_initFunc.frontLocator=cmds.spaceLocator(n="CircleLocFront")
    cmds.scale(5,5,5)
    cmds.move(0,0,10,r=True)
    F_TM_initFunc.backLocator=cmds.spaceLocator(n="CircleLocBack")
    cmds.scale(5,5,5)
    cmds.move(0,0,-10,r=True)
    cmds.confirmDialog(m="Place the two locators at the FRONT and BACK of your model.")  ## changed wording
    F_TM_OnOff("disInit");    F_TM_OnOff("enCurve");    F_TM_OnOff("enReset")

def F_TM_makeCurve(): #creates a curve based on the two locators
    FW_RM.curveCheckTM=1
    cmds.select(F_TM_initFunc.frontLocator)
    frontLocPos=cmds.getAttr(".translateZ")
    cmds.select(F_TM_initFunc.backLocator)
    backLocPos=cmds.getAttr(".translateZ")
    LocDistance=abs(frontLocPos-backLocPos)
    curveRadius=LocDistance/2
    F_TM_makeCurve.treadCurve=cmds.circle(n="TreadCurve",r=curveRadius,nr=(1,0,0),sections=12)[0]
    cmds.group(F_TM_initFunc.frontLocator,F_TM_initFunc.backLocator,n="locGroup")
    cmds.select(F_TM_makeCurve.treadCurve,r=True)
    cmds.select("locGroup",add=True)
    cmds.align(z="mid", atl=True)
    cmds.select(F_TM_makeCurve.treadCurve)
    cmds.FreezeTransformations()
    cmds.DeleteHistory()
    cmds.select(cl=True)
    F_TM_OnOff("disCurve");    F_TM_OnOff("enPickedObj")
    
def F_TM_pickingObj(): #function to pick the tread object
    global selectedOBJ
    selectedOBJ=cmds.ls(sl=True,o=True)
    F_TM_pickingObj.loc=cmds.getAttr(selectedOBJ[0]+".translate") #getting the original location of the object to return in case user reset
    if len(selectedOBJ)==1:
        F_TM_OnOff("disPickObj");        F_TM_OnOff("enMakeTread")
    else:
        cmds.confirmDialog(m="Please select one object")
    return selectedOBJ

def F_TM_useDefault():
    global selectedOBJ
    defaultCube=cmds.polyCube(h=1,d=1,w=4)
    cmds.move(10,0,0,ws=True)
    selectedOBJ=cmds.ls(sl=True,o=True)
    if len(selectedOBJ)==1:
        F_TM_OnOff("disPickObj");        F_TM_OnOff("enMakeTread")
    return selectedOBJ

def F_TM_numChange(): #function to define the number of treads
    cmds.button(FW_RM.makeTreadTM,edit=True,enable=False)
    if cmds.objExists("TreadFull"): cmds.delete("TreadFull")
    if cmds.objExists("_wire"): cmds.delete("_wire")
    
    global updateCopyNum
    updateCopyNum=cmds.intSliderGrp(FW_RM.copyNumTM,query=True,v=True)
    #animates the picked obj around the path
    cmds.select(selectedOBJ,r=True)
    cmds.select(F_TM_makeCurve.treadCurve,add=True)
    cmds.pathAnimation(f=True,fa="z",ua="y",wut="vector",wu=(0,1,0),inverseFront=False,iu=False,b=False,stu=1,etu=updateCopyNum)
    cmds.select(selectedOBJ,r=True)
    cmds.selectKey("motionPath1_uValue",time=(1,updateCopyNum))
    cmds.keyTangent(itt="linear",ott="linear")
    cmds.snapshot(n="TreadSS",i=1,ch=False,st=1,et=updateCopyNum,u="animCurve")
    cmds.DeleteMotionPaths()
    #combines duplicates and deletes Snapshot
    cmds.select("TreadSSGroup",r=True)
    cmds.polyUnite(n="TreadFull",ch=False)
    cmds.select("TreadSSGroup",r=True)
    cmds.delete()
    def createWireD(geo,wireCRV,dropoffDist=40):
        wire=cmds.wire(geo,w=wireCRV,n="_wire")
        wirenode=wire[0]
        cmds.setAttr(wirenode+".dropoffDistance[0]",dropoffDist)

    cmds.select("TreadFull")
    wireObj=cmds.ls(sl=True,o=True)[0]
    cmds.select(F_TM_makeCurve.treadCurve)
    wirecurve=cmds.ls(sl=True,o=True)[0]
    createWireD(wireObj,wirecurve)
    F_TM_OnOff("disPickObj");    F_TM_OnOff("enCheckbox")
    return updateCopyNum

def F_TM_makeTread(): #function to make treads based on obj and number
    #animates the tread around the path
    cmds.button(FW_RM.makeTreadTM,edit=True,enable=False)
    cmds.select(selectedOBJ,r=True)
    cmds.select(F_TM_makeCurve.treadCurve,add=True)
    cmds.pathAnimation(follow=True,followAxis="z",upAxis="y",
        worldUpType="vector",worldUpVector=(0,1,0),
        inverseFront=False,inverseUp=False,bank=False,startTimeU=1,endTimeU=updateCopyNum)
    cmds.select(selectedOBJ,r=True)
    cmds.selectKey("motionPath1_uValue",time=(1,updateCopyNum))
    cmds.keyTangent(itt="linear",ott="linear")
    cmds.snapshot(n="TreadSS",i=1,ch=False,st=1,et=updateCopyNum,u="animCurve")
    cmds.DeleteMotionPaths()
    #combines duplicates and deletes Snapshot
    cmds.select("TreadSSGroup",r=True)
    cmds.polyUnite(n="TreadFull",ch=False)
    cmds.select("TreadSSGroup",r=True)
    cmds.delete()
    def createWireD(geo,wireCRV,dropoffDist=40):
        wire=cmds.wire(geo,w=wireCRV,n="_wire")
        wirenode=wire[0]
        cmds.setAttr(wirenode+".dropoffDistance[0]",dropoffDist)
    cmds.select("TreadFull")
    wireObj=cmds.ls(sl=True,o=True)[0]
    cmds.select(F_TM_makeCurve.treadCurve)
    wirecurve=cmds.ls(sl=True,o=True)[0]
    createWireD(wireObj,wirecurve)
    F_TM_OnOff("disMakeTread");    F_TM_OnOff("enCheckbox")

def F_TM_resetLoc(): #resets the tool
    CheckF_WM_resetAll=cmds.checkBox(FW_RM.resetAllTM, q=True, v=True)
    if CheckF_WM_resetAll==True:
        if cmds.objExists("TreadFull"): cmds.delete("TreadFull")
        if cmds.objExists("_wire"):     cmds.delete("_wire")
    if cmds.objExists(F_TM_initFunc.frontLocator[0]):   cmds.delete(F_TM_initFunc.frontLocator[0])
    if cmds.objExists(F_TM_initFunc.backLocator[0]):    cmds.delete(F_TM_initFunc.backLocator[0])
    if FW_RM.curveCheckTM==1:
        if cmds.objExists(F_TM_makeCurve.treadCurve):   cmds.delete(F_TM_makeCurve.treadCurve)
        if cmds.objExists("locGroup"):  cmds.delete("locGroup")
    try:
        cmds.select(selectedOBJ[0])
        cmds.move(F_TM_pickingObj.loc[0][0],F_TM_pickingObj.loc[0][1],F_TM_pickingObj.loc[0][2])
    except:
        pass
    selectedOBJ[0]=""
    F_TM_OnOff("disCurve");    F_TM_OnOff("disPickObj");    F_TM_OnOff("disMakeTread")
    cmds.intSliderGrp(FW_RM.copyNumTM,edit=True,enable=False)
    F_TM_OnOff("disReset");    F_TM_OnOff("enInit")

def F_TM_OnOff(whichUI):
    if whichUI=="enInit":
        cmds.text(FW_RM.msgInitTM,e=True,enable=True)
        cmds.button(FW_RM.initBtnTM,edit=True,en=True,bgc=enabledColor)
    if whichUI=="disInit":
        cmds.text(FW_RM.msgInitTM,e=True,enable=False)
        cmds.button(FW_RM.initBtnTM,edit=True,en=False, bgc=disabledColor)
    if whichUI=="enCurve":
        cmds.text(FW_RM.msgCurveTM, e=True, enable=True)
        cmds.button(FW_RM.makeCurveBtnTM,edit=True,enable=True, bgc=enabledColor)
    if whichUI=="disCurve":
        cmds.text(FW_RM.msgCurveTM,e=True,enable=False)
        cmds.button(FW_RM.makeCurveBtnTM,edit=True,enable=False,bgc=disabledColor)
    if whichUI=='enPickedObj':
        cmds.text(FW_RM.objPickTM, e=True, enable=True)
        cmds.textFieldButtonGrp(FW_RM.objTextTM, e=True, enable=True,bgc=enabledColor)
        cmds.text(FW_RM.msgDefaultCubeTM,edit=True,enable=True)
        cmds.button(FW_RM.makeDefaultCubeTM,edit=True,enable=True,bgc=enabledColor)
    if whichUI=="disPickObj":
        cmds.text(FW_RM.objPickTM,e=True,enable=False)
        cmds.textFieldButtonGrp(FW_RM.objTextTM,e=True,enable=False,tx=selectedOBJ[0],bgc=disabledColor)
        cmds.text(FW_RM.msgDefaultCubeTM,edit=True,enable=False)
        cmds.button(FW_RM.makeDefaultCubeTM,edit=True,enable=False,bgc=disabledColor)
    if whichUI=="enMakeTread":
        cmds.intSliderGrp(FW_RM.copyNumTM,edit=True,enable=True)
        cmds.button(FW_RM.makeTreadTM,edit=True,enable=True,bgc=enabledColor)
        cmds.text(FW_RM.objNumTM,e=True,enable=True)
    if whichUI=="disMakeTread":
        cmds.text(FW_RM.objNumTM,e=True,enable=False)
        cmds.button(FW_RM.makeTreadTM,edit=True,enable=False,bgc=disabledColor)
    if whichUI=="enReset":
        cmds.button(FW_RM.resetBtnTM,edit=True,en=True, bgc=brightColor)
    if whichUI=="enCheckbox":
        cmds.checkBox(FW_RM.resetAllTM, e=True, enable=True)
    if whichUI=="disReset":
        cmds.button(FW_RM.resetBtnTM,edit=True,en=False,bgc=disabledColor)
        cmds.checkBox(FW_RM.resetAllTM, e=True, enable=False)

######################################
###  FUNCTIONS HYDRAULIC RIGGER    ###
###################################### 

def F_HR_createHyd(): #function to create inner and outer hydraulics objects
    outerExtrude=(FW_RM.outerThickHR*-(1-(FW_RM.innerMultHR/100)-0.01))
    innerRadius=FW_RM.outerThickHR*((FW_RM.innerMultHR/100))
    #creating first cylinder
    F_HR_createHyd.outerHyd=cmds.polyCylinder(n="HydraulicOuter",h=FW_RM.hydHeightHR,r=FW_RM.outerThickHR,sx=32,sy=1,sz=1,cuv=3,ch=False)[0]
    cmds.rotate(90,0,0)
    #moving the pivot 
    cmds.move(0,0,-FW_RM.hydHeightHR/2, F_HR_createHyd.outerHyd+'.scalePivot', F_HR_createHyd.outerHyd+'.rotatePivot',absolute=True)
    cmds.delete(F_HR_createHyd.outerHyd+".f[64:95]")   #deleting faces to fit the inner cylinder
    cmds.select(F_HR_createHyd.outerHyd+".e[32:63]")   #selecting the edges to extrude 
    edgesToExt=cmds.polyExtrudeEdge(ch=True,keepFacesTogether=True,pvx=1.639127731,pvy=-1.639127731,pvz=1,d=1,twist=0,taper=1,offset=0,thickness=0,smoothingAngle=30)[0]
    cmds.setAttr(edgesToExt+".localTranslate",0,0,outerExtrude) 
    cmds.select(F_HR_createHyd.outerHyd+".e[156]",F_HR_createHyd.outerHyd+".e[130]",F_HR_createHyd.outerHyd+".e[132]",F_HR_createHyd.outerHyd+".e[134]",F_HR_createHyd.outerHyd+".e[136]",F_HR_createHyd.outerHyd+".e[138]",F_HR_createHyd.outerHyd+".e[140]",
    F_HR_createHyd.outerHyd+".e[142]",F_HR_createHyd.outerHyd+".e[144]",F_HR_createHyd.outerHyd+".e[146]",F_HR_createHyd.outerHyd+".e[148]",F_HR_createHyd.outerHyd+".e[150]",F_HR_createHyd.outerHyd+".e[152]",F_HR_createHyd.outerHyd+".e[154]",F_HR_createHyd.outerHyd+".e[156]",
    F_HR_createHyd.outerHyd+".e[158]",F_HR_createHyd.outerHyd+".e[160]",F_HR_createHyd.outerHyd+".e[162]",F_HR_createHyd.outerHyd+".e[164]",F_HR_createHyd.outerHyd+".e[166]",F_HR_createHyd.outerHyd+".e[168]",F_HR_createHyd.outerHyd+".e[170]",F_HR_createHyd.outerHyd+".e[172]",
    F_HR_createHyd.outerHyd+".e[174]",F_HR_createHyd.outerHyd+".e[176]",F_HR_createHyd.outerHyd+".e[178]",F_HR_createHyd.outerHyd+".e[180]",F_HR_createHyd.outerHyd+".e[182]",F_HR_createHyd.outerHyd+".e[184]",F_HR_createHyd.outerHyd+".e[186]",F_HR_createHyd.outerHyd+".e[188]",
    F_HR_createHyd.outerHyd+".e[190:191]",r=True)
    edgesToInt=cmds.polyExtrudeEdge(ch=True,keepFacesTogether=True,pvx=1.639127731,pvy=-1.639127731,pvz=1,d=1,twist=0,taper=1,offset=0,thickness=0,smoothingAngle=30)[0]
    cmds.setAttr(edgesToInt+".localTranslate",0,0,-FW_RM.hydHeightHR*0.8) 
    cmds.select(F_HR_createHyd.outerHyd)   #selecting created obj to freezetransform and delete history
    cmds.FreezeTransformations()
    cmds.DeleteHistory()
    F_HR_applyColor() #applying a different color to the outer obj
    #creating the inner cylinder 
    F_HR_createHyd.innerHyd=cmds.polyCylinder(n="HydraulicInner",h=FW_RM.hydHeightHR,r=innerRadius,sx=32,sy=1,sz=1,cuv=3,ch=False)[0]
    cmds.rotate(90,0,0)
    #moving pivot 
    cmds.move(0,0,FW_RM.hydHeightHR/2, F_HR_createHyd.innerHyd+'.scalePivot', F_HR_createHyd.innerHyd+'.rotatePivot',absolute=True)
    cmds.move(0,0,FW_RM.hydHeightHR*0.1)
    cmds.FreezeTransformations()       
    cmds.DeleteHistory()
    F_HR_hydSliderOFF() #disabling buttons
    
def F_HR_controlers(conectType):
    if conectType=="outer":
        nameCTRL="outerCTRL"
        z=-FW_RM.hydHeightHR+controlerDistance
        locatorSel="outerLocator1"
    if conectType=="inner":
        nameCTRL="innerCTRL"
        z=FW_RM.hydHeightHR+controlerDistance
        locatorSel="innerLocator1"
    cmds.curve(d=1,n=nameCTRL,p=[(-1,0,-1),(-3,0,-1),(-3,0,-2),(-5,0,0),(-3,0,2),(-3,0,1),
        (-1,0,1),(-1,0,3),(-2,0,3),(0,0,5),(2,0,3),(1,0,3),(1,0,3),(1,0,1),(3,0,1),(3,0,2),(5,0,0),
        (3,0,-2),(3,0,-1),(1,0,-1),(1,0,-3),(2,0,-3),(0,0,-5),(-2,0,-3),(-1,0,-3),(-1,0,-1)],
        k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25])
    cmds.scale(controlerScale,controlerScale,controlerScale,relative=True)
    cmds.rotate(0,90,90);           cmds.move(0,0,z);
    cmds.closeCurve(rpo=True);      cmds.select(cl=True)
    cmds.select(locatorSel);        cmds.select(nameCTRL,add=True);cmds.parent()

def F_HR_constraintsGen():
    outer=F_HR_createHyd.outerHyd; inner=F_HR_createHyd.innerHyd
    #creating locators 
    cmds.spaceLocator(n="outerLocator1");    cmds.move(0,0,-FW_RM.hydHeightHR/2)
    cmds.spaceLocator(n="innerLocator1");    cmds.move(0,0,(FW_RM.hydHeightHR/2)+FW_RM.hydHeightHR*0.1)
    F_HR_controlers("inner")
    F_HR_controlers("outer")
    cmds.select("outerCTRL")
    cmds.confirmDialog(m="Move the Arrow controlers -outerCTRL- and -innerCTRL-, \n do not choose the position moving the outer or inner objects", t="Warning")
    #selecting and applying aim and point constraints to the "pipes"
    cmds.select("innerLocator1");cmds.select(inner,add=True);cmds.pointConstraint(mo=False)
    cmds.select("outerLocator1");cmds.select(outer,add=True);cmds.pointConstraint(mo=False)
    cmds.select("innerLocator1");cmds.select(outer,add=True);cmds.aimConstraint(mo=True)
    cmds.select("outerLocator1");cmds.select(inner,add=True);cmds.aimConstraint(mo=True)
    FUI_endis([FW_RM.rigCBtnHR,FW_RM.rigJBtnHR],"button",False)
    FUI_endis([FW_RM.finalizeHR],"button",True)
    FUI_endis([FW_RM.outerNHR,FW_RM.innerNHR,FW_RM.loc1HR,FW_RM.loc2HR,FW_RM.jntO1NHR,FW_RM.jntO2NHR,FW_RM.jntI1NHR,FW_RM.jntI2NHR],"textFieldGrp",True)
    global rigType; rigType="const"; return rigType

def F_HR_jntsGen():
    outer=F_HR_createHyd.outerHyd; inner=F_HR_createHyd.innerHyd
    #creating outer Locators and moving 
    cmds.spaceLocator(n="outerLocator1");    cmds.move(0,0,-FW_RM.hydHeightHR/2)
    cmds.spaceLocator(n="outerLocator2");    cmds.move(0,0,FW_RM.hydHeightHR/2)
    cmds.select(cl=True)
    #creating inner Locators and moving 
    cmds.spaceLocator(n="innerLocator1");   cmds.move(0,0,(FW_RM.hydHeightHR/2)+FW_RM.hydHeightHR*0.1)
    cmds.spaceLocator(n="innerLocator2");   cmds.move(0,0,-(FW_RM.hydHeightHR/2)+FW_RM.hydHeightHR*0.1)
    cmds.select(cl=True)
    F_HR_controlers("inner") #call func to create controlers/handles
    F_HR_controlers("outer")
    cmds.confirmDialog(m="Move the Arrow controlers -outerCTRL- and -innerCTRL-, \n do not choose the position moving the outer or inner objects", t="Warning")
    cmds.joint(n="outerJoint1");cmds.matchTransform("outerJoint1","outerLocator1")    #Make joints
    cmds.select(cl=True)
    cmds.joint(n="outerJoint2");cmds.matchTransform("outerJoint2","outerLocator2")
    cmds.select(cl=True)
    cmds.parent("outerJoint2","outerJoint1");cmds.select(cl=True)
    cmds.joint(n="innerJoint1");cmds.matchTransform("innerJoint1","innerLocator1")
    cmds.select(cl=True)
    cmds.joint(n="innerJoint2");cmds.matchTransform("innerJoint2","innerLocator2")
    cmds.select(cl=True)
    cmds.parent("innerJoint2","innerJoint1")
    cmds.select(cl=True)
    cmds.delete("innerLocator2","outerLocator2")    #delete extra locators
    cmds.aimConstraint('outerJoint1', 'innerJoint1', w=1, mo=True)     #making Constrain
    cmds.aimConstraint('innerJoint1', 'outerJoint1', w=1, mo=True) 
    cmds.parentConstraint("outerJoint1",outer,mo=True)
    cmds.parentConstraint("innerJoint1",inner,mo=True)
    cmds.select("outerJoint1")
    cmds.parentConstraint("outerLocator1",'outerJoint1',mo=True,w=1,sr=["x","y","z"])
    cmds.parentConstraint("innerLocator1",'innerJoint1',mo=True,w=1,sr=["x","y","z"])
    cmds.button(FW_RM.rigCBtnHR,e=True,enable=False)
    cmds.button(FW_RM.rigJBtnHR,e=True,enable=False)
    cmds.button(FW_RM.finalizeHR,e=True,enable=True)
    FUI_endis([FW_RM.outerNHR,FW_RM.innerNHR,FW_RM.loc1HR,FW_RM.loc2HR,FW_RM.jntO1NHR,FW_RM.jntO2NHR,FW_RM.jntI1NHR,FW_RM.jntI2NHR],"textFieldGrp",True)
    global rigType; rigType="joint"; return rigType

def F_HR_pickingObj(obj_pick): #function to pick the first object
    selObj1=cmds.ls(sl=True)
    if not selObj1:
        cmds.confirmDialog(m="Please select one object")
        cmds.messageLine("No object selected")
    cmds.textFieldButtonGrp(obj_pick,edit=True, tx="".join(selObj1), buttonLabel='Selected')
    F_HR_Vpick()

def F_HR_pickingObj2(obj_pick): #function to pick the second object
    selObj2=cmds.ls(sl=True)
    if not selObj2:
        cmds.confirmDialog(m="Please select one object")
        cmds.messageLine("No object selected")
    cmds.textFieldButtonGrp(obj_pick,edit=True, tx=''.join(selObj2), buttonLabel='Selected')
    F_HR_Vpick()

def F_HR_rename(): #this function rename according with the user choice
    cmds.parent("outerLocator1",w=True);             cmds.parent("innerLocator1",w=True)
    cmds.delete("innerCTRL");cmds.delete("outerCTRL")
    if rigType=="const" or "joints":
        outerN=cmds.textFieldGrp(FW_RM.outerNHR,q=True,tx=True)
        innerN=cmds.textFieldGrp(FW_RM.innerNHR,q=True,tx=True)
        loc1N=cmds.textFieldGrp(FW_RM.loc1HR,q=True,tx=True)
        loc2N=cmds.textFieldGrp(FW_RM.loc2HR,q=True,tx=True)
        cmds.rename("outerLocator1",loc1N);             cmds.rename("innerLocator1",loc2N)
        cmds.rename(F_HR_createHyd.outerHyd,outerN);       cmds.rename(F_HR_createHyd.innerHyd,innerN)

    if rigType=="joint":
        jO1=cmds.textFieldGrp(FW_RM.jntO1NHR,q=True,tx=True)
        jO2=cmds.textFieldGrp(FW_RM.jntO2NHR,q=True,tx=True)
        jI1=cmds.textFieldGrp(FW_RM.jntI1NHR,q=True,tx=True)
        jI2=cmds.textFieldGrp(FW_RM.jntI2NHR,q=True,tx=True)
        cmds.rename("outerJoint1",jO1);                   cmds.rename("outerJoint2",jO2);                   
        cmds.rename("innerJoint1",jI1);                   cmds.rename("innerJoint2",jI2);   

def F_HR_finalize(): #function to finalize
    obj1=F_HR_Vpick.obj1; obj2=F_HR_Vpick.obj2
    #parenting the selected objects to the locators
    cmds.select(obj1);cmds.select("outerLocator1",add=True);cmds.parentConstraint(mo=True,w=1)
    cmds.select(obj2);cmds.select("innerLocator1",add=True);cmds.parentConstraint(mo=True,w=1)
    F_HR_rename()
    FUI_endis([FW_RM.outerNHR,FW_RM.innerNHR,FW_RM.loc1HR,FW_RM.loc2HR,FW_RM.jntO1NHR,FW_RM.jntO2NHR,FW_RM.jntI1NHR,FW_RM.jntI2NHR],"textFieldGrp",False)
    F_HR_hydSliderON()

def F_HR_Vpick(): #setting the selected objects to a variable.
    F_HR_Vpick.obj1=cmds.textFieldButtonGrp(FW_RM.obj1HR,q=True,tx=True)
    F_HR_Vpick.obj2=cmds.textFieldButtonGrp(FW_RM.obj2HR,q=True,tx=True)
    
def F_HR_applyColor(): #check if the tempBlinn exists; if not, apply a blinn to one obj only
    if cmds.objExists("tempBlinn")==True:
        cmds.select(F_HR_createHyd.outerHyd)
        cmds.hyperShade(assign="tempBlinn")
    else:    
        myBlinn = cmds.shadingNode('blinn',n="tempBlinn",asShader=True) 
        cmds.setAttr ((myBlinn+'.color'), 0.78,0.78,0.78,type="double3") 
        cmds.select(F_HR_createHyd.outerHyd)
        cmds.hyperShade(assign=myBlinn)

def F_HR_hydSliderON():
    #turn on first stage
    FUI_endis([FW_RM.sizeOptHR,FW_RM.tickOptHR,FW_RM.innerRtxtHR],"text",True)
    FUI_endis([FW_RM.hydHeightHR_,FW_RM.outerThickHR_,FW_RM.innerMultHR_],"floatSliderGrp",True)
    FUI_endis([FW_RM.createbtnHR],"button",True)
    #turn off second stage
    FUI_endis([FW_RM.moveLocHR,FW_RM.moveLocHR2,FW_RM.moveLocHR3],"text",False)
    FUI_endis([FW_RM.obj1HR,FW_RM.obj2HR],"textFieldButtonGrp",False)
    FUI_endis([FW_RM.finalizeHR,FW_RM.resetHR,FW_RM.rigCBtnHR,FW_RM.rigJBtnHR],"button",False)

def F_HR_hydSliderOFF():
    #turn off first stage
    FUI_endis([FW_RM.sizeOptHR,FW_RM.tickOptHR,FW_RM.innerRtxtHR],"text",False)
    FUI_endis([FW_RM.hydHeightHR_,FW_RM.outerThickHR_,FW_RM.innerMultHR_],"floatSliderGrp",False)
    FUI_endis([FW_RM.createbtnHR],"button",False)
    #turn on second stage 
    FUI_endis([FW_RM.moveLocHR,FW_RM.moveLocHR2,FW_RM.moveLocHR3],"text",True)
    FUI_endis([FW_RM.obj1HR,FW_RM.obj2HR],"textFieldButtonGrp",True)
    FUI_endis([FW_RM.rigCBtnHR,FW_RM.rigJBtnHR,FW_RM.resetHR],"button",True)

def F_HR_hydReset(): #function to reset the tool
    resetList=[F_HR_createHyd.outerHyd,F_HR_createHyd.innerHyd,"outerLocator1","innerLocator1","innerCTRL","outerCTRL","innerJoint1"]
    for item in resetList:
        if cmds.objExists(item):cmds.delete(item)
    F_HR_hydSliderON() #turning on buttons
    FUI_endis([FW_RM.outerNHR,FW_RM.innerNHR,FW_RM.loc1HR,FW_RM.loc2HR,FW_RM.jntO1NHR,FW_RM.jntO2NHR,FW_RM.jntI1NHR,FW_RM.jntI2NHR],"textFieldGrp",False)   

########################################
###       UTILITY FUNCTIONS          ###
########################################

"""
this function work enabling and disabling any UI item ex: button, text, sliders
use FUI_endis ( item = to variable item or a list of button to disable
                uiAttr = text, button, floatSliderGrp, etc
                onoff = pass True or False)                
"""
def FUI_endis(uiName,uiAttr,onoff):
    for i in uiName:
        if uiAttr == "text":cmds.text(i,edit=True,enable=onoff)
        if uiAttr == "textScrollList": cmds.textScrollList(i,edit=True,enable=onoff)    
        if uiAttr == "floatSliderGrp":cmds.floatSliderGrp(i,edit=True,enable=onoff)     
        if uiAttr == "textFieldButtonGrp": cmds.textFieldButtonGrp(i,edit=True,enable=onoff) 
        if uiAttr == "textFieldGrp":cmds.textFieldGrp(i,edit=True,enable=onoff)       
        if uiAttr == "intSliderGrp": cmds.intSliderGrp(i,edit=True,enable=onoff)      
        if uiAttr == "vis_text":  cmds.text(i,edit=True,visible=onoff)         
        if uiAttr == "button":
            if onoff==True:                 cmds.button(i,edit=True,enable=onoff,bgc=brightColor)
            if onoff==False:                cmds.button(i,edit=True,enable=onoff,bgc=disabledColor)
                

###################################
###   MAIN WINDOW FUNCTION      ###
###################################
def FW_RM():
    FW_RM.hydHeightHR=2.0;  FW_RM.outerThickHR=0.5;   FW_RM.innerMultHR=90
    #check if the windows exists to close it 
    if cmds.window(FW_RMName,q=True,exists=True):cmds.deleteUI(FW_RMName)

    cmds.window(FW_RMName,title="Rigging Menu",width=UIWidth,sizeable=0)
    column=cmds.columnLayout(adj=True)
    #main logo
    cmds.image(image=logopath,w=400,h=120,annotation=annoImage)
    #start tab layout
    form = cmds.formLayout()
    tabs = cmds.tabLayout(innerMarginWidth=15, innerMarginHeight=15)
    cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )
    #Tool 1 - Arm Rigger
    tool1 = cmds.rowColumnLayout(numberOfColumns=1,adj=True)
    cmds.text("Before anything, ensure your model is aiming at Positive Z",h=40)
    cmds.separator(w=UIWidth,h=20)
    FW_RM.jointsQ=cmds.intSliderGrp(l="Joint Count:",h=40,min=3,max=20,v=3,f=True,cc="F_AR_locNumber()",annotation=annoARJntCount)
    FW_RM.makeBtnAR=cmds.button(l="make Locators",w=UIWidth,h=40,c="F_AR_makeLoc()",annotation=annoARmakeloc)
    cmds.separator(w=UIWidth,h=20)
    FW_RM.resetBtnAR=cmds.button(l="Reset/Delete Locators",h=40,w=UIWidth,enable=False, c="F_AR_resetLoc()",annotation=annoARresetLoc)
    cmds.separator(w=UIWidth,h=20)
    FW_RM.msg001AR=cmds.text("Now place the locators in the order of root and children,\n When is done click on save locations",h=40,vis=False)
    cmds.separator(w=UIWidth,h=20)
    FW_RM.locListScrAR=cmds.textScrollList(h=40,nr=10, ams=False,append=locList, vis=False, shi=4,ai=True)
    FW_RM.msg002AR=cmds.text("Now click on create Joints",vis=False)
    FW_RM.jointsBtnAR=cmds.button(l='Make Joints',h=40,w=UIWidth, en=False,c="F_AR_makeJoints()",annotation=annoARmakeJnts)
    cmds.separator(w=UIWidth,h=20)
    #here i create a scrol list with joints to the user choose the IK 
    cmds.rowLayout(numberOfColumns=2)
    FW_RM.sjAR=cmds.text("Start Joint",width=UIWidth/2,en=False)
    FW_RM.eeAR=cmds.text("End Effector",width=UIWidth/2,en=False)
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns=2)
    FW_RM.jntsAR=cmds.textScrollList(nr=6,w=UIWidth/2,ams=False,append=JointList,ai=False, annotation=annoARstartIK)
    FW_RM.jntsAR1=cmds.textScrollList(nr=6,w=UIWidth/2,ams=False,append=JointList,ai=False,annotation=annoARendIK)
    cmds.setParent('..')
    cmds.separator(w=UIWidth,h=50)
    FW_RM.ikBtnAR=cmds.button(l="Create IK Handle",h=40,w=UIWidth, en=False,c="F_AR_ikHandle()",annotation=annoARcreateIK)
    cmds.separator(w=UIWidth,h=50)
    cmds.helpLine()
    cmds.setParent('..')
    #Tool 2 - Tread Maker
    tool2 = cmds.rowColumnLayout(numberOfColumns=1,adj=True)
    FW_RM.curveCheckTM=0
    # Step 1 - Confirms model orientation
    FW_RM.msgOrientTM=cmds.text("Please ensure your model is placed along the Z axis",wordWrap=1,align="center")
    FW_RM.confirmBtnTM=cmds.button(l="Confirm Z-Axis Orient",bgc=brightColor, h=60,c="F_TM_confirmAxis()",annotation=annoTMconfirmAxix)
    cmds.separator(h=20)    
    # Step 2 - Initialize
    FW_RM.msgInitTM=cmds.text("Makes two locators to set the FRONT and BACK of the tread",wordWrap=1,align="center",enable=False)  ## added variable
    FW_RM.initBtnTM=cmds.button(l="Initialize", enable=False,h=40,c="F_TM_initFunc()",annotation=annoTMmakeLoc) ## enable=False until confirmed
    # Step 3 - Generates a curve for the tread
    cmds.separator(h=20)
    FW_RM.msgCurveTM=cmds.text("Draws a curve according to the two locators",wordWrap=1,align="center",enable=False)  ## added variable
    FW_RM.makeCurveBtnTM=cmds.button(l="Make Tread Curve",h=40,c="F_TM_makeCurve()",enable=False,align="center",annotation=annoTMmakeCurve)
    # Step 4 - Defines the object used to model tread
    cmds.separator(h=20) ## Changed the formatting here
    FW_RM.objPickTM=cmds.text("OPTION 1: Select the OBJECT that will be spread around the tread",wordWrap=1,h=40,enable=False,align="center") ## set height instead of using extra lines
    FW_RM.objTextTM=cmds.textFieldButtonGrp(bl="Pick Tread OBJ",bc="F_TM_pickingObj()",enable=False, w=UIWidth,editable=False,h=40,annotation=annoTMpickObj)
    #gives the option to make a proxy object
    FW_RM.msgDefaultCubeTM=cmds.text("OPTION 2: Use a default cube",enable=False, align="center",h=40)
    FW_RM.makeDefaultCubeTM=cmds.button(l="Use Default Tread OBJ",c="F_TM_useDefault()",enable=False,h=40,annotation=annoTMdefaultOj)
    # Step 5 - Defines the number of instances of the object
    cmds.separator(h=20)
    FW_RM.makeTreadTM=cmds.button(l="Make Tread",enable=False, c="F_TM_makeTread()",h=40,annotation=annoTMmakeTread)
    FW_RM.objNumTM=cmds.text("Adjust distribuition of the object on the curve",enable=False,h=40) 
    FW_RM.copyNumTM=cmds.intSliderGrp(min=10,max=100,v=35,f=True, enable=False, cc="F_TM_numChange()",annotation=annoTMobjDistribuition)
    # Optional - Resets the tool
    cmds.separator(h=20)
    FW_RM.resetBtnTM=cmds.button(l="Reset",h=60,c="F_TM_resetLoc()",en=False,annotation=annoTMreset)
    FW_RM.resetAllTM=cmds.checkBox(label="Delete track geometry",enable=False,value=False,h=50,align="center",annotation=annoTMdelCheckbox)
    cmds.separator(w=UIWidth,h=50)
    cmds.helpLine()
    cmds.setParent('..')
    #Tool 3 - Wheel Maker
    tool3 = cmds.rowColumnLayout(numberOfColumns=1,adj=True)
    cmds.text(l="Please enter the wheels radius")
    FW_RM.wheelRad=cmds.floatSliderGrp(l='Wheel radius',f=True,value=1,min=1,max=100,h=30,sbm="What is the Wheel's radius",annotation=annoWSwheelRadius)
    cmds.separator(h=10)
    cmds.text(l="Select Diraction of General Movement")
    FW_RM.radioSel=cmds.radioButtonGrp(l="Choose Direction",h=40,la3=["X","Y","Z"],nrb=3,sl=True,annotation=annoWSdirection)
    cmds.button(l="Make Move Controller ",w=UIWidth,h=40,c="F_WM_arrowDrop()",annotation=annoWSarrowDrop)
    cmds.separator(h=10)
    cmds.text(l="Select the wheels you want to control together, and click the button")
    cmds.text(l="---> Wheels are gonna rotate on their X axis <---")
    cmds.separator(h=10)
    cmds.button(l="Rig ALL Wheels (Rotation)",w=UIWidth,h=40,c="F_WM_wheelSel()",annotation=annoWSwheelcontrols)
    cmds.separator(h=20)
    cmds.text(l="---> Now select front wheels for turning Rig  <---")
    cmds.separator(h=8)
    cmds.button(l="Front Wheels Side Turn",w=UIWidth,h=40,c="F_WM_FrontWheel()",annotation=annoWSwheelcontrols)
    cmds.separator(h=20)
    cmds.separator(w=UIWidth,h=20)
    cmds.button(l="Reset",w=UIWidth,h=40,c="F_WM_resetAll()",annotation=annoWSreset)
    cmds.separator(h=20)
    cmds.helpLine()
    cmds.setParent('..')
    #Tool 4 - Hydraulics Maker
    tool4 = cmds.rowColumnLayout(numberOfColumns=1,adj=True)
    #creates hydraulics objs based on selected size and thickness
    FW_RM.sizeOptHR=cmds.text("Set the size of the hydraulics",enable=True,ww=True,al="left") 
    FW_RM.hydHeightHR_=cmds.floatSliderGrp(l="Height/Distance", min=0.5,max=30,v=2,h=40,f=True, enable=True,annotation=annoHRMObj, cc="FW_RM.hydHeightHR=cmds.floatSliderGrp(FW_RM.hydHeightHR_,q=True, v=True)")
    FW_RM.tickOptHR=cmds.text("Set the thickness (Radius) of the hydraulics",enable=True,ww=True,al="left") 
    FW_RM.outerThickHR_=cmds.floatSliderGrp(l="Outer Thickness", min=0.1,max=30,v=0.5,h=40,f=True, enable=True,cc="FW_RM.outerThickHR=cmds.floatSliderGrp(FW_RM.outerThickHR_,q=True, v=True)",annotation=annoHRObjR)
    FW_RM.innerRtxtHR=cmds.text("Set the inner radius (percentage) relative to chosen outer radius",enable=True,ww=True,al="left") 
    FW_RM.innerMultHR_= cmds.floatSliderGrp(l="Inner Radius in %", min=10,max=95,v=90,h=40,f=True, enable=True,cc="FW_RM.innerMultHR=cmds.floatSliderGrp(FW_RM.innerMultHR_,q=True, v=True)",annotation=annoHRInnerR)
    FW_RM.createbtnHR=cmds.button(label="Create Hydraulics Objs",width=UIWidth,h=40,enable=True,c="F_HR_createHyd()",annotation=annoHRBtnCreate)
    cmds.separator(h=20)
    #button for choosing desired type of rig
    cmds.rowLayout(numberOfColumns=2)
    FW_RM.rigCBtnHR=cmds.button(label="Rig Contraints (only)",width=UIWidth/2,h=40,enable=False,c="F_HR_constraintsGen()",annotation=annoHRbtnRigC)
    FW_RM.rigJBtnHR=cmds.button(label="Rig Constraints AND Joints",width=UIWidth/2,h=40,enable=False,c="F_HR_jntsGen()",annotation=annoHRbtnRigJ)
    cmds.setParent('..')
    cmds.separator(h=20)
    #places locators for hydraulics
    FW_RM.moveLocHR=cmds.text("Move the Arrow Controllers to where the hydraulics will connect",enable=False,ww=True,al="left")
    FW_RM.moveLocHR2=cmds.text("Position outerCTRL to the first object connected to the base",enable=False,ww=True,al="left")
    #choosing the object where the hydraulics will be attached
    FW_RM.obj1HR=cmds.textFieldButtonGrp(en=True,ed=False,h=40,buttonLabel="---> Pick parent for base",bc="F_HR_pickingObj(FW_RM.obj1HR)",annotation=annoHRbtnPick1)
    FW_RM.moveLocHR3=cmds.text("Position Locator2 to the second object connected to the inner cylinder",enable=False,ww=True,al="left")
    FW_RM.obj2HR=cmds.textFieldButtonGrp(en=True,ed=False,h=40, buttonLabel="---> Pick parent for shaft",bc='F_HR_pickingObj2(FW_RM.obj2HR)',annotation=annoHRbtnPick2)
    cmds.separator(h=20)
    #buttons to finalize or reset
    cmds.rowLayout(numberOfColumns=2)
    FW_RM.finalizeHR=cmds.button(label="Finalize",en=False,width=UIWidth/2,h=40,c="F_HR_finalize()",annotation=annoHRbtnFinalize)
    FW_RM.resetHR=cmds.button(label="Reset All",enable=False,width=UIWidth/2,h=40,c="F_HR_hydReset()",annotation=annoHRbtnReset)
    cmds.setParent('..')
    cmds.separator(h=20)
    FW_RM.outerNHR=cmds.textFieldGrp(label="Hydraulics outer Name",text="hyd_Outer_1",enable=False,annotation=annoHRnaming)
    FW_RM.innerNHR=cmds.textFieldGrp(label="Hydraulics Inner Name",text="hyd_Inner_1",enable=False,annotation=annoHRnaming)
    FW_RM.loc1HR=cmds.textFieldGrp(label="Locator outer Name",text="outerLocator_1",enable=False,annotation=annoHRnaming)
    FW_RM.loc2HR=cmds.textFieldGrp(label="Locator inner Name",text="innerLocator_1",enable=False,annotation=annoHRnaming)
    FW_RM.jntO1NHR=cmds.textFieldGrp(label="Outer Joint 1 Name",text="outer_jnt_1",enable=False,annotation=annoHRnaming)
    FW_RM.jntO2NHR=cmds.textFieldGrp(label="Outer Joint 2 Name",text="outer_jnt_1_end",enable=False,annotation=annoHRnaming)
    FW_RM.jntI1NHR=cmds.textFieldGrp(label="Inner Joint 1 Name",text="inner_jnt_1",enable=False,annotation=annoHRnaming)
    FW_RM.jntI2NHR=cmds.textFieldGrp(label="Inner Joint 2 Name",text="inner_jnt_1_end",enable=False,annotation=annoHRnaming)
    cmds.separator(w=UIWidth,h=50)
    cmds.helpLine()
    cmds.setParent('..')
    #make tabs
    cmds.tabLayout( tabs, edit=True, tabLabel=((tool1, 'Arm Rigger'), (tool2, 'Tread Maker'), (tool3, 'Wheel Set Maker'), (tool4, 'Hydraulics Maker')) )
    #opens the window
    cmds.showWindow(FW_RMName)

###################################
###       ANNOTATIONS           ###
###################################

annoImage="This tool was developed by the Kiddos team"

###################################
###    ARM RIG  ANNOTATIONS     ###
###################################

annoARJntCount="How many joints do you need"
annoARmakeloc="Create locators and where the joints will be create"
annoARresetLoc="Reset only locators"
annoARmakeJnts="Create the joints exactly where the locators were placed"
annoARstartIK="Select the start joint for the IK"
annoARendIK="Select the end joint for the IK"
annoARcreateIK="Create IK within the start and end joints selected"

###################################
###   TREAD MAKER ANNOTATIONS   ###
###################################

annoTMconfirmAxix="Confirm your model is along Z axis"
annoTMmakeLoc=""
annoTMmakeCurve="The two locators should be placed where the tread will be created"
annoTMpickObj=""
annoTMdefaultOj="The tool will create an object to fill the tread"
annoTMmakeTread=""
annoTMobjDistribuition=""
annoTMreset="Click on the checkbox to reset ALL"
annoTMdelCheckbox="Click on the checkbox to reset ALL"

###################################
###   WHEEL SET ANNOTATIONS     ###
###################################

annoWSwheelcontrols="Create the controlers"
annoWSdirection="Set the direction of the controllers"
annoWSarrowDrop="Add an extra arrow controller to your scene"
annoWSwheelRadius="Let us know the wheel's radius"
annoWSreset="delete the itens you create"

###################################
###  HYDRAULICS ANNOTATIONS     ###
###################################

annoHRMObj="Distance/Height of the Hydraulics"
annoHRObjR="Radius/Thickness of the Hydraulics"
annoHRInnerR="The value of the slider is a percentage of the outer radius"
annoHRBtnCreate="Create Hydraulics based on the slider values"
annoHRbtnRigC="Build the rig with Contraints only"
annoHRbtnRigJ="Build the rig with Joints and Contraints"
annoHRbtnPick1="This will be the object where the base will be parented"
annoHRbtnPick2="This will be the object where the inner will be parented"
annoHRbtnFinalize="Check and change the names before you finalize"
annoHRbtnReset="Reset everything"
annoHRnaming="change the text field to rename"

#####################
###  MAIN SCRIPT  ###
#####################
image_url="https://static.wixstatic.com/media/f8a747_06486519162c4a8e9d300d71fa85aabb~mv2.png/v1/fill/w_400,h_118,al_c,enc_auto/f8a747_06486519162c4a8e9d300d71fa85aabb~mv2.png"
save_file="TeamKiddosLogo.jpg"
logopath=cmds.internalVar(upd=True)+"TeamKiddosLogo.jpg"
urllib.request.urlretrieve(image_url,logopath)

FW_RM()