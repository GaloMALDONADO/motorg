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
    jump_dq = np.load('./motions/'+participantName+'_jump_dq.npy')
    fly_dq = np.load('./motions/'+participantName+'_fly_dq.npy')  
    land_dq = np.load('./motions/'+participantName+'_land_dq.npy')
    jump_ddq = np.load('./motions/'+participantName+'_jump_ddq.npy')
    fly_ddq = np.load('./motions/'+participantName+'_fly_ddq.npy')  
    land_ddq = np.load('./motions/'+participantName+'_land_ddq.npy')
    #trial = References(mconf.traceurs_list[idxTraceur])
    #trial.loadModel()
    #trial.display()
    #trial.getTrials()
    return jump,fly,land, jump_dq,fly_dq,land_dq,jump_ddq,fly_ddq,land_ddq

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
FLMmask = np.array([True,True,True,True,True,True])
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

    (jump,fly,land,jump_dq,fly_dq,land_dq,jump_ddq,fly_ddq,land_ddq) = getTrials(i)
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

''' Rate of Change '''
#Study of contribution of joints 
#means and std
data0x = []; data40x = []; data70x = []; data99x = [];
data0y = []; data40y = []; data70y = []; data99y = [];
data0z = []; data40z = []; data70z = []; data99z = [];
data0xx = []; data40xx = []; data70xx = []; data99xx = [];
data0yy = []; data40yy = []; data70yy = []; data99yy = [];
data0zz = []; data40zz = []; data70zz = []; data99zz = [];
for i in xrange (len(mconf.traceurs_list)):   
    data0x += [JumpLM[i].contributionF[0][:,0]]
    data40x += [JumpLM[i].contributionF[40][:,0]]
    data70x += [JumpLM[i].contributionF[70][:,0]]
    data99x += [JumpLM[i].contributionF[99][:,0]]
    data0y += [JumpLM[i].contributionF[0][:,1]]
    data40y += [JumpLM[i].contributionF[40][:,1]]
    data70y += [JumpLM[i].contributionF[70][:,1]]
    data99y += [JumpLM[i].contributionF[99][:,1]]
    data0z += [JumpLM[i].contributionF[0][:,2]]
    data40z += [JumpLM[i].contributionF[40][:,2]]
    data70z += [JumpLM[i].contributionF[70][:,2]]
    data99z += [JumpLM[i].contributionF[99][:,2]]
    data0xx += [JumpAM[i].contributionF[0][:,3]]
    data40xx += [JumpAM[i].contributionF[40][:,3]]
    data70xx += [JumpAM[i].contributionF[70][:,3]]
    data99xx += [JumpAM[i].contributionF[99][:,3]]
    data0yy += [JumpAM[i].contributionF[0][:,4]]
    data40yy += [JumpAM[i].contributionF[40][:,4]]
    data70yy += [JumpAM[i].contributionF[70][:,4]]
    data99yy += [JumpAM[i].contributionF[99][:,4]]
    data0zz += [JumpAM[i].contributionF[0][:,5]]
    data40zz += [JumpAM[i].contributionF[40][:,5]]
    data70zz += [JumpAM[i].contributionF[70][:,5]]
    data99zz += [JumpAM[i].contributionF[99][:,5]]

table_JumpMx = np.matrix([np.mean(np.matrix(data0x), 0).A1, 
                          np.mean(np.matrix(data40x), 0).A1, 
                          np.mean(np.matrix(data70x), 0).A1, 
                          np.mean(np.matrix(data99x), 0).A1])
table_JumpM_stdx = np.matrix([np.std(np.matrix(data0x), 0).A1, 
                              np.std(np.matrix(data40x), 0).A1, 
                              np.std(np.matrix(data70x), 0).A1, 
                              np.std(np.matrix(data99x), 0).A1])
table_JumpMy = np.matrix([np.mean(np.matrix(data0y), 0).A1, 
                          np.mean(np.matrix(data40y), 0).A1, 
                          np.mean(np.matrix(data70y), 0).A1, 
                          np.mean(np.matrix(data99y), 0).A1])
table_JumpM_stdy = np.matrix([np.std(np.matrix(data0y), 0).A1, 
                              np.std(np.matrix(data40y), 0).A1, 
                              np.std(np.matrix(data70y), 0).A1, 
                              np.std(np.matrix(data99y), 0).A1])
table_JumpMz = np.matrix([np.mean(np.matrix(data0z), 0).A1, 
                          np.mean(np.matrix(data40z), 0).A1, 
                          np.mean(np.matrix(data70z), 0).A1, 
                          np.mean(np.matrix(data99z), 0).A1])
