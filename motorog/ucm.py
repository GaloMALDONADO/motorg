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
        #self.fs = 400 
        #self.cutoff = 50
        #self.filter_order = 4

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


    def getReferenceConfigurations(self, Q):
        '''
        meanConf, stdConf, data = meanConfiguration(Q)
        '''
        (self.time_mean, self.time_std, self.time_data) = tools.meanTime(Q)
        (self.q_mean, self.q_std, self.q_data) = tools.meanConfiguration(self.robot,Q)
        (self.dq_mean, self.dq_std, self.dq_data) = tools.meanConfiguration2(self.robot,self.DQ)
        (self.ddq_mean, self.ddq_std, self.ddq_data) = tools.meanConfiguration2(self.robot,self.DDQ)
        #(self.dq_mean, self.dq_std, self.dq_data) = tools.meanVelocities(self.robot.model, 
        #                                                                 self.q_data, 
        #                                                                 self.time_data,
        #                                                                 20, 
        #                                                                 self.fs, 
        #                                                                 self.filter_order)
        #(self.ddq_mean, self.ddq_std, self.ddq_data) = tools.meanAccelerations(self.dq_data, 
        #                                                                       self.time_data,
        #                                                                       50, 
        #                                                                       self.fs, 
        #                                                                       self.filter_order)
        

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
                v_ucm += np.square(np.linalg.norm(ucm))
                v_cm  += np.square(np.linalg.norm(cm))
                #v_ucm += np.linalg.norm(ucm)
                #v_cm  += np.linalg.norm(cm)
                

            Vucm.append(v_ucm)
            Vcm.append (v_cm)

        Vcm_n = np.array(Vcm)/np.float64(normCM)
        Vucm_n = np.array(Vucm)/np.float64(normUCM)
        if criteria is 'log':
            c = np.log(Vucm_n/Vcm_n)
        else:
            c = Vucm_n/Vcm_n
        return Vucm_n, Vcm_n, c


