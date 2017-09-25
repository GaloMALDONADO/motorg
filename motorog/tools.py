import numpy as np
from bmtools.filters import filtfilt_butter
import pinocchio as se3
import hqp.wrapper as wrapper
import tools
def meanConfiguration(robot,motion):
    ''' 
    Motion is a collection of configurations that
    should be normalized between 0% and 100%
    Get reference configuration and std:
    dataMean = mean(q(t))                                                                      
    dataStd = std(q(t))
    '''
    nRep = len(motion)
    tmax = len(motion[0]['pinocchio_data'])
    #DoF = motion[0]['pinocchio_data'][0].A1.shape[0] 
    DoF = 42
    data = []
    dataMean = []
    dataStd = []
    dataStr = np.zeros((tmax,49,nRep))
    #for dof in xrange(DoF):
    for t in xrange(tmax):
        for i in xrange (nRep):
            #data += [np.array(motion[i]['pinocchio_data'][t]).squeeze()]
            #dataStr[t,:,i] = motion[i]['pinocchio_data'][t]
            data += [np.array(motion[i]['osim_data'][t]).squeeze()]
            dataStr[t,:,i] = motion[i]['pinocchio_data'][t]
        data2 = np.matrix(data)
        dataMean += [robot.dof2pinocchio(np.mean(data2,0).A1)]
        dataStd += [robot.dof2pinocchio(np.std(data2,0).A1)]
    return np.matrix(dataMean), np.matrix(dataStd), dataStr


def meanConfiguration2(robot,motion):
    ''' 
    Motion is a collection of configurations that
    should be normalized between 0% and 100%
    Get reference configuration and std:
    dataMean = mean(q(t))                                                                      
    dataStd = std(q(t))
    '''
    nRep = len(motion)
    tmax = 100
    #DoF = motion[0]['pinocchio_data'][0].A1.shape[0] 
    DoF = 42
    data = []
    dataMean = []
    dataStd = []
    dataStr = np.zeros((tmax,DoF,nRep))
    #for dof in xrange(DoF):
    for t in xrange(tmax):
        for i in xrange (nRep):
            #data += [np.array(motion[i]['pinocchio_data'][t]).squeeze()]
            #dataStr[t,:,i] = motion[i]['pinocchio_data'][t]
            coordinates= motion[i][t]
            data += [np.array(coordinates).squeeze()]
            dataStr[t,:,i] = coordinates
        data2 = np.matrix(data)
        dataMean += [np.mean(data2,0).A1]
        dataStd += [np.std(data2,0).A1]
    return np.matrix(dataMean), np.matrix(dataStd), dataStr


def meanVelocities(model, x, t, cutoff, fs, filter_order):
    Nrep = x.shape[2]
    tmax = x.shape[0]
    DoF = model.nv
    #v = []
    data = []
    dataMean = []
    dataStd = []
    dataStr = np.zeros((tmax,DoF,Nrep))
    dataF = np.zeros((tmax,DoF,Nrep))
    for r in xrange(Nrep):
        for i in range(1,tmax):
        # velocity
            if i >= 1:
                dt = (t[i,r]-t[i-1,r]) #foward difference
                q1 = x[i-1,:,r]
                q2 = x[i,:,r]
                diff = se3.differentiate(model, q1,  q2)/dt
                dataStr[i,:,r] = diff.A1
        dataStr[0,:,r] = dataStr[1,:,r].copy()
        #filter
        for j in xrange(DoF):
            dataF[:,j,r] = filtfilt_butter(dataStr[:,j,r],
                                           cutoff,
                                           fs,
                                           filter_order)
    # stats
    for i in xrange(tmax):
        data = dataF[i,:,:]
        data2 = np.matrix(data)
        dataMean += [np.mean(data2,1).A1]
        dataStd += [np.std(data2,1).A1]
    return np.matrix(dataMean), np.matrix(dataStd), dataF