table_JumpM_stdz = np.matrix([np.std(np.matrix(data0z), 0).A1, 
                              np.std(np.matrix(data40z), 0).A1, 
                              np.std(np.matrix(data70z), 0).A1, 
                              np.std(np.matrix(data99z), 0).A1])

table_JumpMxx = np.matrix([np.mean(np.matrix(data0xx), 0).A1, 
                           np.mean(np.matrix(data40xx), 0).A1, 
                           np.mean(np.matrix(data70xx), 0).A1, 
                           np.mean(np.matrix(data99xx), 0).A1])
table_JumpM_stdxx = np.matrix([np.std(np.matrix(data0xx), 0).A1, 
                               np.std(np.matrix(data40xx), 0).A1, 
                               np.std(np.matrix(data70xx), 0).A1, 
                               np.std(np.matrix(data99xx), 0).A1])
table_JumpMyy = np.matrix([np.mean(np.matrix(data0yy), 0).A1, 
                           np.mean(np.matrix(data40yy), 0).A1, 
                           np.mean(np.matrix(data70yy), 0).A1, 
                           np.mean(np.matrix(data99yy), 0).A1])
table_JumpM_stdyy = np.matrix([np.std(np.matrix(data0yy), 0).A1, 
                               np.std(np.matrix(data40yy), 0).A1, 
                               np.std(np.matrix(data70yy), 0).A1, 
                               np.std(np.matrix(data99yy), 0).A1])
table_JumpMzz = np.matrix([np.mean(np.matrix(data0zz), 0).A1, 
                           np.mean(np.matrix(data40zz), 0).A1, 
                           np.mean(np.matrix(data70zz), 0).A1, 
                           np.mean(np.matrix(data99zz), 0).A1])
table_JumpM_stdzz = np.matrix([np.std(np.matrix(data0zz), 0).A1, 
                               np.std(np.matrix(data40zz), 0).A1, 
                               np.std(np.matrix(data70zz), 0).A1, 
                               np.std(np.matrix(data99zz), 0).A1])


np.savetxt("tables/momenta/mean/JumpFLMx.csv", table_JumpMx, delimiter=",")
np.savetxt("tables/momenta/std/JumpFLMx.csv", table_JumpM_stdx, delimiter=",")
np.savetxt("tables/momenta/mean/JumpFLMy.csv", table_JumpMy, delimiter=",")
np.savetxt("tables/momenta/std/JumpFLMy.csv", table_JumpM_stdy, delimiter=",")
np.savetxt("tables/momenta/mean/JumpFLMz.csv", table_JumpMz, delimiter=",")
np.savetxt("tables/momenta/std/JumpFLMz.csv", table_JumpM_stdz, delimiter=",")

np.savetxt("tables/momenta/mean/JumpTAMx.csv", table_JumpMxx, delimiter=",")
np.savetxt("tables/momenta/std/JumpTAMx.csv", table_JumpM_stdxx, delimiter=",")
np.savetxt("tables/momenta/mean/JumpTAMy.csv", table_JumpMyy, delimiter=",")
np.savetxt("tables/momenta/std/JumpTAMy.csv", table_JumpM_stdyy, delimiter=",")
np.savetxt("tables/momenta/mean/JumpTAMz.csv", table_JumpMzz, delimiter=",")
np.savetxt("tables/momenta/std/JumpTAMz.csv", table_JumpM_stdzz, delimiter=",")


#means and std
data0x = []; data40x = []; data70x = []; data99x = [];
data0y = []; data40y = []; data70y = []; data99y = [];
data0z = []; data40z = []; data70z = []; data99z = [];
data0xx = []; data40xx = []; data70xx = []; data99xx = [];
data0yy = []; data40yy = []; data70yy = []; data99yy = [];
data0zz = []; data40zz = []; data70zz = []; data99zz = [];
for i in xrange (len(mconf.traceurs_list)):   
    data0x += [LandLM_abs[i].contributionF[5][:,0]]
    data40x += [LandLM_abs[i].contributionF[20][:,0]]
    data70x += [LandLM_abs[i].contributionF[40][:,0]]
    data99x += [LandLM_abs[i].contributionF[99][:,0]]
    data0y += [LandLM_abs[i].contributionF[5][:,1]]
    data40y += [LandLM_abs[i].contributionF[20][:,1]]
    data70y += [LandLM_abs[i].contributionF[40][:,1]]
    data99y += [LandLM_abs[i].contributionF[99][:,1]]
    data0z += [LandLM_abs[i].contributionF[5][:,2]]
    data40z += [LandLM_abs[i].contributionF[20][:,2]]
    data70z += [LandLM_abs[i].contributionF[40][:,2]]
    data99z += [LandLM_abs[i].contributionF[99][:,2]]
    data0xx += [LandAM[i].contributionF[5][:,3]]
    data40xx += [LandAM[i].contributionF[20][:,3]]
    data70xx += [LandAM[i].contributionF[40][:,3]]
    data99xx += [LandAM[i].contributionF[99][:,3]]
    data0yy += [LandAM[i].contributionF[5][:,4]]
    data40yy += [LandAM[i].contributionF[20][:,4]]
    data70yy += [LandAM[i].contributionF[40][:,4]]
    data99yy += [LandAM[i].contributionF[99][:,4]]
    data0zz += [LandAM[i].contributionF[5][:,5]]
    data40zz += [LandAM[i].contributionF[20][:,5]]
    data70zz += [LandAM[i].contributionF[40][:,5]]
    data99zz += [LandAM[i].contributionF[99][:,5]]

