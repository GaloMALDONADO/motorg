import numpy as np
import paths as lp
import robot_config as rconf
import mocap_config as mconf
from hqp.wrapper import Wrapper
from trajectory_extractor import References
import ucm
import plot_tools 
import csv
import indexes 
import plotTasks

coordinateNames = np.matrix(indexes.coordinates).squeeze()[:,1]
jointNames = np.matrix(indexes.joints).squeeze()[:,1]

def getTrials(i):
    participantName = mconf.traceurs_list[i]
    idxTraceur = mconf.traceurs_list.index(participantName)
    jump = np.load('./motions/'+participantName+'_jump.npy')
    fly = np.load('./motions/'+participantName+'_fly.npy')  
    land = np.load('./motions/'+participantName+'_land.npy')
    #trial = References(mconf.traceurs_list[idxTraceur])
    #trial.loadModel()
    #trial.display()
    #trial.getTrials()
    return jump,fly,land

def getRobot(i):
    participantName = mconf.traceurs_list[i]
    idxTraceur = mconf.traceurs_list.index(participantName)
    model_path = lp.models_path+'/'+participantName+'.osim'
    mesh_path = lp.mesh_path
    robot = Wrapper(model_path, mesh_path, participantName, True)
    return robot

''' *******************************  MAIN SCRIPT  ******************************* '''
# ------------------ Configuration ---------------
# LM : linear momentum
# AM : angular momentum
# V : gaze
#Jump
JumpLM = []; JumpAM = []; JumpV = []; JumpNC = [];
JLMmask = np.array([True,False,True,False,False,False])
JAMmask = np.array([False,False,False,False,True,False])
JVmask  = np.array([False,False,False,True,True,True])
JNCmask = np.array([False,False,False,True,False,False])
#Fly
FlyV = []; #FlyP = []; 
FVmask=np.array([False,False,False,True,True,True])
#Land
LandV = []; LandLM_abs = []; LandLM_stab = []; LandAM = []; LandM_stab = []; LandNC = []; LandBack = [];
LVmask  =   np.array([False, False, False, True, True, True])
LAMmask =   np.array([False, False, False, False, True,False])
LLM_Abs_mask =   np.array([False, False, True, False, False, False])
LLM_Stab_mask =   np.array([True, True, False, False, False, False])
LM_Stab_mask =   np.array([True, True, False, False, True, False])
nc_mask = np.array([False, False, False, True, False, False])
back_mask = np.array([False, False, False, True, True, True])

robots=[]



