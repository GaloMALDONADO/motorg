import numpy as np
import paths as lp
import robot_config as rconf
import mocap_config as mconf
from hqp.wrapper import Wrapper
from trajectory_extractor import References
import ucm


participantName = 'Lucas'
robot = Wrapper(lp.models_path+'/'+participantName+'.osim', lp.mesh_path, participantName, True)
idxTraceur = mconf.traceurs_list.index(participantName)
trial = References(mconf.traceurs_list[idxTraceur])
trial.loadModel()
trial.display()
trial.getTrials()

taskCoM = ucm.ucmCoM(robot, trial.jump)
Vcm, Vucm, criteria =taskCoM.getUCMVariances()
title = 'CENTER OF MASS DURING JUMP PHASE'
taskCoM.plotUCM(Vucm, Vcm, criteria, title)


''' Get reference trajectories
    Xi_hat = mean(x(t))
    Reference tasks(trajectories)
    JUMP = CoM trajectory, lower-limb impulsion, maximize angular momentum with arms
    FLY = neck orientation                                                                                
    LAND = stability(CoMx,CoMy), damping(CoMz), posture(IC:i.e. foot)
'''

