print 'tools'
import numpy as np
from bmtools.filters import filtfilt_butter
import pinocchio as se3

def meanConfiguration(motion):
    ''' 
    Motion is a collection of configurations that
    should be normalized between 0% and 100%
    Get reference configuration and std:
    dataMean = mean(q(t))                                                                      
    dataStd = std(q(t))
    '''
    nRep = len(motion)
    tmax = len(motion[0]['pinocchio_data'])
    DoF = motion[0]['pinocchio_data'][0].A1.shape[0] 
    data = []
    dataMean = []
    dataStd = []
    dataStr = np.zeros((tmax,DoF,nRep))
    #for dof in xrange(DoF):
    for t in xrange(tmax):
        for i in xrange (nRep):
            data += [np.array(motion[i]['pinocchio_data'][t]).squeeze()]
            dataStr[t,:,i] = motion[i]['pinocchio_data'][t]
        data2 = np.matrix(data)
        dataMean += [np.mean(data2,0).A1]
        dataStd += [np.std(data2,0).A1]
    return np.matrix(dataMean), np.matrix(dataStd), dataStr

def meanVelocities(model, x, t, cutoff, fs, filter_order):
    Nrep = x.shape[2]
    tmax = x.shape[0]
    DoF = model.nv
    v = []
    data = []
    dataMean = []
    dataStd = []
    dataStr = np.zeros((tmax,DoF,Nrep))
    dataF = np.zeros((tmax,DoF,Nrep))
    for r in xrange(Nrep):
        for i in xrange(tmax):
        # velocity
            if i >= 1:
                dt = (t[i,r]-t[i-1,r])
                q1 = x[i-1,:,r]
                q2 = x[i,:,r]
                diff = se3.differentiate(model, q1,  q2)/dt
                dataStr[i,:,r] = diff.A1
        #filter
        for j in xrange(DoF):
            dataF[:,j,r] = filtfilt_butter(dataStr[:,j,r],
                                           10,
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

