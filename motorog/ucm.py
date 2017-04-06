import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
import pinocchio as se3
import tools 

#from bmtools.filters import filtfilt_butter

class UCM:
    def __init__(self, robot):
        self.robot = robot
        self.name = robot.name
        self.nq = robot.nq
        self.nv = robot.nv
        self.tf = 100
        self.time = np.linspace(1,100,100)
        self.dt = 0.0025
        self.fs = 400
        self.cutoff = 30
        self.filter_order = 4

    def nullspace(self, Jq):
        ''' Computes the null space from SVD
        returns the nulls space and the rank
        '''
        def getNullSpaceAndRank(A, eps = 1e-15):
            U, s, V = np.linalg.svd(A)
            rank = (s>=eps).sum()
            nullspace = V[rank:].T.copy()
            return nullspace, rank

        N=[]
        for i in xrange(100):
            P=np.matrix(np.identity(42)) - (np.linalg.pinv(Jq[i])*Jq[i])
            N.append(P)

        projector = np.array(N)
        self.projector = projector
        #print np.sum((np.matrix(projector[1])*np.matrix(projector[1]))-np.matrix(projector[1]))
        return projector
    
    def updateAll(self,q,v,a):
        se3.computeAllTerms(self.robot.model, self.robot.data, q, v)
        self.robot.q=q
        self.robot.v=v
        self.robot.a=a
        self.robot.tau = se3.rnea(self.robot.model, self.robot.data, q, v, a)

    def getReferenceConfigurations(self, motions):
        '''
        meanConf, stdConf, data = meanConfiguration(motions)
        '''
        (self.time_mean, self.time_std, self.time_data) = tools.meanTime(motions)
        (self.q_mean, self.q_std, self.q_data) = tools.meanConfiguration(self.robot,motions)
        (self.dq_mean, self.dq_std, self.dq_data) = tools.meanVelocities(self.robot.model, 
                                                                         self.q_data, 
                                                                         self.time_data,
                                                                         self.cutoff, 
                                                                         self.fs, 
                                                                         self.filter_order)
        (self.ddq_mean, self.ddq_std, self.ddq_data) = tools.meanAccelerations(self.dq_data, 
                                                                               self.time_data,
                                                                               self.cutoff, 
                                                                               self.fs, 
                                                                               self.filter_order)
        
    
    def getMeanTime(self, motions):
        ''' computes the mean time and the std'''
        x=[]
        for i in xrange (self.repNo):
            x += [motions[i]['time']]
        meanT =  np.mean(x,0)
        stdT = np.std(x,0)
        return meanT.squeeze(), stdT.squeeze()

    def differentiate(self, q1, q2):
        return se3.differentiate(self.robot.model, np.asmatrix(q1), np.asmatrix(q2))

    def getVelocity(self, Q, T, filterFlag=True):
        Vi = []
        for i in range(1,len(Q)):
            dt = T[i]-T[i-1]
            Vi += [self.differentiate(Q[i-1],Q[i])/dt]        
        Vi.insert(0,Vi[0])
        V = np.matrix(np.array(Vi))
        if filterFlag is True:
            Vf = tools.filterMatrix(V, self.cutoff, self.fs, self.filter_order)
            return Vf
        else:
            return V

    def getAcceleration(self, V, T, filterFlag=True):
        Ai = []
        for i in range(1,len(V)):
            dt = T[i]-T[i-1]
            Ai += [np.asmatrix(np.gradient(V[i].A1, dt))]
        Ai.insert(0,Ai[0])
        A = np.matrix(np.array(Ai))
        if filterFlag is True:
            Af = tools.filterMatrix(A, self.cutoff, self.fs, self.filter_order)
            return Af
        else:
            return A


    def varianceFromManifolds(self, Q_hat, Qi, Pi, normUCM, normCM, criteria='log'):
        ''' Vcm, Vucm, c = varianceFromManifolds(Q_hat, Qi, Pi) 
        Return a normalized array of the variance of the CM and the UCM, and the hypothesis test result
        Param-in :
        Q_hat = mean joint configuration (1x100)
        Qi = matrix of joint configurations (100, joints_dof, nTrials)
        Ni = list of size (100) containing the nullspace (1 x joints_dof- task_dof)
        norm UCM = value to which the variance of UCM is normalized. Default is 1
        norm CM = value to which the variance of CM is normalized. Default is 1 
        normaly the value is calculated as : # of dof involved (joints and tasks) * # of trials
        '''
        
        Vucm = []; Vcm =[];
        ntrials = np.shape(Qi)[2]

        for i in xrange(100):
            v_ucm = 0; v_cm = 0;
            for trls in xrange(ntrials):
                #devq = np.matrix(Q_hat[i] - Qi[i,:,trls]).T
                #devq = se3.differentiate(self.robot.model, np.matrix(Qi[i,:,trls]), Q_hat[0])
                devq = (Qi[i,:,trls]-Q_hat[i])
                #print devq.shape
                # the deviations from the mean trajectories in joint-space are projected onto the null-space
                #ucm = (np.matrix(Ni[trls]) * np.matrix(Ni[trls]).T) * devq.copy()
                ucm = np.matrix(Pi[i]) * devq.copy().T
                # and onto the range space (orthogonal to the null space)
                # which is a lineat appoximation of the controlled manifold
                cm = devq.copy().T - ucm.copy()
                # the variance per degree of freedom of the projected deviations is
                #v_ucm += np.square(np.linalg.norm(ucm))
                #v_cm  += np.square(np.linalg.norm(cm))
                v_ucm += np.linalg.norm(ucm)
                v_cm  += np.linalg.norm(cm)
                

            Vucm.append(v_ucm)
            Vcm.append (v_cm)

        Vcm_n = np.array(Vcm)/np.float64(normCM)
        Vucm_n = np.array(Vucm)/np.float64(normUCM)
        if criteria is 'log':
            c = np.log(Vucm_n/Vcm_n)
        else:
            c = Vucm_n/Vcm_n
        return Vucm_n, Vcm_n, c


    '''
    Plot the task
    '''
    def plotTask(self, var, X, X_std, Xi, title, deg=True):
        if deg is True:
            X[:,3:6] = np.rad2deg(X[:,3:6])
            X_std[:,3:6] = np.rad2deg(X_std[:,3:6])
            Xi[:,3:6] = np.rad2deg(Xi[:,3:6])
            sangle='degrees'
        else:
                sangle='rad'
        ntrials = np.shape(Xi)[2]
        legends=[]
        legends.append('mean')
        legends.append('mean+std')
        legends.append('mean-std')
        plt.ion()
        if var is 'com':
            fig = plt.figure()
            fig.canvas.set_window_title(title)
            ax = fig.add_subplot ('311')
            plt.title('Medial-Lateral center of Mass during jump [m]')
            ax.plot(self.time, X[:,1],'r', linewidth=3.0)
            ax.plot(self.time, X[:,1]+X_std[:,0],'--r', linewidth=3.0)
            ax.plot(self.time, X[:,1]-X_std[:,0],'--r', linewidth=3.0)
            color=iter(cm.rainbow(np.linspace(0,1,ntrials)))
            for trls in xrange(ntrials):
                c = next(color)
                ax.plot(self.time,Xi[:, 1, trls], color=c, linewidth=1.0)
                legends.append('trials'+str(trls))
            plt.ylabel('m')
            
            ax = fig.add_subplot ('312')
            plt.title('Antero-Posterior center of Mass during jump [m]')
            ax.plot(self.time, X[:,0],'r', linewidth=3.0)
            ax.plot(self.time, X[:,0]+X_std[:,0],'--r', linewidth=3.0)
            ax.plot(self.time, X[:,0]-X_std[:,0],'--r', linewidth=3.0)
            color=iter(cm.rainbow(np.linspace(0,1,ntrials)))
            for trls in xrange(ntrials):
                c = next(color)
                ax.plot(self.time,Xi[:, 0, trls], color=c, linewidth=1.0)
            plt.ylabel('m')

            ax = fig.add_subplot ('313')
            plt.title('Vertical center of Mass during jump [m]')
            ax.plot(self.time,X[:,2], 'r', linewidth=3.0)
            ax.plot(self.time,X[:,2]+X_std[:,2],'--r', linewidth=3.0)
            ax.plot(self.time,X[:,2]-X_std[:,2],'--r', linewidth=3.0)
            color=iter(cm.rainbow(np.linspace(0,1,ntrials)))
            for trls in xrange(ntrials):
                c = next(color)
                ax.plot(self.time,Xi[:, 2, trls], color=c, linewidth=1.0)
            plt.xlabel('% of phase')
            plt.ylabel('m')

            # Shrink current axis's height by 10% on the bottom                                                  
            box = ax.get_position()
            ax.set_position([box.x0, box.y0 + box.height * 0.1,
                              box.width, box.height * 0.9])
            ax.legend(legends,loc='upper center', bbox_to_anchor=(0.5, -0.2),
                      ncol=7, fancybox=True, shadow=True)
        if var is 'joint':
            fig = plt.figure ()
            fig.canvas.set_window_title(title)

            ax = fig.add_subplot ('323')
            plt.title('Y Position [m]')
            ax.plot(self.time, X[:,0],'r', linewidth=3.0)
            ax.plot(self.time, X[:,0]+X_std[:,0],'--r', linewidth=3.0)
            ax.plot(self.time ,X[:,0]-X_std[:,0],'--r', linewidth=3.0)
            color=iter(cm.rainbow(np.linspace(0,1,ntrials)))
            for trls in xrange(ntrials):
                c = next(color)
                ax.plot(self.time, Xi[:, 0, trls], color=c, linewidth=1.00)
                legends.append('trials'+str(trls))

            ax = fig.add_subplot ('321')
            plt.title('X Position [m]')
            ax.plot(self.time, X[:,1],'r', linewidth=3.0)
            ax.plot(self.time, X[:,1]+X_std[:,1],'--r', linewidth=3.0)
            ax.plot(self.time, X[:,1]-X_std[:,1],'--r', linewidth=3.0)
            color=iter(cm.rainbow(np.linspace(0,1,ntrials)))
            for trls in xrange(ntrials):
                c = next(color)
                ax.plot(self.time, Xi[:, 0, trls], color=c, linewidth=1.00)
                legends.append('trials'+str(trls))
            
            ax = fig.add_subplot ('321')
            plt.title('X Position [m]')
            ax.plot(self.time, X[:,1],'r', linewidth=3.0)
            ax.plot(self.time, X[:,1]+X_std[:,1],'--r', linewidth=3.0)
            ax.plot(self.time, X[:,1]-X_std[:,1],'--r', linewidth=3.0)
            color=iter(cm.rainbow(np.linspace(0,1,ntrials)))
            for trls in xrange(ntrials):
                c = next(color)
                ax.plot(self.time,Xi[:, 1, trls], color=c, linewidth=1.0)

            ax = fig.add_subplot ('325')
            plt.title('Z Position  [m]')
            ax.plot(self.time, X[:,2],'r', linewidth=3.0)
            ax.plot(self.time, X[:,2]+X_std[:,2],'--r', linewidth=3.0)
            ax.plot(self.time, X[:,2]-X_std[:,2],'--r', linewidth=3.0)
            color=iter(cm.rainbow(np.linspace(0,1,ntrials)))

            ax = fig.add_subplot ('324')
            plt.title('Rot Y'+sangle)
            ax.plot(self.time, X[:,3],'r', linewidth=3.0)
            ax.plot(self.time, X[:,3]+X_std[:,3],'--r', linewidth=3.0)
            ax.plot(self.time ,X[:,3]-X_std[:,3],'--r', linewidth=3.0)
            color=iter(cm.rainbow(np.linspace(0,1,ntrials)))
            for trls in xrange(ntrials):
                c = next(color)
                ax.plot(self.time, Xi[:, 3, trls], color=c, linewidth=1.0)

            ax = fig.add_subplot ('322')
            plt.title('Rot X'+sangle)
            ax.plot(self.time, X[:,4],'r', linewidth=3.0)
            ax.plot(self.time, X[:,4]+X_std[:,4],'--r', linewidth=3.0)
            ax.plot(self.time, X[:,4]-X_std[:,4],'--r', linewidth=3.0)
            color=iter(cm.rainbow(np.linspace(0,1,ntrials)))
            for trls in xrange(ntrials):
                c = next(color)
                ax.plot(self.time, Xi[:, 4, trls], color=c, linewidth=1.0)

            ax = fig.add_subplot ('326')
            plt.title('Rot Z'+sangle)
            ax.plot(self.time, X[:,5],'r', linewidth=3.0)
            ax.plot(self.time, X[:,5]+X_std[:,5],'--r', linewidth=3.0)
            ax.plot(self.time, X[:,5]-X_std[:,5],'--r', linewidth=3.0)
            color=iter(cm.rainbow(np.linspace(0,1,ntrials)))
            for trls in xrange(ntrials):
                c = next(color)
                ax.plot(self.time, Xi[:, 5, trls], color=c, linewidth=1.0)

            # Shrink current axis's height by 10% on the bottom                                                  
            box = ax.get_position()
            ax.set_position([box.x0, box.y0 + box.height * 0.1,
                              box.width, box.height * 0.9])
            ax.legend(legends,loc='upper center', bbox_to_anchor=(0., -0.2),
                      ncol=7, fancybox=True, shadow=True)


    '''
    Plot the uncontrolled manifold 
    '''
    def plotUCM(self,title='Ucontrolled Manifold Analysis'):#,Vucm,Vcm,criteria, title, degree=True)
        plt.ion()
        fig = plt.figure ()
        fig.canvas.set_window_title(title)
        ax = fig.add_subplot ('311')
        plt.title('Uncontrolled Manifold')
        plt.ylabel('variance')
        ax.plot(self.time, self.Vucm, 'b', linewidth=3.0)
        ax = fig.add_subplot ('312')
        plt.title('Controlled Manifold')
        plt.ylabel('variance')
        ax.plot(self.time, self.Vcm, 'r', linewidth=3.0)
        ax = fig.add_subplot ('313')
        plt.title('Criteria')
        ax.plot(self.time, self.criteria, 'k', linewidth=3.0)
        plt.xlabel('% of phase')
    

    def plot(self,y):
        if type(y) is list:
            y=np.array(y).squeeze()
        plt.ion()
        fig = plt.figure()
        ax = fig.add_subplot ('111')
        ax.plot(self.time, y, 'b', linewidth=3.0)



