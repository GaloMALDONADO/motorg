import matplotlib.pyplot as plt
import numpy as np
import indexes

class Plot:
    def __init__(self, task, degrees=True):
        self.task = task
        self.participantsNo = len(self.task)
        self.coordinateNames = np.matrix(indexes.coordinates).squeeze()[:,1].A1
        self.jointNames = np.matrix(indexes.joints).squeeze()[:,1].A1
        plt.ion()
        if degrees is True:
            self.k = np.rad2deg(1)

    def plot(self):
        fig = plt.figure ()
        fig.canvas.set_window_title(self.windowTitle)
        ax = fig.add_subplot ('111')
        return fig, ax

    def plotAllVelocities(self):
        fig = plt.figure ()
        fig.canvas.set_window_title('Generalized Velocities')
        ax = fig.add_subplot ('111')
        plt.title('Generalized Velocities')
        for i in xrange (self.participantsNo):
            ax.plot(self.k * self.task[i].v_mean, linewidth=3.0)

        legends = self.coordinateNames
        ax.legend(legends)
        plt.show()
    
    def plotTask(self):
        fig = plt.figure()
        fig.canvas.set_window_title(self.windowTitle)
        
        task = [np.array(self.task[i].task).squeeze() for i in xrange(self.participantsNo)]
        task_hat = np.mean(task,0)
        taskStd_hat = np.std(task,0)
        
        taskPlus = task_hat + taskStd_hat
        taskMin = task_hat - taskStd_hat
        
        dim = task_hat.ndim
        if dim == 1:
            ax_str = '111'
            ax = fig.add_subplot(ax_str)
            plt.title('Task')
            ax.plot(task_hat,'-r', linewidth=3.0)
            ax.plot(taskPlus,'-k',color = '0.75', linewidth=1.0, linestyle='--')
            ax.plot(taskMin,'-k' ,color = '0.75',linewidth=1.0, linestyle='--')
            plt.xlabel('Phase' + '%')
            plt.ylabel('Momentum $[N]$')
        else:
            rows = task_hat.shape[1]
            for i in xrange(rows):
                ax_str = str(rows)+'1'+str(i+1)
                ax = fig.add_subplot(ax_str)
                plt.title('Task')
                ax.plot(task_hat[:,i],'-r', linewidth=3.0)
                ax.plot(taskPlus[:,i],'-k',color = '0.75', linewidth=1.0, linestyle='--')
                ax.plot(taskMin[:,i],'-k' ,color = '0.75',linewidth=1.0, linestyle='--')
                plt.ylabel('$[N]$')
                plt.xlabel('Phase' + '%')
            

        self.task_hat = task_hat
        self.task_std = taskStd_hat
        return ax, plt

    def UCMAnalysis(self):
        fig = plt.figure()
        s = self.windowTitle+' '+self.name
        fig.canvas.set_window_title(s)

        vucm = [self.task[i].Vucm for i in xrange(self.participantsNo)]
        vcm = [self.task[i].Vcm for i in xrange(self.participantsNo)]
        c = [self.task[i].criteria for i in xrange(self.participantsNo)]
        
        vucm_hat = np.mean(vucm,0)
        vucmStd_hat = np.std(vucm,0)
        vcm_hat = np.mean(vcm,0)
        vcmStd_hat = np.std(vcm,0)
        c_hat = np.mean(c,0)
        cStd_hat = np.std(c,0)
        
        vucmPlus = vucm_hat + vucmStd_hat
        vcmPlus = vcm_hat + vcmStd_hat
        cPlus = c_hat + cStd_hat
        vucmMin = vucm_hat - vucmStd_hat
        vcmMin = vcm_hat - vcmStd_hat
        cMin = c_hat - cStd_hat
        
        ax = fig.add_subplot ('311')
        plt.title('Uncontrolled Manifold')
        ax.plot(vucm_hat, 'r', linewidth=3.0)
        ax.plot(vucmPlus.T,'-k',color = '0.75', linewidth=1.0, linestyle='--')
        ax.plot(vucmMin.T,'-k' ,color = '0.75',linewidth=1.0, linestyle='--')
        plt.xlabel('Phase '  + '%')
        plt.ylabel('variance')

        ax = fig.add_subplot ('312')
        plt.title('Orthogonal Manifold')
        ax.plot(vcm_hat, 'b', linewidth=3.0)
        ax.plot(vcmPlus.T,'-k',color = '0.75', linewidth=1.0, linestyle='--')
        ax.plot(vcmMin.T,'-k' ,color = '0.75',linewidth=1.0, linestyle='--')
        plt.xlabel('Phase '  + '%')
        plt.ylabel('variance')

        ax = fig.add_subplot ('313')
        plt.title('Criteria')
        ax.plot(c_hat, 'k', linewidth=3.0)
        ax.plot(cPlus.T,'-k',color = '0.75', linewidth=1.0, linestyle='--')
        ax.plot(cMin.T,'-k' ,color = '0.75',linewidth=1.0, linestyle='--')
        plt.xlabel('Phase '  + '%')

        self.vucm_hat = vucm_hat
        self.vucmStd_hat = vucmStd_hat
        self.vcm_hat = vcm_hat
        self.vcmStd_hat = vcmStd_hat
        self.c_hat = c_hat
        self.cStd_hat = cStd_hat

    

