# Analysis of Variances from uncontrolled manifold and its orthogonal space
rm(list = ls())



# ------------------------------------------------------------------------
#    JUMP LAND
# Task 1: impulsion through antero-posterior and vertical force
# Task 2: impulsion through antero posterior angular momentum (around M-L axis at the center of mass)
# ------------------------------------------------------------------------
#p='/galo/devel/gepetto/motorg/motorog/' #home
p='/local/gmaldona/devel/motorg/motorog/' #lab
nparticipants = 5
ddl=nparticipants-1
t = qt(.975,ddl)
names<- c('pelvis','thigh_r','leg_r','ankle_r','subtalar_r','mtp_r','thigh_l','leg_l','ankle_l','subtalar_l',
          'mtp_l','back','neck','acromial_r','elbow_r','radioulnar_r','radius_lunate_r','lunate_hand_r','fingers_r',
          'acromial_l','elbow_l','radioulnar_l','radius_lunate_l','lunate_hand_l','fingers_l')

# ---------------------- Read the data -----------------------------------
pathName = paste(p,'TableMomentaland.csv',sep="")
LAND = read.csv(pathName,
                   header = FALSE, 
                   col.names = list('Participant', 'Phase', 'Task', 'Coordinate' ,'Momenta'))
LAND$Participant<-as.factor(LAND$Participant)
LAND$Phase<-as.factor(LAND$Phase)
LAND$Task<-as.factor(LAND$Task)
LAND$Coordinate<-as.factor(LAND$Coordinate)


boxplot(LAND$Momenta[LAND$Task=="1" & LAND$Phase=="0"] ~ LAND$Coordinate[LAND$Task=="1" & LAND$Phase=="0"]) 

aovstats <-aov(LAND$Momenta ~ 
                 (LAND$Task+LAND$Phase+LAND$Coordinate) + 
                 Error(LAND$Participant  / (LAND$Task+LAND$Phase+LAND$Coordinate)), 
               data = LAND)
summary(aovstats)
# joints are different
# phases are different
# joints are different
pairwise.t.test(LAND$Momenta, LAND$Task, p.adj = "bonf",paired=TRUE)
pairwise.t.test(LAND$Momenta, LAND$Phase, p.adj = "bonf",paired=TRUE)
pairwise.t.test(LAND$Momenta, LAND$Coordinate, p.adj = "bonf",paired=TRUE)
















# ----------------------- Means - Std - Confidence Interval --------------------------
pathName = paste(p,'means/LandLMx.csv',sep="")
meanDataLMx = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'means/LandLMy.csv',sep="")
meanDataLMy = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'means/LandLMz.csv',sep="")
meanDataLMz = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'std/LandLMx.csv',sep="")
stdDataLMx = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'std/LandLMy.csv',sep="")
stdDataLMy = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'std/LandLMz.csv',sep="")
stdDataLMz = read.csv(pathName, header = FALSE, col.names = names)

pathName = paste(p,'means/LandAMx.csv',sep="")
meanDataAMx = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'means/LandAMy.csv',sep="")
meanDataAMy = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'means/LandAMz.csv',sep="")
meanDataAMz = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'std/LandAMx.csv',sep="")
stdDataAMx = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'std/LandAMy.csv',sep="")
stdDataAMy = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'std/LandAMz.csv',sep="")
stdDataAMz = read.csv(pathName, header = FALSE, col.names = names)

