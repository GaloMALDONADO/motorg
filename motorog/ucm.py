import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
import pinocchio as se3
import tools 
import bmtools.processing as bm
from IPython import embed
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

    def _diag(self, L):
        shp = L[0].shape
        mask = np.kron(np.eye(len(L)), np.ones(shp))==1
        out = np.zeros(np.asarray(shp)*len(L))
        out[mask] = np.concatenate(L).ravel()
        return out

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
        n,m = Jq[0].shape
        for i in xrange(100):
            P=(np.matrix(np.identity(m))) - (np.linalg.pinv(Jq[i])*Jq[i])
            N.append(P)

        projector = np.array(N)
        self.projector = projector
        #print np.sum((np.matrix(projector)*np.matrix(projector))-np.matrix(projector))
        return projector
    
    def updateAll(self,q,v,a):
        se3.computeAllTerms(self.robot.model, self.robot.data, q, v)
        self.robot.q=q
        self.robot.v=v
        self.robot.a=a
        #self.robot.tau = se3.rnea(self.robot.model, self.robot.data, q, v, a)


    #def getRoM(self, Q):
    #    (self.rom_mean, self.rom_std, self.rom_data) = tools.RoM(Q)

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
        
    def varianceFromManifoldsPos(self, Q_hat, Qi, Pi, normUCM, normCM, criteria='log'):
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
                # the deviations from the mean trajectories in joint-space are projected onto the null-space
                devQ = np.matrix(Q_hat[i] - Qi[i,:,trls]).T
                proj = self.ProjJ
                # and onto the range space (orthogonal to the null space)
                # which is a lineat appoximation of the controlled manifold
                ucm = np.matrix(proj[i]) * devQ.copy().T
                cm = devQ.copy().T - ucm
                # the variance per degree of freedom of the projected deviations is
                v_ucm += np.square(np.linalg.norm(ucm))
                v_cm  += np.square(np.linalg.norm(cm))
                #embed()
            Vucm.append(v_ucm)
            Vcm.append (v_cm)
        Vcm_n = np.array(Vcm)/np.float64(normCM)
        Vucm_n = np.array(Vucm)/np.float64(normUCM)
        #embed()
        if criteria is 'log':
            c = np.log(Vucm_n/Vcm_n)
        else:
            c = Vucm_n/Vcm_n
        return Vucm_n, Vcm_n, c

    def varianceFromManifoldsVel(self, Q_hat, Qi, Pi, normUCM, normCM, criteria='log'):
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
        Vucm_q = []; Vcm_q =[];
        Vucm_dq = []; Vcm_dq =[];
        ntrials = np.shape(Qi)[2]
        
        for i in xrange(100):
            v_ucm = 0; v_cm = 0;
            v_ucm_q = 0; v_cm_q = 0;
            v_ucm_dq = 0; v_cm_dq = 0;
            for trls in xrange(ntrials):
                devq = se3.differentiate(self.robot.model, np.matrix(Qi[i,:49,trls]), Q_hat[i][0,:49]).T
                devdq = (Qi[i,49:91,trls]-Q_hat[i][0,49:91]).squeeze()
                devQ = np.hstack([devq,devdq])
                proj = self.ProjJ
                ucm = np.matrix(proj[i]) * devQ.copy().T
                cm = devQ.copy().T - ucm
                cm_q = cm[:-42]
                cm_dq = cm[-42:]
                ucm_q = ucm[:-42]
                ucm_dq = ucm[-42:]
                v_ucm += np.square(np.linalg.norm(ucm))
                v_cm  += np.square(np.linalg.norm(cm))
                v_ucm_q += np.square(np.linalg.norm(ucm_q))
                v_cm_q  += np.square(np.linalg.norm(cm_q))
                v_ucm_dq += np.square(np.linalg.norm(ucm_dq))
                v_cm_dq  += np.square(np.linalg.norm(cm_dq))
            Vucm.append(v_ucm)
            Vcm.append (v_cm)
            Vucm_q.append(v_ucm_q)
            Vucm_dq.append(v_ucm_dq)
            Vcm_q.append(v_cm_q)
            Vcm_dq.append(v_cm_dq)

        Vcm_n = np.array(Vcm_dq)/np.float64(normCM)
        Vucm_n = np.array(Vucm_dq)/np.float64(normUCM)
        #embed()
        if criteria is 'log':
            c = np.log(Vucm_n/Vcm_n)
            #c = Vucm_n/Vcm_n
            #c = log(Vucm_n)
            #c = log(Vcm)
        else:
            c = Vucm_n/Vcm_n
        return Vucm_n, Vcm_n, c

    def varianceFromManifoldsAcc(self, Q_hat, Qi, Pi, normUCM, normCM, criteria='log'):
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
        Vucm_q = []; Vcm_q =[];
        Vucm_dq = []; Vcm_dq =[];
        Vucm_ddq = []; Vcm_ddq =[];
        ntrials = np.shape(Qi)[2]
        ddq_variance = np.zeros((100,126,ntrials))
        
        for i in xrange(100):
            v_ucm = 0; v_cm = 0;
            v_ucm_q = 0; v_cm_q = 0;
            v_ucm_dq = 0; v_cm_dq = 0;
            v_ucm_ddq = 0; v_cm_ddq = 0;
            for trls in xrange(ntrials):
                devq = se3.differentiate(self.robot.model, np.matrix(Qi[i,:49,trls]), Q_hat[i][0,:49]).T
                devdq = (Qi[i,49:91,trls]-Q_hat[i][0,49:91]).squeeze()
                devddq = (Qi[i,91:133,trls]-Q_hat[i][0,91:133]).squeeze()

                devQ = np.hstack([devq, devdq, devddq])
                proj = self.ProjJ
                #ucm = np.matrix(proj[i]) * devQ.copy().T
                #cm = devQ.copy().T - ucm
                
                #ucm_q = ucm[:-84]
                #ucm_dq = ucm[-84:-42]
                #ucm_ddq = ucm[-42:]
                #cm_q = cm[:-84]
                #cm_dq = cm[-84:-42]
                #cm_ddq = cm[-42:]
                
                
                ucm_ddq = np.matrix(proj[i]) * devQ.copy().T[-42:]
                cm_ddq = devQ.copy().T[-42:] - ucm_ddq


                #v_ucm += np.square(np.linalg.norm(ucm))
                #v_cm  += np.square(np.linalg.norm(cm))
                #v_ucm_q += np.square(np.linalg.norm(ucm_q))
                #v_cm_q  += np.square(np.linalg.norm(cm_q))
                #v_ucm_dq += np.square(np.linalg.norm(ucm_dq))
                #v_cm_dq  += np.square(np.linalg.norm(cm_dq))
                v_ucm_ddq += np.square(np.linalg.norm(ucm_ddq))
                v_cm_ddq  += np.square(np.linalg.norm(cm_ddq))               
                #embed()

            #Vucm.append(v_ucm)
            #Vcm.append (v_cm)
            #Vucm_q.append(v_ucm_q)
            #Vucm_dq.append(v_ucm_dq)
            Vucm_ddq.append(v_ucm_ddq)
            #Vcm_q.append(v_cm_q)
            #Vcm_dq.append(v_cm_dq)
            Vcm_ddq.append(v_cm_ddq)

        Vcm_n = np.array(Vcm_ddq)/np.float64(normCM)
        Vucm_n = np.array(Vucm_ddq)/np.float64(normUCM)#*3)
        #embed()
        if criteria is 'log':
            c = np.log(Vucm_n/Vcm_n)
            #c = (Vucm_n-Vcm_n) / (Vucm_n+Vcm_n)
            #c = Vucm_n/Vcm_n
            #c = log(Vucm_n)
            #c = log(Vcm)
        else:
            c = Vucm_n/Vcm_n
        return np.log(Vucm_n), np.log(Vcm_n), c

