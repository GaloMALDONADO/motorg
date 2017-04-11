'''
This script is useful to be run only once
It parses and stores the motion phases using numpy 
These motions can after be retrieved using np.load function
'''
import numpy as np
import mocap_config as mconf
from hqp.wrapper import Wrapper
from trajectory_extractor import References


for i in xrange (len(mconf.traceurs_list)):
    participantName = mconf.traceurs_list[i]
    idxTraceur = mconf.traceurs_list.index(participantName)
    trial = References(mconf.traceurs_list[idxTraceur])
    trial.loadModel()
    trial.display()
    trial.getTrials()
    np.save('./motions/'+participantName+'_jump.npy', trial.jump)
    np.save('./motions/'+participantName+'_fly.npy', trial.fly)
    np.save('./motions/'+participantName+'_land.npy', trial.land)
    np.save('./motions/'+participantName+'_jump_dq.npy', trial.jumpdq)
    np.save('./motions/'+participantName+'_fly_dq.npy', trial.flydq)
    np.save('./motions/'+participantName+'_land_dq.npy', trial.landdq)
    np.save('./motions/'+participantName+'_jump_ddq.npy', trial.jumpddq)
    np.save('./motions/'+participantName+'_fly_ddq.npy', trial.flyddq)
    np.save('./motions/'+participantName+'_land_ddq.npy', trial.landddq)
    

    