table_JumpMx = np.matrix([np.mean(np.matrix(data0x), 0).A1, 
                          np.mean(np.matrix(data40x), 0).A1, 
                          np.mean(np.matrix(data70x), 0).A1, 
                          np.mean(np.matrix(data99x), 0).A1])
table_JumpM_stdx = np.matrix([np.std(np.matrix(data0x), 0).A1, 
                              np.std(np.matrix(data40x), 0).A1, 
                              np.std(np.matrix(data70x), 0).A1, 
                              np.std(np.matrix(data99x), 0).A1])
table_JumpMy = np.matrix([np.mean(np.matrix(data0y), 0).A1, 
                          np.mean(np.matrix(data40y), 0).A1, 
                          np.mean(np.matrix(data70y), 0).A1, 
                          np.mean(np.matrix(data99y), 0).A1])
table_JumpM_stdy = np.matrix([np.std(np.matrix(data0y), 0).A1, 
                              np.std(np.matrix(data40y), 0).A1, 
                              np.std(np.matrix(data70y), 0).A1, 
                              np.std(np.matrix(data99y), 0).A1])
table_JumpMz = np.matrix([np.mean(np.matrix(data0z), 0).A1, 
                          np.mean(np.matrix(data40z), 0).A1, 
                          np.mean(np.matrix(data70z), 0).A1, 
                          np.mean(np.matrix(data99z), 0).A1])
table_JumpM_stdz = np.matrix([np.std(np.matrix(data0z), 0).A1, 
                              np.std(np.matrix(data40z), 0).A1, 
                              np.std(np.matrix(data70z), 0).A1, 
                              np.std(np.matrix(data99z), 0).A1])

table_JumpMxx = np.matrix([np.mean(np.matrix(data0xx), 0).A1, 
                           np.mean(np.matrix(data40xx), 0).A1, 
                           np.mean(np.matrix(data70xx), 0).A1, 
                           np.mean(np.matrix(data99xx), 0).A1])
table_JumpM_stdxx = np.matrix([np.std(np.matrix(data0xx), 0).A1, 
                               np.std(np.matrix(data40xx), 0).A1, 
                               np.std(np.matrix(data70xx), 0).A1, 
                               np.std(np.matrix(data99xx), 0).A1])
table_JumpMyy = np.matrix([np.mean(np.matrix(data0yy), 0).A1, 
                           np.mean(np.matrix(data40yy), 0).A1, 
                           np.mean(np.matrix(data70yy), 0).A1, 
                           np.mean(np.matrix(data99yy), 0).A1])
table_JumpM_stdyy = np.matrix([np.std(np.matrix(data0yy), 0).A1, 
                               np.std(np.matrix(data40yy), 0).A1, 
                               np.std(np.matrix(data70yy), 0).A1, 
                               np.std(np.matrix(data99yy), 0).A1])
table_JumpMzz = np.matrix([np.mean(np.matrix(data0zz), 0).A1, 
                           np.mean(np.matrix(data40zz), 0).A1, 
                           np.mean(np.matrix(data70zz), 0).A1, 
                           np.mean(np.matrix(data99zz), 0).A1])
table_JumpM_stdzz = np.matrix([np.std(np.matrix(data0zz), 0).A1, 
                               np.std(np.matrix(data40zz), 0).A1, 
                               np.std(np.matrix(data70zz), 0).A1, 
                               np.std(np.matrix(data99zz), 0).A1])


np.savetxt("tables/momenta/mean/LandFLMx.csv", table_JumpMx, delimiter=",")
np.savetxt("tables/momenta/std/LandFLMx.csv", table_JumpM_stdx, delimiter=",")
np.savetxt("tables/momenta/mean/LandFLMy.csv", table_JumpMy, delimiter=",")
np.savetxt("tables/momenta/std/LandFLMy.csv", table_JumpM_stdy, delimiter=",")
np.savetxt("tables/momenta/mean/LandFLMz.csv", table_JumpMz, delimiter=",")
np.savetxt("tables/momenta/std/LandFLMz.csv", table_JumpM_stdz, delimiter=",")