# Linear Momentum x
land.means.x <- structure(list('pelvis'=c(meanDataLMx[1,1], meanDataLMx[2,1], meanDataLMx[3,1], meanDataLMx[4,1]),
                               'thigh_r'=c(meanDataLMx[1,2], meanDataLMx[2,2], meanDataLMx[3,2], meanDataLMx[4,2]),
                               'leg_r'=c(meanDataLMx[1,3], meanDataLMx[2,3], meanDataLMx[3,3], meanDataLMx[4,3]),
                               'ankle_r'=c(meanDataLMx[1,4], meanDataLMx[2,4], meanDataLMx[3,4], meanDataLMx[4,4]),
                               'subtalar_r'=c(meanDataLMx[1,5], meanDataLMx[2,5], meanDataLMx[3,5], meanDataLMx[4,5]),
                               'mtp_r'=c(meanDataLMx[1,6], meanDataLMx[2,6], meanDataLMx[3,6], meanDataLMx[4,6]),
                               'thigh_l'=c(meanDataLMx[1,7], meanDataLMx[2,7], meanDataLMx[3,7], meanDataLMx[4,7]),
                               'leg_l'=c(meanDataLMx[1,8], meanDataLMx[2,8], meanDataLMx[3,8], meanDataLMx[4,8]),
                               'ankle_l'=c(meanDataLMx[1,9], meanDataLMx[2,9], meanDataLMx[3,9], meanDataLMx[4,9]),
                               'subtalar_l'=c(meanDataLMx[1,10], meanDataLMx[2,10], meanDataLMx[3,10], meanDataLMx[4,10]),
                               'mtp_l'=c(meanDataLMx[1,11], meanDataLMx[2,11], meanDataLMx[3,11], meanDataLMx[4,11]),
                               'back'=c(meanDataLMx[1,12], meanDataLMx[2,12], meanDataLMx[3,12], meanDataLMx[4,12]),
                               'neck'=c(meanDataLMx[1,13], meanDataLMx[2,13], meanDataLMx[3,13], meanDataLMx[4,13]),
                               'acromial_r'=c(meanDataLMx[1,14], meanDataLMx[2,14], meanDataLMx[3,14], meanDataLMx[4,14]),
                               'elbow_r'=c(meanDataLMx[1,15], meanDataLMx[2,15], meanDataLMx[3,15], meanDataLMx[4,15]),
                               'radioulnar_r'=c(meanDataLMx[1,16], meanDataLMx[2,16], meanDataLMx[3,16], meanDataLMx[4,16]),
                               'radius_lunate_r'=c(meanDataLMx[1,17], meanDataLMx[2,17], meanDataLMx[3,17], meanDataLMx[4,17]),
                               'lunate_hand_r'=c(meanDataLMx[1,18], meanDataLMx[2,18], meanDataLMx[3,18], meanDataLMx[4,18]),
                               'fingers_r'=c(meanDataLMx[1,19], meanDataLMx[2,19], meanDataLMx[3,19], meanDataLMx[4,19]),
                               'acromial_l'=c(meanDataLMx[1,20], meanDataLMx[2,20], meanDataLMx[3,20], meanDataLMx[4,20]),
                               'elbow_l'=c(meanDataLMx[1,21], meanDataLMx[2,21], meanDataLMx[3,21], meanDataLMx[4,21]),
                               'radioulnar_l'=c(meanDataLMx[1,22], meanDataLMx[2,22], meanDataLMx[3,22], meanDataLMx[4,22]),
                               'radius_lunate_l'=c(meanDataLMx[1,23], meanDataLMx[2,23], meanDataLMx[3,23], meanDataLMx[4,23]),
                               'lunate_hand_l'=c(meanDataLMx[1,24], meanDataLMx[2,24], meanDataLMx[3,24], meanDataLMx[4,24]),
                               'fingers_l'=c(meanDataLMx[1,25], meanDataLMx[2,25], meanDataLMx[3,25], meanDataLMx[4,25])
), 
.Names = names, 
class = "data.frame", row.names = c(NA, -4L))



# Linear Momentum Y
land.means.y <- structure(list('pelvis'=c(meanDataLMy[1,1], meanDataLMy[2,1], meanDataLMy[3,1], meanDataLMy[4,1]),
                               'thigh_r'=c(meanDataLMy[1,2], meanDataLMy[2,2], meanDataLMy[3,2], meanDataLMy[4,2]),
                               'leg_r'=c(meanDataLMy[1,3], meanDataLMy[2,3], meanDataLMy[3,3], meanDataLMy[4,3]),
                               'ankle_r'=c(meanDataLMy[1,4], meanDataLMy[2,4], meanDataLMy[3,4], meanDataLMy[4,4]),
                               'subtalar_r'=c(meanDataLMy[1,5], meanDataLMy[2,5], meanDataLMy[3,5], meanDataLMy[4,5]),
                               'mtp_r'=c(meanDataLMy[1,6], meanDataLMy[2,6], meanDataLMy[3,6], meanDataLMy[4,6]),
                               'thigh_l'=c(meanDataLMy[1,7], meanDataLMy[2,7], meanDataLMy[3,7], meanDataLMy[4,7]),
                               'leg_l'=c(meanDataLMy[1,8], meanDataLMy[2,8], meanDataLMy[3,8], meanDataLMy[4,8]),
                               'ankle_l'=c(meanDataLMy[1,9], meanDataLMy[2,9], meanDataLMy[3,9], meanDataLMy[4,9]),
                               'subtalar_l'=c(meanDataLMy[1,10], meanDataLMy[2,10], meanDataLMy[3,10], meanDataLMy[4,10]),
                               'mtp_l'=c(meanDataLMy[1,11], meanDataLMy[2,11], meanDataLMy[3,11], meanDataLMy[4,11]),
                               'back'=c(meanDataLMy[1,12], meanDataLMy[2,12], meanDataLMy[3,12], meanDataLMy[4,12]),
                               'neck'=c(meanDataLMy[1,13], meanDataLMy[2,13], meanDataLMy[3,13], meanDataLMy[4,13]),
                               'acromial_r'=c(meanDataLMy[1,14], meanDataLMy[2,14], meanDataLMy[3,14], meanDataLMy[4,14]),
                               'elbow_r'=c(meanDataLMy[1,15], meanDataLMy[2,15], meanDataLMy[3,15], meanDataLMy[4,15]),
                               'radioulnar_r'=c(meanDataLMy[1,16], meanDataLMy[2,16], meanDataLMy[3,16], meanDataLMy[4,16]),
                               'radius_lunate_r'=c(meanDataLMy[1,17], meanDataLMy[2,17], meanDataLMy[3,17], meanDataLMy[4,17]),
                               'lunate_hand_r'=c(meanDataLMy[1,18], meanDataLMy[2,18], meanDataLMy[3,18], meanDataLMy[4,18]),
                               'fingers_r'=c(meanDataLMy[1,19], meanDataLMy[2,19], meanDataLMy[3,19], meanDataLMy[4,19]),
                               'acromial_l'=c(meanDataLMy[1,20], meanDataLMy[2,20], meanDataLMy[3,20], meanDataLMy[4,20]),
                               'elbow_l'=c(meanDataLMy[1,21], meanDataLMy[2,21], meanDataLMy[3,21], meanDataLMy[4,21]),
                               'radioulnar_l'=c(meanDataLMy[1,22], meanDataLMy[2,22], meanDataLMy[3,22], meanDataLMy[4,22]),
                               'radius_lunate_l'=c(meanDataLMy[1,23], meanDataLMy[2,23], meanDataLMy[3,23], meanDataLMy[4,23]),
                               'lunate_hand_l'=c(meanDataLMy[1,24], meanDataLMy[2,24], meanDataLMy[3,24], meanDataLMy[4,24]),
                               'fingers_l'=c(meanDataLMy[1,25], meanDataLMy[2,25], meanDataLMy[3,25], meanDataLMy[4,25])
), 
.Names = names, 
class = "data.frame", row.names = c(NA, -4L))


