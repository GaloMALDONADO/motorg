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

import matplotlib.pyplot as plt

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
    return jump,fly,land, jump_dq,fly_dq,land_dq,jump_ddq,fly_ddq,land_ddq

def getForces(i):
    participantName = mconf.traceurs_list[i]
    idxTraceur = mconf.traceurs_list.index(participantName)
    jump = np.load('./motions/'+participantName+'_jump_grfs.npy')
    land = np.load('./motions/'+participantName+'_land_grfs.npy')
    return jump, land

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
#Jump
JumpLM = []; JumpAM = []; 
JLMmask = np.array([True,False,True,False,False,False])
JAMmask = np.array([False,False,False,False,True,False])
#Land
LandLM_abs = []; LandLM_stab = []; LandAM = []; 
LAMmask =   np.array([False, False, False, True, True, True])
LLM_Abs_mask =   np.array([False, False, True, False, False, False])
LLM_Stab_mask =   np.array([True, True, False, False, False, False])


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
    JumpLM += [ucm.ucmMomentum(robots[i], jump, jump_dq, jump_ddq, JLMmask, KF, 1)]
    Vucm, Vcm, criteria = JumpLM[i].getUCMVariances()
    ''' Impulsion task is also defined with the angular momentum around the Antero-Posterior axis'''
    JumpAM += [ucm.ucmMomentum(robots[i], jump, jump_dq, jump_ddq, JAMmask, 1, KT)]
    Vucm, Vcm, criteria = JumpAM[i].getUCMVariances()
    
    ''' *******************************  LAND  ******************************* '''
    ''' Damping and reducing GRFs task is defined with the linear momentum '''
    LandLM_abs += [ucm.ucmMomentum(robots[i], land, land_dq, land_ddq, LLM_Abs_mask, KF, 1)]
    Vucm, Vcm, criteria = LandLM_abs[i].getUCMVariances()
    LandLM_stab += [ucm.ucmMomentum(robots[i], land, land_dq, land_ddq, LLM_Stab_mask, KF,1)]
    Vucm, Vcm, criteria = LandLM_stab[i].getUCMVariances()
    ''' Angular stability task is also defined with the ang momentum around Antero-Posterior axis'''
    LandAM += [ucm.ucmMomentum(robots[i], land, land_dq, land_ddq, LAMmask, 1, KT)]
    Vucm, Vcm, criteria = LandAM[i].getUCMVariances()

#    
plotLinMomJ = plotTasks.CentroidalMomentum(JumpLM,'Impulsion through Linear Momentum (A-P and V) during Jump')
plotAngMomJ = plotTasks.CentroidalMomentum(JumpAM, 'Angular Momentum (around M-L) contribution during Jump')
plotLinMomL_stab = plotTasks.CentroidalMomentum(LandLM_stab,'Linear Momentum stability (A-P and M-L) task during Landing')
plotLinMomL_abs = plotTasks.CentroidalMomentum(LandLM_abs, 'Linear Momentum absorption (V) task during Landing')
plotAngMomL = plotTasks.CentroidalMomentum(LandAM, 'Angular Momentum (around M-L) contribution to stability during Landing')
plotAML = plotTasks.CentroidalMomentum(LandAM,"")


''' *******************************  Prepare files for R  ******************************* '''
nsubjects = 5;

''' Impulsion Phase '''
#j: 0(start)  40 60(A-P_F, AM_UCM) 70(BW) 100(end)
''''
# For ITC
nphases = 4
ntasks = 2
subjects = np.matrix(np.repeat(np.linspace(1,5,5), ntasks*nphases*k)).T
variabilityFactor = np.matrix([1,2]*nsubjects*nphases*ntasks).T
taskFactor =  np.matrix([1,1,2,2]*nsubjects*nphases).T
phaseFactor = np.matrix([  0, 0, 0, 0, 40, 40, 40, 40, 70, 70, 70, 70, 99, 99, 99, 99]*nsubjects).T
    #C += [
    #    JumpLM[i].criteria[2],
    #    JumpAM[i].criteria[2],
    #    JumpLM[i].criteria[40],
    #    JumpAM[i].criteria[40],
    #    JumpLM[i].criteria[70],
    #    JumpAM[i].criteria[70],
    #    JumpLM[i].criteria[97],
    #    JumpAM[i].criteria[97],
    #
'''
k=2
nphases = 4
subjects = np.matrix(np.repeat(np.linspace(1,5,5), nphases*k)).T
variabilityFactor = np.matrix([1,2]*nsubjects*nphases).T
phaseFactor = np.matrix([  0, 0, 40, 40, 70, 70, 99, 99]*nsubjects).T
C=[]; V1=[]; V2=[]; 
for i in xrange (len(mconf.traceurs_list)):
    V1 += [
        # good variability
        # bad variability
        JumpLM[i].Vucm[2],
        JumpLM[i].Vcm[2],
        JumpLM[i].Vucm[40],
        JumpLM[i].Vcm[40],
        JumpLM[i].Vucm[70],
        JumpLM[i].Vcm[70],
        JumpLM[i].Vucm[97],
        JumpLM[i].Vcm[97]
    ]
    V2 += [
        # good variability
        # bad variability
        JumpAM[i].Vucm[2],
        JumpAM[i].Vcm[2],
        JumpAM[i].Vucm[40],
        JumpAM[i].Vcm[40],
        JumpAM[i].Vucm[70],
        JumpAM[i].Vcm[70],
        JumpAM[i].Vucm[97],
        JumpAM[i].Vcm[97]
    ]