np.savetxt("tables/momenta/mean/LandTAMx.csv", table_JumpMxx, delimiter=",")
np.savetxt("tables/momenta/std/LandTAMx.csv", table_JumpM_stdxx, delimiter=",")
np.savetxt("tables/momenta/mean/LandTAMy.csv", table_JumpMyy, delimiter=",")
np.savetxt("tables/momenta/std/LandTAMy.csv", table_JumpM_stdyy, delimiter=",")
np.savetxt("tables/momenta/mean/LandTAMz.csv", table_JumpMzz, delimiter=",")
np.savetxt("tables/momenta/std/LandTAMz.csv", table_JumpM_stdzz, delimiter=",")
















''' ***************** MOMENTUM IN PARKOUR STUDY ****************** '''
import matplotlib.pyplot as plt
#plot total linear and angular momenta CoM
JLM_ap = []; JLM_ml=[]; JLM_v=[]; JAM_y=[]; JAM_x=[]; JAM_z=[]; 
for i in xrange (len(mconf.traceurs_list)):
    JLM_ap += [-np.array(JumpLM[i].h)[:,0]]
    JLM_ml += [np.array(JumpLM[i].h)[:,1]]
    JLM_v += [np.array(JumpLM[i].h)[:,2]]
    JAM_y += [-np.array(JumpAM[i].h)[:,3]]
    JAM_x += [np.array(JumpAM[i].h)[:,4]]
    JAM_z += [np.array(JumpAM[i].h)[:,5]]

hmean=np.vstack([np.mean(np.array(JLM_ml).squeeze(),0),
                 np.mean(np.array(JLM_ap).squeeze(),0),
                 np.mean(np.array(JLM_v).squeeze(),0),
                 np.mean(np.array(JAM_x).squeeze(),0),
                 np.mean(np.array(JAM_y).squeeze(),0),
                 np.mean(np.array(JAM_z).squeeze(),0)
             ]).T
hstd=np.vstack([np.std(np.array(JLM_ml).squeeze(),0),
                np.std(np.array(JLM_ap).squeeze(),0),
                np.std(np.array(JLM_v).squeeze(),0),
                np.std(np.array(JAM_x).squeeze(),0),
                np.std(np.array(JAM_y).squeeze(),0),
                np.std(np.array(JAM_z).squeeze(),0)
            ]).T


fig = plt.figure()
fig.canvas.set_window_title('Takeoff Motion')
Plus = hmean + hstd
Min = hmean - hstd

ax = fig.add_subplot('211')
#ax.plot(hmean[:,0],'-r', linewidth=3.0)
#ax.plot(Plus[:,0],'-k',color = '0.75', linewidth=1.0, linestyle='--')
#ax.plot(Min[:,0],'-k' ,color = '0.75',linewidth=1.0, linestyle='--')
ax.plot(hmean[:,1],'-r', linewidth=4.0)
ax.plot(hmean[:,2],':g', linewidth=4.0)
ax.plot(Plus[:,1],'-k',color = '0.75', linewidth=3.0, linestyle='--')
plt.legend(['mean (antero posterior)','mean (vertical)','mean $\pm$ std'],loc=2)
ax.plot(Min[:,1],'-k' ,color = '0.75',linewidth=3.0, linestyle='--')
ax.plot(Plus[:,2],'-k',color = '0.75', linewidth=3.0, linestyle='--')
ax.plot(Min[:,2],'-k' ,color = '0.75',linewidth=3.0, linestyle='--')
plt.ylabel('Linear Momentum \n $[kg \cdot m \cdot s^{-1} \cdot BW^{-1}]$',{'fontsize': 18})

ax = fig.add_subplot('212')
ax.plot(hmean[:,3],'-b', linewidth=4.0)
ax.plot(Plus[:,3],'-k',color = '0.75', linewidth=3.0, linestyle='--')
ax.plot(Min[:,3],'-k' ,color = '0.75',linewidth=3.0, linestyle='--')
plt.legend(['mean (sagittal plane)','mean $\pm$ std'],loc=2)
#plt.legend(['sagittal plane'],loc=1)
#ax.plot(hmean[:,4],'-g', linewidth=3.0)
#ax.plot(Plus[:,4],'-k',color = '0.75', linewidth=1.0, linestyle='--')
#ax.plot(Min[:,4],'-k' ,color = '0.75',linewidth=1.0, linestyle='--')
#ax.plot(hmean[:,5],'-b', linewidth=3.0)
#ax.plot(Plus[:,5],'-k',color = '0.75', linewidth=1.0, linestyle='--')
#ax.plot(Min[:,5],'-k' ,color = '0.75',linewidth=1.0, linestyle='--')
plt.ylabel('Angular Momentum \n $[Kg \cdot m^{2} \cdot s^{-1} \cdot  BW^{-1} \cdot H^{-1}]$',{'fontsize': 18})