# Linear Momentum Z
land.means.z <- structure(list('pelvis'=c(meanDataLMz[1,1], meanDataLMz[2,1], meanDataLMz[3,1], meanDataLMz[4,1]),
                               'thigh_r'=c(meanDataLMz[1,2], meanDataLMz[2,2], meanDataLMz[3,2], meanDataLMz[4,2]),
                               'leg_r'=c(meanDataLMz[1,3], meanDataLMz[2,3], meanDataLMz[3,3], meanDataLMz[4,3]),
                               'ankle_r'=c(meanDataLMz[1,4], meanDataLMz[2,4], meanDataLMz[3,4], meanDataLMz[4,4]),
                               'subtalar_r'=c(meanDataLMz[1,5], meanDataLMz[2,5], meanDataLMz[3,5], meanDataLMz[4,5]),
                               'mtp_r'=c(meanDataLMz[1,6], meanDataLMz[2,6], meanDataLMz[3,6], meanDataLMz[4,6]),
                               'thigh_l'=c(meanDataLMz[1,7], meanDataLMz[2,7], meanDataLMz[3,7], meanDataLMz[4,7]),
                               'leg_l'=c(meanDataLMz[1,8], meanDataLMz[2,8], meanDataLMz[3,8], meanDataLMz[4,8]),
                               'ankle_l'=c(meanDataLMz[1,9], meanDataLMz[2,9], meanDataLMz[3,9], meanDataLMz[4,9]),
                               'subtalar_l'=c(meanDataLMz[1,10], meanDataLMz[2,10], meanDataLMz[3,10], meanDataLMz[4,10]),
                               'mtp_l'=c(meanDataLMz[1,11], meanDataLMz[2,11], meanDataLMz[3,11], meanDataLMz[4,11]),
                               'back'=c(meanDataLMz[1,12], meanDataLMz[2,12], meanDataLMz[3,12], meanDataLMz[4,12]),
                               'neck'=c(meanDataLMz[1,13], meanDataLMz[2,13], meanDataLMz[3,13], meanDataLMz[4,13]),
                               'acromial_r'=c(meanDataLMz[1,14], meanDataLMz[2,14], meanDataLMz[3,14], meanDataLMz[4,14]),
                               'elbow_r'=c(meanDataLMz[1,15], meanDataLMz[2,15], meanDataLMz[3,15], meanDataLMz[4,15]),
                               'radioulnar_r'=c(meanDataLMz[1,16], meanDataLMz[2,16], meanDataLMz[3,16], meanDataLMz[4,16]),
                               'radius_lunate_r'=c(meanDataLMz[1,17], meanDataLMz[2,17], meanDataLMz[3,17], meanDataLMz[4,17]),
                               'lunate_hand_r'=c(meanDataLMz[1,18], meanDataLMz[2,18], meanDataLMz[3,18], meanDataLMz[4,18]),
                               'fingers_r'=c(meanDataLMz[1,19], meanDataLMz[2,19], meanDataLMz[3,19], meanDataLMz[4,19]),
                               'acromial_l'=c(meanDataLMz[1,20], meanDataLMz[2,20], meanDataLMz[3,20], meanDataLMz[4,20]),
                               'elbow_l'=c(meanDataLMz[1,21], meanDataLMz[2,21], meanDataLMz[3,21], meanDataLMz[4,21]),
                               'radioulnar_l'=c(meanDataLMz[1,22], meanDataLMz[2,22], meanDataLMz[3,22], meanDataLMz[4,22]),
                               'radius_lunate_l'=c(meanDataLMz[1,23], meanDataLMz[2,23], meanDataLMz[3,23], meanDataLMz[4,23]),
                               'lunate_hand_l'=c(meanDataLMz[1,24], meanDataLMz[2,24], meanDataLMz[3,24], meanDataLMz[4,24]),
                               'fingers_l'=c(meanDataLMz[1,25], meanDataLMz[2,25], meanDataLMz[3,25], meanDataLMz[4,25])
), 
.Names = names, 
class = "data.frame", row.names = c(NA, -4L))