#np.savetxt("TableCriteriaImpulse.csv", 
#           np.hstack([subjects,phaseFactor,taskFactor,np.matrix(C).T]), 
#           delimiter=",")
np.savetxt("TableVariancesImpulseLM.csv", 
           np.hstack([subjects,phaseFactor,variabilityFactor,np.matrix(V1).T]), 
           delimiter=",")

np.savetxt("TableVariancesImpulseAM.csv", 
           np.hstack([subjects,phaseFactor,variabilityFactor,np.matrix(V2).T]), 
           delimiter=",")


''' Landing Phase '''
# 7 - 16 - 25 - 40 -100
#l: 5(start) 20(maxForce) 40(lowerForce/stab) 100(end) 
# ******************* ITC *********************************
nphases = 5
ntasks = 3
subjects = np.matrix(np.repeat(np.linspace(1,5,5), ntasks*nphases)).T 
taskFactor =  np.matrix([1,2,3]*nsubjects*nphases).T
phaseFactor = np.matrix([  4, 4, 4, 13, 13, 13, 20, 20, 20, 40, 40, 40, 97, 97,97]*nsubjects).T
C=[]
for i in xrange (len(mconf.traceurs_list)):
    C += [
        LandLM_abs[i].criteria[4],
        LandLM_stab[i].criteria[4],
        LandAM[i].criteria[4],
        LandLM_abs[i].criteria[13],
        LandLM_stab[i].criteria[13],
        LandAM[i].criteria[13],
        LandLM_abs[i].criteria[20],
        LandLM_stab[i].criteria[20],
        LandAM[i].criteria[20],
        LandLM_abs[i].criteria[40],
        LandLM_stab[i].criteria[40],
        LandAM[i].criteria[40],
        LandLM_abs[i].criteria[97],
        LandLM_stab[i].criteria[97],
        LandAM[i].criteria[97],
    ]

np.savetxt("TableCriteriaLand.csv", np.hstack([subjects,phaseFactor,taskFactor,np.matrix(C).T]), delimiter=",") 
# ********************************************************************

k=2
nphases = 5
subjects = np.matrix(np.repeat(np.linspace(1,5,5), nphases*k)).T 
variabilityFactor = np.matrix([1,2]*nsubjects*nphases).T
phaseFactor = np.matrix([  4, 4, 13, 13, 20, 20, 40, 40, 97, 97]*nsubjects).T

C=[]; V1=[]; V2=[]; V3=[]; #for each task
for i in xrange (len(mconf.traceurs_list)):
    V1 += [
        # good variability
        # bad variability
        LandLM_abs[i].Vucm[4],
        LandLM_abs[i].Vcm[4],
        LandLM_abs[i].Vucm[13],
        LandLM_abs[i].Vcm[13],
        LandLM_abs[i].Vucm[20],
        LandLM_abs[i].Vcm[20],
        LandLM_abs[i].Vucm[40],
        LandLM_abs[i].Vcm[40],
        LandLM_abs[i].Vucm[97],
        LandLM_abs[i].Vcm[97]
    ]
    V2 += [
        # good variability
        # bad variability
        LandLM_stab[i].Vucm[4],
        LandLM_stab[i].Vcm[4],
        LandLM_stab[i].Vucm[13],
        LandLM_stab[i].Vcm[13],
        LandLM_stab[i].Vucm[20],
        LandLM_stab[i].Vcm[20],
        LandLM_stab[i].Vucm[40],
        LandLM_stab[i].Vcm[40],
        LandLM_stab[i].Vucm[97],
        LandLM_stab[i].Vcm[97]
    ]
    V3 += [
        # good variability
        # bad variability
        LandAM[i].Vucm[4],
        LandAM[i].Vcm[4],
        LandAM[i].Vucm[13],
        LandAM[i].Vcm[13],
        LandAM[i].Vucm[20],
        LandAM[i].Vcm[20],
        LandAM[i].Vucm[40],
        LandAM[i].Vcm[40],
        LandAM[i].Vucm[97],
        LandAM[i].Vcm[97]
    ]
    