''' Uncontrolled Manifold of the Momentum '''
class ucmMomentum(UCM):

    def __init__(self, robot, order, Q, dq, ddq, mask, KF=1, KT=1, name="UCM of CoM"):
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
        self.order = order #0 pos, 1 vel, 2 acc        

    @property
    def dim(self):
        return self._mask.sum()

    def mask(self, mask):
        assert len(mask) == 6, "The mask must have 6 elements".format(6)
        self._mask = mask.astype(bool)

    def _getBiais(self,q,v):
        model = self.robot.model
        data = self.robot.data
        p_com = self.robot.com(q)
        
        oXi = data.oMi[1]
        cXi = se3.SE3.Identity()
        cXi.rotation = oXi.rotation
        cXi.translation = oXi.translation - p_com
        #cXi.translation = p_com
        
        m_gravity = model.gravity.copy()
        model.gravity.setZero()
        b = se3.nle(model,data,q,v)
        model.gravity = m_gravity
        f_ff = se3.Force(b[:6])
        f_com = cXi.act(f_ff)
        return f_com.np

    def check2(self):
        Ag=self._test()
        print Ag.shape
        print '*************'
        print 'Pinocchio:'
        print self.robot.data.Ag*self.robot.v.T
        print np.sum(self.robot.data.Ag)
        print 'Method 1'
        print Ag * self.robot.v.T
        print np.sum(Ag)

    def check(self):
        #Ag = self._getAg()
        P_sys1 = self._getP_sys1()
        P_sys2 = self._getP_sys2()
        J_sys = self._getJ_sys()
        Xg_sys = self._getXg_sys()
        Ag1 = Xg_sys.T * P_sys1 * J_sys
        Ag2 = Xg_sys.T * P_sys2 * J_sys
        print '*************'
        print 'Pinocchio:'
        print self.robot.data.Ag*self.robot.v.T
        print np.sum(self.robot.data.Ag)
        print 'Method 1'
        print Ag1 * self.robot.v.T
        print np.sum(Ag1)
        print 'Method 2'
        print Ag2 * self.robot.v.T
        print np.sum(Ag2)
        #dAg = self._getdAg()
        #print dAg*self.robot.a.T
        #print self.dH

    def _getAg(self):
        P_sys = self._getP_sys1()
        J_sys = self._getJ_sys()
        Xg_sys = self._getXg_sys()
        Ag = Xg_sys.T * P_sys * J_sys
        return Ag

        
    def _test(self):
        se3.computeJacobians(self.robot.model, self.robot.data, self.q_mean[self.i])
        arr_s = []
        for s in range(1,26):
            oMi = self.robot.data.oMi[1]
            oMc = se3.SE3.Identity()
            oMc.rotation = oMi.rotation
            #oMc.translation = oMi.translation - self.robot.data.com[0]
            oMc.translation = self.robot.data.com[0]
            cMi = oMc.actInv( self.robot.data.oMi[s] )
            cXi = cMi.action
            cFi = cMi.inverse().action
            #
            iJ = se3.jacobian(self.robot.model, self.robot.data, self.q_mean[self.i].T, s, False, True)
            #
            iI = self.robot.model.inertias[s].matrix()
            #
            cIi = cFi * iI
            cJi = cXi * iJ
            cAi = cIi * cJi
            arr_s += [cAi]
            #self.Ag_ = np.hstack(y[:] for y in arr_s)
        self.Ag_ = np.sum(arr_s,0)
        return self.Ag_
            
            
    def _getXg_sys(self):
        '''
        dimensions = 6x150
        '''
        arr_s1 = []
        arr_s2 = []
        for s in range(1,26):
            oMi = self.robot.data.oMi[1]
            oMc = se3.SE3.Identity()
            oMc.rotation = oMi.rotation
            oMc.translation = oMi.translation - self.robot.data.com[0]
            #oMc.translation = self.robot.data.com[0]
            cMi = oMc.actInv( self.robot.data.oMi[s] )
            #cXi = cMi.action.T
            cXfi = cMi.inverse().action #.T
            
            # ---------- motion application
            A = cMi.rotation
            B = se3.utils.skew(cMi.translation) * cMi.rotation
            C = se3.utils.zero((3,3))
            D = cMi.rotation
            row1 = np.hstack([A, B])
            row2 = np.hstack([C, D])
            cXi_2 = np.vstack([row1,row2]) # the same as cMi.action
            # ---------- force application
            Af = cMi.rotation
            Bf = se3.utils.zero((3,3))
            Cf = se3.utils.skew(cMi.translation) * cMi.rotation
            Df = cMi.rotation
            row1f = np.hstack([Af, Bf])
            row2f = np.hstack([Cf, Df])
            #cXfi = np.vstack([row1f,row2f]).T  
            # -----------------
            #arr_s1 += [cXi]
            arr_s2 += [cXfi]
        #self.Xg_sys = np.hstack(y[:] for y in arr_s1).T
        self.Xgf_sys = np.hstack(y[:] for y in arr_s2).T
        return self.Xgf_sys

    def _getJ_sys(self):
        '''
        dim = 150x42
        '''
        arr_s = []
        se3.computeJacobians(self.robot.model, self.robot.data, self.q_mean[self.i])
        for s in range(1,26):
            #wrt body
            J_s = se3.jacobian(self.robot.model, self.robot.data, self.q_mean[self.i].T, s, False, True)
            arr_s += [J_s.T]
        #[150,42]
        self.J_sys = np.hstack(y[:] for y in arr_s).T
        return self.J_sys

    def _getP_sys1(self):
        '''
        dim = 6,150
        '''
        arr_s = []
        for s in range(1,26):
            #wrt body
            I = self.robot.model.inertias[s].matrix()
            arr_s += [np.array(I.squeeze())]
        self.P_sys1 = self._diag((arr_s[0], arr_s[1], arr_s[2], arr_s[3], arr_s[4], arr_s[5], 
                                  arr_s[6], arr_s[7], arr_s[8], arr_s[9], arr_s[10],
                                  arr_s[11], arr_s[12], arr_s[13], arr_s[14], arr_s[15], 
                                  arr_s[16], arr_s[17], arr_s[18], arr_s[19], arr_s[20],
                                  arr_s[21], arr_s[22], arr_s[23], arr_s[24] ))
        #self.P_sys = np.hstack(y[:] for y in arr_s)
        return self.P_sys1

    def _getP_sys2(self):
        '''
        [ T 0 ; U V]
        '''
        arr_s = []
        for s in range(1,26):
            m_s = self.robot.model.inertias[s].mass
            p_com = self.robot.data.com[0]
            #lever from joint to CoM
            lever = self.robot.model.inertias[s].lever
            #postion of the joint wrt world
            #p_i = self.robot.data.oMi[s].translation
            p_i = self.robot.data.liMi[s].translation
            #postion of the segment CoM wrt world
            p_s =  p_i + lever
            #intertia wrt to joint
            I_j = self.robot.model.inertias[s].inertia 
            #intertia expressed at the CoM
            I_s = I_j - ( (m_s*np.identity(3)) * (lever.A1*lever.A1) )
            # get matrix components of size [3 x 3s] each
            T = m_s * np.identity(3)
            #U = np.identity(3) * m_s*(p_s - p_com).A1
            #U = m_s*se3.utils.skew(p_s) #- p_com)
            U = m_s*se3.utils.skew(p_i) #- p_com)
            #U = m_s*se3.utils.skew(lever)
            #V = I_s
            V = I_j
            O = np.zeros((3,3))
            col1 = np.vstack([T,U])
            col2 = np.vstack([O,V])
            arr_s += [np.hstack([col1,col2]).A]
        #[6,150]
        self.P_sys2 = self._diag((arr_s[0], arr_s[1], arr_s[2], arr_s[3], arr_s[4], arr_s[5], 
                                 arr_s[6], arr_s[7], arr_s[8], arr_s[9], arr_s[10],
                                 arr_s[11], arr_s[12], arr_s[13], arr_s[14], arr_s[15], 
                                 arr_s[16], arr_s[17], arr_s[18], arr_s[19], arr_s[20],
                                 arr_s[21], arr_s[22], arr_s[23], arr_s[24] ))
        #self.P_sys = np.hstack(y[:] for y in arr_s) 
        return self.P_sys2
        
    def _getdJ_sys(self):
        arr_s = []
        se3.computeJacobiansTimeVariation(self.robot.model, 
                                          self.robot.data, 
                                          self.q_mean[self.i], 
                                          self.dq_mean[self.i])
        for s in range(1,26):
            dJ_s = se3.getJacobianTimeVariation(self.robot.model, self.robot.data, s, True)
            arr_s += [dJ_s]
        dJ_sys = np.vstack(y[:] for y in arr_s)
        return dJ_sys
    
    def _getdP_sys(self):
        '''
        [ dT 0 ; dU dV]
        '''
        arr_s = []
        for s in range(1,26):
            m_s = self.robot.model.inertias[s].mass
            twist_s = self.robot.velocity(self.robot.q, self.robot.v, s, True)
            v_s = twist_s.linear
            w_j = twist_s.angular
            #lever from joint to CoM
            lever = self.robot.model.inertias[s].lever
            #angular velocity around center of mass
            w_s = w_j + np.matrix(np.cross(lever.A1,v_s.A1)).T
            v_com = self.robot.data.vcom[0]
            #postion of the joint wrt world
            p_i = self.robot.data.oMi[s].translation
            #postion of the segment CoM wrt world
            p_s =  p_i + lever
            #intertia wrt to joint
            I_j = self.robot.model.inertias[s].inertia 
            #intertia expressed at the CoM, parallel axis theorem
            I_s = I_j - ( (m_s*np.identity(3)) * (lever.A1*lever.A1) )
            # get matrix components of size [3 x 3s] each
            dT = np.zeros((3,3))
            dU = m_s*se3.utils.skew(v_s - v_com)
            dV = se3.utils.skew(w_s) * I_s 
            dO = np.zeros((3,3))
            col1 = np.vstack([dT, dU])
            col2 = np.vstack([dO, dV])
            arr_s += [np.hstack([col1,col2])]
        #[6,150]
        self.dP_sys = np.hstack(y[:] for y in arr_s) 
        return self.dP_sys

    def _getdAg(self):
        P_sys = self._getP_sys()
        J_sys = self._getJ_sys()
        dP_sys = self._getdP_sys()
        dJ_sys = self._getdJ_sys()
        dAg = (dP_sys * J_sys) + (P_sys * dJ_sys)
        return dAg

    def _getD(self, dA, dq):
        '''
        partial(dAg) / partial(dq)
        '''
        h = 1e-4
        #q1 = q0 (spatial operator) v1*h
        pass
    
    def _getE(self, A, dA, q):
        pass
        
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
        # TO VERIFY
        iHDi = (self.robot.model.inertias[s]*self.robot.data.a[s]) + se3.Inertia.vxiv(Y,V)
        #iHDi.linear 
        # express at the center of mass
        oMc = se3.SE3.Identity()
        oMc.translation = self.robot.data.oMi[1].translation - com
        #oMc.translation = com
        # uncomment in case need to change the rotation of the reference frame
        oMc.rotation = self.robot.data.oMi[1].rotation 
        cMi = oMc.actInv( self.robot.data.oMi[s] )
        
        cHi = cMi.act(iHi).np.A1
        cHDi = cMi.act(iHDi).np.A1 
        return cHi, cHDi        
    
    def _getJmean(self):
        # Get jacobian matrices
        Ag_list=[]
        for i in range(0, 100):
            se3.forwardKinematics(self.robot.model, 
                                  self.robot.data, 
                                  self.q_mean[i], 
                                  self.dq_mean[i], 
                                  self.ddq_mean[i])
            Ag = se3.ccrba(self.robot.model,
                           self.robot.data, 
                           self.q_mean[i], 
                           self.dq_mean[i])
            Ag_list.append(Ag[self._mask,:])       
        #D = bm.get_ddA_ddq + np.nan_to_num(self.robot.dAg)
        
        dAg_list = bm.diffM(Ag_list, self.time_mean)
        ddAg_list = bm.diffM(dAg_list, self.time_mean)
        self.G = bm.diffM(dAg_list, self.dq_mean.A1)
        self.H = bm.diffM(dAg_list, self.q_mean.A1)
        self.I = bm.diffM(Ag_list, self.q_mean.A1)
         
        Ag=[]; dAg=[];  ddAg=[]
        Je=[]
        if self.order == 1:
            for i in range(0, 100):
                Ag.append(np.matrix(Ag_list[i]))
                dAg.append(np.matrix(dAg_list[i]))
                ddAg.append(np.nan)
                Je.append(np.hstack([dAg_list[i], Ag_list[i]]))
            # Compute projector onto the nullspace
            NAg=self.nullspace(Ag)
            NdAg=self.nullspace(dAg)
            NddAg=np.nan
            self.ProjJ = self.nullspace(Je)

        elif self.order == 2:
            for i in range(0, 100):
                Ag.append(np.matrix(Ag_list[i]))
                #D = self._getD(dA_list[i], self.robot.dq_mean[i])
                dAg.append(np.matrix(2*dAg_list[i]))
                #E = self._getE(A_list[i], dA_list[i], self.robot.q_mean[i])
                ddAg.append(np.matrix(ddAg_list[i]))
                Je.append(np.hstack([ddAg_list[i], 2*dAg_list[i], Ag_list[i]]))
            # Compute projector onto the nullspace
            NAg=self.nullspace(Ag)
            NdAg=self.nullspace(dAg)
            NddAg=self.nullspace(ddAg)
            #self.ProjJ = self.nullspace(Je)
            self.ProjJ = self.nullspace(Ag)

        return Ag, NAg, dAg, NdAg, ddAg, NddAg
    

    def _getDynTask(self):
        task=[]; Jtask=[]; drift=[] ;taskNormalized=[]; Ntask=[];
        contributionH=[]; contributionF=[];
        hg=[];# H2=[]
        Ag, NAg, dAg, NdAg, ddAg, NddAg = self._getJmean()
        Jtask.append(['J',Ag])
        Jtask.append(['dJ',dAg])
        Jtask.append(['ddJ', ddAg])
        Ntask.append(['NJ', NAg])
        Ntask.append(['NdJ', NdAg])
        Ntask.append(['NddJ', NddAg])
        for i in range(0, 100):
            self.i = i
            self.updateAll(self.q_mean[i], self.dq_mean[i], self.ddq_mean[i])
            se3.forwardKinematics(self.robot.model, 
                                  self.robot.data, 
                                  self.q_mean[i], 
                                  self.dq_mean[i], 
                                  self.ddq_mean[i])

            # --- Centroidal Momenta
            A = se3.ccrba(self.robot.model, 
                          self.robot.data, 
                          self.q_mean[i], 
                          self.dq_mean[i])
            Hg = self.robot.data.hg.np.A.copy()
            # ---- Its rate of change
            b = self._getBiais(self.q_mean[i], self.dq_mean[i]) #check it
            # Individual contributions to centroidal momenta (and its rate of change)
            segH = []; segF=[]
            p_com = self.robot.com(self.q_mean[i])
            for s in range(1,26):
                hc, hcd = self._getContribution(p_com,s) 
                segH.append(hc)
                segF.append(hcd)
            Hdot = np.matrix(np.sum(np.array(segF).squeeze(),0)).T
            self.dH = Hdot.copy() 
            #gravityF = np.matrix([[0,0,1/self._KF,0,0,0]]).T
            #Hdot += gravityF
            Hdot = np.matrix(np.vstack([self._KF * Hdot[0:3], self._KT * Hdot[3:6]]))
            self.Hdot = Hdot 
            #self.robot.data.com[0] = p_com
            self.check()
            # ---- Store data
            # Centroidal Momenta
            hg.append(Hg.copy()*self._K)
            self.h = hg
            # Rate of Change
            taskNormalized.append(Hdot)#[self._mask])
            self.taskNormalized = taskNormalized
            drift.append(b[self._mask] * self._K)
            #Jtask.append(A[self._mask,:])
            # Invidual joint contribution
            contributionH.append(np.array(segH).squeeze())
            contributionF.append(np.array(segF).squeeze())
            self.contribution = contributionH
            self.contributionF = contributionF
        return taskNormalized, Jtask, Ntask, drift
        
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

        for i in xrange (nRep):
            for t in xrange(tmax):
                q[t,:,i] = np.matrix(self.Q[i]['pinocchio_data'][t]).squeeze()
                dq[t,:,i] = np.matrix(self.DQ[i][t]).squeeze()
                ddq[t,:,i] = np.matrix(self.DDQ[i][t]).squeeze()
                se3.forwardKinematics(self.robot.model, 
                                      self.robot.data, 
                                      q[t,:,i], 
                                      dq[t,:,i], 
                                      ddq[t,:,i])
                se3.centerOfMass(self.robot.model,
                                 self.robot.data,
                                 q[t,:,i], 
                                 dq[t,:,i], 
                                 ddq[t,:,i])#, True)
    
                # centroidal momenta
                A = se3.ccrba(self.robot.model, 
                              self.robot.data, 
                              q[t,:,i], 
                              dq[t,:,i])
                #H = self.robot.data.hg.np.A.copy()
                b = self._getBiais(q[t,:,i], dq[t,:,i]) # check calculation
                #Hdot2 = (A * np.matrix(ddq[t,:,i]).squeeze().T) + b.copy() - (self.robot.data.mass[0] * self.robot.model.gravity.vector)

                # Segmental contributions to centroidal momenta (and its rate of change)
                segH = []; segF=[]
                p_com = self.robot.com(q[t,:,i])
                for s in range(1,26):
                    (segH, segF) =  self._getContribution(p_com,s)
                    data_Hgs[t,:,i,s] = segH #* self._K
                    data_dHgs[t,:,i,s] = segF #* self._K
                Hdot =  np.matrix(np.sum(data_dHgs[t,:,i],1)).T #- (self.robot.data.mass[0] * self.robot.model.gravity.vector*self._K)
                Hdot = np.matrix(np.vstack([self._KF * Hdot[0:3], self._KT * Hdot[3:6]]))
                
                #+ (b*self._K) #
                #Hdot = self._K * Hdot2.copy()
                #Hdot[0:3] = (self.robot.data.mass[0]*self.robot.data.acom[0]) *self._K
                #HH = np.matrix(np.vstack([self._KF * H[0:3], self._KT * H[3:6]]))
                H =  np.matrix(np.sum(data_Hgs[t,:,i],1)).T
                HNormalized = np.matrix(np.vstack([self._KF * H[0:3], self._KT * H[3:6]]))#H.copy()*self._K
                bNormalized = b.copy()*self._K
                HdotNormalized = Hdot.copy()*self._K
                data_Hg[t,:,i] = HNormalized.squeeze()
                data_dHg[t,:,i] = Hdot.squeeze()
                data_drift[t,:,i] = b.squeeze()
                                
        data['q'].append(q)
        data['dq'].append(dq)
        data['ddq'].append(ddq)
        data['hg'].append(data_Hg)
        data['dhg'].append(data_dHg)
        data['drift'].append(data_drift)
        data['hg_segments'].append(data_Hgs)
        data['dhg_segments'].append(data_dHgs)
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