''' Uncontrolled Manifold of the Momentum '''
class ucmMomentum(UCM):

    def __init__(self, robot, Q, dq, ddq, mask, KF=1, KT=1, name="UCM of CoM"):
        UCM.__init__(self, robot)
        self.name = name
        self.robot = robot
        self.Q = Q
        self.DQ = dq
        self.DDQ = ddq
        self.repNo = len(Q)
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
        #oXi = data.oMi[1]
        #cXi.rotation = oXi.rotation
        #cXi.translation = oXi.translation - p_com
        cXi.translation = p_com
        m_gravity = model.gravity.copy()
        model.gravity.setZero()
        b = se3.nle(model,data,q,v)
        model.gravity = m_gravity
        f_ff = se3.Force(b[:6])
        f_com = cXi.act(f_ff)
        return f_com.np

    def _getContribution(self,com,s):
        '''
        Get segment contribution to centroidal angular 
        momenta and its rate of change
        Inputs:
        - s : segment index
        - com : position of the CoM in world reference frame
        '''
        # get spatial inertia and velocity
        Y = self.robot.model.inertias[s]
        V = self.robot.data.v[s] 
        # centroidal momenta in body frame
        # ihi = I Vi
        iHi = se3.Force(Y.matrix()*V.vector)
        # rate of change of centroidal momenta in body frame
        # ih_doti = Iai + Vi x* hi
        iHDi = self.robot.model.inertias[s]*self.robot.data.a[s] + se3.Inertia.vxiv(Y,V)
        
        # express at the center of mass
        oMc = se3.SE3.Identity()
        oMc.translation = com
        # uncomment in case need to change the rotation of the reference frame
        #oMc.rotation = self.robot.data.oMi[1].rotation 
        cMi = oMc.actInv( self.robot.data.oMi[s] )
        
        cHi = cMi.act(iHi).np.A1
        cHDi = cMi.act(iHDi).np.A1
        return cHi, cHDi        
        
    def _getJmean(self):
        Jtask=[]
        for i in range(0, 100):
            se3.forwardKinematics(self.robot.model, 
                                  self.robot.data, 
                                  self.q_mean[i], 
                                  self.dq_mean[i], 
                                  self.ddq_mean[i])
            JH = se3.ccrba(self.robot.model,
                           self.robot.data, 
                           self.q_mean[i], 
                           self.dq_mean[i])
            Jtask.append(JH[self._mask,:])
        return Jtask
    

    def _getDynTask(self):
        task=[]; Jtask=[]; drift=[] ;taskNormalized=[];  momenta=[];
        contributionH=[]; contributionF=[];
        h=[];# H2=[]
        for i in range(0, 100):
            self.updateAll(self.q_mean[i],self.dq_mean[i],self.ddq_mean[i])
            se3.forwardKinematics(self.robot.model, self.robot.data, self.q_mean[i], self.dq_mean[i], self.ddq_mean[i])
            JH = se3.ccrba(self.robot.model, self.robot.data, self.q_mean[i], self.dq_mean[i])
            H = self.robot.data.hg.np.A.copy()
            b = self._getBiais(self.q_mean[i], self.dq_mean[i])
            Hdot = (JH * self.ddq_mean[i].T) - b.copy() - (self.robot.data.mass[0] * self.robot.model.gravity.vector)
            h.append(H.copy()*self._K)
            self.h = h
            task.append(Hdot[self._mask])
            taskNormalized.append(Hdot[self._mask] * self._K) 
            self.taskNormalized = taskNormalized
            drift.append(b[self._mask])
            Jtask.append(JH[self._mask,:])
            momenta.append(JH[self._mask,:]*self.dq_mean[i].T)

            # Individual contributions to centroidal momenta (and its rate of change)
            segH = []; segF=[]
            p_com = self.robot.com(self.q_mean[i])
            for s in range(1,26):
                hc, hcd = self._getContribution(p_com,s) 
                segH.append(hc*self._K)
                segF.append(hcd*self._K)
            contributionH.append(np.array(segH).squeeze())
            contributionF.append(np.array(segF).squeeze())
            self.contribution = contributionH
            self.contributionF = contributionF
            
            # Get Torques
            
            
        return task, Jtask, drift
        
    def _getReferenceTask(self, Q):
        '''
        Xi_hat = mean(x(t))
        '''
        x=[]
        for i in xrange (self.repNo):
            x += [self._getTask(Q[i]['pinocchio_data'],Q[i]['time'])]
        meanV, stdV = meanVar(np.array(x).squeeze())
        self.repData = x
        return meanV, stdV

    def momentaExtraction(self):
        # create Dictionary
        data = {
            'hg':[],'dhg':[], "drift":[],
            'hg_segments':[],'dhg_segments':[], 
            'q':[], 'dq':[], 'ddq':[]
        }
        tmax = 100
        nRep = self.repNo
        q = np.zeros((tmax,49,nRep))
        dq = np.zeros((tmax,42,nRep))
        ddq = np.zeros((tmax,42,nRep))
        data_Hg = np.zeros((tmax,6,nRep))
        data_dHg = np.zeros((tmax,6,nRep))
        data_drift = np.zeros((tmax,6,nRep))
        data_Hgs  = np.zeros((tmax,6,nRep,26))
        data_dHgs = np.zeros((tmax,6,nRep,26))
        for t in xrange(tmax):
            for i in xrange (nRep):
                q[t,:,i] = np.matrix(self.Q[i]['pinocchio_data'][t]).squeeze()
                dq[t,:,i] = np.matrix(self.DQ[i][t]).squeeze()
                ddq[t,:,i] = np.matrix(self.DDQ[i][t]).squeeze()
                self.updateAll(q[t,:,i],
                               dq[t,:,i],
                               ddq[t,:,i])
                se3.forwardKinematics(self.robot.model, 
                                      self.robot.data, 
                                      q[t,:,i], 
                                      dq[t,:,i], 
                                      ddq[t,:,i])
                # centroidal momenta
                JH = se3.ccrba(self.robot.model, 
                               self.robot.data, 
                               q[t,:,i], 
                               dq[t,:,i])
                H = self.robot.data.hg.np.A.copy()
                b = self._getBiais(q[t,:,i], dq[t,:,i])
                Hdot = (JH * np.matrix(ddq[t,:,i]).squeeze().T) - b.copy() - (self.robot.data.mass[0] * self.robot.model.gravity.vector) 
                HNormalized = H.copy()*self._K
                bNormalized = b.copy()*self._K
                HdotNormalized = Hdot.copy()*self._K
                data_Hg[t,:,i] = HNormalized.squeeze()
                data_dHg[t,:,i] = HdotNormalized.squeeze()
                data_drift[t,:,i] = bNormalized.squeeze()
                # Segmental contributions to centroidal momenta (and its rate of change)
                segH = []; segF=[]
                p_com = self.robot.com(q[t,:,i])
                for s in range(1,26):
                    (data_Hgs[t,:,i,s], data_dHgs[t,:,i,s]) = self._getContribution(p_com,s) 
        data['q'].append(q)
        data['dq'].append(dq)
        data['ddq'].append(ddq)
        data['hg'].append(data_Hg)
        data['dhg'].append(data_dHg)
        data['drift'].append(data_drift)
        data['hg_segments'].append(data_dHgs)
        data['dhg_segments'].append(data_Hgs)
        return data
    '''
    def computeStats(self):
        # computes mean,std of H, Hdot and segmetal contributions
        (data_Hg, data_dHg, data_Hgs, data_dHgs) = self.momentaExtraction()
        meanData = {'q':[], 'dq':[], 'ddq':[], 'hg':[], 'dhg':[], 'hg_contrib', 'dhg_contrib':[]}
        stdData = {'q':[], 'dq':[], 'ddq':[], 'hg':[], 'dhg':[], 'hg_contrib', 'dhg_contrib':[]}
        data = {'q':[], 'dq':[], 'ddq':[], 'hg':[], 'dhg':[], 'hg_contrib', 'dhg_contrib':[]}
        nRep = len(self.Q)
        tmax = 100
        DoF = 42

        data = []
        dataMean = []
        dataStd = []
        dataStr = np.zeros((tmax,49,nRep))

                
        # Store data
        data = np.matrix(q)
        dataMean += [robot.dof2pinocchio(np.mean(data2,0).A1)]
        dataStd += [robot.dof2pinocchio(np.std(data2,0).A1)]    
        #-  (self.robot.data.mass[0] * self.robot.model.gravity.vector)
                

        h.append(H*self._K)
        self.h = h
        taskNormalized.append(Hdot[self._mask] * self._K) 
        self.taskNormalized = taskNormalized
        task.append(Hdot[self._mask])
        drift.append(b[self._mask])
        Jtask.append(JH[self._mask,:])
        momenta.append(JH[self._mask,:]*self.dq_mean[i].T)

            
        contributionH.append(np.array(segH).squeeze())
        contributionF.append(np.array(segF).squeeze())
        self.contribution = contributionH
        self.contributionF = contributionF


        data += []
        dataStr[t,:,i] = Q[i]['pinocchio_data'][t]
        data2 = np.matrix(data)
        dataMean += [robot.dof2pinocchio(np.mean(data2,0).A1)]
        dataStd += [robot.dof2pinocchio(np.std(data2,0).A1)]

    '''
    
    def getUCMVariances(self):
        #self.computeStats()
        self.getReferenceConfigurations(self.Q)
        self.data = self.momentaExtraction()
        (self.task, self.JTask, self.drift) = self._getDynTask()
        #self.JTask = self._getJmeank()
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