# 
# Angular Momentum x
land.means.xx <- structure(list('pelvis'=c(meanDataAMx[1,1], meanDataAMx[2,1], meanDataAMx[3,1], meanDataAMx[4,1]),
                                'thigh_r'=c(meanDataAMx[1,2], meanDataAMx[2,2], meanDataAMx[3,2], meanDataAMx[4,2]),
                                'leg_r'=c(meanDataAMx[1,3], meanDataAMx[2,3], meanDataAMx[3,3], meanDataAMx[4,3]),
                                'ankle_r'=c(meanDataAMx[1,4], meanDataAMx[2,4], meanDataAMx[3,4], meanDataAMx[4,4]),
                                'subtalar_r'=c(meanDataAMx[1,5], meanDataAMx[2,5], meanDataAMx[3,5], meanDataAMx[4,5]),
                                'mtp_r'=c(meanDataAMx[1,6], meanDataAMx[2,6], meanDataAMx[3,6], meanDataAMx[4,6]),
                                'thigh_l'=c(meanDataAMx[1,7], meanDataAMx[2,7], meanDataAMx[3,7], meanDataAMx[4,7]),
                                'leg_l'=c(meanDataAMx[1,8], meanDataAMx[2,8], meanDataAMx[3,8], meanDataAMx[4,8]),
                                'ankle_l'=c(meanDataAMx[1,9], meanDataAMx[2,9], meanDataAMx[3,9], meanDataAMx[4,9]),
                                'subtalar_l'=c(meanDataAMx[1,10], meanDataAMx[2,10], meanDataAMx[3,10], meanDataAMx[4,10]),
                                'mtp_l'=c(meanDataAMx[1,11], meanDataAMx[2,11], meanDataAMx[3,11], meanDataAMx[4,11]),
                                'back'=c(meanDataAMx[1,12], meanDataAMx[2,12], meanDataAMx[3,12], meanDataAMx[4,12]),
                                'neck'=c(meanDataAMx[1,13], meanDataAMx[2,13], meanDataAMx[3,13], meanDataAMx[4,13]),
                                'acromial_r'=c(meanDataAMx[1,14], meanDataAMx[2,14], meanDataAMx[3,14], meanDataAMx[4,14]),
                                'elbow_r'=c(meanDataAMx[1,15], meanDataAMx[2,15], meanDataAMx[3,15], meanDataAMx[4,15]),
                                'radioulnar_r'=c(meanDataAMx[1,16], meanDataAMx[2,16], meanDataAMx[3,16], meanDataAMx[4,16]),
                                'radius_lunate_r'=c(meanDataAMx[1,17], meanDataAMx[2,17], meanDataAMx[3,17], meanDataAMx[4,17]),
                                'lunate_hand_r'=c(meanDataAMx[1,18], meanDataAMx[2,18], meanDataAMx[3,18], meanDataAMx[4,18]),
                                'fingers_r'=c(meanDataAMx[1,19], meanDataAMx[2,19], meanDataAMx[3,19], meanDataAMx[4,19]),
                                'acromial_l'=c(meanDataAMx[1,20], meanDataAMx[2,20], meanDataAMx[3,20], meanDataAMx[4,20]),
                                'elbow_l'=c(meanDataAMx[1,21], meanDataAMx[2,21], meanDataAMx[3,21], meanDataAMx[4,21]),
                                'radioulnar_l'=c(meanDataAMx[1,22], meanDataAMx[2,22], meanDataAMx[3,22], meanDataAMx[4,22]),
                                'radius_lunate_l'=c(meanDataAMx[1,23], meanDataAMx[2,23], meanDataAMx[3,23], meanDataAMx[4,23]),
                                'lunate_hand_l'=c(meanDataAMx[1,24], meanDataAMx[2,24], meanDataAMx[3,24], meanDataAMx[4,24]),
                                'fingers_l'=c(meanDataAMx[1,25], meanDataAMx[2,25], meanDataAMx[3,25], meanDataAMx[4,25])
), 
.Names = names, 
class = "data.frame", row.names = c(NA, -4L))