# Now get tables for stats
''' Impulsion Phase '''
nphases = 4;
segments = 25
subjects = np.matrix(np.repeat(np.linspace(1,5,5), nphases*segments)).T 
#j: 0(start)  40 60(A-P_F, AM_UCM) 70(BW) 100(end)
phaseFactor = np.matrix([  0, 40, 70,  99]*nsubjects*segments).T
segmentFactor = np.matrix(range(segments)*nsubjects*nphases).T

H_ap=[]; H_v=[]; L=[]; 
for i in xrange (len(mconf.traceurs_list)):
    H_ap += [JumpLM[i].contribution[0][:,0]]
    H_v += [JumpLM[i].contribution[0][:,2]]
    L += [JumpAM[i].contribution[0][:,4]]
    H_ap += [JumpLM[i].contribution[40][:,0]]
    H_v += [JumpLM[i].contribution[40][:,2]]
    L += [JumpAM[i].contribution[40][:,4]]
    H_ap += [JumpLM[i].contribution[70][:,0]]
    H_v += [JumpLM[i].contribution[70][:,2]]
    L += [JumpAM[i].contribution[70][:,4]]
    H_ap += [JumpLM[i].contribution[99][:,0]]
    H_v += [JumpLM[i].contribution[99][:,2]]
    L += [JumpAM[i].contribution[99][:,4]]

hap = np.matrix(H_ap).A1
hv = np.matrix(H_v).A1
l = np.matrix(L).A1
np.savetxt("tables/momenta/TableMomentaJumpLinMomAP.csv", 
           np.hstack([subjects,phaseFactor,segmentFactor,np.matrix(hap).T]), 
           delimiter=",")
np.savetxt("tables/momenta/TableMomentaJumpLinMomV.csv", 
           np.hstack([subjects,phaseFactor,segmentFactor,np.matrix(hv).T]), 
           delimiter=",")
np.savetxt("tables/momenta/TableMomentaJumpAngMom.csv", 
           np.hstack([subjects,phaseFactor,segmentFactor,np.matrix(l).T]), 
           delimiter=",")


#means and std
data0x = []; data40x = []; data70x = []; data99x = [];
data0y = []; data40y = []; data70y = []; data99y = [];
data0z = []; data40z = []; data70z = []; data99z = [];
data0xx = []; data40xx = []; data70xx = []; data99xx = [];
data0yy = []; data40yy = []; data70yy = []; data99yy = [];
data0zz = []; data40zz = []; data70zz = []; data99zz = [];
for i in xrange (len(mconf.traceurs_list)):   
    data0x += [JumpLM[i].contribution[0][:,0]]
    data40x += [JumpLM[i].contribution[40][:,0]]
    data70x += [JumpLM[i].contribution[70][:,0]]
    data99x += [JumpLM[i].contribution[99][:,0]]
    data0y += [JumpLM[i].contribution[0][:,1]]
    data40y += [JumpLM[i].contribution[40][:,1]]
    data70y += [JumpLM[i].contribution[70][:,1]]
    data99y += [JumpLM[i].contribution[99][:,1]]
    data0z += [JumpLM[i].contribution[0][:,2]]
    data40z += [JumpLM[i].contribution[40][:,2]]
    data70z += [JumpLM[i].contribution[70][:,2]]
    data99z += [JumpLM[i].contribution[99][:,2]]
    data0xx += [JumpAM[i].contribution[0][:,3]]
    data40xx += [JumpAM[i].contribution[40][:,3]]
    data70xx += [JumpAM[i].contribution[70][:,3]]
    data99xx += [JumpAM[i].contribution[99][:,3]]
    data0yy += [JumpAM[i].contribution[0][:,4]]
    data40yy += [JumpAM[i].contribution[40][:,4]]
    data70yy += [JumpAM[i].contribution[70][:,4]]
    data99yy += [JumpAM[i].contribution[99][:,4]]
    data0zz += [JumpAM[i].contribution[0][:,5]]
    data40zz += [JumpAM[i].contribution[40][:,5]]
    data70zz += [JumpAM[i].contribution[70][:,5]]
    data99zz += [JumpAM[i].contribution[99][:,5]]