'''
Joints
'''
class ucmJoint(UCM):
    def __init__(self, robot, Q, dq, ddq, frame_id, mask, name="UCM of CoM"):
        assert len(mask) == 6, "The mask must have 6 elements"
        UCM.__init__(self, robot)
        self.name = name
        self.robot = robot
        self.Q = Q
        self.DQ = dq
        self.DDQ = ddq
        self.repNo = len(Q)
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
        self.getReferenceConfigurations(self.Q)
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










''' Uncontrolled Manifold of the Center of Mass '''
class ucmCoM(UCM):

    def __init__(self, robot,Q, dq, ddq, mask=(np.ones(3)).astype(bool), name="UCM of CoM"):
        UCM.__init__(self, robot)
        self.name = name
        self.robot = robot
        self.Q = Q
        self.repNo = len(Q)
        self._mask = mask

    @property
    def dim(self):
        return self._mask.sum()

    def mask(self, mask):
        assert len(mask) == 3, "The mask must have 3 elements"
        self._mask = mask.astype(bool)

    def getReferenceTask(self, Q):
        '''
        Xi_hat = mean(x(t))
        '''
        x=[]
        for i in xrange (self.repNo):
            x += [self._getTask(Q[i]['pinocchio_data'])]
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
        self.meanConf, self.stdConf, self.data = self.getReferenceConfiguration(self.Q)
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
        self.meanCoM, self.stdCoM = self.getReferenceTask(self.Q)
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
    
        
        
    
    #Plot the task
    
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


    
    #Plot the uncontrolled manifold 
    
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