#np.savetxt("TableCriteriaLand.csv", 
#           np.hstack([subjects,phaseFactor,taskFactor,np.matrix(C).T]), 
#           delimiter=",")

np.savetxt("TableVariancesLandVDLM.csv", 
           np.hstack([subjects,phaseFactor,variabilityFactor,np.matrix(V1).T]), 
           delimiter=",")
np.savetxt("TableVariancesLandStabDLM.csv", 
           np.hstack([subjects,phaseFactor,variabilityFactor,np.matrix(V2).T]), 
           delimiter=",")
np.savetxt("TableVariancesLandStabDAM.csv", 
           np.hstack([subjects,phaseFactor,variabilityFactor,np.matrix(V3).T]), 
           delimiter=",")

# ITC
''' Landing Phase '''
# 7 - 16 - 25 - 40 -100                                                                                         
#l: 5(start) 20(maxForce) 40(lowerForce/stab) 100(end)                                                          
nphases = 5
ntasks = 3
subjects = np.matrix(np.repeat(np.linspace(1,5,5), ntasks*nphases)).T
variabilityFactor = np.matrix([1,2]*nsubjects*nphases*ntasks).T
taskFactor =  np.matrix([1,1,2,2,3,3]*nsubjects*nphases).T
phaseFactor = np.matrix([  4, 4, 4, 4, 4, 4, 13, 13, 13, 13, 13, 13, 20, 20, 20, 20, 20, 20, 40, 40, 40, 40, 40, 40, 97, 97, 97, 97, 97,97]*nsubjects).T


C=[]; V=[];
for i in xrange (len(mconf.traceurs_list)):
    C += [
        LandLM_abs[i].criteria[4],
        LandLM_stab[i].criteria[4],
        LandAM[i].criteria[4],
        LandLM_abs[i].criteria[13],
        LandLM_stab[i].criteria[13],
        LandAM[i].criteria[13],
        LandLM_abs[i].criteria[20],
        LandLM_stab[i].criteria[20],
        LandAM[i].criteria[20],
        LandLM_abs[i].criteria[40],
        LandLM_stab[i].criteria[40],
        LandAM[i].criteria[40],
        LandLM_abs[i].criteria[97],
        LandLM_stab[i].criteria[97],
        LandAM[i].criteria[97],
    ]



''' Display '''
#launch with gepetto viewer
x=land[4]['pinocchio_data']
viewer = Viewer('avatar viewer',avatar0)
#viewer.display(x[7],avatar4.name)
#viewer.display(x[14],avatar4.name)
#viewer.display(x[21],avatar4.name)
#viewer.display(x[40],avatar4.name)
#viewer.display(x[99],avatar4.name)
viewer.addRobot(avatar1)
viewer.addRobot(avatar2)
viewer.addRobot(avatar3)
viewer.addRobot(avatar4)
#viewer.viewer.gui.setBackgroundColor1(viewer.windowID,(255,255,255,0))