'''
Joints
'''
class ucmJoint(UCM):
    def __init__(self, robot, motions, frame_id, mask, name="UCM of CoM"):
        assert len(mask) == 6, "The mask must have 6 elements"
        UCM.__init__(self, robot)
        self.name = name
        self.robot = robot
        self.motions = motions
        self.repNo = len(motions)
        self._mask = mask
        self._frame_id = frame_id

    @property
    def dim(self):
        return self._mask.sum()

    def mask(self, mask):
        assert len(mask) == 6, "The mask must have 6 elements"
        self._mask = mask.astype(bool)

    def _getDrift(self):
        v_frame = self.robot.frameVelocity(self._frame_id)
        drift = self.robot.frameAcceleration(self._frame_id)
        drift.linear += np.cross(v_frame.angular.T, v_frame.linear.T).T
        return drift.vector

    def _getDynTask(self):
        '''
        Let M be an m-dimensional manifold representing the task space
        Let U be an n-dimensional manifold representing the control space
        task : the hypothetized accelerations element of R^m
        Jtask : the task jacobian that maps task accelerations to controlled joint accelerations
        drift : the dynamic drift of the task
        '''
        task=[]; JTask=[]; drift=[];
        for i in range(0, 100):
            self.updateAll(self.q_mean[i], self.dq_mean[i], self.ddq_mean[i])
            se3.forwardKinematics(self.robot.model, self.robot.data, self.q_mean[i], self.dq_mean[i])
            se3.framesKinematics(self.robot.model, self.robot.data, self.q_mean[i])
            J = self.robot.frameJacobian(self.q_mean[i],self._frame_id, True)
            b = self._getDrift()
            dx = self.robot.frameAcceleration(self._frame_id).vector[self._mask]
            ddx = (J * self.ddq_mean[i].T) + b - (self.robot.data.mass[0] * self.robot.model.gravity.vector)
            task.append(ddx[self._mask])
            drift.append(b[self._mask])
            JTask.append(J[self._mask,:])
        return task, JTask , drift
    
    def getUCMVariances(self):
        self.getReferenceConfigurations(self.motions)
        (self.task, self.JTask, self.drift) = self._getDynTask()
        self.NTask = self.nullspace(self.JTask)
        self.n_ucm = self.repNo * self.robot.nv
        self.n_cm = self.repNo * self.dim
        self.Vucm, self.Vcm, self.criteria = self.varianceFromManifolds(self.dq_mean, 
                                                                        self.dq_data, 
                                                                        self.NTask, 
                                                                        self.n_ucm, 
                                                                        self.n_cm, 
                                                                        'log')
        return self.Vucm, self.Vcm, self.criteria








