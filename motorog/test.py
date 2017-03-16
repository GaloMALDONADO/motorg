import pinocchio as se3
robot=robots[4]
se3.computeAllTerms(robot.model,robot.data, robot.q, robot.v)

vardq = 0.0001
varddq = 0.
dq = np.matrix(np.ones(robot.nv)*vardq)
ddq = np.matrix(np.ones(robot.nv)*varddq)
frame_id = IDX_NECK #25

#a
x_dot_dot = robot.frameAcceleration(frame_id)
#b
J = robot.frameJacobian(robot.q.copy(),frame_id, True)
v_frame = robot.frameVelocity(frame_id).copy()
drift = x_dot_dot.copy()
drift.linear += np.cross(v_frame.angular.T, v_frame.linear.T).T
J_dot = drift.vector*np.linalg.pinv(robot.v).T
q_dot = robot.v.copy()
q_dot_dot = robot.a.copy()

b=(J_dot+J)*dq.T + J*ddq.T
b2=J*dq.T + J*ddq.T
b3=(2*J_dot)*dq.T + J*ddq.T

robot.v += dq
robot.a += ddq 
se3.computeAllTerms(robot.model,robot.data, robot.q, robot.v)
x_dot_dot_next = robot.frameAcceleration(frame_id).copy()
a=x_dot_dot.vector-x_dot_dot_next.vector
