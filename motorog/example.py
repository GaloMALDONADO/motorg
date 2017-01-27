import numpy as np
import paths as lp
import robot_config as rconf
import mocap_config as mconf
from hqp.wrapper import Wrapper
from trajectory_extractor import References
import ucm
import csv

#def setTasks():
LImpulsion = []; AImpulsion = []; Vision = []; Damping = []; StabilityCM = []; StabilityAM = []

def getTrials(i):
    participantName = mconf.traceurs_list[i]
    idxTraceur = mconf.traceurs_list.index(participantName)
    trial = References(mconf.traceurs_list[idxTraceur])
    trial.loadModel()
    trial.display()
    trial.getTrials()
    return trial

for i in xrange (len(mconf.traceurs_list)):
    trial = getTrials(i)
    ''' Impulsion task is defined with the linear momentum '''
    LImpulsion += [ucm.ucmMomentum(trial.human, trial.jump, mask=np.array([True,True,True,False,False,False]))]
    Vucm, Vcm, criteria = LImpulsion[i].getUCMVariances()
    ''' Impulsion task is defined with the angular momentum '''
    AImpulsion += [ucm.ucmMomentum(trial.human, trial.jump, mask=np.array([True,True,True,False,False,False]))]
    Vucm, Vcm, criteria = AImpulsion[i].getUCMVariances()
    #title = 'CENTER OF MASS DURING JUMP PHASE: '+participantName
    #Impulsion[i].plotUCM( Impulsion[i].Vucm,  Impulsion[i].Vcm,  Impulsion[i].criteria, title)
    ''' Vision task is defined with the joint flexion '''
    Vision += [ucm.ucmJoint(trial.human, trial.fly, 
                            trial.human.model.getFrameId('neck'), 
                            mask=np.array([False,False,False,True,False,False]))]
    Vucm, Vcm, criteria = Vision[i].getUCMVariances()
    ''' Damping task is defined with the linear momentum '''
    Damping += [ucm.ucmMomentum(trial.human, trial.jump, mask=np.array([True,True,True,False,False,False]))]
    Vucm, Vcm, criteria = Damping[i].getUCMVariances()
    ''' Stability task is defined with the center of mass '''
    StabilityCM += [ucm.ucmCoM(trial.human, trial.land, mask=np.array([True,True,False]))]
    Vucm, Vcm, criteria = StabilityCM[i].getUCMVariances()
    ''' Stability task is also defined with the ang momentum '''
    StabilityAM += [ucm.ucmMomentum(trial.human, trial.land, mask=np.array([False,False,False,True,True,True]))]
    Vucm, Vcm, criteria = StabilityAM[i].getUCMVariances()



# prepare files for R    
# 5 participants * 2 tasks * 3 phases inside landing
ntasks = 6
nsubjects = 5
nphases = 3
subjects = np.matrix(np.repeat(np.linspace(1,5,5), ntasks*nphases)).T 
phaseFactor = np.matrix([  1, 1,  1,  1,  1,  1,
                          50, 50, 50, 50, 50, 50,
                           100,100,100,100,100,100]*nsubjects).T
taskFactor =  np.matrix([1,2,3,4,5,6]*nsubjects*nphases).T

VU = []; VO=[]; C=[]
for i in xrange (len(mconf.traceurs_list)):
    VU += [LImpulsion[i].Vucm[0],
           AImpulsion[i].Vucm[0],

           Vision[i].Vucm[0],

           Damping[i].Vucm[10],
           StabilityCM[i].Vucm[10],
           StabilityAM[i].Vucm[10],          

           LImpulsion[i].Vucm[50],
           AImpulsion[i].Vucm[50],
           Vision[i].Vucm[50],
           Damping[i].Vucm[55],
           StabilityCM[i].Vucm[55],
           StabilityAM[i].Vucm[55],
           LImpulsion[i].Vucm[99],
           AImpulsion[i].Vucm[99],
           Vision[i].Vucm[99],
           Damping[i].Vucm[99],
           StabilityCM[i].Vucm[99],
           StabilityAM[i].Vucm[99]]

    VO += [LImpulsion[i].Vcm[0],
           AImpulsion[i].Vcm[0],
           Vision[i].Vcm[0],
           Damping[i].Vcm[10],
           StabilityCM[i].Vcm[10],
           StabilityAM[i].Vcm[10],          
           LImpulsion[i].Vcm[50],
           AImpulsion[i].Vcm[50],
           Vision[i].Vcm[50],
           Damping[i].Vcm[55],
           StabilityCM[i].Vcm[55],
           StabilityAM[i].Vcm[55],
           LImpulsion[i].Vcm[99],
           AImpulsion[i].Vcm[99],
           Vision[i].Vcm[99],
           Damping[i].Vcm[99],
           StabilityCM[i].Vcm[99],
           StabilityAM[i].Vcm[99]]

    C += [LImpulsion[i].criteria[0],
          AImpulsion[i].criteria[0],
          Vision[i].criteria[0],
          Damping[i].criteria[10],
          StabilityCM[i].criteria[10],
          StabilityAM[i].criteria[10],          
          LImpulsion[i].criteria[50],
          AImpulsion[i].criteria[50],
          Vision[i].criteria[50],
          Damping[i].criteria[55],
          StabilityCM[i].criteria[55],
          StabilityAM[i].criteria[55],
          LImpulsion[i].criteria[99],
          AImpulsion[i].criteria[99],
          Vision[i].criteria[99],
          Damping[i].criteria[99],
          StabilityCM[i].criteria[99],
          StabilityAM[i].criteria[99]]

TableVucm = np.hstack([subjects,phaseFactor,taskFactor,np.matrix(VU).T])
TableVort = np.hstack([subjects,phaseFactor,taskFactor,np.matrix(VO).T])
TableCriteria = np.hstack([subjects,phaseFactor,taskFactor,np.matrix(C).T])

np.savetxt("TableVucm.csv", TableVucm, delimiter=",")
np.savetxt("TableVort.csv",TableVort, delimiter=",")
np.savetxt("TableCriteria.csv", TableCriteria, delimiter=",")

# TODO: tables for each phase of the movement
#posture IC : variance between subjects
#play motion
#trial.playTrial(rep=0,dt=0.0025,stp=1,start=0,end=-1)


''' Get reference trajectories
    Xi_hat = mean(x(t))
    Reference tasks(trajectories)
    JUMP = CoM trajectory, lower-limb impulsion, maximize angular momentum with arms
    FLY = neck orientation                                                                                
    LAND = stability(CoMx,CoMy), damping(CoMz), posture(IC:i.e. foot)
'''

