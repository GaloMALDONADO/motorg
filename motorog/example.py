import numpy as np
import paths as lp
import robot_config as rconf
import mocap_config as mconf
from hqp.wrapper import Wrapper
from trajectory_extractor import References
import ucm
import csv

#def setTasks():
LImpulsion = []; AImpulsion = []; Vision = []; Pelvis = []; 
Damping = []; Stiffness = []; StabilityCM = []; StabilityAM = []

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
    ''' Impulsion/Explosivness task is defined with the linear momentum in the Antero-Posterior and Vertical axis'''
    LImpulsion += [ucm.ucmMomentum(trial.human, trial.jump, mask=np.array([True,False,True,False,False,False]))]
    Vucm, Vcm, criteria = LImpulsion[i].getUCMVariances()
    ''' Impulsion task is also defined with the angular momentum around the Antero-Posterior axis'''
    AImpulsion += [ucm.ucmMomentum(trial.human, trial.jump, mask=np.array([False,False,False,False,True,False]))]
    Vucm, Vcm, criteria = AImpulsion[i].getUCMVariances()
    #title = 'CENTER OF MASS DURING JUMP PHASE: '+participantName
    #Impulsion[i].plotUCM( Impulsion[i].Vucm,  Impulsion[i].Vcm,  Impulsion[i].criteria, title)
    ''' Vision task is defined with the joint flexion of the neck '''
    Vision += [ucm.ucmJoint(trial.human, trial.fly, 
                            trial.human.model.getFrameId('neck'), 
                            mask=np.array([False,False,False,True,False,False]))]
    Vucm, Vcm, criteria = Vision[i].getUCMVariances()
    ''' Pelvis task is defined with the joint flexion of the pelvis '''
    Pelvis += [ucm.ucmJoint(trial.human, trial.fly, 
                            trial.human.model.getFrameId('ground_pelvis'), 
                            mask=np.array([False,False,False,True,False,False]))]
    Vucm, Vcm, criteria = Pelvis[i].getUCMVariances()
    ''' Preparation to land is defined with the variance of joints before IC with the ground'''
    ''' Damping and reducing GRFs task is defined with the linear momentum '''
    Damping += [ucm.ucmMomentum(trial.human, trial.jump, mask=np.array([False,False,True,False,False,False]))]
    Vucm, Vcm, criteria = Damping[i].getUCMVariances()
    ''' Landing stiffness through the Z displacement of the center of mass '''
    Stiffness += [ucm.ucmCoM(trial.human, trial.land, mask=np.array([False,False,True]))]
    Vucm, Vcm, criteria = Stiffness[i].getUCMVariances()
    ''' Stability task is defined with the center of mass in X and Y'''
    StabilityCM += [ucm.ucmCoM(trial.human, trial.land, mask=np.array([True,True,False]))]
    Vucm, Vcm, criteria = StabilityCM[i].getUCMVariances()
    ''' Angular stability task is also defined with the ang momentum around Antero-Posterior axis'''
    StabilityAM += [ucm.ucmMomentum(trial.human, trial.land, mask=np.array([False,False,False,False,True,False]))]
    Vucm, Vcm, criteria = StabilityAM[i].getUCMVariances()
    ''' The dissipation task is defined throught the energy of the centero of mass '''


# prepare files for R    
nsubjects = 5; nphases = 3;

''' Impulsion Phase '''
ntasks = 2
subjects = np.matrix(np.repeat(np.linspace(1,5,5), ntasks*nphases)).T 
phaseFactor = np.matrix([  1, 1, 50, 50, 100, 100]*nsubjects).T
taskFactor =  np.matrix([1,2]*nsubjects*nphases).T

VU = []; VO=[]; C=[];
for i in xrange (len(mconf.traceurs_list)):
    VU += [LImpulsion[i].Vucm[0],
           AImpulsion[i].Vucm[0],
           LImpulsion[i].Vucm[50],
           AImpulsion[i].Vucm[50],
           LImpulsion[i].Vucm[99],
           AImpulsion[i].Vucm[99]]

    VO += [LImpulsion[i].Vcm[0],
           AImpulsion[i].Vcm[0],
           LImpulsion[i].Vcm[50],
           AImpulsion[i].Vcm[50],
           LImpulsion[i].Vcm[99],
           AImpulsion[i].Vcm[99]]

    C += [LImpulsion[i].criteria[0],
          AImpulsion[i].criteria[0],
          LImpulsion[i].criteria[50],
          AImpulsion[i].criteria[50],
          LImpulsion[i].criteria[99],
          AImpulsion[i].criteria[99]]

np.savetxt("TableVucmImpulse.csv", 
           np.hstack([subjects,phaseFactor,taskFactor,np.matrix(VU).T]), 
           delimiter=",")
np.savetxt("TableVortImpulse.csv", 
           np.hstack([subjects,phaseFactor,taskFactor,np.matrix(VO).T]), 
           delimiter=",")
np.savetxt("TableCriteriaImpulse.csv", 
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

''' Landing Phase '''
ntasks = 4
subjects = np.matrix(np.repeat(np.linspace(1,5,5), ntasks*nphases)).T 
phaseFactor = np.matrix([  1, 1, 1, 1, 50, 50, 50, 50, 100, 100, 100, 100]*nsubjects).T
taskFactor =  np.matrix([1,2,3,4]*nsubjects*nphases).T

VU = []; VO=[]; C=[];
for i in xrange (len(mconf.traceurs_list)):
    VU += [Damping[i].Vucm[10],
           Stiffness[i].Vucm[10],
           StabilityCM[i].Vucm[10],
           StabilityAM[i].Vucm[10],          
           Damping[i].Vucm[55],
           Stiffness[i].Vucm[55],
           StabilityCM[i].Vucm[55],
           StabilityAM[i].Vucm[55],
           Damping[i].Vucm[99],
           Stiffness[i].Vucm[99],
           StabilityCM[i].Vucm[99],
           StabilityAM[i].Vucm[99]]

    VO += [Damping[i].Vcm[10],
           Stiffness[i].Vcm[10],
           StabilityCM[i].Vcm[10],
           StabilityAM[i].Vcm[10],          
           Damping[i].Vcm[55],
           Stiffness[i].Vcm[55],
           StabilityCM[i].Vcm[55],
           StabilityAM[i].Vcm[55],
           Damping[i].Vcm[99],
           Stiffness[i].Vcm[99],
           StabilityCM[i].Vcm[99],
           StabilityAM[i].Vcm[99]]

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

'''
ntasks = 6
nsubjects = 5
nphases = 3
subjects = np.matrix(np.repeat(np.linspace(1,5,5), ntasks*nphases)).T 
phaseFactor = np.matrix([  1, 1,  1,  1,  1,  1,
                          50, 50, 50, 50, 50, 50,
                           100,100,100,100,100,100]*nsubjects).T
taskFactor =  np.matrix([1,2,3,4,5,6]*nsubjects*nphases).T

VU = []; VO=[]; C=[];
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
'''
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