Jtask=[]
        for i in range(0, 100):
            Jtask.append(np.hstack([sublist[i],Alist[i]]))
    '''
    
    def getUCMVariances(self):
        #self.computeStats()
        self.getReferenceConfigurations(self.Q)
        self.data = self.momentaExtraction()
        (self.task, self.JTask, self.NTask, self.drift) = self._getDynTask()
        #self.JTask = self._getJmeank()
        #self.NTask = self.nullspace(self.JTask)
        self.n_ucm = self.repNo * (self.robot.nv-self.dim)
        self.n_cm = self.repNo * self.dim
        #print q_dq_ddq_data.shape
        #print q_dq_ddq.shape
        #print self.NTask.shape
        if self.order == 0:
            data_mean = self.q_mean
            data = self.q_data
            (self.Vucm, self.Vcm, self.criteria) = self.varianceFromManifoldsPos(data_mean, 
                                                                          data, 
                                                                          self.NTask, 
                                                                          self.n_ucm, 
                                                                          self.n_cm, 
                                                                          'log')
        elif self.order == 1:
            dof=self.robot.nq+self.robot.nv
            data_mean = np.matrix(np.zeros([100,dof]))
            data = np.array(np.zeros([100,dof,self.repNo]))
            for i in xrange (0,100):
                data_mean[i,:] = np.hstack([self.q_mean[i],self.dq_mean[i]])
                for nrep in xrange(0,self.repNo):
                    data[i,:,nrep] = np.hstack([self.q_data[i,:,nrep],self.dq_data[i,:,nrep]])
            (self.Vucm, self.Vcm, self.criteria) = self.varianceFromManifoldsVel(data_mean, 
                                                                          data, 
                                                                          self.NTask, 
                                                                          self.n_ucm, 
                                                                          self.n_cm, 
                                                                          'log')
        elif self.order == 2:
            dof=self.robot.nq+self.robot.nv+self.robot.nv
            data_mean = np.matrix(np.zeros([100,dof]))
            data = np.array(np.zeros([100,dof,self.repNo]))
            for i in xrange (0,100):
                data_mean[i,:] = np.hstack([self.q_mean[i],self.dq_mean[i],self.ddq_mean[i]])
                for nrep in xrange(0,self.repNo):
                    data[i,:,nrep] = np.hstack([self.q_data[i,:,nrep],
                                                self.dq_data[i,:,nrep],
                                                self.ddq_data[i,:,nrep]])
            (self.Vucm, self.Vcm, self.criteria) = self.varianceFromManifoldsAcc(data_mean, 
                                                                          data, 
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
        self.n_ucm = self.repNo * (self.robot.nv - self.dim)
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