table_JumpMx = np.matrix([np.mean(np.matrix(data0x), 0).A1, 
                          np.mean(np.matrix(data40x), 0).A1, 
                          np.mean(np.matrix(data70x), 0).A1, 
                          np.mean(np.matrix(data99x), 0).A1])
table_JumpM_stdx = np.matrix([np.std(np.matrix(data0x), 0).A1, 
                              np.std(np.matrix(data40x), 0).A1, 
                              np.std(np.matrix(data70x), 0).A1, 
                              np.std(np.matrix(data99x), 0).A1])
table_JumpMy = np.matrix([np.mean(np.matrix(data0y), 0).A1, 
                          np.mean(np.matrix(data40y), 0).A1, 
                          np.mean(np.matrix(data70y), 0).A1, 
                          np.mean(np.matrix(data99y), 0).A1])
table_JumpM_stdy = np.matrix([np.std(np.matrix(data0y), 0).A1, 
                              np.std(np.matrix(data40y), 0).A1, 
                              np.std(np.matrix(data70y), 0).A1, 
                              np.std(np.matrix(data99y), 0).A1])
table_JumpMz = np.matrix([np.mean(np.matrix(data0z), 0).A1, 
                          np.mean(np.matrix(data40z), 0).A1, 
                          np.mean(np.matrix(data70z), 0).A1, 
                          np.mean(np.matrix(data99z), 0).A1])
table_JumpM_stdz = np.matrix([np.std(np.matrix(data0z), 0).A1, 
                              np.std(np.matrix(data40z), 0).A1, 
                              np.std(np.matrix(data70z), 0).A1, 
                              np.std(np.matrix(data99z), 0).A1])

table_JumpMxx = np.matrix([np.mean(np.matrix(data0xx), 0).A1, 
                           np.mean(np.matrix(data40xx), 0).A1, 
                           np.mean(np.matrix(data70xx), 0).A1, 
                           np.mean(np.matrix(data99xx), 0).A1])
table_JumpM_stdxx = np.matrix([np.std(np.matrix(data0xx), 0).A1, 
                               np.std(np.matrix(data40xx), 0).A1, 
                               np.std(np.matrix(data70xx), 0).A1, 
                               np.std(np.matrix(data99xx), 0).A1])
table_JumpMyy = np.matrix([np.mean(np.matrix(data0yy), 0).A1, 
                           np.mean(np.matrix(data40yy), 0).A1, 
                           np.mean(np.matrix(data70yy), 0).A1, 
                           np.mean(np.matrix(data99yy), 0).A1])
table_JumpM_stdyy = np.matrix([np.std(np.matrix(data0yy), 0).A1, 
                               np.std(np.matrix(data40yy), 0).A1, 
                               np.std(np.matrix(data70yy), 0).A1, 
                               np.std(np.matrix(data99yy), 0).A1])
table_JumpMzz = np.matrix([np.mean(np.matrix(data0zz), 0).A1, 
                           np.mean(np.matrix(data40zz), 0).A1, 
                           np.mean(np.matrix(data70zz), 0).A1, 
                           np.mean(np.matrix(data99zz), 0).A1])
table_JumpM_stdzz = np.matrix([np.std(np.matrix(data0zz), 0).A1, 
                               np.std(np.matrix(data40zz), 0).A1, 
                               np.std(np.matrix(data70zz), 0).A1, 
                               np.std(np.matrix(data99zz), 0).A1])


np.savetxt("tables/momenta/mean/JumpLMx.csv", table_JumpMx, delimiter=",")
np.savetxt("tables/momenta/std/JumpLMx.csv", table_JumpM_stdx, delimiter=",")
np.savetxt("tables/momenta/mean/JumpLMy.csv", table_JumpMy, delimiter=",")
np.savetxt("tables/momenta/std/JumpLMy.csv", table_JumpM_stdy, delimiter=",")
np.savetxt("tables/momenta/mean/JumpLMz.csv", table_JumpMz, delimiter=",")
np.savetxt("tables/momenta/std/JumpLMz.csv", table_JumpM_stdz, delimiter=",")

np.savetxt("tables/momenta/mean/JumpAMx.csv", table_JumpMxx, delimiter=",")
np.savetxt("tables/momenta/std/JumpAMx.csv", table_JumpM_stdxx, delimiter=",")
np.savetxt("tables/momenta/mean/JumpAMy.csv", table_JumpMyy, delimiter=",")
np.savetxt("tables/momenta/std/JumpAMy.csv", table_JumpM_stdyy, delimiter=",")
np.savetxt("tables/momenta/mean/JumpAMz.csv", table_JumpMzz, delimiter=",")
np.savetxt("tables/momenta/std/JumpAMz.csv", table_JumpM_stdzz, delimiter=",")




