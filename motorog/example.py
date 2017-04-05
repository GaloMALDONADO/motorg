import pinocchio as se3
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
from hqp.viewer_utils import Viewer

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
    robot.com(robot.q)
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
FlyV = []; FlyLM = [];#FlyP = []; 
FVmask=np.array([False,False,False,True,True,True])
FLMmask = np.array([True,True,True,False,False,False])
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


participantsNo = len(mconf.traceurs_list)
for i in xrange (participantsNo):

    (jump,fly,land) = getTrials(i)
    robots += [getRobot(i)]
    # coefficient of force normalization for inter-subject comparison 
    # BW^{-1}
    KF = 1./(robots[i].data.mass[0] * 9.81)
    # BW^{-1} * H^{-1}
    # coefficient of torque normalization for inter-subject comparison 
    KT = 1./(rconf.heights[i] * robots[i].data.mass[0] * 9.81)
    # get frame indexes of interest for the UCM analysis
    IDX_NECK = robots[i].model.getFrameId('neck')
    IDX_RHAND = robots[i].model.getFrameId('mtp_r')
    IDX_PELVIS = robots[i].model.getFrameId('ground_pelvis')
    IDX_BACK = robots[i].model.getFrameId('back')

    ''' *******************************  JUMP  ******************************* '''
    ''' Impulsion/Explosivness task is defined with the linear momentum rate in the Antero-Posterior and Vertical axis'''
    JumpLM += [ucm.ucmMomentum(robots[i], jump, JLMmask, KF, 1)]
    Vucm, Vcm, criteria = JumpLM[i].getUCMVariances()
    ''' Impulsion task is also defined with the angular momentum around the Antero-Posterior axis'''
    JumpAM += [ucm.ucmMomentum(robots[i], jump, JAMmask, 1, KT)]
    Vucm, Vcm, criteria = JumpAM[i].getUCMVariances()
    ''' Vision task to calculate the distance to the target '''
    JumpV += [ucm.ucmJoint(robots[i], jump, IDX_NECK, JVmask)]
    Vucm, Vcm, criteria = JumpV[i].getUCMVariances()
    #JumpNC += [ucm.ucmJoint(robots[i], jump, IDX_RHAND, JNCmask)]
    #Vucm, Vcm, criteria = JumpNC[i].getUCMVariances()

    ''' *******************************  FLY *******************************  '''
    ''' Vision task is defined with the joint flexion of the neck to track the target '''
    FlyV += [ucm.ucmJoint(robots[i], fly, IDX_NECK,FVmask)]
    Vucm, Vcm, criteria = FlyV[i].getUCMVariances()
    FlyLM += [ucm.ucmMomentum(robots[i], fly, FLMmask)]
    Vucm, Vcm, criteria = FlyLM[i].getUCMVariances()
    ''' Pelvis task is defined with the joint flexion of the pelvis '''
    #Pelvis += [ucm.ucmJoint(robots[i], fly, 
    #                        IDX_PELVIS, 
    #                        mask=np.array([False,False,False,True,False,False]))]
    #Vucm, Vcm, criteria = Pelvis[i].getUCMVariances()
    ''' Preparation to land is defined with the variance of joints before IC with the ground'''
    #TODO

    ''' *******************************  LAND  ******************************* '''
    ''' Damping and reducing GRFs task is defined with the linear momentum '''
    LandLM_abs += [ucm.ucmMomentum(robots[i], land, LLM_Abs_mask, 1, KF)]
    Vucm, Vcm, criteria = LandLM_abs[i].getUCMVariances()
    LandLM_stab += [ucm.ucmMomentum(robots[i], land, LLM_Stab_mask, 1, KF)]
    Vucm, Vcm, criteria = LandLM_stab[i].getUCMVariances()
    LandM_stab += [ucm.ucmMomentum(robots[i], land, LM_Stab_mask, 1, KF)]
    Vucm, Vcm, criteria = LandM_stab[i].getUCMVariances()
    ''' Angular stability task is also defined with the ang momentum around Antero-Posterior axis'''
    LandAM += [ucm.ucmMomentum(robots[i], land, LAMmask, 1, KT)]
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
plotLinMomF = plotTasks.CentroidalMomentum(FlyLM,'Fly Linear Momentum')