class Joint(Plot):
    def __init__(self, task, name):
        Plot.__init__(self, task)
        self.windowTitle = 'Joint task'
        self.coordinatesTitle = 'Generalized coordinates'
        self.velocityTitle = 'Generalized velocities'
        self.accelerationTitle = 'Generalized accelerations'
        self.name = name
        
        
    def plotQ(self):
        fig, ax = self.plot()
        plt.title(self.coordinatesTitle)
        q=[]
        qstd=[]
        for i in xrange (self.participantsNo):
            q+=[self.k*self.task[i].q_mean[:,indexes.coordinateIndex(self.name)].squeeze()]
            qstd += [self.k*self.task[i].q_std[:,indexes.coordinateIndex(self.name)].squeeze()]
        q_hat = np.mean(np.array(q),0)
        qstd_hat =  np.std(np.array(qstd),0)
        qMin = q_hat - qstd_hat
        qPlus = q_hat + qstd_hat
        ax.plot(q_hat.T,'-r', linewidth=3.0)
        ax.plot(qPlus.T,'-k',color = '0.75', linewidth=1.0, linestyle='--')
        ax.plot(qMin.T,'-k' ,color = '0.75',linewidth=1.0, linestyle='--')
        plt.xlabel('Phase' + '%')
        plt.ylabel(self.name + ' $[deg]$')
        self.q_hat = q_hat
        self.q_std = qstd_hat
        

    def plotV(self):
        fig, ax = self.plot()
        plt.title(self.velocityTitle)
        dq=[]
        dqstd=[]
        for i in xrange (self.participantsNo):
            dq+=[self.k*self.task[i].dq_mean[:,indexes.coordinateIndex(self.name)].squeeze()]
            dqstd += [self.k*self.task[i].dq_std[:,indexes.coordinateIndex(self.name)].squeeze()]
        dq_hat = np.mean(np.array(dq),0)
        dqstd_hat =  np.std(np.array(dqstd),0)
        dqMin = dq_hat - dqstd_hat
        dqPlus = dq_hat + dqstd_hat
        ax.plot(dq_hat.T,'-r', linewidth=3.0)
        ax.plot(dqPlus.T,'-k',color = '0.75', linewidth=1.0, linestyle='--')
        ax.plot(dqMin.T,'-k' ,color = '0.75',linewidth=1.0, linestyle='--')
        plt.xlabel('Phase' + '%')
        plt.ylabel(self.name + '$[deg \cdot s^{-1}]$')
        self.dq_hat = dq_hat
        self.dq_std = dqstd_hat

    def plotA(self):
        fig, ax = self.plot()
        plt.title(self.accelerationTitle)
        ddq=[]
        ddqstd=[]
        for i in xrange (self.participantsNo):
            ddq+=[self.k*self.task[i].ddq_mean[:,indexes.coordinateIndex(self.name)].squeeze()]
            ddqstd += [self.k*self.task[i].ddq_std[:,indexes.coordinateIndex(self.name)].squeeze()]
        ddq_hat = np.mean(np.array(ddq),0)
        ddqstd_hat =  np.std(np.array(ddqstd),0)
        ddqMin = ddq_hat - ddqstd_hat
        ddqPlus = ddq_hat + ddqstd_hat
        ax.plot(ddq_hat.T,'-r', linewidth=3.0)
        ax.plot(ddqPlus.T,'-k',color = '0.75', linewidth=1.0, linestyle='--')
        ax.plot(ddqMin.T,'-k' ,color = '0.75',linewidth=1.0, linestyle='--')
        plt.xlabel('Phase '  + '%')
        plt.ylabel(self.name + '$[deg \cdot s^{-2}]$')
        self.ddq_hat = ddq_hat
        self.ddq_std = ddqstd_hat
    
        

        