''' Landing Phase '''
nphases = 4;
segments = 25
subjects = np.matrix(np.repeat(np.linspace(1,5,5), nphases*segments)).T 
#l: 5(start) 20(maxForce) 40(lowerForce/stab) 100(end) 
phaseFactor = np.matrix([  5, 20, 40,  99]*nsubjects*segments).T
segmentFactor = np.matrix(range(segments)*nsubjects*nphases).T

H_v=[]; H_ap=[]; L=[]; H_ml=[];
for i in xrange (len(mconf.traceurs_list)):
    H_ml += [JumpLM[i].contribution[5][:,1]]
    H_ap += [JumpLM[i].contribution[5][:,0]]
    H_v += [JumpLM[i].contribution[5][:,2]]
    L += [JumpAM[i].contribution[5][:,4]]
    H_ml += [JumpLM[i].contribution[20][:,1]]
    H_ap += [JumpLM[i].contribution[20][:,0]]
    H_v += [JumpLM[i].contribution[20][:,2]]
    L += [JumpAM[i].contribution[20][:,4]]
    H_ml += [JumpLM[i].contribution[40][:,1]]
    H_ap += [JumpLM[i].contribution[40][:,0]]
    H_v += [JumpLM[i].contribution[40][:,2]]
    L += [JumpAM[i].contribution[40][:,4]]
    H_ml += [JumpLM[i].contribution[99][:,1]]
    H_ap += [JumpLM[i].contribution[99][:,0]]
    H_v += [JumpLM[i].contribution[99][:,2]]
    L += [JumpAM[i].contribution[99][:,4]]

hml = np.matrix(H_ml).A1
hap = np.matrix(H_ap).A1
hv = np.matrix(H_v).A1
l = np.matrix(L).A1
np.savetxt("tables/momenta/TableMomentaLandLinMomML.csv", 
           np.hstack([subjects,phaseFactor,segmentFactor,np.matrix(hml).T]), 
           delimiter=",")
np.savetxt("tables/momenta/TableMomentaLandLinMomAP.csv", 
           np.hstack([subjects,phaseFactor,segmentFactor,np.matrix(hap).T]), 
           delimiter=",")
np.savetxt("tables/momenta/TableMomentaLandLinMomV.csv", 
           np.hstack([subjects,phaseFactor,segmentFactor,np.matrix(hv).T]), 
           delimiter=",")
np.savetxt("tables/momenta/TableMomentaLandAngMom.csv", 
           np.hstack([subjects,phaseFactor,segmentFactor,np.matrix(l).T]), 
           delimiter=",")


#means and std
data0x = []; data40x = []; data70x = []; data99x = [];
data0y = []; data40y = []; data70y = []; data99y = [];
data0z = []; data40z = []; data70z = []; data99z = [];
data0xx = []; data40xx = []; data70xx = []; data99xx = [];
data0yy = []; data40yy = []; data70yy = []; data99yy = [];
data0zz = []; data40zz = []; data70zz = []; data99zz = [];
for i in xrange (len(mconf.traceurs_list)):   
    data0x += [LandLM_abs[i].contribution[5][:,0]]
    data40x += [LandLM_abs[i].contribution[20][:,0]]
    data70x += [LandLM_abs[i].contribution[40][:,0]]
    data99x += [LandLM_abs[i].contribution[99][:,0]]
    data0y += [LandLM_abs[i].contribution[5][:,1]]
    data40y += [LandLM_abs[i].contribution[20][:,1]]
    data70y += [LandLM_abs[i].contribution[40][:,1]]
    data99y += [LandLM_abs[i].contribution[99][:,1]]
    data0z += [LandLM_abs[i].contribution[5][:,2]]
    data40z += [LandLM_abs[i].contribution[20][:,2]]
    data70z += [LandLM_abs[i].contribution[40][:,2]]
    data99z += [LandLM_abs[i].contribution[99][:,2]]
    data0xx += [LandAM[i].contribution[5][:,3]]
    data40xx += [LandAM[i].contribution[20][:,3]]
    data70xx += [LandAM[i].contribution[40][:,3]]
    data99xx += [LandAM[i].contribution[99][:,3]]
    data0yy += [LandAM[i].contribution[5][:,4]]
    data40yy += [LandAM[i].contribution[20][:,4]]
    data70yy += [LandAM[i].contribution[40][:,4]]
    data99yy += [LandAM[i].contribution[99][:,4]]
    data0zz += [LandAM[i].contribution[5][:,5]]
    data40zz += [LandAM[i].contribution[20][:,5]]
    data70zz += [LandAM[i].contribution[40][:,5]]
    data99zz += [LandAM[i].contribution[99][:,5]]

