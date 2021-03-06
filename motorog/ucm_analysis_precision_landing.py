''' 
Uncontrolled Manifold Study of Precision Landing
'''
import numpy as np
import paths as lp
import robot_config as rconf
import mocap_config as mconf
from hqp.wrapper import Wrapper
from hqp.viewer_utils import Viewer
from trajectory_extractor import References
import ucm
import csv


def getTrials(i):
    participantName = mconf.traceurs_list[i]
    idxTraceur = mconf.traceurs_list.index(participantName)
    jump = np.load('./motions/'+participantName+'_jump.npy')    
    fly = np.load('./motions/'+participantName+'_fly.npy')    
    land = np.load('./motions/'+participantName+'_land.npy')    
    return jump,fly,land

def loadRobot(robot,name):
    participantName = mconf.traceurs_list[i]
    viewer = Viewer(name, robot)
    viewer.display(robot.q,name)

def getRobot(i, load=False):
    participantName = mconf.traceurs_list[i]
    idxTraceur = mconf.traceurs_list.index(participantName)
    model_path = lp.models_path+'/'+participantName+'.osim'
    mesh_path = lp.mesh_path
    robot = Wrapper(model_path, mesh_path, participantName, True)
    if load is True:
        loadRobot(robot,participantName)
    return robot


''' *******************************  MAIN SCRIPT  ******************************* '''
robots=[]

# ------------------ Configuration ---------------
# LM : linear momentum
# AM : angular momentum
# V : gaze
# ------------------------------------------------
#Jump
JumpLM = []; JumpAM = []; JumpV = [];
JLMmask = np.array([False,False,True,False,False,False]) #linear momentum
JAMmask = np.array([False,False,False,False,True,False]) #angular momentum
JVmask  = np.array([False,False,False,True,False,False]) #vision
#Fly
FlyV = []; 
FVmask=np.array([False,False,False,True,False,False]) #vision
#Land
LandV = []; LandLM = []; LandAM = [];
LLMmask =   np.array([True,True,True,True,True,True]) #linear momentum
LVmask  =   np.array([False,False,False,True,False,False]) #vision
LAMmask =   np.array([False,False,False,False,True,False]) #angular momentum


for i in xrange (len(mconf.traceurs_list)):
    (jump,fly,land) = getTrials(i)
    robots += [getRobot(i)]
    IDX_NECK = robots[i].model.getFrameId('neck')

    ''' *******************************  JUMP  ******************************* '''
    ''' Impulsion/Explosivness task is defined with the linear momentum rate in the Antero-Posterior and Vertical axis'''
    JumpLM += [ucm.ucmMomentum(robots[i], jump, JLMmask)]
    JumpLM[i].getUCMVariances()
    ''' Impulsion task is also defined with the angular momentum around the Antero-Posterior axis'''
    JumpAM += [ucm.ucmMomentum(robots[i], jump, JAMmask)]
    JumpAM[i].getUCMVariances()
    ''' Vision task to calculate the distance to the target '''
    JumpV += [ucm.ucmJoint(robots[i], jump, IDX_NECK, JVmask)]
    JumpV[i].getUCMVariances()


    ''' *******************************  FLY *******************************  '''
    ''' Vision task is defined with the joint flexion of the neck to track the target '''
    FlyV += [ucm.ucmJoint(robots[i], fly,IDX_NECK,FVmask)]
    FlyV[i].getUCMVariances()

    ''' Preparation to land is defined with the variance of joints before IC with the ground'''
    #TODO

    ''' *******************************  LAND  ******************************* '''
    ''' Damping and reducing GRFs task is defined with the linear momentum '''
    LandLM += [ucm.ucmMomentum(robots[i], land, LLMmask)]
    LandLM[i].getUCMVariances()
    ''' Angular stability task is also defined with the ang momentum around Antero-Posterior axis'''
    LandAM += [ucm.ucmMomentum(robots[i], land, LAMmask)]
    LandAM[i].getUCMVariances()
    ''' The head is stabilized during landing throught neck flexion'''
    LandV += [ucm.ucmJoint(robots[i], land, IDX_NECK, LVmask)]
    LandV[i].getUCMVariances()


# -- plot --
# -- express force in ground --
# 

# -------------------------------------- Save Workspace --------------------------------------
JLM={'Vucm':[],'Vort':[],'Criteria':[]}
JAM={'Vucm':[],'Vort':[],'Criteria':[]}
JV={'Vucm':[],'Vort':[],'Criteria':[]}
FV={'Vucm':[],'Vort':[],'Criteria':[]}
LLM={'Vucm':[],'Vort':[],'Criteria':[]}
LAM={'Vucm':[],'Vort':[],'Criteria':[]}
LV={'Vucm':[],'Vort':[],'Criteria':[]}

for i in xrange (len(mconf.traceurs_list)):
    JLM['Vucm'] +=      [JumpLM[i].Vucm]
    JLM['Vort'] +=      [JumpLM[i].Vcm]
    JLM['Criteria'] +=  [JumpLM[i].criteria]
    JAM['Vucm'] +=      [JumpAM[i].Vucm]
    JAM['Vort'] +=      [JumpAM[i].Vcm]
    JAM['Criteria'] +=  [JumpAM[i].criteria]
    JV['Vucm'] +=       [JumpV[i].Vucm]
    JV['Vort'] +=       [JumpV[i].Vcm]
    JV['Criteria'] +=   [JumpV[i].criteria]

    FV['Vucm'] +=       [FlyV[i].Vucm]
    FV['Vort'] +=       [FlyV[i].Vcm]
    FV['Criteria'] +=   [FlyV[i].criteria]

    LLM['Vucm'] +=      [LandLM[i].Vucm]
    LLM['Vort'] +=      [LandLM[i].Vcm]
    LLM['Criteria'] +=  [LandLM[i].criteria]
    LAM['Vucm'] +=      [LandAM[i].Vucm]
    LAM['Vort'] +=      [LandAM[i].Vcm]
    LAM['Criteria'] +=  [LandAM[i].criteria]
    LV['Vucm'] +=       [LandV[i].Vucm]
    LV['Vort'] +=       [LandV[i].Vcm]
    LV['Criteria'] +=   [LandV[i].criteria]



jump = {'LinearMomentum':[],'AngularMomentum':[],'Vision':[]}
jump['LinearMomentum'].append(JLM)
jump['AngularMomentum'].append(JAM)
jump['Vision'].append(JV)

fly  = {'LinearMomentum':[],'AngularMomentum':[],'Vision':[]}
fly['Vision'].append(FV)

land = {'LinearMomentum':[],'AngularMomentum':[],'Vision':[]}
land['LinearMomentum'].append(LLM)
land['AngularMomentum'].append(LAM)
land['Vision'].append(LV)

np.save('./ucm_analysis/jump.npy',jump)
np.save('./ucm_analysis/fly.npy',fly)
np.save('./ucm_analysis/land',land)


# --------------- Save files for R -------------------------------------