# Angular Momentum Y
land.means.yy <- structure(list('pelvis'=c(meanDataAMy[1,1], meanDataAMy[2,1], meanDataAMy[3,1], meanDataAMy[4,1]),
                                'thigh_r'=c(meanDataAMy[1,2], meanDataAMy[2,2], meanDataAMy[3,2], meanDataAMy[4,2]),
                                'leg_r'=c(meanDataAMy[1,3], meanDataAMy[2,3], meanDataAMy[3,3], meanDataAMy[4,3]),
                                'ankle_r'=c(meanDataAMy[1,4], meanDataAMy[2,4], meanDataAMy[3,4], meanDataAMy[4,4]),
                                'subtalar_r'=c(meanDataAMy[1,5], meanDataAMy[2,5], meanDataAMy[3,5], meanDataAMy[4,5]),
                                'mtp_r'=c(meanDataAMy[1,6], meanDataAMy[2,6], meanDataAMy[3,6], meanDataAMy[4,6]),
                                'thigh_l'=c(meanDataAMy[1,7], meanDataAMy[2,7], meanDataAMy[3,7], meanDataAMy[4,7]),
                                'leg_l'=c(meanDataAMy[1,8], meanDataAMy[2,8], meanDataAMy[3,8], meanDataAMy[4,8]),
                                'ankle_l'=c(meanDataAMy[1,9], meanDataAMy[2,9], meanDataAMy[3,9], meanDataAMy[4,9]),
                                'subtalar_l'=c(meanDataAMy[1,10], meanDataAMy[2,10], meanDataAMy[3,10], meanDataAMy[4,10]),
                                'mtp_l'=c(meanDataAMy[1,11], meanDataAMy[2,11], meanDataAMy[3,11], meanDataAMy[4,11]),
                                'back'=c(meanDataAMy[1,12], meanDataAMy[2,12], meanDataAMy[3,12], meanDataAMy[4,12]),
                                'neck'=c(meanDataAMy[1,13], meanDataAMy[2,13], meanDataAMy[3,13], meanDataAMy[4,13]),
                                'acromial_r'=c(meanDataAMy[1,14], meanDataAMy[2,14], meanDataAMy[3,14], meanDataAMy[4,14]),
                                'elbow_r'=c(meanDataAMy[1,15], meanDataAMy[2,15], meanDataAMy[3,15], meanDataAMy[4,15]),
                                'radioulnar_r'=c(meanDataAMy[1,16], meanDataAMy[2,16], meanDataAMy[3,16], meanDataAMy[4,16]),
                                'radius_lunate_r'=c(meanDataAMy[1,17], meanDataAMy[2,17], meanDataAMy[3,17], meanDataAMy[4,17]),
                                'lunate_hand_r'=c(meanDataAMy[1,18], meanDataAMy[2,18], meanDataAMy[3,18], meanDataAMy[4,18]),
                                'fingers_r'=c(meanDataAMy[1,19], meanDataAMy[2,19], meanDataAMy[3,19], meanDataAMy[4,19]),
                                'acromial_l'=c(meanDataAMy[1,20], meanDataAMy[2,20], meanDataAMy[3,20], meanDataAMy[4,20]),
                                'elbow_l'=c(meanDataAMy[1,21], meanDataAMy[2,21], meanDataAMy[3,21], meanDataAMy[4,21]),
                                'radioulnar_l'=c(meanDataAMy[1,22], meanDataAMy[2,22], meanDataAMy[3,22], meanDataAMy[4,22]),
                                'radius_lunate_l'=c(meanDataAMy[1,23], meanDataAMy[2,23], meanDataAMy[3,23], meanDataAMy[4,23]),
                                'lunate_hand_l'=c(meanDataAMy[1,24], meanDataAMy[2,24], meanDataAMy[3,24], meanDataAMy[4,24]),
                                'fingers_l'=c(meanDataAMy[1,25], meanDataAMy[2,25], meanDataAMy[3,25], meanDataAMy[4,25])
), 
.Names = names, 
class = "data.frame", row.names = c(NA, -4L))


# Angular Momentum Z
land.means.zz <- structure(list('pelvis'=c(meanDataAMz[1,1], meanDataAMz[2,1], meanDataAMz[3,1], meanDataAMz[4,1]),
                                'thigh_r'=c(meanDataAMz[1,2], meanDataAMz[2,2], meanDataAMz[3,2], meanDataAMz[4,2]),
                                'leg_r'=c(meanDataAMz[1,3], meanDataAMz[2,3], meanDataAMz[3,3], meanDataAMz[4,3]),
                                'ankle_r'=c(meanDataAMz[1,4], meanDataAMz[2,4], meanDataAMz[3,4], meanDataAMz[4,4]),
                                'subtalar_r'=c(meanDataAMz[1,5], meanDataAMz[2,5], meanDataAMz[3,5], meanDataAMz[4,5]),
                                'mtp_r'=c(meanDataAMz[1,6], meanDataAMz[2,6], meanDataAMz[3,6], meanDataAMz[4,6]),
                                'thigh_l'=c(meanDataAMz[1,7], meanDataAMz[2,7], meanDataAMz[3,7], meanDataAMz[4,7]),
                                'leg_l'=c(meanDataAMz[1,8], meanDataAMz[2,8], meanDataAMz[3,8], meanDataAMz[4,8]),
                                'ankle_l'=c(meanDataAMz[1,9], meanDataAMz[2,9], meanDataAMz[3,9], meanDataAMz[4,9]),
                                'subtalar_l'=c(meanDataAMz[1,10], meanDataAMz[2,10], meanDataAMz[3,10], meanDataAMz[4,10]),
                                'mtp_l'=c(meanDataAMz[1,11], meanDataAMz[2,11], meanDataAMz[3,11], meanDataAMz[4,11]),
                                'back'=c(meanDataAMz[1,12], meanDataAMz[2,12], meanDataAMz[3,12], meanDataAMz[4,12]),
                                'neck'=c(meanDataAMz[1,13], meanDataAMz[2,13], meanDataAMz[3,13], meanDataAMz[4,13]),
                                'acromial_r'=c(meanDataAMz[1,14], meanDataAMz[2,14], meanDataAMz[3,14], meanDataAMz[4,14]),
                                'elbow_r'=c(meanDataAMz[1,15], meanDataAMz[2,15], meanDataAMz[3,15], meanDataAMz[4,15]),
                                'radioulnar_r'=c(meanDataAMz[1,16], meanDataAMz[2,16], meanDataAMz[3,16], meanDataAMz[4,16]),
                                'radius_lunate_r'=c(meanDataAMz[1,17], meanDataAMz[2,17], meanDataAMz[3,17], meanDataAMz[4,17]),
                                'lunate_hand_r'=c(meanDataAMz[1,18], meanDataAMz[2,18], meanDataAMz[3,18], meanDataAMz[4,18]),
                                'fingers_r'=c(meanDataAMz[1,19], meanDataAMz[2,19], meanDataAMz[3,19], meanDataAMz[4,19]),
                                'acromial_l'=c(meanDataAMz[1,20], meanDataAMz[2,20], meanDataAMz[3,20], meanDataAMz[4,20]),
                                'elbow_l'=c(meanDataAMz[1,21], meanDataAMz[2,21], meanDataAMz[3,21], meanDataAMz[4,21]),
                                'radioulnar_l'=c(meanDataAMz[1,22], meanDataAMz[2,22], meanDataAMz[3,22], meanDataAMz[4,22]),
                                'radius_lunate_l'=c(meanDataAMz[1,23], meanDataAMz[2,23], meanDataAMz[3,23], meanDataAMz[4,23]),
                                'lunate_hand_l'=c(meanDataAMz[1,24], meanDataAMz[2,24], meanDataAMz[3,24], meanDataAMz[4,24]),
                                'fingers_l'=c(meanDataAMz[1,25], meanDataAMz[2,25], meanDataAMz[3,25], meanDataAMz[4,25])
), 
.Names = names, 
class = "data.frame", row.names = c(NA, -4L))