plotLinMomL_stab = plotTasks.CentroidalMomentum(LandLM_stab,'Linear Momentum stability (A-P and M-L) task during Landing')
plotLinMomL_abs = plotTasks.CentroidalMomentum(LandLM_abs, 'Linear Momentum absorption (V) task during Landing')
plotAngMomL = plotTasks.CentroidalMomentum(LandAM, 'Angular Momentum (around M-L) contribution to stability during Landing')
plotMomL_stab = plotTasks.CentroidalMomentum(LandM_stab, 'Stability with Momentum (Linear M-L and A-P plus Angular around M-L)')
plotBackL = plotTasks.Joint(LandBack,'back_flexion')
plotVisionL = plotTasks.Joint(LandV,'neck_flexion')
#plotNC = plotTasks.CentroidalMomentum(LandNC)



''' *******************************  Prepare files for R  ******************************* '''
nsubjects = 5;

''' Impulsion Phase '''
nphases = 4;
ntasks = 2
subjects = np.matrix(np.repeat(np.linspace(1,5,5), ntasks*nphases)).T 
#j: 0(start)  40 60(A-P_F, AM_UCM) 70(BW) 100(end)
phaseFactor = np.matrix([  0, 0, 40, 40,  70, 70, 99, 99]*nsubjects).T
taskFactor =  np.matrix([1,2]*nsubjects*nphases).T

C=[];
for i in xrange (len(mconf.traceurs_list)):
    C += [
        #JumpV[i].criteria[10],
        JumpLM[i].criteria[0],
        JumpAM[i].criteria[0],
        #JumpV[i].criteria[50],
        JumpLM[i].criteria[40],
        JumpAM[i].criteria[40],
        #JumpV[i].criteria[90],
        JumpLM[i].criteria[70],
        JumpAM[i].criteria[70],
        JumpLM[i].criteria[99],
        JumpAM[i].criteria[99],
    ]

np.savetxt("TableCriteriaImpulse.csv", 
           np.hstack([subjects,phaseFactor,taskFactor,np.matrix(C).T]), 
           delimiter=",")

''' Fly Phase  '''
nphases =3
ntasks = 1
subjects = np.matrix(np.repeat(np.linspace(1,5,5), ntasks*nphases)).T 
phaseFactor = np.matrix([  10, 50, 90]*nsubjects).T
taskFactor =  np.matrix([1]*nsubjects*nphases).T

C=[];
for i in xrange (len(mconf.traceurs_list)):
    C += [
        FlyV[i].criteria[10],
        FlyV[i].criteria[50],
        FlyV[i].criteria[90],
    ]

np.savetxt("TableCriteriaFly.csv", 
           np.hstack([subjects,phaseFactor,taskFactor,np.matrix(C).T]), 
           delimiter=",")



''' Landing Phase '''
nphases = 4
ntasks = 3
subjects = np.matrix(np.repeat(np.linspace(1,5,5), ntasks*nphases)).T 
#l: 5(start) 20(maxForce) 40(lowerForce/stab) 100(end) 
phaseFactor = np.matrix([  5, 5, 5, 20, 20, 20, 40, 40, 40, 99, 99, 99]*nsubjects).T
taskFactor =  np.matrix([1,2,3]*nsubjects*nphases).T

C=[];
for i in xrange (len(mconf.traceurs_list)):
    C += [
        #LandV[i].criteria[10],
        LandLM_abs[i].criteria[5],
        LandLM_stab[i].criteria[5],
        LandAM[i].criteria[5],
        #LandV[i].criteria[50],
        LandLM_abs[i].criteria[20],
        LandLM_stab[i].criteria[20],
        LandAM[i].criteria[20],
        #LandV[i].criteria[90],
        LandLM_abs[i].criteria[40],
        LandLM_stab[i].criteria[40],
        LandAM[i].criteria[40],
        LandLM_abs[i].criteria[99],
        LandLM_stab[i].criteria[99],
        LandAM[i].criteria[99],
    ]

np.savetxt("TableCriteriaLand.csv", 
           np.hstack([subjects,phaseFactor,taskFactor,np.matrix(C).T]), 
           delimiter=",")


''' Display '''

avatar0 = robots[0]
avatar1 = robots[1]
avatar2 = robots[2]
avatar3 = robots[3]
avatar4 = robots[4]

#launch with gepetto viewer
viewer = Viewer('avatar viewer0',avatar0)
viewer.addRobot(avatar1)
viewer.addRobot(avatar2)
viewer.addRobot(avatar3)
viewer.addRobot(avatar4)
viewer.viewer.gui.setBackgroundColor1(viewer.windowID,(255,255,255,0))

