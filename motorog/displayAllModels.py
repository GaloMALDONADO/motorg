import time
import os
import sys
import subprocess
import numpy as np
import mocap_config as mconf
from hqp.wrapper import Wrapper
from hqp.viewer_utils import Viewer
import paths as lp

# call the gepetto viewer server
gvs = subprocess.Popen(["./gepetto-viewer.sh","&"])
print 'Loading the viewer ...'
time.sleep(2)

for i in xrange (len(mconf.traceurs_list)):
    name = mconf.traceurs_list[i]
    model_path = lp.models_path+'/'+name+'.osim'
    mesh_path = lp.mesh_path
    if i == 0:
        r = Wrapper(model_path, mesh_path, name, True)
        viewer = Viewer(name, r)
    else:
        r = Wrapper(model_path, mesh_path, name, True)
        viewer.addRobot(r)
        
    r.q[2] = 1
    r.q[0] = i*0.5
    viewer.display(r.q, name)

viewer.viewer.gui.setBackgroundColor1(viewer.windowID,(255,255,255,1))
viewer.viewer.gui.setBackgroundColor2(viewer.windowID,(255,255,255,1))