#viewer.viewer.gui.setVisibility('world/Melvin/floor','OFF')
#viewer.viewer.gui.setVisibility('world/Cyril/floor','OFF')
#viewer.viewer.gui.setVisibility('world/Michael/floor','OFF')
#viewer.viewer.gui.setVisibility('world/Lucas/floor','OFF')
viewer.viewer.gui.setVisibility('world/Yoan/floor','OFF')



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
    data0x += [JumpLM[i].contributionF[1][:,0]]
    data40x += [JumpLM[i].contributionF[40][:,0]]
    data70x += [JumpLM[i].contributionF[70][:,0]]
    data99x += [JumpLM[i].contributionF[98][:,0]]
    data0y += [JumpLM[i].contributionF[1][:,1]]
    data40y += [JumpLM[i].contributionF[40][:,1]]
    data70y += [JumpLM[i].contributionF[70][:,1]]
    data99y += [JumpLM[i].contributionF[98][:,1]]
    data0z += [JumpLM[i].contributionF[1][:,2]]
    data40z += [JumpLM[i].contributionF[40][:,2]]
    data70z += [JumpLM[i].contributionF[70][:,2]]
    data99z += [JumpLM[i].contributionF[98][:,2]]
    data0xx += [JumpAM[i].contributionF[1][:,3]]
    data40xx += [JumpAM[i].contributionF[40][:,3]]
    data70xx += [JumpAM[i].contributionF[70][:,3]]
    data99xx += [JumpAM[i].contributionF[98][:,3]]
    data0yy += [JumpAM[i].contributionF[1][:,4]]
    data40yy += [JumpAM[i].contributionF[40][:,4]]
    data70yy += [JumpAM[i].contributionF[70][:,4]]
    data99yy += [JumpAM[i].contributionF[98][:,4]]
    data0zz += [JumpAM[i].contributionF[1][:,5]]
    data40zz += [JumpAM[i].contributionF[40][:,5]]
    data70zz += [JumpAM[i].contributionF[70][:,5]]
    data99zz += [JumpAM[i].contributionF[98][:,5]]

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
data7x = []; data16x = []; data30x = []; data40x = []; data99x = []; 
data7y = []; data16y = []; data30y = []; data40y = []; data99y = [];
data7z = []; data16z = []; data30z = []; data40z = []; data99z = [];
data7xx = []; data16xx = []; data30xx = []; data40xx = []; data99xx = [];
data7yy = []; data16yy = []; data30yy = []; data40yy = []; data99yy = [];
data7zz = []; data16zz = []; data30zz = []; data40zz = []; data99zz = [];
for i in xrange (len(mconf.traceurs_list)):   
    data7x += [LandLM_abs[i].contributionF[7][:,0]]
    data16x += [LandLM_abs[i].contributionF[16][:,0]]
    data30x += [LandLM_abs[i].contributionF[30][:,0]]
    data40x += [LandLM_abs[i].contributionF[40][:,0]]
    data99x += [LandLM_abs[i].contributionF[98][:,0]]
    #
    data7y += [LandLM_abs[i].contributionF[7][:,1]]
    data16y += [LandLM_abs[i].contributionF[16][:,1]]
    data30y += [LandLM_abs[i].contributionF[30][:,1]]
    data40y += [LandLM_abs[i].contributionF[40][:,1]]
    data99y += [LandLM_abs[i].contributionF[98][:,1]]
    #
    data7z += [LandLM_abs[i].contributionF[7][:,2]]
    data16z += [LandLM_abs[i].contributionF[16][:,2]]
    data30z += [LandLM_abs[i].contributionF[30][:,2]]
    data40z += [LandLM_abs[i].contributionF[40][:,2]]
    data99z += [LandLM_abs[i].contributionF[98][:,2]]
    #
    data7xx += [LandAM[i].contributionF[7][:,3]]
    data16xx += [LandAM[i].contributionF[16][:,3]]
    data30xx += [LandAM[i].contributionF[30][:,3]]
    data40xx += [LandAM[i].contributionF[40][:,3]]
    data99xx += [LandAM[i].contributionF[98][:,3]]
    #
    data7yy += [LandAM[i].contributionF[7][:,4]]
    data16yy += [LandAM[i].contributionF[16][:,4]]
    data30yy += [LandAM[i].contributionF[30][:,4]]
    data40yy += [LandAM[i].contributionF[40][:,4]]
    data99yy += [LandAM[i].contributionF[98][:,4]]
    #
    data7zz += [LandAM[i].contributionF[7][:,5]]
    data16zz += [LandAM[i].contributionF[16][:,5]]
    data30zz += [LandAM[i].contributionF[30][:,5]]
    data40zz += [LandAM[i].contributionF[40][:,5]]
    data99zz += [LandAM[i].contributionF[98][:,5]]

table_LandMx = np.matrix([np.mean(np.matrix(data7x), 0).A1, 
                          np.mean(np.matrix(data16x), 0).A1, 
                          np.mean(np.matrix(data30x), 0).A1,
                          np.mean(np.matrix(data40x), 0).A1,
                          np.mean(np.matrix(data99x), 0).A1])
table_LandM_stdx = np.matrix([np.std(np.matrix(data7x), 0).A1, 
                              np.std(np.matrix(data16x), 0).A1, 
                              np.std(np.matrix(data30x), 0).A1, 
                              np.std(np.matrix(data40x), 0).A1,
                              np.std(np.matrix(data99x), 0).A1])
table_LandMy = np.matrix([np.mean(np.matrix(data7y), 0).A1, 
                          np.mean(np.matrix(data16y), 0).A1, 
                          np.mean(np.matrix(data30y), 0).A1,
                          np.mean(np.matrix(data40y), 0).A1,
                          np.mean(np.matrix(data99y), 0).A1])