class CentroidalMomentum(Plot):
    def __init__(self, task, name=''):
        Plot.__init__(self, task)
        self.windowTitle = 'Momentum task'
        self.Title = 'Centroidal momenta task'
        self.momentumTitle = 'Rate of change of centroidal momenta task'
        self.name = name
    
    def plotLinearMomentumImpulsion(self):
        fig = plt.figure()
        fig.canvas.set_window_title(self.windowTitle)
        
        task = [np.array(self.task[i].taskNormalized).squeeze() for i in xrange(self.participantsNo)]
        task_hat = np.mean(task,0)
        taskStd_hat = np.std(task,0)
        
        taskPlus = task_hat + taskStd_hat
        taskMin = task_hat - taskStd_hat
        
        ax = fig.add_subplot('211')
        plt.title('Impulsion: antero-posterior force')
        ax.plot(task_hat[:,0],'-r', linewidth=3.0)
        ax.plot(taskPlus[:,0],'-k',color = '0.75', linewidth=1.0, linestyle='--')
        ax.plot(taskMin[:,0],'-k' ,color = '0.75',linewidth=1.0, linestyle='--')
        plt.ylabel('$[N \cdot BW^{-1}]$')
        plt.legend(['mean','mean $\pm$ std'],loc=4)

        ax = fig.add_subplot('212')
        plt.title('Impulsion: vertical force')
        ax.plot(task_hat[:,1],'-r', linewidth=3.0)
        ax.plot(taskPlus[:,1],'-k',color = '0.75', linewidth=1.0, linestyle='--')
        ax.plot(taskMin[:,1],'-k' ,color = '0.75',linewidth=1.0, linestyle='--')
        plt.ylabel('$[N \cdot BW^{-1}]$')
        plt.xlabel('Phase' + '%')
        plt.legend(['mean','mean $\pm$ std'],loc=1)
        plt.xlabel('Phase' + '%')
        
    def plotLinearMomentumAbs(self):
        fig = plt.figure()
        fig.canvas.set_window_title(self.windowTitle)
        
        task = [np.array(self.task[i].taskNormalized).squeeze() for i in xrange(self.participantsNo)]
        task_hat = np.mean(task,0)
        taskStd_hat = np.std(task,0)
        
        taskPlus = task_hat + taskStd_hat
        taskMin = task_hat - taskStd_hat
        
        ax = fig.add_subplot('111')
        plt.title('Landing: vertical force')
        ax.plot(task_hat,'-r', linewidth=3.0)
        ax.plot(taskPlus,'-k',color = '0.75', linewidth=1.0, linestyle='--')
        ax.plot(taskMin,'-k' ,color = '0.75',linewidth=1.0, linestyle='--')
        plt.ylabel('$[N \cdot BW^{-1}]$')
        plt.xlabel('Phase' + '%')
        plt.legend(['mean','mean $\pm$ std'],loc=4)
        plt.xlabel('Phase' + '%')

    def plotLinearMomentumStab(self):
        fig = plt.figure()
        fig.canvas.set_window_title(self.windowTitle)
        
        task = [np.array(self.task[i].taskNormalized).squeeze() for i in xrange(self.participantsNo)]
        task_hat = np.mean(task,0)
        taskStd_hat = np.std(task,0)
        
        taskPlus = task_hat + taskStd_hat
        taskMin = task_hat - taskStd_hat
        
        ax = fig.add_subplot('211')
        plt.title('Landing: medial-lateral force')
        ax.plot(task_hat[:,1],'-r', linewidth=3.0)
        ax.plot(taskPlus[:,1],'-k',color = '0.75', linewidth=1.0, linestyle='--')
        ax.plot(taskMin[:,1],'-k' ,color = '0.75',linewidth=1.0, linestyle='--')
        plt.ylabel('$[N \cdot BW^{-1}]$')
        plt.legend(['mean','mean $\pm$ std'],loc=1)
        
    
        ax = fig.add_subplot('212')
        plt.title('Landing: antero-posterior force')
        ax.plot(task_hat[:,0],'-r', linewidth=3.0)
        ax.plot(taskPlus[:,0],'-k',color = '0.75', linewidth=1.0, linestyle='--')
        ax.plot(taskMin[:,0],'-k' ,color = '0.75',linewidth=1.0, linestyle='--')
        plt.ylabel('$[N \cdot BW^{-1}]$')
        plt.legend(['mean','mean $\pm$ std'],loc=1)


    def plotAngularMomentumImpulsion(self):
        fig = plt.figure()
        fig.canvas.set_window_title(self.windowTitle)
        
        task = [np.array(self.task[i].taskNormalized).squeeze() for i in xrange(self.participantsNo)]
        task_hat = np.mean(task,0)
        taskStd_hat = np.std(task,0)
        
        taskPlus = task_hat + taskStd_hat
        taskMin = task_hat - taskStd_hat
        
        ax = fig.add_subplot('111')
        plt.title('Impulsion: torque in sagittal plane')
        ax.plot(task_hat,'-r', linewidth=3.0)
        ax.plot(taskPlus,'-k',color = '0.75', linewidth=1.0, linestyle='--')
        ax.plot(taskMin,'-k' ,color = '0.75',linewidth=1.0, linestyle='--')
        plt.ylabel('$[Nm \cdot BW^{-1} \cdot H^{-1}]$')
        plt.legend(['mean','mean $\pm$ std'],loc=1)

    def plotAngularMomentumStab(self):
        fig = plt.figure()
        fig.canvas.set_window_title(self.windowTitle)
        
        task = [np.array(self.task[i].taskNormalized).squeeze() for i in xrange(self.participantsNo)]
        task_hat = np.mean(task,0)
        taskStd_hat = np.std(task,0)
        
        taskPlus = task_hat + taskStd_hat
        taskMin = task_hat - taskStd_hat
        
        ax = fig.add_subplot('111')
        plt.title('Landing: torque in sagittal plane')
        ax.plot(task_hat,'-r', linewidth=3.0)
        ax.plot(taskPlus,'-k',color = '0.75', linewidth=1.0, linestyle='--')
        ax.plot(taskMin,'-k' ,color = '0.75',linewidth=1.0, linestyle='--')
        plt.ylabel('$[Nm \cdot BW^{-1} \cdot H^{-1}]$')
        plt.legend(['mean','mean $\pm$ std'],loc=1)