''' Uncontrolled Manifold of the Momentum '''
class ucmMomentum(UCM):

    def __init__(self, robot, motions, mask, KF=1, KT=1, name="UCM of CoM"):
        UCM.__init__(self, robot)
        self.name = name
        self.robot = robot
        self.motions = motions
        self.repNo = len(motions)
        self._mask = mask
        self._KF = np.float64(KF)
        self._KT = np.float64(KT)
        self._K = self._KF * self._KT

    @property
    def dim(self):
        return self._mask.sum()

    def mask(self, mask):
        assert len(mask) == 6, "The mask must have 6 elements".format(6)
        self._mask = mask.astype(bool)

    def _getBiais(self,q,v):
        model = self.robot.model
        data = self.robot.data
        p_com = self.robot.com(q)#data.com[0]
        cXi = se3.SE3.Identity()
        oXi = data.oMi[1]
        cXi.rotation = oXi.rotation
        cXi.translation = oXi.translation - p_com
        m_gravity = model.gravity.copy()
        model.gravity.setZero()
        b = se3.nle(model,data,q,v)
        model.gravity = m_gravity
        f_ff = se3.Force(b[:6])
        f_com = cXi.act(f_ff)
        return f_com.np

    def _getMomentaCoM(self,com,s):
        #iHi = self.robot.model.inertias[i].se3Action(self.robot.data.v[i])
        Y = self.robot.model.inertias[s]
        V = self.robot.data.v[s] 
        iHi = se3.Inertia.vxiv(Y,V)
        cMo = se3.SE3.Identity()
        cMo.translation = com
        cMi = cMo * self.robot.data.oMi[s]
        return cMi.act(iHi).np.A1
        
        #cXi = se3.SE3.Identity()
        #oXi = data.oMi[i]
        #cXi = cXo * oXi
        #cXi.rotation = oXi.rotation
        #cXi.translation = oXi.translation - com
        #cHi = cXi.act(iHi)
        #return cHi.np.A1*(self._K)
        
        #linM = np.matrix(M[0:3]).A1*(self._K*9.81)
        #angM = M_com.np.A1[3:6] *(self._K*9.81)
        #f = np.hstack([linM, angM])
        #return f #f_com.np.A1

    def _getDynTask(self):
        task=[]; Jtask=[]; drift=[] ;taskNormalized=[]; contribution=[]; momenta=[];
        h=[]
        for i in range(0, 100):
            self.updateAll(self.q_mean[i],self.dq_mean[i],self.ddq_mean[i])
            se3.forwardKinematics(self.robot.model, self.robot.data, self.q_mean[i], self.dq_mean[i], self.ddq_mean[i])
            JH = se3.ccrba(self.robot.model, self.robot.data, self.q_mean[i], self.dq_mean[i])
            H = self.robot.data.hg.np.A.copy()
            b = self._getBiais(self.q_mean[i], self.dq_mean[i])
            Hdot = (JH * self.ddq_mean[i].T) + b #- (self.robot.data.mass[0] * self.robot.model.gravity.vector)
            taskNormalized.append(Hdot[self._mask] * self._K) 
            self.taskNormalized = taskNormalized
            M = []
            p_com = self.robot.com(self.q_mean)
            for s in range(1,26):
                M.append((self._getMomentaCoM(p_com,s) )*self._K)
            contribution.append(np.array(M).squeeze())
            self.contribution = contribution
            h.append(H)
            self.h = h
            task.append(Hdot[self._mask])
            drift.append(b[self._mask])
            Jtask.append(JH[self._mask,:])
            momenta.append(JH[self._mask,:]*self.dq_mean[i].T)
        return task, Jtask, drift
        
    def _getReferenceTask(self, motions):
        '''
        Xi_hat = mean(x(t))
        '''
        x=[]
        for i in xrange (self.repNo):
            x += [self._getTask(motions[i]['pinocchio_data'],motions[i]['time'])]
        meanV, stdV = meanVar(np.array(x).squeeze())
        self.repData = x
        return meanV, stdV
    
    def getUCMVariances(self):
        self.getReferenceConfigurations(self.motions)
        (self.task, self.JTask, self.drift) = self._getDynTask()
        self.NTask = self.nullspace(self.JTask)
        self.n_ucm = self.repNo * (self.robot.nv-self.dim)
        self.n_cm = self.repNo * self.dim
        (self.Vucm, self.Vcm, self.criteria) = self.varianceFromManifolds(self.dq_mean, 
                                                                          self.dq_data, 
                                                                          self.NTask, 
                                                                          self.n_ucm, 
                                                                          self.n_cm, 
                                                                          'log')
        return self.Vucm, self.Vcm, self.criteria