table_LandM_stdy = np.matrix([np.std(np.matrix(data7y), 0).A1, 
                              np.std(np.matrix(data16y), 0).A1, 
                              np.std(np.matrix(data30y), 0).A1,
                              np.std(np.matrix(data40y), 0).A1,
                              np.std(np.matrix(data99y), 0).A1])
table_LandMz = np.matrix([np.mean(np.matrix(data7z), 0).A1, 
                          np.mean(np.matrix(data16z), 0).A1, 
                          np.mean(np.matrix(data30z), 0).A1,
                          np.mean(np.matrix(data40z), 0).A1,
                          np.mean(np.matrix(data99z), 0).A1])
table_LandM_stdz = np.matrix([np.std(np.matrix(data7z), 0).A1, 
                              np.std(np.matrix(data16z), 0).A1, 
                              np.std(np.matrix(data30z), 0).A1,
                              np.std(np.matrix(data40z), 0).A1,
                              np.std(np.matrix(data99z), 0).A1])

table_LandMxx = np.matrix([np.mean(np.matrix(data7xx), 0).A1, 
                           np.mean(np.matrix(data16xx), 0).A1, 
                           np.mean(np.matrix(data30xx), 0).A1,
                           np.mean(np.matrix(data40xx), 0).A1,
                           np.mean(np.matrix(data99xx), 0).A1])
table_LandM_stdxx = np.matrix([np.std(np.matrix(data7xx), 0).A1, 
                               np.std(np.matrix(data16xx), 0).A1, 
                               np.std(np.matrix(data30xx), 0).A1,
                               np.std(np.matrix(data40xx), 0).A1,
                               np.std(np.matrix(data99xx), 0).A1])
table_LandMyy = np.matrix([np.mean(np.matrix(data7yy), 0).A1, 
                           np.mean(np.matrix(data16yy), 0).A1, 
                           np.mean(np.matrix(data30yy), 0).A1,
                           np.mean(np.matrix(data40yy), 0).A1,
                           np.mean(np.matrix(data99yy), 0).A1])
table_LandM_stdyy = np.matrix([np.std(np.matrix(data7yy), 0).A1, 
                               np.std(np.matrix(data16yy), 0).A1, 
                               np.std(np.matrix(data30yy), 0).A1,
                               np.std(np.matrix(data40yy), 0).A1,
                               np.std(np.matrix(data99yy), 0).A1])
table_LandMzz = np.matrix([np.mean(np.matrix(data7zz), 0).A1, 
                           np.mean(np.matrix(data16zz), 0).A1, 
                           np.mean(np.matrix(data30zz), 0).A1,
                           np.mean(np.matrix(data40zz), 0).A1,
                           np.mean(np.matrix(data99zz), 0).A1])
table_LandM_stdzz = np.matrix([np.std(np.matrix(data7zz), 0).A1, 
                               np.std(np.matrix(data16zz), 0).A1, 
                               np.std(np.matrix(data30zz), 0).A1,
                               np.std(np.matrix(data40zz), 0).A1,
                               np.std(np.matrix(data99zz), 0).A1])


np.savetxt("tables/momenta/mean/LandFLMx.csv", table_LandMx, delimiter=",")
np.savetxt("tables/momenta/std/LandFLMx.csv", table_LandM_stdx, delimiter=",")
np.savetxt("tables/momenta/mean/LandFLMy.csv", table_LandMy, delimiter=",")
np.savetxt("tables/momenta/std/LandFLMy.csv", table_LandM_stdy, delimiter=",")
np.savetxt("tables/momenta/mean/LandFLMz.csv", table_LandMz, delimiter=",")
np.savetxt("tables/momenta/std/LandFLMz.csv", table_LandM_stdz, delimiter=",")

np.savetxt("tables/momenta/mean/LandTAMx.csv", table_LandMxx, delimiter=",")
np.savetxt("tables/momenta/std/LandTAMx.csv", table_LandM_stdxx, delimiter=",")
np.savetxt("tables/momenta/mean/LandTAMy.csv", table_LandMyy, delimiter=",")
np.savetxt("tables/momenta/std/LandTAMy.csv", table_LandM_stdyy, delimiter=",")
np.savetxt("tables/momenta/mean/LandTAMz.csv", table_LandMzz, delimiter=",")
np.savetxt("tables/momenta/std/LandTAMz.csv", table_LandM_stdzz, delimiter=",")
















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