for i in xrange (len(mconf.traceurs_list)):

    (jump,fly,land) = getTrials(i)
    robots += [getRobot(i)]
    IDX_NECK = robots[i].model.getFrameId('neck')
    IDX_RHAND = robots[i].model.getFrameId('mtp_r')
    IDX_PELVIS = robots[i].model.getFrameId('ground_pelvis')
    IDX_BACK = robots[i].model.getFrameId('back')

    ''' *******************************  JUMP  ******************************* '''
    ''' Impulsion/Explosivness task is defined with the linear momentum rate in the Antero-Posterior and Vertical axis'''
    JumpLM += [ucm.ucmMomentum(robots[i], jump, JLMmask)]
    Vucm, Vcm, criteria = JumpLM[i].getUCMVariances()
    ''' Impulsion task is also defined with the angular momentum around the Antero-Posterior axis'''
    JumpAM += [ucm.ucmMomentum(robots[i], jump, JAMmask)]
    Vucm, Vcm, criteria = JumpAM[i].getUCMVariances()
    ''' Vision task to calculate the distance to the target '''
    JumpV += [ucm.ucmJoint(robots[i], jump, IDX_NECK, JVmask)]
    Vucm, Vcm, criteria = JumpV[i].getUCMVariances()
    #JumpNC += [ucm.ucmJoint(robots[i], jump, IDX_RHAND, JNCmask)]
    #Vucm, Vcm, criteria = JumpNC[i].getUCMVariances()

    ''' *******************************  FLY *******************************  '''
    ''' Vision task is defined with the joint flexion of the neck to track the target '''
    FlyV += [ucm.ucmJoint(robots[i], fly,IDX_NECK,FVmask)]
    Vucm, Vcm, criteria = FlyV[i].getUCMVariances()
    ''' Pelvis task is defined with the joint flexion of the pelvis '''
    #Pelvis += [ucm.ucmJoint(robots[i], fly, 
    #                        IDX_PELVIS, 
    #                        mask=np.array([False,False,False,True,False,False]))]
    #Vucm, Vcm, criteria = Pelvis[i].getUCMVariances()
    ''' Preparation to land is defined with the variance of joints before IC with the ground'''
    #TODO

    ''' *******************************  LAND  ******************************* '''
    ''' Damping and reducing GRFs task is defined with the linear momentum '''
    LandLM_abs += [ucm.ucmMomentum(robots[i], land, LLM_Abs_mask)]
    Vucm, Vcm, criteria = LandLM_abs[i].getUCMVariances()
    LandLM_stab += [ucm.ucmMomentum(robots[i], land, LM_Stab_mask)]
    Vucm, Vcm, criteria = LandLM_stab[i].getUCMVariances()
    LandM_stab += [ucm.ucmMomentum(robots[i], land, LLM_Stab_mask)]
    Vucm, Vcm, criteria = LandM_stab[i].getUCMVariances()
    ''' Angular stability task is also defined with the ang momentum around Antero-Posterior axis'''
    LandAM += [ucm.ucmMomentum(robots[i], land, LAMmask)]
    Vucm, Vcm, criteria = LandAM[i].getUCMVariances()
    ''' The head is stabilized during landing throught neck flexion'''
    LandV += [ucm.ucmJoint(robots[i], land, IDX_NECK, LVmask)]
    Vucm, Vcm, criteria = LandV[i].getUCMVariances()
    # not controlled task
    #LandNC += [ucm.ucmMomentum(robots[i], land, nc_mask)]
    #Vucm, Vcm, criteria = LandNC[i].getUCMVariances()
    # back
    LandBack += [ucm.ucmMomentum(robots[i], land, back_mask)]
    Vucm, Vcm, criteria = LandBack[i].getUCMVariances()
    ''' Landing stiffness through the Z displacement of the center of mass '''
    #Stiffness += [ucm.ucmCoM(robots[i], land, mask=np.array([False,False,True]))]
    #Vucm, Vcm, criteria = Stiffness[i].getUCMVariances()
    ''' Stability task is defined with the center of mass in X and Y'''
    #StabilityCM += [ucm.ucmCoM(robots[i], land, mask=np.array([True,True,False]))]
    #Vucm, Vcm, criteria = StabilityCM[i].getUCMVariances()


#animate robot with mean configurations !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
#plotNCJ = plotTasks.Joint(JumpNC,'rmtp')
plotVisionJ = plotTasks.Joint(JumpV,'neck_flexion')
plotLinMomJ = plotTasks.CentroidalMomentum(JumpLM,'Impulsion through Linear Momentum (A-P and V) during Jump')
plotAngMomJ = plotTasks.CentroidalMomentum(JumpAM, 'Angular Momentum (around M-L) contribution during Jump')

plotVisionF = plotTasks.Joint(FlyV,'neck_flexion')

plotLinMomL_stab = plotTasks.CentroidalMomentum(LandLM_stab,'Linear Momentum stability (A-P and M-L) task during Landing')
plotLinMomL_abs = plotTasks.CentroidalMomentum(LandLM_abs, 'Linear Momentum absorption (V) task during Landing')
plotAngMomL = plotTasks.CentroidalMomentum(LandAM, 'Angular Momentum (around M-L) contribution to stability during Landing')
plotMomL_stab = plotTasks.CentroidalMomentum(LandM_stab, 'Stability with Momentum (Linear M-L and A-P plus Angular around M-L)')
plotBackL = plotTasks.Joint(LandBack,'back_flexion')
plotVisionL = plotTasks.Joint(LandV,'neck_flexion')
#plotNC = plotTasks.CentroidalMomentum(LandNC)





''' *******************************  Prepare files for R  ******************************* '''
nsubjects = 5; nphases = 3;

