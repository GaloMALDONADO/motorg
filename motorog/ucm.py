import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
import pinocchio as se3
from tools import *
from bmtools.filters import filtfilt_butter

class UCM:
    def __init__(self, robot):
        self.robot = robot
        self.name = robot.name
        self.nq = robot.nq
        self.nv = robot.nv
        self.tf = 100
        self.time = np.linspace(1,100,100)

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
            N.append(getNullSpaceAndRank(Jq[i])[0])
        return np.array(N)

    def varianceFromManifolds(self, Q_hat, Qi, Ni, normUCM=1, normCM=1, criteria='log'):
        ''' Vcm, Vucm, c = varianceFromManifolds(Q_hat, Qi, Ni) 
        Return a normalized array of the variance of the CM and the UCM, and the hypothesis test result
        Param-in :
        Q_hat = mean joint configuration (1x100)
        Qi = matrix of joint configurations (100, joints_dof, nTrials)
        Ni = list of size (100) containing the nullspace (1 x joints_dof- task_dof)
        norm UCM = value to which the variance of UCM is normalized. Default is 1
        norm CM = value to which the variance of CM is normalized. Default is 1 
        normaly the value is calculated as : # of dof involved (joints and tasks) * # of trials
        '''
        q_ucm = []; q_cm = [];
        Vucm = []; Vcm =[];
        ntrials = np.shape(Qi)[2]
        for i in xrange(100):
            v_ucm = 0; v_cm = 0;
            for trls in xrange(ntrials):
                #devq = np.matrix(Q_hat[i] - Qi[i,:,trls]).T
                devq = se3.differentiate(self.robot.model, Q_hat[0], np.matrix(Qi[i,:,trls]))
                # the deviations from the mean trajectories in joint-space are projected onto the null-space
                ucm = np.matrix(Ni[trls]) * np.matrix(Ni[trls]).T * devq
                # and onto the range space (orthogonal to the null space)
                # which is a lineat appoximation of the controlled manifold
                cm = devq - ucm
                # the variance per degree of freedom of the projected deviations is
                v_ucm = v_ucm + np.square(np.linalg.norm(ucm))
                v_cm = v_cm + np.square(np.linalg.norm(cm))

            Vucm.append(v_ucm)
            Vcm.append (v_cm)

        Vcm_n = np.array(Vcm)/normCM
        Vucm_n = np.array(Vucm)/normUCM
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
    def plotUCM(self,Vucm,Vcm,criteria, title, degree=True):
        if degree is True:
            np.rad2deg(Vucm)
            np.rad2deg(Vcm)
        plt.ion()
        fig = plt.figure ()
        fig.canvas.set_window_title(title)
        ax = fig.add_subplot ('311')
        plt.title('Uncontrolled Manifold')
        plt.ylabel('variance')
        ax.plot(self.time, Vucm, 'b', linewidth=3.0)
        ax = fig.add_subplot ('312')
        plt.title('Controlled Manifold')
        plt.ylabel('variance')
        ax.plot(self.time, Vcm, 'r', linewidth=3.0)
        ax = fig.add_subplot ('313')
        plt.title('Criteria')
        ax.plot(self.time, criteria, 'k', linewidth=3.0)
        plt.xlabel('% of phase')


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

    def getReferenceConfiguration(self, motions):
        '''
        meanConf, stdConf, data = meanConfiguration(motions)
        '''
        return meanConfiguration(motions)

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
        #
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
'''
Joints
'''
class ucmJoint(UCM):
    def __init__(self, robot, motions, frame_id, mask=(np.ones(6)).astype(bool), name="UCM of CoM"):
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

    def referenceConfiguration(self, motions):
        '''
        meanConf, stdConf, data = meanConfiguration(motions)
        '''
        return meanConfiguration(motions)

    def referenceTask(self, motions):
        '''
        Xi_hat = mean(x(t))
        '''
        x=[]
        for i in xrange (self.repNo):
            x += [self.getTask(motions[i]['pinocchio_data'])]
        meanTask, stdTask = meanVar(np.array(x).squeeze())
        return meanTask, stdTask
    
    def getTask(self, Q):
        task=[]
        for i in range(0, len(Q)):
            se3.forwardKinematics(self.robot.model, self.robot.data, Q[i])
            se3.framesKinematics(self.robot.model, self.robot.data, Q[i])
            task.append(self.robot.framePosition(self._frame_id))
        return task 

    def getJacobian(self, Q):
        taskJacobian=[]
        for i in range(0, len(Q)):
            se3.forwardKinematics(self.robot.model, self.robot.data, Q[i])
            se3.framesKinematics(self.robot.model, self.robot.data, Q[i])
            taskJacobian.append(self.robot.frameJacobian(Q[i], 
                                                         self._frame_id, True)[self._mask,:])

        return taskJacobian
        
    def getUCMVariances(self):
        self.meanConf, self.stdConf, self.data = self.referenceConfiguration(self.motions)
        #self.meanCoM, self.stdCoM = self.referenceTask(self.motions)
        self.J = self.getJacobian(self.meanConf)
        self.N = self.nullspace(self.J)
        self.n_ucm = self.repNo * self.robot.nv
        self.n_cm = self.repNo * self.dim
        self.Vucm, self.Vcm, self.criteria = self.varianceFromManifolds(self.meanConf, 
                                                                        self.data, 
                                                                        self.N, 
                                                                        self.n_ucm, 
                                                                        self.n_cm, 
                                                                        'log')
        return self.Vucm, self.Vcm, self.criteria