def meanAccelerations(v, t, cutoff, fs, filter_order):
    Nrep = v.shape[2]
    tmax = v.shape[0]
    DoF = 42
    data = []
    dataMean = []
    dataStd = []
    dataStr = np.zeros((tmax,DoF,Nrep))
    dataF = np.zeros((tmax,DoF,Nrep))
    for r in xrange(Nrep):
        
        for i in range(1,tmax):
        # velocity
            if i >= 1:
                dt = (t[i,r]-t[i-1,r])
                v1 = v[i-1,:,r]
                v2 = v[i,:,r]
                diff = np.gradient(np.array([v1,  v2]), dt)[0][0]
                dataStr[i,:,r] = diff.copy()
        dataStr[0,:,r] = dataStr[1,:,r].copy()
        #filter
        for j in xrange(DoF):
            dataF[:,j,r] = filtfilt_butter(dataStr[:,j,r],
                                           cutoff,
                                           fs,
                                           filter_order)
    # stats
    for i in xrange(tmax):
        data = dataF[i,:,:]
        data2 = np.matrix(data)
        dataMean += [np.mean(data2,1).A1]
        dataStd += [np.std(data2,1).A1]
    return np.matrix(dataMean), np.matrix(dataStd), dataF


def meanVar(var):
    tmax = len(var[0])
    dataMean = []  
    dataStd = []
    for t in xrange(tmax):
        dataMean += [np.mean(var[:,t],0)]
        dataStd += [np.std(var[:,t],0)]
    return np.matrix(dataMean), np.matrix(dataStd)


def meanTime(motion):
    nRep = len(motion)
    tmax = 100
    data = []
    dataMean = []
    dataStd = []
    dataStr = np.zeros((tmax,nRep))
    for r in xrange (nRep):
        data += [motion[r]['time']]
        dataStr[:,r] = motion[r]['time']
    dataMean =  np.mean(data,0)
    dataStd = np.std(data,0)
    return np.matrix(dataMean).squeeze(), np.matrix(dataStd).squeeze(), dataStr



def filterMatrix(M, cutoff, fs, filter_order):
    # time x degreees of freedom
    fDof = []
    colsNo = np.shape(M)[1]    
    for i in xrange(colsNo):
        fDof += [
                filtfilt_butter(np.array(M[:,i]).squeeze(),
                        cutoff,
                        fs,
                        filter_order)
        ]
    return np.matrix(fDof,dtype=np.float64).T

def meanTask(task):
    pass