viewer.viewer.gui.setVisibility('world/Melvin/floor','OFF')
viewer.viewer.gui.setVisibility('world/Cyril/floor','OFF')
viewer.viewer.gui.setVisibility('world/Michael/floor','OFF')
viewer.viewer.gui.setVisibility('world/Lucas/floor','OFF')
#viewer.viewer.gui.setVisibility('world/Yoan/floor','OFF')

task = JumpV
jq=[]
for i in xrange (participantsNo):
    jq+=[task[i].q_mean.squeeze()]
jq_mean =  np.mean(np.array(jq),0)

task = FlyV
fq=[]
for i in xrange (participantsNo):
    fq+=[task[i].q_mean.squeeze()]
fq_mean =  np.mean(np.array(fq),0)

task = LandV
lq=[]
for i in xrange (participantsNo):
    lq+=[task[i].q_mean.squeeze()]
lq_mean =  np.mean(np.array(lq),0)




#viewer.display(lq_mean[99],avatar.name) 

jump0 = jump[0]['pinocchio_data']
land0 = land[0]['pinocchio_data']
jump1 = jump[1]['pinocchio_data']
land1 = land[1]['pinocchio_data']
jump2 = jump[2]['pinocchio_data']
land2 = land[2]['pinocchio_data']
jump3 = jump[3]['pinocchio_data']
land3 = land[3]['pinocchio_data']
jump4 = jump[4]['pinocchio_data']
land4 = land[4]['pinocchio_data']

viewer.display(jump0[0],avatar0.name) 
viewer.display(jump1[0],avatar1.name) 
viewer.display(jump2[0],avatar2.name) 
viewer.display(jump3[0],avatar3.name) 

viewer.display(land4[5],avatar4.name)




''' ***************** MOMENTUM IN PARKOUR STUDY ****************** '''
import matplotlib.pyplot as plt
''' Impulsion Phase '''
nphases = 4;
ntasks = 2
coordinates = 25
subjects = np.matrix(np.repeat(np.linspace(1,5,5), ntasks*nphases*coordinates)).T 
#j: 0(start)  40 60(A-P_F, AM_UCM) 70(BW) 100(end)
phaseFactor = np.matrix([  0, 0, 40, 40,  70, 70, 99, 99]*nsubjects*coordinates).T
taskFactor =  np.matrix([1,2]*nsubjects*nphases*coordinates).T
coordinateFactor = np.matrix(range(coordinates)*nsubjects*nphases*ntasks).T

Aj=[];
for i in xrange (len(mconf.traceurs_list)):
    Aj += [np.sum(JumpLM[i].contribution[0],1)]
    Aj += [JumpAM[i].contribution[0]]
    Aj += [np.sum(JumpLM[i].contribution[40],1)]
    Aj += [JumpAM[i].contribution[40]]
    Aj += [np.sum(JumpLM[i].contribution[70],1)]
    Aj += [JumpAM[i].contribution[70]]
    Aj += [np.sum(JumpLM[i].contribution[99],1)]
    Aj += [JumpAM[i].contribution[99]]
    
M=np.matrix(Aj).A1
np.savetxt("TableMomentaJump.csv", 
           np.hstack([subjects,phaseFactor,taskFactor,coordinateFactor,np.matrix(M).T]), 
           delimiter=",")


#means and std
# linear momentum
data5 = []; data40 = []; data70 = []; data99 = [];
for i in xrange (len(mconf.traceurs_list)):
    data5 += [np.sum(JumpLM[i].contribution[5],1)]
    data40 += [np.sum(JumpLM[i].contribution[40],1)]
    data70 += [np.sum(JumpLM[i].contribution[70],1)]
    data99 += [np.sum(JumpLM[i].contribution[99],1)]

table_JumpLM = np.matrix([np.mean(np.matrix(data5), 0).A1, 
                          np.mean(np.matrix(data40), 0).A1, 
                          np.mean(np.matrix(data70), 0).A1, 
                          np.mean(np.matrix(data99), 0).A1])
table_JumpLM_std = np.matrix([np.std(np.matrix(data5), 0).A1, 
                              np.std(np.matrix(data40), 0).A1, 
                              np.std(np.matrix(data70), 0).A1, 
                              np.std(np.matrix(data99), 0).A1])
