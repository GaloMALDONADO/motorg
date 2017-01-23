import numpy as np
import paths as lp
import robot_config as rconf
import mocap_config as mconf
from hqp.wrapper import Wrapper
from trajectory_extractor import References
from tools import *



participantName = 'Lucas'
robot = Wrapper(lp.models_path+'/'+participantName+'.osim', lp.mesh_path, participantName, True)
robot.q0 = rconf.half_sitting

idxTraceur = mconf.traceurs_list.index('Lucas')
trial = References(mconf.traceurs_list[idxTraceur])
trial.loadModel()
trial.display()
trial.getTrials()


''' Get reference configuration 
    Qi_hat = mean(q(t)) 
'''
jumpMeanConf, jumpStdConf = meanConfiguration(trial.jump)

''' Get reference trajectories
    Xi_hat = mean(x(t))
    Reference tasks(trajectories)
    JUMP = CoM trajectory, lower-limb impulsion, maximize angular momentum with arms
    FLY = neck orientation                                                                                
    LAND = stability(CoMx,CoMy), damping(CoMz), posture(IC:i.e. foot)
'''

x=[]
for i in xrange (len(trial.jump)):
    x += [robot.record(trial.jump[i]['pinocchio_data'],'com',0)[0]]

jumpMeanCoM, jumpStdCoM = meanVar(np.array(x))
#x = jumpMeanCoM[:,0]

