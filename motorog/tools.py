import numpy as np
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
        for t in xrange(tmax):
            for dof in xrange(DoF):
                for i in xrange (nRep):
                    data += [np.array(motion[i]['pinocchio_data'][t]).squeeze()]
            data2 = np.matrix(data)
            dataMean += [np.mean(data2,0).A1]
            dataStd += [np.std(data2,0).A1]
        return np.matrix(dataMean), np.matrix(dataStd)