table_JumpMx = np.matrix([np.mean(np.matrix(data0x), 0).A1, 
                          np.mean(np.matrix(data40x), 0).A1, 
                          np.mean(np.matrix(data70x), 0).A1, 
                          np.mean(np.matrix(data99x), 0).A1])
table_JumpM_stdx = np.matrix([np.std(np.matrix(data0x), 0).A1, 
                              np.std(np.matrix(data40x), 0).A1, 
                              np.std(np.matrix(data70x), 0).A1, 
                              np.std(np.matrix(data99x), 0).A1])
table_JumpMy = np.matrix([np.mean(np.matrix(data0y), 0).A1, 
                          np.mean(np.matrix(data40y), 0).A1, 
                          np.mean(np.matrix(data70y), 0).A1, 
                          np.mean(np.matrix(data99y), 0).A1])
table_JumpM_stdy = np.matrix([np.std(np.matrix(data0y), 0).A1, 
                              np.std(np.matrix(data40y), 0).A1, 
                              np.std(np.matrix(data70y), 0).A1, 
                              np.std(np.matrix(data99y), 0).A1])
table_JumpMz = np.matrix([np.mean(np.matrix(data0z), 0).A1, 
                          np.mean(np.matrix(data40z), 0).A1, 
                          np.mean(np.matrix(data70z), 0).A1, 
                          np.mean(np.matrix(data99z), 0).A1])
table_JumpM_stdz = np.matrix([np.std(np.matrix(data0z), 0).A1, 
                              np.std(np.matrix(data40z), 0).A1, 
                              np.std(np.matrix(data70z), 0).A1, 
                              np.std(np.matrix(data99z), 0).A1])

table_JumpMxx = np.matrix([np.mean(np.matrix(data0xx), 0).A1, 
                           np.mean(np.matrix(data40xx), 0).A1, 
                           np.mean(np.matrix(data70xx), 0).A1, 
                           np.mean(np.matrix(data99xx), 0).A1])
table_JumpM_stdxx = np.matrix([np.std(np.matrix(data0xx), 0).A1, 
                               np.std(np.matrix(data40xx), 0).A1, 
                               np.std(np.matrix(data70xx), 0).A1, 
                               np.std(np.matrix(data99xx), 0).A1])
table_JumpMyy = np.matrix([np.mean(np.matrix(data0yy), 0).A1, 
                           np.mean(np.matrix(data40yy), 0).A1, 
                           np.mean(np.matrix(data70yy), 0).A1, 
                           np.mean(np.matrix(data99yy), 0).A1])
table_JumpM_stdyy = np.matrix([np.std(np.matrix(data0yy), 0).A1, 
                               np.std(np.matrix(data40yy), 0).A1, 
                               np.std(np.matrix(data70yy), 0).A1, 
                               np.std(np.matrix(data99yy), 0).A1])
table_JumpMzz = np.matrix([np.mean(np.matrix(data0zz), 0).A1, 
                           np.mean(np.matrix(data40zz), 0).A1, 
                           np.mean(np.matrix(data70zz), 0).A1, 
                           np.mean(np.matrix(data99zz), 0).A1])
table_JumpM_stdzz = np.matrix([np.std(np.matrix(data0zz), 0).A1, 
                               np.std(np.matrix(data40zz), 0).A1, 
                               np.std(np.matrix(data70zz), 0).A1, 
                               np.std(np.matrix(data99zz), 0).A1])


np.savetxt("tables/momenta/mean/LandLMx.csv", table_JumpMx, delimiter=",")
np.savetxt("tables/momenta/std/LandLMx.csv", table_JumpM_stdx, delimiter=",")
np.savetxt("tables/momenta/mean/LandLMy.csv", table_JumpMy, delimiter=",")
np.savetxt("tables/momenta/std/LandLMy.csv", table_JumpM_stdy, delimiter=",")
np.savetxt("tables/momenta/mean/LandLMz.csv", table_JumpMz, delimiter=",")
np.savetxt("tables/momenta/std/LandLMz.csv", table_JumpM_stdz, delimiter=",")

np.savetxt("tables/momenta/mean/LandAMx.csv", table_JumpMxx, delimiter=",")
np.savetxt("tables/momenta/std/LandAMx.csv", table_JumpM_stdxx, delimiter=",")
np.savetxt("tables/momenta/mean/LandAMy.csv", table_JumpMyy, delimiter=",")
np.savetxt("tables/momenta/std/LandAMy.csv", table_JumpM_stdyy, delimiter=",")
np.savetxt("tables/momenta/mean/LandAMz.csv", table_JumpMzz, delimiter=",")
np.savetxt("tables/momenta/std/LandAMz.csv", table_JumpM_stdzz, delimiter=",")















'''


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
