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


participantName = mconf.traceurs_list[2]
idxTraceur = mconf.traceurs_list.index(participantName)
model_path = lp.models_path+'/'+participantName+'.osim'
mesh_path = lp.mesh_path
robot1 = Wrapper(model_path, mesh_path, participantName+'1', True)
robot2 = Wrapper(model_path, mesh_path, participantName+'2', True)
robot3 = Wrapper(model_path, mesh_path, participantName+'3', True)
robot4 = Wrapper(model_path, mesh_path, participantName+'4', True)

jump = np.load('./motions/'+participantName+'_jump.npy')
land = np.load('./motions/'+participantName+'_land.npy')
trial=4
x1=jump[trial]['pinocchio_data']
x2=land[trial]['pinocchio_data']


viewer = Viewer('Robot 1',robot1)
viewer.setVisibility("Melvin1/floor", "OFF")
viewer.viewer.gui.setBackgroundColor1(viewer.windowID,(255,255,255,1))
viewer.viewer.gui.setBackgroundColor2(viewer.windowID,(255,255,255,1))
viewer.display(x1[3],robot1.name)


position = se3.SE3.Identity()
position.translation += np.matrix([-.5,-0.98,1.]).T
robotNode = 'world/'+robot1.name+'/'
filename = lp.objects+'/cage_paper.obj'
viewer.viewer.gui.addMesh(robotNode+'cage', filename)
viewer.placeObject(robotNode+'cage', position, True)
viewer.viewer.gui.deleteNode('world/Melvin1/globalCoM',True)

viewer.addRobot(robot2)
viewer.setVisibility("Melvin2/floor", "OFF")
viewer.viewer.gui.deleteNode('world/Melvin2/globalCoM',True)
viewer.display(x1[99],robot2.name)

viewer.addRobot(robot3)
viewer.setVisibility("Melvin3/floor", "OFF")
viewer.viewer.gui.deleteNode('world/Melvin3/globalCoM',True)
viewer.display(x2[3],robot3.name)

viewer.addRobot(robot4)
viewer.setVisibility("Melvin4/floor", "OFF")
viewer.viewer.gui.deleteNode('world/Melvin4/globalCoM',True)
viewer.display(x2[99],robot4.name)

color=(0.7,0.7,0.7,1)
color2=(1,0.7,0.7,1)
color3=(1,0.7,0.7,1)
viewer.viewer.gui.setColor('world/Melvin1',color)
viewer.viewer.gui.setColor('world/Melvin2',color2)
viewer.viewer.gui.setColor('world/Melvin3',color)
viewer.viewer.gui.setColor('world/Melvin4',color2)