''' Impulsion Phase '''
ntasks = 3
subjects = np.matrix(np.repeat(np.linspace(1,5,5), ntasks*nphases)).T 
phaseFactor = np.matrix([  10, 10, 10, 50, 50, 50, 90, 90, 90]*nsubjects).T
taskFactor =  np.matrix([1,2,3]*nsubjects*nphases).T

VU = []; VO=[]; C=[];
for i in xrange (len(mconf.traceurs_list)):
    C += [
        JumpV[i].criteria[10],
        JumpLM[i].criteria[10],
        JumpAM[i].criteria[10],
        JumpV[i].criteria[50],
        JumpLM[i].criteria[50],
        JumpAM[i].criteria[50],
        JumpV[i].criteria[90],
        JumpLM[i].criteria[90],
        JumpAM[i].criteria[90],
    ]

np.savetxt("TableCriteriaImpulse.csv", 
           np.hstack([subjects,phaseFactor,taskFactor,np.matrix(C).T]), 
           delimiter=",")


''' Landing Phase '''
ntasks = 4
subjects = np.matrix(np.repeat(np.linspace(1,5,5), ntasks*nphases)).T 
phaseFactor = np.matrix([  1, 1, 1, 1, 50, 50, 50, 50, 100, 100, 100, 100]*nsubjects).T
taskFactor =  np.matrix([1,2,3,4]*nsubjects*nphases).T

VU = []; VO=[]; C=[];
for i in xrange (len(mconf.traceurs_list)):
    C += [Damping[i].criteria[10],
          Stiffness[i].criteria[10],
          StabilityCM[i].criteria[10],
          StabilityAM[i].criteria[10],          
          Damping[i].criteria[55],
          Stiffness[i].criteria[55],
          StabilityCM[i].criteria[55],
          StabilityAM[i].criteria[55],
          Damping[i].criteria[99],
          Stiffness[i].criteria[99],
          StabilityCM[i].criteria[99],
          StabilityAM[i].criteria[99]]


np.savetxt("TableVucmLand.csv", 
           np.hstack([subjects,phaseFactor,taskFactor,np.matrix(VU).T]), 
           delimiter=",")
np.savetxt("TableVortLand.csv", 
           np.hstack([subjects,phaseFactor,taskFactor,np.matrix(VO).T]), 
           delimiter=",")
np.savetxt("TableCriteriaLand.csv", 
           np.hstack([subjects,phaseFactor,taskFactor,np.matrix(C).T]), 
           delimiter=",")



''' Fly Phase '''
ntasks = 2
subjects = np.matrix(np.repeat(np.linspace(1,5,5), ntasks*nphases)).T 
phaseFactor = np.matrix([  1, 1, 50, 50, 100, 100]*nsubjects).T
taskFactor =  np.matrix([1,2]*nsubjects*nphases).T

VU = []; VO=[]; C=[];
for i in xrange (len(mconf.traceurs_list)):
    VU += [Vision[i].Vucm[0],
           Pelvis[i].Vucm[0],
           Vision[i].Vucm[50],
           Pelvis[i].Vucm[50],
           Vision[i].Vucm[99],
           Pelvis[i].Vucm[99]]

    VO += [Vision[i].Vcm[0],
           Pelvis[i].Vcm[0],
           Vision[i].Vcm[50],
           Pelvis[i].Vcm[50],
           Vision[i].Vcm[99],
           Pelvis[i].Vcm[99]]

    C += [Vision[i].criteria[0],
          Pelvis[i].criteria[0],
          Vision[i].criteria[50],
          Pelvis[i].criteria[50],
          Vision[i].criteria[99],
          Pelvis[i].criteria[99]]


np.savetxt("TableVucmFly.csv", 
           np.hstack([subjects,phaseFactor,taskFactor,np.matrix(VU).T]), 
           delimiter=",")
np.savetxt("TableVortFly.csv", 
           np.hstack([subjects,phaseFactor,taskFactor,np.matrix(VO).T]), 
           delimiter=",")
np.savetxt("TableCriteriaFly.csv", 
           np.hstack([subjects,phaseFactor,taskFactor,np.matrix(C).T]), 
           delimiter=",")