# ----------------------------------------                                                                       
#   Tools for computing range of motion                                                                          
# ----------------------------------------  
class RoM(object):
    def __init__(self, robot):
        self.robot = robot

    def qRoM(self, q, idx, deg=True):
        qidx = [q[i][idx] for i in xrange(len(q))]
        if deg is True:
            return np.rad2deg(max(qidx)-min(qidx))
        else:
            return max(qidx)-min(qidx)

    def quatToRpy(self, quat, deg=True):
        quatM = np.matrix([quat[0,0], quat[1,0],
                           quat[2,0], quat[3,0] ], np.float)
        quatA = np.squeeze(np.asarray(quatM))
        rpy = se3.utils.matrixToRpy(se3.Quaternion(quatA[3], quatA[0], quatA[1], quatA[2]).matrix())
        return rpy

    def quatRoM(self, q, idx , deg=True):
        # get rpy matrix                                                                                        
        qidx = [self.quatToRpy(q[i].T[idx:idx+4,0]) for i in xrange(len(q))]
        x = [qidx[i][0,0] for i in xrange(len(qidx))]
        y = [qidx[i][1,0] for i in xrange(len(qidx))]
        z = [qidx[i][2,0] for i in xrange(len(qidx))]
        if deg is True:
            r = np.rad2deg(max(x)-min(x))
            p = np.rad2deg(max(y)-min(y))
            y = np.rad2deg(max(z)-min(z))
            return r, p, y
        else:
            r = max(x)-min(x)
            p = max(y)-min(y)
            y = max(z)-min(z)
            return r, p, y
    def getRoM(self, q, deg=True):
        RoM = {'knee_flex_ext_l':[], 'knee_flex_ext_r':[],
               'elbow_flex_ext_l':[], 'elbow_flex_ext_r':[],
               'trunk_flex_ext':[], 'trunk_abd_add':[], 'trunk_rot':[],
               'neck_flex_ext':[], 'neck_abd_add':[], 'neck_rot':[],
               'shoulder_flex_ext_l':[], 'shoulder_flex_ext_r':[],
               'shoulder_abd_add_l':[], 'shoulder_abd_add_r':[],
               'shoulder_rot_l':[], 'shoulder_rot_r':[],
               'hip_flex_ext_l':[], 'hip_flex_ext_r':[],
               'hip_abd_add_l':[], 'hip_abd_add_r':[],
               'hip_rot_l':[], 'hip_rot_r':[]}
        # Head and Neck                                                                                         
        r,p,y = self.quatRoM(q, self.robot.getDoF('neck'), deg)
        RoM['neck_flex_ext'].append(r)
        RoM['neck_abd_add'].append(p)
        RoM['neck_rot'].append(y)
        # Trunk                                                                                                 
        r,p,y = self.quatRoM(q, self.robot.getDoF('back'), deg)
        RoM['trunk_flex_ext'].append(r)
        RoM['trunk_abd_add'].append(p)
        RoM['trunk_rot'].append(y)
        # Shoulders                                                                                             
        r,p,y = self.quatRoM(q, self.robot.getDoF('acromial_r'), deg)
        RoM['shoulder_flex_ext_r'].append(r)
        RoM['shoulder_abd_add_r'].append(p)
        RoM['shoulder_rot_r'].append(y)
        r,p,y = self.quatRoM(q, self.robot.getDoF('acromial_l'), deg)
        RoM['shoulder_flex_ext_l'].append(r)
        RoM['shoulder_abd_add_l'].append(p)
        RoM['shoulder_rot_l'].append(y)
        # Elbows                                                                                                
        RoM['elbow_flex_ext_r'].append( self.qRoM(q, self.robot.getDoF('elbow_r'), deg) )
        RoM['elbow_flex_ext_l'].append( self.qRoM(q, self.robot.getDoF('elbow_l'), deg) )
        # Hips                                                                                                  
        r,p,y = self.quatRoM(q, self.robot.getDoF('hip_r'), deg)
        RoM['hip_flex_ext_r'].append(r)
        RoM['hip_abd_add_r'].append(p)
        RoM['hip_rot_r'].append(y)
        r,p,y = self.quatRoM(q, self.robot.getDoF('hip_l'), deg)
        RoM['hip_flex_ext_l'].append(r)
        RoM['hip_abd_add_l'].append(p)
        RoM['hip_rot_l'].append(y)
        RoM['knee_flex_ext_r'].append( self.qRoM(q, self.robot.getDoF('knee_r'), deg) )
        RoM['knee_flex_ext_l'].append( self.qRoM(q, self.robot.getDoF('knee_l'), deg) )
        return RoM

def meanQ(robot,q):
    ''' 
    Motion is a collection of configurations that
    should be normalized between 0% and 100%
    Get reference configuration and std:
    dataMean = mean(q(t))                                                                      
    dataStd = std(q(t))
    '''
    nRep = len(motion)
    tmax = len(motion[0]['pinocchio_data'])
    #DoF = motion[0]['pinocchio_data'][0].A1.shape[0] 
    DoF = 42
    data = []
    dataMean = []
    dataStd = []
    dataStr = np.zeros((tmax,49,nRep))
    #for dof in xrange(DoF):
    for t in xrange(tmax):
        for i in xrange (nRep):
            data += [np.array(motion[i][t]).squeeze()]
            dataStr[t,:,i] = motion[i][t]
        data2 = np.matrix(data)
        dataMean += [robot.dof2pinocchio(np.mean(data2,0).A1)]
        dataStd += [robot.dof2pinocchio(np.std(data2,0).A1)]
    return np.matrix(dataMean), np.matrix(dataStd), dataStr