# ----------- BARPLOT

op = par(mar=c(8,5,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(land.means.x), main="Land Linear Momentum A-P",
               ylab=expression(kg %.% m %.% s^-1 %.% BM^-1),
               xlim=c(0,30),ylim=c(-0.15,0.015),
               col=c("red","green","blue","yellow"),
               legend = c( "1%","40%", "70%", "100%"),  las=2, cex.names = 1) #beside=TRUE,xlab="joint",
rm(op)


op = par(mar=c(8,4,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(land.means.y), main="Land Linear Momentum M-L",
               ylab=expression(kg %.% m %.% s^-1 %.% BM^-1),
               xlim=c(0,30),ylim=c(-0.0,0.15),
               col=c("red","green","blue","yellow"),
               legend = c( "1%","40%", "70%", "100%"),  las=2, cex.names = 1) #beside=TRUE,xlab="joint",
rm(op)


op = par(mar=c(8,4,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(land.means.z), main="Land Linear Momentum Vertical",
               ylab=expression(kg %.% m %.% s^-1 %.% BM^-1),
               xlim=c(0,30),ylim=c(-0.45,0),
               col=c("red","green","blue","yellow"),
               legend = c( "1%","40%", "70%", "100%"),  las=2, cex.names = 1) #beside=TRUE,xlab="joint",
rm(op)


# unconmment to plot with SD
#arrows(barx,xx+er, barx,xx, angle=90, code=3, length=0.05)



# 
op = par(mar=c(8,5,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(land.means.xx), main="Land Angular Momentum around Medial Lateral Axis",
               ylab=expression(kg %.% m %.% s^-1 %.% BM^-1 %.% H),
               xlim=c(0,30),ylim=c(-0.02,0.01),
               col=c("red","green","blue","yellow"),
               legend = c( "1%","40%", "70%", "100%"),  las=2, cex.names = 1) #beside=TRUE,xlab="joint",
rm(op)


op = par(mar=c(8,5,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(land.means.yy), main="Land Angular Momentum around Medial Lateral",
               ylab=expression(kg %.% m %.% s^-1 %.% BM^-1 %.% H),
               xlim=c(0,30),ylim=c(-0.03,0.01),
               col=c("red","green","blue","yellow"),
               legend = c( "1%","40%", "70%", "100%"),  las=2, cex.names = 1) #beside=TRUE,xlab="joint",
rm(op)


op = par(mar=c(8,5,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(land.means.zz), main="Land Angular Momentum Z",
               ylab=expression(kg %.% m %.% s^-1 %.% BM^-1 %.% H),
               xlim=c(0,30),ylim=c(-0.02,0.01),
               col=c("red","green","blue","yellow"),
               legend = c( "1%","40%", "70%", "100%"),  las=2, cex.names = 1) #beside=TRUE,xlab="joint",
rm(op)
















# *****************************************************************************
rm(list = ls())
# LAND
pathName = paste(p,'means/LandLM_abs.csv',sep="")
meanDataLM_abs = read.csv(pathName, header = FALSE, col.names = names)

pathName = paste(p,'means/LandLM_stab.csv',sep="")
meanDataLM_stab = read.csv(pathName, header = FALSE, col.names = names)

pathName = paste(p,'means/LandAM.csv',sep="")
meanDataAM = read.csv(pathName, header = FALSE, col.names = names)

pathName = paste(p,'std/LandLM_abs.csv',sep="")
stdDataLM = read.csv(pathName, header = FALSE, col.names = names)

pathName = paste(p,'std/LandLM_stab.csv',sep="")
meanDataLM_stab = read.csv(pathName, header = FALSE, col.names = names)

pathName = paste(p,'std/LandAM.csv',sep="")
stdDataAM = read.csv(pathName, header = FALSE, col.names = names)

simp_names = list('pelvis','thigh_r','leg_r','thigh_l','leg_l','back','neck')


# ABSORPTION
land_abs.means <- structure(list('pelvis'=c(meanDataLM_abs[1,1], meanDataLM_abs[2,1], meanDataLM_abs[3,1], meanDataLM_abs[4,1]),
                                 'thigh_r'=c(meanDataLM_abs[1,2], meanDataLM_abs[2,2], meanDataLM_abs[3,2], meanDataLM_abs[4,2]),
                                 'leg_r'=c(meanDataLM_abs[1,3], meanDataLM_abs[2,3], meanDataLM_abs[3,3], meanDataLM_abs[4,3]),
                                 'thigh_l'=c(meanDataLM_abs[1,7], meanDataLM_abs[2,7], meanDataLM_abs[3,7], meanDataLM_abs[4,7]),
                                 'leg_l'=c(meanDataLM_abs[1,8], meanDataLM_abs[2,8], meanDataLM_abs[3,8], meanDataLM_abs[4,8]),
                                 'back'=c(meanDataLM_abs[1,12], meanDataLM_abs[2,12], meanDataLM_abs[3,12], meanDataLM_abs[4,12]),
                                 'neck'=c(meanDataLM_abs[1,13], meanDataLM_abs[2,13], meanDataLM_abs[3,13], meanDataLM_abs[4,13])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -4L))

#
land_abs.stds <- structure(list('pelvis'=c(stdDataLM_abs[1,1], stdDataLM_abs[2,1], stdDataLM_abs[3,1], stdDataLM_abs[4,1]),
                                'thigh_r'=c(stdDataLM_abs[1,2], stdDataLM_abs[2,2], stdDataLM_abs[3,2], stdDataLM_abs[4,2]),
                                'leg_r'=c(stdDataLM_abs[1,3], stdDataLM_abs[2,3], stdDataLM_abs[3,3], stdDataLM_abs[4,3]),
                                'thigh_l'=c(stdDataLM_abs[1,7], stdDataLM_abs[2,7], stdDataLM_abs[3,7], stdDataLM_abs[4,7]),
                                'leg_l'=c(stdDataLM_abs[1,8], stdDataLM_abs[2,8], stdDataLM_abs[3,8], stdDataLM_abs[4,8]),
                                'back'=c(stdDataLM_abs[1,12], stdDataLM_abs[2,12], stdDataLM_abs[3,12], stdDataLM_abs[4,12]),
                                'neck'=c(stdDataLM_abs[1,13], stdDataLM_abs[2,13], stdDataLM_abs[3,13], stdDataLM_abs[4,13])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -4L))

land_abs.ci <- structure(list('pelvis'=c(t*stdDataLM_abs[1,1]/sqrt(nparticipants), t*stdDataLM_abs[2,1]/sqrt(nparticipants), t*stdDataLM_abs[3,1]/sqrt(nparticipants), t*stdDataLM_abs[4,1]/sqrt(nparticipants)),
                              'thigh_r'=c(t*stdDataLM_abs[1,2]/sqrt(nparticipants), t*stdDataLM_abs[2,2]/sqrt(nparticipants), t*stdDataLM_abs[3,2]/sqrt(nparticipants), t*stdDataLM_abs[4,2]/sqrt(nparticipants)),
                              'leg_r'=c(t*stdDataLM_abs[1,3]/sqrt(nparticipants), t*stdDataLM_abs[2,3]/sqrt(nparticipants), t*stdDataLM_abs[3,3]/sqrt(nparticipants), t*stdDataLM_abs[4,3]/sqrt(nparticipants)),
                              'thigh_l'=c(t*stdDataLM_abs[1,7]/sqrt(nparticipants), t*stdDataLM_abs[2,7]/sqrt(nparticipants), t*stdDataLM_abs[3,7]/sqrt(nparticipants), t*stdDataLM_abs[4,7]/sqrt(nparticipants)),
                              'leg_l'=c(t*stdDataLM_abs[1,8]/sqrt(nparticipants), t*stdDataLM_abs[2,8]/sqrt(nparticipants), t*stdDataLM_abs[3,8]/sqrt(nparticipants), t*stdDataLM_abs[4,8]/sqrt(nparticipants)),
                              'back'=c(t*stdDataLM_abs[1,12]/sqrt(nparticipants), t*stdDataLM_abs[2,12]/sqrt(nparticipants), t*stdDataLM_abs[3,12]/sqrt(nparticipants), t*stdDataLM_abs[4,12]/sqrt(nparticipants)),
                              'neck'=c(t*stdDataLM_abs[1,13]/sqrt(nparticipants), t*stdDataLM_abs[2,13]/sqrt(nparticipants), t*stdDataLM_abs[3,13]/sqrt(nparticipants), t*stdDataLM_abs[4,13]/sqrt(nparticipants))
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -4L))



op = par(mar=c(4,4,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(land_abs.means), main="Jump Linear Momentum",
               ylab="kg.m/s",
               xlim=c(0,35),ylim=c(-70,10),
               col=c("red","green","blue","yellow"),
               legend = c( "1%","40%", "70%", "100%"),  las=2, cex.names = 1, beside=TRUE) #beside=TRUE,xlab="joint",
rm(op)


xx=as.matrix(land_abs.means)
er=as.matrix(land_abs.stds)
erci=as.matrix(land_abs.ci)
arrows(barx,xx+erci, barx,xx, angle=90, code=3, length=0.05)
arrows(barx,xx-erci, barx,xx, angle=90, code=3, length=0.05)










# STABILITY **************************************************************************
land_stab.means <- structure(list('pelvis'=c(meanDataLM_stab[1,1], meanDataLM_stab[2,1], meanDataLM_stab[3,1], meanDataLM_stab[4,1]),
                                  'thigh_r'=c(meanDataLM_stab[1,2], meanDataLM_stab[2,2], meanDataLM_stab[3,2], meanDataLM_stab[4,2]),
                                  'leg_r'=c(meanDataLM_stab[1,3], meanDataLM_stab[2,3], meanDataLM_stab[3,3], meanDataLM_stab[4,3]),
                                  'thigh_l'=c(meanDataLM_stab[1,7], meanDataLM_stab[2,7], meanDataLM_stab[3,7], meanDataLM_stab[4,7]),
                                  'leg_l'=c(meanDataLM_stab[1,8], meanDataLM_stab[2,8], meanDataLM_stab[3,8], meanDataLM_stab[4,8]),
                                  'back'=c(meanDataLM_stab[1,12], meanDataLM_stab[2,12], meanDataLM_stab[3,12], meanDataLM_stab[4,12]),
                                  'neck'=c(meanDataLM_stab[1,13], meanDataLM_stab[2,13], meanDataLM_stab[3,13], meanDataLM_stab[4,13])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -4L))

#
land_stab.stds <- structure(list('pelvis'=c(stdDataLM_stab[1,1], stdDataLM_stab[2,1], stdDataLM_stab[3,1], stdDataLM_stab[4,1]),
                                 'thigh_r'=c(stdDataLM_stab[1,2], stdDataLM_stab[2,2], stdDataLM_stab[3,2], stdDataLM_stab[4,2]),
                                 'leg_r'=c(stdDataLM_stab[1,3], stdDataLM_stab[2,3], stdDataLM_stab[3,3], stdDataLM_stab[4,3]),
                                 'thigh_l'=c(stdDataLM_stab[1,7], stdDataLM_stab[2,7], stdDataLM_stab[3,7], stdDataLM_stab[4,7]),
                                 'leg_l'=c(stdDataLM_stab[1,8], stdDataLM_stab[2,8], stdDataLM_stab[3,8], stdDataLM_stab[4,8]),
                                 'back'=c(stdDataLM_stab[1,12], stdDataLM_stab[2,12], stdDataLM_stab[3,12], stdDataLM_stab[4,12]),
                                 'neck'=c(stdDataLM_stab[1,13], stdDataLM_stab[2,13], stdDataLM_stab[3,13], stdDataLM_stab[4,13])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -4L))

land_stab.ci <- structure(list('pelvis'=c(t*stdDataLM_stab[1,1]/sqrt(nparticipants), t*stdDataLM_stab[2,1]/sqrt(nparticipants), t*stdDataLM_stab[3,1]/sqrt(nparticipants), t*stdDataLM_stab[4,1]/sqrt(nparticipants)),
                               'thigh_r'=c(t*stdDataLM_stab[1,2]/sqrt(nparticipants), t*stdDataLM_stab[2,2]/sqrt(nparticipants), t*stdDataLM_stab[3,2]/sqrt(nparticipants), t*stdDataLM_stab[4,2]/sqrt(nparticipants)),
                               'leg_r'=c(t*stdDataLM_stab[1,3]/sqrt(nparticipants), t*stdDataLM_stab[2,3]/sqrt(nparticipants), t*stdDataLM_stab[3,3]/sqrt(nparticipants), t*stdDataLM_stab[4,3]/sqrt(nparticipants)),
                               'thigh_l'=c(t*stdDataLM_stab[1,7]/sqrt(nparticipants), t*stdDataLM_stab[2,7]/sqrt(nparticipants), t*stdDataLM_stab[3,7]/sqrt(nparticipants), t*stdDataLM_stab[4,7]/sqrt(nparticipants)),
                               'leg_l'=c(t*stdDataLM_stab[1,8]/sqrt(nparticipants), t*stdDataLM_stab[2,8]/sqrt(nparticipants), t*stdDataLM_stab[3,8]/sqrt(nparticipants), t*stdDataLM_stab[4,8]/sqrt(nparticipants)),
                               'back'=c(t*stdDataLM_stab[1,12]/sqrt(nparticipants), t*stdDataLM_stab[2,12]/sqrt(nparticipants), t*stdDataLM_stab[3,12]/sqrt(nparticipants), t*stdDataLM_stab[4,12]/sqrt(nparticipants)),
                               'neck'=c(t*stdDataLM_stab[1,13]/sqrt(nparticipants), t*stdDataLM_stab[2,13]/sqrt(nparticipants), t*stdDataLM_stab[3,13]/sqrt(nparticipants), t*stdDataLM_stab[4,13]/sqrt(nparticipants))
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -4L))

op = par(mar=c(4,4,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(land_stab.means), main="Jump Linear Momentum Stability",
               ylab="kg.m/s",
               xlim=c(0,35),ylim=c(-20,80),
               col=c("red","green","blue","yellow"),
               legend = c( "1%","40%", "70%", "100%"),  las=2, cex.names = 1, beside=TRUE) #beside=TRUE,xlab="joint",
rm(op)


xx=as.matrix(land_stab.means)
er=as.matrix(land_stab.stds)
erci=as.matrix(land_stab.ci)
arrows(barx,xx+erci, barx,xx, angle=90, code=3, length=0.05)
arrows(barx,xx-erci, barx,xx, angle=90, code=3, length=0.05)