''' Uncontrolled Manifold of the Center of Mass '''
class ucmCoM(UCM):

    def __init__(self, robot,motions, mask=(np.ones(3)).astype(bool), name="UCM of CoM"):
        UCM.__init__(self, robot)
        self.name = name
        self.robot = robot
        self.motions = motions
        self.repNo = len(motions)
        self._mask = mask

    @property
    def dim(self):
        return self._mask.sum()

    def mask(self, mask):
        assert len(mask) == 3, "The mask must have 3 elements"
        self._mask = mask.astype(bool)

    def getReferenceTask(self, motions):
        '''
        Xi_hat = mean(x(t))
        '''
        x=[]
        for i in xrange (self.repNo):
            x += [self._getTask(motions[i]['pinocchio_data'])]
        meanCoM, stdCoM = meanVar(np.array(x).squeeze())
        self.repCoM = x
        return meanCoM, stdCoM
    
    def _getTask(self, Q):
        task=[]
        for i in range(0, len(Q)):
            se3.forwardKinematics(self.robot.model, self.robot.data, Q[i])
            task.append(self.robot.com(Q[i]).getA().squeeze()[self._mask])
        return task 

    def _getJacobian(self, Q):
        taskJacobian=[]
        for i in range(0, len(Q)):
            se3.forwardKinematics(self.robot.model, self.robot.data, Q[i])
            taskJacobian.append(self.robot.Jcom(Q[i])[self._mask,:])
        return taskJacobian
        
    def getUCMVariances(self):
        self.meanConf, self.stdConf, self.data = self.getReferenceConfiguration(self.motions)
        self.JCoM = self._getJacobian(self.meanConf)
        self.NCoM = self.nullspace(self.JCoM)
        self.n_ucm = self.repNo * self.robot.nv
        self.n_cm = self.repNo * self.dim
        self.Vucm, self.Vcm, self.criteria = self.varianceFromManifolds(self.meanConf, 
                                                                        self.data, 
                                                                        self.NCoM, 
                                                                        self.n_ucm, 
                                                                        self.n_cm, 
                                                                        'log')
        return self.Vucm, self.Vcm, self.criteria

    
    
    def plotTask(self, deg=True):
        self.meanCoM, self.stdCoM = self.getReferenceTask(self.motions)
        sangle = 'degrees'
        title = 'Center of mass task'
        ntrials = self.repNo
        legends=[]
        legends.append('mean')
        legends.append('mean+std')
        legends.append('mean-std')
        plt.ion()
        fig = plt.figure()
        fig.canvas.set_window_title(title)
        ax = fig.add_subplot ('111')
        plt.title('Center of Mass [m]')
        if self.dim == 1:
            ax.plot(np.array(self.meanCoM).squeeze(),'k', linewidth=3.0)
        else:
            for i in xrange(self.dim):
                ax.plot(self.meanCoM[:,i],'k', linewidth=3.0)
                ax.plot(self.meanCoM[:,i]+self.stdCoM[:,i],'--b', linewidth=3.0)
                ax.plot(self.meanCoM[:,i]-self.stdCoM[:,i],'--b', linewidth=3.0)

        ax.legend(legends,loc='upper center', bbox_to_anchor=(0.5, -0.2),
                  ncol=7, fancybox=True, shadow=True)




