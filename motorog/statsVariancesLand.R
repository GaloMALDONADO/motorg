# Analysis of Variances from uncontrolled manifold and its orthogonal space
# ----------------------------------------------
#                 Landing
# Task 1: vertical force. Decrease it.
# Task 2: M-L and A-P force. Stability
# Task 3: DAM CoM 3 axis. Stability.
# ----------------------------------------------
rm(list = ls())
#p='/galo/devel/gepetto/motorg/motorog/' #home
p='/local/gmaldona/devel/motorg/motorog/' #lab
nparticipants = 5
ddl=nparticipants-1
t = qt(.975,ddl)

# ---------------------- Read the data -----------------------------------
pathName = paste(p,'TableVariancesLand.csv',sep="")
SOT_LAND = read.csv(pathName, header = FALSE, col.names = list('Participant', 'Phase', 'Task', 'Variability' ,'Variance'))
SOT_LAND$Participant<-as.factor(SOT_LAND$Participant)
SOT_LAND$Phase<-as.factor(SOT_LAND$Phase)
SOT_LAND$Task<-as.factor(SOT_LAND$Task)
SOT_LAND$Variability<-as.factor(SOT_LAND$Variability)
# ----------------------------- Repeated Measures Anova ---------------------------
# compute repetitive measures anova
statsaov2 <-aov(SOT_LAND$Ratio ~ (SOT_LAND$Task+SOT_LAND$Phase) + 
                  Error(SOT_LAND$Participant / (SOT_LAND$Task+SOT_LAND$Phase)), 
                data = SOT_LAND)
summary(statsaov2) 
# tasks are significantly differents p = 1.96e-06 ***
# phases are not significantly differents
# tasks:phase interactions are significant p=7.9e-08 ***
