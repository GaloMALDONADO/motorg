import numpy as np
from bmtools.filters import filtfilt_butter

def derivatefilterQ(model, q, t, cutoff, fs, filter_order=4):
    '''                                   
    Differentiate data using backwards finite differences and 
    butterworth low pass filter. Takes care of quaternions
    Inputs:                               
    - Q : numpy matrix double x=time, y=coordinates(model.nq) 
    - t : numpy vector of time 
    - cutoff : cutoff frequency
    - fs : sampling frequency
    Output                                
    - V : numpy matrix double x=time, y=coordinates(model.nv)
    '''
    
    # Debug
    q = q.squeeze()
    t = t.squeeze()
    if type(q) != np.matrixlib.defmatrix.matrix:
        q = np.matrix(q).squeeze()
    if type(t) != np.ndarray:
        t = np.array(t).squeeze()
        
    assert type(q) == np.matrixlib.defmatrix.matrix
    assert type(t) == np.ndarray
    assert q.shape[0] == len(t)
    assert q.shape[1] == model.nq
    
    # Differentiate
    dq = np.empty((len(t), model.nv))
    for frame in xrange(0,len(t)-1):
        # Backward differences
        dt = np.float64(t[frame+1]-t[frame])
        q1 = q[frame,:]
        q2 = q[frame+1,:]
        diff = se3.differentiate(model, q1,  q2)/dt
        dq[frame,:] = diff.A1
    dq[-1,:] = dq[-2,:]

    # Filter
    dq_prime = np.empty((len(t), model.nv))
    for i in xrange(model.nv):
        filtered = filtfilt_butter(dq[:,i], cutoff, fs, filter_order)    
        dq_prime[:,i] = filtered
  
    return np.matrix(dq_prime)

    
def derivatefilterV(model, dq, t, cutoff, fs, filter_order=4):
    '''                                   
    Differentiate data using backwards finite differences and 
    butterworth low pass filter
    Inputs:                               
    - dq : numpy matrix double x=time, y=coordinates(model.nv) 
    - t : numpy vector of time 
    - cutoff : cutoff frequency
    - fs : sampling frequency
    Output                                
    - ddq : numpy matrix double x=time, y=coordinates(model.nv)
    '''
    # Debug
    dq = dq.squeeze()
    t = t.squeeze()
    if type(dq) != np.matrixlib.defmatrix.matrix:
        dq = np.matrix(dq).squeeze()
    if type(t) != np.ndarray:
        t = np.array(t).squeeze()
        
    assert type(dq) == np.matrixlib.defmatrix.matrix
    assert type(t) == np.ndarray
    assert dq.shape[0] == len(t)
    assert dq.shape[1] == model.nv

    # Differentiate
    ddq = np.empty((len(t), model.nv))

    for frame in xrange(0,len(t)-1):
        # Backward differences
        dt = np.float64(t[frame+1]-t[frame])
        diff = (dq[frame+1,:] - dq[frame,:])/np.float64(dt)
        ddq[frame,:] = diff.A1
    ddq[-1,:] = ddq[-2,:]

    # Filter
    ddq_prime = np.empty((len(t), model.nv))
    for i in xrange(model.nv):
        filtered = filtfilt_butter(ddq[:,i], cutoff, fs, filter_order)    
        ddq_prime[:,i] = filtered
  
    return np.matrix(ddq_prime)
    