#def ucmEnergy(UCM):
'''
    def plotCoM(self, deg=True):
        
    if deg is True:
            X[:,3:6] = np.rad2deg(X[:,3:6])
            X_std[:,3:6] = np.rad2deg(X_std[:,3:6])
            Xi[:,3:6] = np.rad2deg(Xi[:,3:6])
            sangle='degrees'
        else:
                sangle='rad'
        ntrials = np.shape(Xi)[2]
        legends=[]
        legends.append('mean')
        legends.append('mean+std')
        legends.append('mean-std')
        plt.ion()
        if var is 'com':
            fig = plt.figure()
            fig.canvas.set_window_title(title)
            ax = fig.add_subplot ('311')
            plt.title('Medial-Lateral center of Mass during jump [m]')
            ax.plot(self.time, X[:,1],'r', linewidth=3.0)
            ax.plot(self.time, X[:,1]+X_std[:,0],'--r', linewidth=3.0)
            ax.plot(self.time, X[:,1]-X_std[:,0],'--r', linewidth=3.0)
            color=iter(cm.rainbow(np.linspace(0,1,ntrials)))
            for trls in xrange(ntrials):
                c = next(color)
                ax.plot(self.time,Xi[:, 1, trls], color=c, linewidth=1.0)
                legends.append('trials'+str(trls))
            plt.ylabel('m')
            
            ax = fig.add_subplot ('312')
            plt.title('Antero-Posterior center of Mass during jump [m]')
            ax.plot(self.time, X[:,0],'r', linewidth=3.0)
            ax.plot(self.time, X[:,0]+X_std[:,0],'--r', linewidth=3.0)
            ax.plot(self.time, X[:,0]-X_std[:,0],'--r', linewidth=3.0)
            color=iter(cm.rainbow(np.linspace(0,1,ntrials)))
            for trls in xrange(ntrials):
                c = next(color)
                ax.plot(self.time,Xi[:, 0, trls], color=c, linewidth=1.0)
            plt.ylabel('m')

            ax = fig.add_subplot ('313')
            plt.title('Vertical center of Mass during jump [m]')
            ax.plot(self.time,X[:,2], 'r', linewidth=3.0)
            ax.plot(self.time,X[:,2]+X_std[:,2],'--r', linewidth=3.0)
            ax.plot(self.time,X[:,2]-X_std[:,2],'--r', linewidth=3.0)
            color=iter(cm.rainbow(np.linspace(0,1,ntrials)))
            for trls in xrange(ntrials):
                c = next(color)
                ax.plot(self.time,Xi[:, 2, trls], color=c, linewidth=1.0)
            plt.xlabel('% of phase')
            plt.ylabel('m')

            # Shrink current axis's height by 10% on the bottom  
            box = ax.get_position()
            ax.set_position([box.x0, box.y0 + box.height * 0.1,
                              box.width, box.height * 0.9])
            ax.legend(legends,loc='upper center', bbox_to_anchor=(0.5, -0.2),
                      ncol=7, fancybox=True, shadow=True)
    
        
        
    
    
'''