np.savetxt("means/JumpLM.csv", table_JumpLM, delimiter=",")
np.savetxt("std/JumpLM.csv", table_JumpLM_std, delimiter=",")

# angular momentum
data5 = []; data40 = []; data70 = []; data99 = [];
for i in xrange (len(mconf.traceurs_list)):
    data5 = JumpAM[i].contribution[5]
    data40 = JumpAM[i].contribution[40] 
    data70 = JumpAM[i].contribution[70] 
    data99 = JumpAM[i].contribution[99] 

table_JumpAM = np.matrix([np.mean(np.matrix(data5).T, 1).A1, 
                          np.mean(np.matrix(data40).T, 1).A1, 
                          np.mean(np.matrix(data70).T, 1).A1, 
                          np.mean(np.matrix(data99).T, 1).A1])
table_JumpAM_std = np.matrix([np.std(np.matrix(data5).T, 1).A1, 
                              np.std(np.matrix(data40).T, 1).A1, 
                              np.std(np.matrix(data70).T, 1).A1, 
                              np.std(np.matrix(data99).T, 1).A1])
np.savetxt("means/JumpAM.csv", table_JumpAM, delimiter=",")
np.savetxt("std/JumpAM.csv", table_JumpAM_std, delimiter=",")





''' Landing Phase '''
nphases = 4
ntasks = 3
coordinates = 25
subjects = np.matrix(np.repeat(np.linspace(1,5,5), ntasks*nphases*coordinates)).T 
#l: 5(start) 20(maxForce) 40(lowerForce/stab) 100(end) 
phaseFactor = np.matrix([  5, 5, 5, 20, 20, 20, 40, 40, 40, 99, 99, 99]*nsubjects*coordinates).T
taskFactor =  np.matrix([1,2,3]*nsubjects*nphases*coordinates).T
coordinateFactor = np.matrix(range(coordinates)*nsubjects*nphases*ntasks).T


y = JumpAM[0].contribution[0]
names=jointNames[1:].A1
N = len(y)
x = range(N)
width = 1/1.5
plt.bar(x, y, color="blue", align='center')
plt.xticks(x, names, rotation='vertical')

def getMomentumData(task, t):
    # Aij
    # i task index
    # j qdot index
    idim, jdim = task.JTask[t].shape
    Aj = np.zeros(jdim)
    if idim == 1 :
        for j in xrange(jdim):
            Aj[j] = task.contribution[t].A1[j] * task.dq_mean[t].A1[j]
        return Aj
    else :
        for j in xrange(jdim):
            for i in xrange(idim):
                Aj[j] += task.JTask[t][i].A1[j] * task.dq_mean[t].A1[j]
        return Aj


Aj=[]
for i in xrange (len(mconf.traceurs_list)):
    Aj += [LandLM_abs[i].contribution[5]]
    Aj += [np.sum(LandLM_stab[i].contribution[5],1)]
    Aj += [LandAM[i].contribution[5]]
    Aj += [LandLM_abs[i].contribution[20]]
    Aj += [np.sum(LandLM_stab[i].contribution[20],1)]
    Aj += [LandAM[i].contribution[20]]
    Aj += [LandLM_abs[i].contribution[40]]
    Aj += [np.sum(LandLM_stab[i].contribution[40],1)]
    Aj += [LandAM[i].contribution[40]]
    Aj += [LandLM_abs[i].contribution[99]]
    Aj += [np.sum(LandLM_stab[i].contribution[99],1)]
    Aj += [LandAM[i].contribution[99]]


M=np.matrix(Aj).A1
np.savetxt("TableMomentaLand.csv", 
           np.hstack([subjects,phaseFactor,taskFactor,coordinateFactor,np.matrix(M).T]), 
           delimiter=",")


#means and std

# vertical
data5 = []; data20 = []; data40 = []; data99 = [];
for i in xrange (len(mconf.traceurs_list)):
    data5 = LandLM_abs[i].contribution[5]
    data20 = LandLM_abs[i].contribution[20]
    data40 = LandLM_abs[i].contribution[40]
    data99 = LandLM_abs[i].contribution[99]

table_LandLM_abs = np.matrix([np.mean(np.matrix(data5).T, 1).A1, 
                              np.mean(np.matrix(data20).T, 1).A1, 
                              np.mean(np.matrix(data40).T, 1).A1, 
                              np.mean(np.matrix(data99).T, 1).A1])
