'''
Program to test partial derivatives of Ag (PLOSCB17)
'''


#---- dJ/dq
# q_dot.T dJ/dq = J_dot
import bmtools.processing as bm
local = True
h=1e-8
robot = robots[0]
model = robot.model.copy()
data = robot.data
q0 = robot.q.copy()
se3.computeJacobiansTimeVariation(robot.model, robot.data, robot.q, robot.v)
for joint in range(1,model.nbodies):
    justin = se3.getJacobianTimeVariation(robot.model, robot.data, joint, local)
    tensor = bm.get_dJi_dq(model, data, q0, joint, h, local)
    prod = bm.prodVecTensor(robot.v.A1, tensor)
    diff = np.linalg.norm(justin-prod)
    print joint,diff


#---- dA/dq
# q_dot.T dA/dq = A_dot
import bmtools.processing as bm
h=1e-8
robot = robots[0]
model = robot.model.copy()
data = robot.data
q0 = robot.q.copy()
se3.forwardKinematics(model, data, q0)
se3.centerOfMass(model, data, q0)
se3.dccrba(robot.model, robot.data, robot.q, robot.v)
justin = np.nan_to_num(data.dAg)
tensor = bm.get_dA_dq(model, data, q0, robot.v, h)
prod = np.matrix(bm.prodVecTensor(robot.v.A1, tensor))
diff = np.linalg.norm(justin-prod)
print diff


#---- d(A_dot)/dq
import bmtools.processing as bm
h=1e-8
robot = robots[0]
model = robot.model.copy()
data = robot.data
N = 10
qrand = []
ddAg = []
dAgp = [] 
v = robot.v.copy()
for t in range(0, N):
    q = np.matrix( np.zeros(robot.nq)).T
    q[t] = 1
    qrand += [q]
    se3.forwardKinematics(model, data, q.copy(), v.copy())
    se3.centerOfMass(model, data, q.copy())
    se3.dccrba(robot.model, robot.data, q, v.copy())
    T = bm.get_ddA_dq(model, data, q, v.copy(), h)
    ddAg += [np.matrix(bm.prodVecTensor(robot.v.A1, T))]
    dAgp += [np.nan_to_num(data.dAg)]

ddAgp = bm.diffM(dAgp, np.arange(N))

print ddAg[4][:,0]
print ddAgp[4][:,0]


#--- d(A_dot)/d(q_dot)
#---- d(A_dot)/dq
import bmtools.processing as bm
h=1e-8
robot = robots[0]
model = robot.model.copy()
data = robot.data
N = 10
qrand = []
ddAg = []
dAgp = [] 
v = robot.v.copy()
a = robot.a.copy()
for t in range(0, N):
    q = np.matrix( np.zeros(robot.nq)).T
    q[t] = 1
    qrand += [q]
    se3.forwardKinematics(model, data, q.copy(), v.copy())
    se3.centerOfMass(model, data, q.copy())
    se3.dccrba(robot.model, robot.data, q, v.copy())
    T = bm.get_ddA_dq(model, data, q, v.copy(), h)
    ddAg += [np.matrix(bm.prodVecTensor(robot.a.A1, T))]
    dAgp += [np.nan_to_num(data.dAg)]

ddAgp = bm.diffM(dAgp, np.arange(N))

print ddAg[4][:,0]
print ddAgp[4][:,0]
