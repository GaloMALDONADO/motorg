# Analysis of Variances from uncontrolled manifold and its orthogonal space
rm(list = ls())



# ------------------------------------------------------------------------
#    JUMP IMPULSE
# Task 1: impulsion through antero-posterior and vertical force
# Task 2: impulsion through antero posterior angular momentum (around M-L axis at the center of mass)
# ------------------------------------------------------------------------
#p='/galo/devel/gepetto/motorg/motorog/' #home
p='/local/gmaldona/devel/motorg/motorog/' #lab
nparticipants = 5
ddl=nparticipants-1
t = qt(.975,ddl)

# ---------------------- Read the data -----------------------------------
pathName = paste(p,'TableMomentaLand.csv',sep="")
IMPULSE = read.csv(pathName,
                       header = FALSE, 
                       col.names = list('Participant', 'Phase', 'Task', 'Coordinate' ,'Momenta'))
IMPULSE$Participant<-as.factor(IMPULSE$Participant)
IMPULSE$Phase<-as.factor(IMPULSE$Phase)
IMPULSE$Task<-as.factor(IMPULSE$Task)
IMPULSE$Coordinate<-as.factor(IMPULSE$Coordinate)

boxplot(IMPULSE$Momenta[IMPULSE$Task=="1" & IMPULSE$Phase=="5"] ~ IMPULSE$Coordinate[IMPULSE$Task=="1" & IMPULSE$Phase=="5"]) 

aovstats <-aov(IMPULSE$Momenta ~ 
                 (IMPULSE$Task+IMPULSE$Phase+IMPULSE$Coordinate) + 
                 Error(IMPULSE$Participant  / (IMPULSE$Task+IMPULSE$Phase+IMPULSE$Coordinate)), 
               data = IMPULSE)
summary(aovstats)