table_LandLM_abs_std = np.matrix([np.std(np.matrix(data5).T, 1).A1, 
                                  np.std(np.matrix(data20).T, 1).A1, 
                                  np.std(np.matrix(data40).T, 1).A1, 
                                  np.std(np.matrix(data99).T, 1).A1])
np.savetxt("means/LandLM_abs.csv", table_LandLM_abs, delimiter=",")
np.savetxt("std/LandLM_abs.csv", table_LandLM_abs_std, delimiter=",")

# stability
data5 = []; data20 = []; data40 = []; data99 = [];
for i in xrange (len(mconf.traceurs_list)):
    data5 = np.sum(LandLM_stab[i].contribution[5],1)
    data20 = np.sum(LandLM_stab[i].contribution[20],1) 
    data40 = np.sum(LandLM_stab[i].contribution[40],1) 
    data99 = np.sum(LandLM_stab[i].contribution[99],1) 

table_LandLM_stab = np.matrix([np.mean(np.matrix(data5).T, 1).A1, 
                              np.mean(np.matrix(data20).T, 1).A1, 
                              np.mean(np.matrix(data40).T, 1).A1, 
                              np.mean(np.matrix(data99).T, 1).A1])
np.savetxt("means/LandLM_stab.csv", table_LandLM_stab, delimiter=",")
np.savetxt("std/LandLM_stab.csv", table_LandLM_stab, delimiter=",")

# angular momentum
data5 = []; data20 = []; data40 = []; data99 = [];
for i in xrange (len(mconf.traceurs_list)):
    data5 = LandAM[i].contribution[5]
    data20 = LandAM[i].contribution[20]
    data40 = LandAM[i].contribution[40]
    data99 = LandAM[i].contribution[99]

table_LandAM = np.matrix([np.mean(np.matrix(data5).T, 1).A1, 
                          np.mean(np.matrix(data20).T, 1).A1, 
                          np.mean(np.matrix(data40).T, 1).A1, 
                          np.mean(np.matrix(data99).T, 1).A1])
table_LandAM_std = np.matrix([np.std(np.matrix(data5).T, 1).A1, 
                              np.std(np.matrix(data20).T, 1).A1, 
                              np.std(np.matrix(data40).T, 1).A1, 
                              np.std(np.matrix(data99).T, 1).A1])
np.savetxt("means/LandAM.csv", table_LandAM, delimiter=",")
np.savetxt("std/LandAM.csv", table_LandAM_std, delimiter=",")

# centroidal momentum ellipsoid



'''
(jump,fly,land) = getTrials(0)
motion = fly
nRep = len(motion)
tmax = len(motion[0]['pinocchio_data'])
DoF = 42#motion[0]['pinocchio_data'][0].A1.shape[0]
data = []
dataStr = np.zeros((tmax,DoF,nRep))
for t in xrange(tmax):
    for i in xrange (nRep):
        data += [np.array(motion[i]['osim_data'][t]).squeeze()]
        dataStr[t,:,i] = motion[i]['osim_data'][t]

'''
'''
def averageQuatertions(Q):
    M = np.zeros((4,4));
    n = Q.shape[1];

    for i in xrange(n):
        q = np.matrix(Q[:,i])
        M += q*q.T

    Mnorm = (1./n)*M
    eigvals, eigvec = np.linalg.eig(Mnorm)
    Qavg=eigvec[eigvals.argmax()]
    return abs(Qavg)


(jump,fly,land) = getTrials(0)
motion = fly
nRep = len(motion)
tmax = len(motion[0]['pinocchio_data'])
DoF = motion[0]['pinocchio_data'][0].A1.shape[0]
data = []
dataStr = np.zeros((tmax,DoF,nRep))
for t in xrange(tmax):
    for i in xrange (nRep):
        data += [np.array(motion[i]['pinocchio_data'][t]).squeeze()]
        dataStr[t,:,i] = motion[i]['pinocchio_data'][t]

Q_avg = np.zeros((100,4))
for i in xrange(100):
    Q = dataStr[i,3:7,:]
    Q_avg[i] = averageQuatertions(Q)

q_mean = fq_mean.copy()
viewer.display(q_mean[99],avatar.name)

q_mean2 = fq_mean.copy()
q_mean2[:,3:7] = Q_avg
viewer.display(q_mean2[0],avatar.name)


'''