''' Uncontrolled Manifold of the Angular Momentum '''
class ucmMomentum(UCM):

    def __init__(self, robot,motions, mask=(np.ones(3)).astype(bool), name="UCM of CoM"):
        UCM.__init__(self, robot)
        self.name = name
        self.robot = robot
        self.motions = motions
        self.repNo = len(motions)
        self._mask = mask
        self.dt = 0.0025
        self.fs = 400
        self.cutoff = 30
        self.filter_order = 4

    @property
    def dim(self):
        return self._mask.sum()

    def mask(self, mask):
        assert len(mask) == 6, "The mask must have 6 elements".format(6)
        self._mask = mask.astype(bool)

    def getReferenceConfiguration(self, motions):
        '''
        meanConf, stdConf, data = meanConfiguration(motions)
        '''
        return meanConfiguration(motions)
        
    def differentiate(self, q1, q2):
        return se3.differentiate(self.robot.model, np.asmatrix(q1), np.asmatrix(q2))

    def getVelocity(self, Q, T, filterFlag=True):
        Vi = []
        for i in range(1,len(Q)):
            dt = T[0,i]-T[0,i-1]
            Vi += [self.differentiate(Q[i-1],Q[i])*dt]

        Vi.insert(0,Vi[0])
        V = np.matrix(np.array(Vi))
        if filterFlag is True:
            fDof = []
            for i in xrange (self.robot.nv):
                fDof += [filtfilt_butter(np.array(V[:,i]).squeeze(), 
                                         self.cutoff, 
                                         self.fs, 
                                         self.filter_order)]
            Vf = np.matrix(fDof).T
            return Vf
        return V

    def _getTask(self, Q, T):
        V = self.getVelocity(Q,T, filterFlag=True)
        task=[]; Jtask=[]
        for i in range(0, len(Q)):
            se3.forwardKinematics(self.robot.model, self.robot.data, Q[i], V[i])
            JH = se3.ccrba(self.robot.model, self.robot.data, Q[i], V[i])
            H = self.robot.data.hg.np.A.copy()
            task.append(H[self._mask,:])
            Jtask.append(JH[self._mask,:])
        return task, Jtask
        
    def getReferenceTask(self, motions):
        '''
        Xi_hat = mean(x(t))
        '''
        x=[]
        for i in xrange (self.repNo):
            x += [self._getTask(motions[i]['pinocchio_data'],motions[i]['time'])]
        meanV, stdV = meanVar(np.array(x).squeeze())
        self.repData = x
        return meanV, stdV
    
    def getMeanTime(self, motions):
        x=[]
        for i in xrange (self.repNo):
            x += [motions[i]['time']]
        meanT =  np.mean(x,0)
        stdT = np.std(x,0)
        self.repData = x
        return meanT, stdT

    def getUCMVariances(self):
        self.meanConf, self.stdConf, self.data = self.getReferenceConfiguration(self.motions)
        self.J = self._getTask(self.meanConf,self.getMeanTime(self.motions)[0])[1]
        self.N = self.nullspace(self.J)
        self.n_ucm = self.repNo * self.robot.nv
        self.n_cm = self.repNo * self.dim
        self.Vucm, self.Vcm, self.criteria = self.varianceFromManifolds(self.meanConf, 
                                                                        self.data, 
                                                                        self.N, 
                                                                        self.n_ucm, 
                                                                        self.n_cm, 
                                                                        'log')
        return self.Vucm, self.Vcm, self.criteria

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





