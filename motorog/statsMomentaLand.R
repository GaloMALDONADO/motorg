# Analysis of Variances from uncontrolled manifold and its orthogonal space
rm(list = ls())


# ------------------------------------------------------------------------
p='/galo/devel/gepetto/motorg/motorog/tables/momenta/' #home
#p='/local/gmaldona/devel/motorg/motorog/tables/momenta/' #lab
nparticipants = 5
ddl=nparticipants-1
t = qt(.975,ddl)
names<- c('pelvis','thigh_r','leg_r','ankle_r','subtalar_r','mtp_r','thigh_l','leg_l','ankle_l','subtalar_l',
          'mtp_l','back','head','arm_r','elbow_r','radioulnar_r','radius_lunate_r','lunate_hand_r','fingers_r',
          'arm_l','elbow_l','radioulnar_l','radius_lunate_l','lunate_hand_l','fingers_l')

# ---------------------- Read the data -----------------------------------
pathName = paste(p,'TableMomentaLandLinMomML.csv',sep="")
h_ml = read.csv(pathName, header = FALSE, col.names = list('Participant', 'Phase', 'Segment' ,'Momenta'))
h_ml$Participant<-as.factor(h_ml$Participant)
h_ml$Phase<-as.factor(h_ml$Phase)
h_ml$Segment<-as.factor(h_ml$Segment)

pathName = paste(p,'TableMomentaLandLinMomAP.csv',sep="")
h_ap = read.csv(pathName, header = FALSE, col.names = list('Participant', 'Phase', 'Segment' ,'Momenta'))
h_ap$Participant<-as.factor(h_ap$Participant)
h_ap$Phase<-as.factor(h_ap$Phase)
h_ap$Segment<-as.factor(h_ap$Segment)

pathName = paste(p,'TableMomentaLandLinMomV.csv',sep="")
h_v = read.csv(pathName, header = FALSE, col.names = list('Participant', 'Phase', 'Segment' ,'Momenta'))
h_v$Participant<-as.factor(h_v$Participant)
h_v$Phase<-as.factor(h_v$Phase)
h_v$Segment<-as.factor(h_v$Segment)

pathName = paste(p,'TableMomentaLandAngMom.csv',sep="")
l = read.csv(pathName, header = FALSE, col.names = list('Participant', 'Phase', 'Segment' ,'Momenta'))
l$Participant<-as.factor(l$Participant)
l$Phase<-as.factor(l$Phase)
l$Segment<-as.factor(l$Segment)


#
aovstats <-aov(h_ml$Momenta ~ 
                 (h_ml$Phase+h_ml$Segment) + 
                 Error(h_ml$Participant  / (h_ml$Phase+h_ml$Segment)), 
               data = h_ml)
summary(aovstats)

pairwise.t.test(h_ap$Momenta, h_ap$Phase, p.adj = "bonf",paired=TRUE)
pairwise.t.test(h_ap$Momenta, h_ap$Segment, p.adj = "bonf",paired=TRUE)

#
aovstats <-aov(h_ap$Momenta ~ 
                 (h_ap$Phase+h_ap$Segment) + 
                 Error(h_ap$Participant  / (h_ap$Phase+h_ap$Segment)), 
               data = h_ap)
summary(aovstats)

pairwise.t.test(h_ap$Momenta, h_ap$Phase, p.adj = "bonf",paired=TRUE)
pairwise.t.test(h_ap$Momenta, h_ap$Segment, p.adj = "bonf",paired=TRUE)

#
aovstats <-aov(h_v$Momenta ~ 
                 (h_v$Phase+h_v$Segment) + 
                 Error(h_v$Participant  / (h_v$Phase+h_v$Segment)), 
               data = h_v)
summary(aovstats)

pairwise.t.test(h_v$Momenta, h_v$Phase, p.adj = "bonf",paired=TRUE)
pairwise.t.test(h_v$Momenta, h_v$Segment, p.adj = "bonf",paired=TRUE)


#
aovstats <-aov(l$Momenta ~ 
                 (l$Phase+l$Segment) + 
                 Error(l$Participant  / (l$Phase+l$Segment)), 
               data = l)
summary(aovstats)

pairwise.t.test(l$Momenta, l$Phase, p.adj = "bonf",paired=TRUE)
pairwise.t.test(l$Momenta, l$Segment, p.adj = "bonf",paired=TRUE)


# 0 pelvis    1 rthigh    2 rleg    6 lthigh     7 lleg    11 back     12 head
#elvis different from right thigh and left thigh, back
#rthigh different from pelvis, rleg













# ----------------------- Means - Std - Confidence Interval --------------------------
pathName = paste(p,'mean/LandLMx.csv',sep="")
meanDataLMx = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'mean/LandLMy.csv',sep="")
meanDataLMy = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'mean/LandLMz.csv',sep="")
meanDataLMz = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'std/LandLMx.csv',sep="")
stdDataLMx = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'std/LandLMy.csv',sep="")
stdDataLMy = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'std/LandLMz.csv',sep="")
stdDataLMz = read.csv(pathName, header = FALSE, col.names = names)

pathName = paste(p,'mean/LandAMx.csv',sep="")
meanDataAMx = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'mean/LandAMy.csv',sep="")
meanDataAMy = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'mean/LandAMz.csv',sep="")
meanDataAMz = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'std/LandAMx.csv',sep="")
stdDataAMx = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'std/LandAMy.csv',sep="")
stdDataAMy = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'std/LandAMz.csv',sep="")
stdDataAMz = read.csv(pathName, header = FALSE, col.names = names)



# MEANS
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
                               'head'=c(meanDataLMx[1,13], meanDataLMx[2,13], meanDataLMx[3,13], meanDataLMx[4,13]),
                               'arm_r'=c(meanDataLMx[1,14], meanDataLMx[2,14], meanDataLMx[3,14], meanDataLMx[4,14]),
                               'elbow_r'=c(meanDataLMx[1,15], meanDataLMx[2,15], meanDataLMx[3,15], meanDataLMx[4,15]),
                               'radioulnar_r'=c(meanDataLMx[1,16], meanDataLMx[2,16], meanDataLMx[3,16], meanDataLMx[4,16]),
                               'radius_lunate_r'=c(meanDataLMx[1,17], meanDataLMx[2,17], meanDataLMx[3,17], meanDataLMx[4,17]),
                               'lunate_hand_r'=c(meanDataLMx[1,18], meanDataLMx[2,18], meanDataLMx[3,18], meanDataLMx[4,18]),
                               'fingers_r'=c(meanDataLMx[1,19], meanDataLMx[2,19], meanDataLMx[3,19], meanDataLMx[4,19]),
                               'arm_l'=c(meanDataLMx[1,20], meanDataLMx[2,20], meanDataLMx[3,20], meanDataLMx[4,20]),
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
                               'head'=c(meanDataLMy[1,13], meanDataLMy[2,13], meanDataLMy[3,13], meanDataLMy[4,13]),
                               'arm_r'=c(meanDataLMy[1,14], meanDataLMy[2,14], meanDataLMy[3,14], meanDataLMy[4,14]),
                               'elbow_r'=c(meanDataLMy[1,15], meanDataLMy[2,15], meanDataLMy[3,15], meanDataLMy[4,15]),
                               'radioulnar_r'=c(meanDataLMy[1,16], meanDataLMy[2,16], meanDataLMy[3,16], meanDataLMy[4,16]),
                               'radius_lunate_r'=c(meanDataLMy[1,17], meanDataLMy[2,17], meanDataLMy[3,17], meanDataLMy[4,17]),
                               'lunate_hand_r'=c(meanDataLMy[1,18], meanDataLMy[2,18], meanDataLMy[3,18], meanDataLMy[4,18]),
                               'fingers_r'=c(meanDataLMy[1,19], meanDataLMy[2,19], meanDataLMy[3,19], meanDataLMy[4,19]),
                               'arm_l'=c(meanDataLMy[1,20], meanDataLMy[2,20], meanDataLMy[3,20], meanDataLMy[4,20]),
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
                               'head'=c(meanDataLMz[1,13], meanDataLMz[2,13], meanDataLMz[3,13], meanDataLMz[4,13]),
                               'arm_r'=c(meanDataLMz[1,14], meanDataLMz[2,14], meanDataLMz[3,14], meanDataLMz[4,14]),
                               'elbow_r'=c(meanDataLMz[1,15], meanDataLMz[2,15], meanDataLMz[3,15], meanDataLMz[4,15]),
                               'radioulnar_r'=c(meanDataLMz[1,16], meanDataLMz[2,16], meanDataLMz[3,16], meanDataLMz[4,16]),
                               'radius_lunate_r'=c(meanDataLMz[1,17], meanDataLMz[2,17], meanDataLMz[3,17], meanDataLMz[4,17]),
                               'lunate_hand_r'=c(meanDataLMz[1,18], meanDataLMz[2,18], meanDataLMz[3,18], meanDataLMz[4,18]),
                               'fingers_r'=c(meanDataLMz[1,19], meanDataLMz[2,19], meanDataLMz[3,19], meanDataLMz[4,19]),
                               'arm_l'=c(meanDataLMz[1,20], meanDataLMz[2,20], meanDataLMz[3,20], meanDataLMz[4,20]),
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
                                'head'=c(meanDataAMx[1,13], meanDataAMx[2,13], meanDataAMx[3,13], meanDataAMx[4,13]),
                                'arm_r'=c(meanDataAMx[1,14], meanDataAMx[2,14], meanDataAMx[3,14], meanDataAMx[4,14]),
                                'elbow_r'=c(meanDataAMx[1,15], meanDataAMx[2,15], meanDataAMx[3,15], meanDataAMx[4,15]),
                                'radioulnar_r'=c(meanDataAMx[1,16], meanDataAMx[2,16], meanDataAMx[3,16], meanDataAMx[4,16]),
                                'radius_lunate_r'=c(meanDataAMx[1,17], meanDataAMx[2,17], meanDataAMx[3,17], meanDataAMx[4,17]),
                                'lunate_hand_r'=c(meanDataAMx[1,18], meanDataAMx[2,18], meanDataAMx[3,18], meanDataAMx[4,18]),
                                'fingers_r'=c(meanDataAMx[1,19], meanDataAMx[2,19], meanDataAMx[3,19], meanDataAMx[4,19]),
                                'arm_l'=c(meanDataAMx[1,20], meanDataAMx[2,20], meanDataAMx[3,20], meanDataAMx[4,20]),
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
                                'head'=c(meanDataAMy[1,13], meanDataAMy[2,13], meanDataAMy[3,13], meanDataAMy[4,13]),
                                'arm_r'=c(meanDataAMy[1,14], meanDataAMy[2,14], meanDataAMy[3,14], meanDataAMy[4,14]),
                                'elbow_r'=c(meanDataAMy[1,15], meanDataAMy[2,15], meanDataAMy[3,15], meanDataAMy[4,15]),
                                'radioulnar_r'=c(meanDataAMy[1,16], meanDataAMy[2,16], meanDataAMy[3,16], meanDataAMy[4,16]),
                                'radius_lunate_r'=c(meanDataAMy[1,17], meanDataAMy[2,17], meanDataAMy[3,17], meanDataAMy[4,17]),
                                'lunate_hand_r'=c(meanDataAMy[1,18], meanDataAMy[2,18], meanDataAMy[3,18], meanDataAMy[4,18]),
                                'fingers_r'=c(meanDataAMy[1,19], meanDataAMy[2,19], meanDataAMy[3,19], meanDataAMy[4,19]),
                                'arm_l'=c(meanDataAMy[1,20], meanDataAMy[2,20], meanDataAMy[3,20], meanDataAMy[4,20]),
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
                                'head'=c(meanDataAMz[1,13], meanDataAMz[2,13], meanDataAMz[3,13], meanDataAMz[4,13]),
                                'arm_r'=c(meanDataAMz[1,14], meanDataAMz[2,14], meanDataAMz[3,14], meanDataAMz[4,14]),
                                'elbow_r'=c(meanDataAMz[1,15], meanDataAMz[2,15], meanDataAMz[3,15], meanDataAMz[4,15]),
                                'radioulnar_r'=c(meanDataAMz[1,16], meanDataAMz[2,16], meanDataAMz[3,16], meanDataAMz[4,16]),
                                'radius_lunate_r'=c(meanDataAMz[1,17], meanDataAMz[2,17], meanDataAMz[3,17], meanDataAMz[4,17]),
                                'lunate_hand_r'=c(meanDataAMz[1,18], meanDataAMz[2,18], meanDataAMz[3,18], meanDataAMz[4,18]),
                                'fingers_r'=c(meanDataAMz[1,19], meanDataAMz[2,19], meanDataAMz[3,19], meanDataAMz[4,19]),
                                'arm_l'=c(meanDataAMz[1,20], meanDataAMz[2,20], meanDataAMz[3,20], meanDataAMz[4,20]),
                                'elbow_l'=c(meanDataAMz[1,21], meanDataAMz[2,21], meanDataAMz[3,21], meanDataAMz[4,21]),
                                'radioulnar_l'=c(meanDataAMz[1,22], meanDataAMz[2,22], meanDataAMz[3,22], meanDataAMz[4,22]),
                                'radius_lunate_l'=c(meanDataAMz[1,23], meanDataAMz[2,23], meanDataAMz[3,23], meanDataAMz[4,23]),
                                'lunate_hand_l'=c(meanDataAMz[1,24], meanDataAMz[2,24], meanDataAMz[3,24], meanDataAMz[4,24]),
                                'fingers_l'=c(meanDataAMz[1,25], meanDataAMz[2,25], meanDataAMz[3,25], meanDataAMz[4,25])
), 
.Names = names, 
class = "data.frame", row.names = c(NA, -4L))



# STD ----------------------------------------
# Linear Momentum x
land.std.x <- structure(list('pelvis'=c(stdDataLMx[1,1], stdDataLMx[2,1], stdDataLMx[3,1], stdDataLMx[4,1]),
                               'thigh_r'=c(stdDataLMx[1,2], stdDataLMx[2,2], stdDataLMx[3,2], stdDataLMx[4,2]),
                               'leg_r'=c(stdDataLMx[1,3], stdDataLMx[2,3], stdDataLMx[3,3], stdDataLMx[4,3]),
                               'ankle_r'=c(stdDataLMx[1,4], stdDataLMx[2,4], stdDataLMx[3,4], stdDataLMx[4,4]),
                               'subtalar_r'=c(stdDataLMx[1,5], stdDataLMx[2,5], stdDataLMx[3,5], stdDataLMx[4,5]),
                               'mtp_r'=c(stdDataLMx[1,6], stdDataLMx[2,6], stdDataLMx[3,6], stdDataLMx[4,6]),
                               'thigh_l'=c(stdDataLMx[1,7], stdDataLMx[2,7], stdDataLMx[3,7], stdDataLMx[4,7]),
                               'leg_l'=c(stdDataLMx[1,8], stdDataLMx[2,8], stdDataLMx[3,8], stdDataLMx[4,8]),
                               'ankle_l'=c(stdDataLMx[1,9], stdDataLMx[2,9], stdDataLMx[3,9], stdDataLMx[4,9]),
                               'subtalar_l'=c(stdDataLMx[1,10], stdDataLMx[2,10], stdDataLMx[3,10], stdDataLMx[4,10]),
                               'mtp_l'=c(stdDataLMx[1,11], stdDataLMx[2,11], stdDataLMx[3,11], stdDataLMx[4,11]),
                               'back'=c(stdDataLMx[1,12], stdDataLMx[2,12], stdDataLMx[3,12], stdDataLMx[4,12]),
                               'head'=c(stdDataLMx[1,13], stdDataLMx[2,13], stdDataLMx[3,13], stdDataLMx[4,13]),
                               'arm_r'=c(stdDataLMx[1,14], stdDataLMx[2,14], stdDataLMx[3,14], stdDataLMx[4,14]),
                               'elbow_r'=c(stdDataLMx[1,15], stdDataLMx[2,15], stdDataLMx[3,15], stdDataLMx[4,15]),
                               'radioulnar_r'=c(stdDataLMx[1,16], stdDataLMx[2,16], stdDataLMx[3,16], stdDataLMx[4,16]),
                               'radius_lunate_r'=c(stdDataLMx[1,17], stdDataLMx[2,17], stdDataLMx[3,17], stdDataLMx[4,17]),
                               'lunate_hand_r'=c(stdDataLMx[1,18], stdDataLMx[2,18], stdDataLMx[3,18], stdDataLMx[4,18]),
                               'fingers_r'=c(stdDataLMx[1,19], stdDataLMx[2,19], stdDataLMx[3,19], stdDataLMx[4,19]),
                               'arm_l'=c(stdDataLMx[1,20], stdDataLMx[2,20], stdDataLMx[3,20], stdDataLMx[4,20]),
                               'elbow_l'=c(stdDataLMx[1,21], stdDataLMx[2,21], stdDataLMx[3,21], stdDataLMx[4,21]),
                               'radioulnar_l'=c(stdDataLMx[1,22], stdDataLMx[2,22], stdDataLMx[3,22], stdDataLMx[4,22]),
                               'radius_lunate_l'=c(stdDataLMx[1,23], stdDataLMx[2,23], stdDataLMx[3,23], stdDataLMx[4,23]),
                               'lunate_hand_l'=c(stdDataLMx[1,24], stdDataLMx[2,24], stdDataLMx[3,24], stdDataLMx[4,24]),
                               'fingers_l'=c(stdDataLMx[1,25], stdDataLMx[2,25], stdDataLMx[3,25], stdDataLMx[4,25])
), 
.Names = names, 
class = "data.frame", row.names = c(NA, -4L))



# Linear Momentum Y
land.std.y <- structure(list('pelvis'=c(stdDataLMy[1,1], stdDataLMy[2,1], stdDataLMy[3,1], stdDataLMy[4,1]),
                               'thigh_r'=c(stdDataLMy[1,2], stdDataLMy[2,2], stdDataLMy[3,2], stdDataLMy[4,2]),
                               'leg_r'=c(stdDataLMy[1,3], stdDataLMy[2,3], stdDataLMy[3,3], stdDataLMy[4,3]),
                               'ankle_r'=c(stdDataLMy[1,4], stdDataLMy[2,4], stdDataLMy[3,4], stdDataLMy[4,4]),
                               'subtalar_r'=c(stdDataLMy[1,5], stdDataLMy[2,5], stdDataLMy[3,5], stdDataLMy[4,5]),
                               'mtp_r'=c(stdDataLMy[1,6], stdDataLMy[2,6], stdDataLMy[3,6], stdDataLMy[4,6]),
                               'thigh_l'=c(stdDataLMy[1,7], stdDataLMy[2,7], stdDataLMy[3,7], stdDataLMy[4,7]),
                               'leg_l'=c(stdDataLMy[1,8], stdDataLMy[2,8], stdDataLMy[3,8], stdDataLMy[4,8]),
                               'ankle_l'=c(stdDataLMy[1,9], stdDataLMy[2,9], stdDataLMy[3,9], stdDataLMy[4,9]),
                               'subtalar_l'=c(stdDataLMy[1,10], stdDataLMy[2,10], stdDataLMy[3,10], stdDataLMy[4,10]),
                               'mtp_l'=c(stdDataLMy[1,11], stdDataLMy[2,11], stdDataLMy[3,11], stdDataLMy[4,11]),
                               'back'=c(stdDataLMy[1,12], stdDataLMy[2,12], stdDataLMy[3,12], stdDataLMy[4,12]),
                               'head'=c(stdDataLMy[1,13], stdDataLMy[2,13], stdDataLMy[3,13], stdDataLMy[4,13]),
                               'arm_r'=c(stdDataLMy[1,14], stdDataLMy[2,14], stdDataLMy[3,14], stdDataLMy[4,14]),
                               'elbow_r'=c(stdDataLMy[1,15], stdDataLMy[2,15], stdDataLMy[3,15], stdDataLMy[4,15]),
                               'radioulnar_r'=c(stdDataLMy[1,16], stdDataLMy[2,16], stdDataLMy[3,16], stdDataLMy[4,16]),
                               'radius_lunate_r'=c(stdDataLMy[1,17], stdDataLMy[2,17], stdDataLMy[3,17], stdDataLMy[4,17]),
                               'lunate_hand_r'=c(stdDataLMy[1,18], stdDataLMy[2,18], stdDataLMy[3,18], stdDataLMy[4,18]),
                               'fingers_r'=c(stdDataLMy[1,19], stdDataLMy[2,19], stdDataLMy[3,19], stdDataLMy[4,19]),
                               'arm_l'=c(stdDataLMy[1,20], stdDataLMy[2,20], stdDataLMy[3,20], stdDataLMy[4,20]),
                               'elbow_l'=c(stdDataLMy[1,21], stdDataLMy[2,21], stdDataLMy[3,21], stdDataLMy[4,21]),
                               'radioulnar_l'=c(stdDataLMy[1,22], stdDataLMy[2,22], stdDataLMy[3,22], stdDataLMy[4,22]),
                               'radius_lunate_l'=c(stdDataLMy[1,23], stdDataLMy[2,23], stdDataLMy[3,23], stdDataLMy[4,23]),
                               'lunate_hand_l'=c(stdDataLMy[1,24], stdDataLMy[2,24], stdDataLMy[3,24], stdDataLMy[4,24]),
                               'fingers_l'=c(stdDataLMy[1,25], stdDataLMy[2,25], stdDataLMy[3,25], stdDataLMy[4,25])
), 
.Names = names, 
class = "data.frame", row.names = c(NA, -4L))


# Linear Momentum Z
land.std.z <- structure(list('pelvis'=c(stdDataLMz[1,1], stdDataLMz[2,1], stdDataLMz[3,1], stdDataLMz[4,1]),
                               'thigh_r'=c(stdDataLMz[1,2], stdDataLMz[2,2], stdDataLMz[3,2], stdDataLMz[4,2]),
                               'leg_r'=c(stdDataLMz[1,3], stdDataLMz[2,3], stdDataLMz[3,3], stdDataLMz[4,3]),
                               'ankle_r'=c(stdDataLMz[1,4], stdDataLMz[2,4], stdDataLMz[3,4], stdDataLMz[4,4]),
                               'subtalar_r'=c(stdDataLMz[1,5], stdDataLMz[2,5], stdDataLMz[3,5], stdDataLMz[4,5]),
                               'mtp_r'=c(stdDataLMz[1,6], stdDataLMz[2,6], stdDataLMz[3,6], stdDataLMz[4,6]),
                               'thigh_l'=c(stdDataLMz[1,7], stdDataLMz[2,7], stdDataLMz[3,7], stdDataLMz[4,7]),
                               'leg_l'=c(stdDataLMz[1,8], stdDataLMz[2,8], stdDataLMz[3,8], stdDataLMz[4,8]),
                               'ankle_l'=c(stdDataLMz[1,9], stdDataLMz[2,9], stdDataLMz[3,9], stdDataLMz[4,9]),
                               'subtalar_l'=c(stdDataLMz[1,10], stdDataLMz[2,10], stdDataLMz[3,10], stdDataLMz[4,10]),
                               'mtp_l'=c(stdDataLMz[1,11], stdDataLMz[2,11], stdDataLMz[3,11], stdDataLMz[4,11]),
                               'back'=c(stdDataLMz[1,12], stdDataLMz[2,12], stdDataLMz[3,12], stdDataLMz[4,12]),
                               'head'=c(stdDataLMz[1,13], stdDataLMz[2,13], stdDataLMz[3,13], stdDataLMz[4,13]),
                               'arm_r'=c(stdDataLMz[1,14], stdDataLMz[2,14], stdDataLMz[3,14], stdDataLMz[4,14]),
                               'elbow_r'=c(stdDataLMz[1,15], stdDataLMz[2,15], stdDataLMz[3,15], stdDataLMz[4,15]),
                               'radioulnar_r'=c(stdDataLMz[1,16], stdDataLMz[2,16], stdDataLMz[3,16], stdDataLMz[4,16]),
                               'radius_lunate_r'=c(stdDataLMz[1,17], stdDataLMz[2,17], stdDataLMz[3,17], stdDataLMz[4,17]),
                               'lunate_hand_r'=c(stdDataLMz[1,18], stdDataLMz[2,18], stdDataLMz[3,18], stdDataLMz[4,18]),
                               'fingers_r'=c(stdDataLMz[1,19], stdDataLMz[2,19], stdDataLMz[3,19], stdDataLMz[4,19]),
                               'arm_l'=c(stdDataLMz[1,20], stdDataLMz[2,20], stdDataLMz[3,20], stdDataLMz[4,20]),
                               'elbow_l'=c(stdDataLMz[1,21], stdDataLMz[2,21], stdDataLMz[3,21], stdDataLMz[4,21]),
                               'radioulnar_l'=c(stdDataLMz[1,22], stdDataLMz[2,22], stdDataLMz[3,22], stdDataLMz[4,22]),
                               'radius_lunate_l'=c(stdDataLMz[1,23], stdDataLMz[2,23], stdDataLMz[3,23], stdDataLMz[4,23]),
                               'lunate_hand_l'=c(stdDataLMz[1,24], stdDataLMz[2,24], stdDataLMz[3,24], stdDataLMz[4,24]),
                               'fingers_l'=c(stdDataLMz[1,25], stdDataLMz[2,25], stdDataLMz[3,25], stdDataLMz[4,25])
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
                                'head'=c(meanDataAMx[1,13], meanDataAMx[2,13], meanDataAMx[3,13], meanDataAMx[4,13]),
                                'arm_r'=c(meanDataAMx[1,14], meanDataAMx[2,14], meanDataAMx[3,14], meanDataAMx[4,14]),
                                'elbow_r'=c(meanDataAMx[1,15], meanDataAMx[2,15], meanDataAMx[3,15], meanDataAMx[4,15]),
                                'radioulnar_r'=c(meanDataAMx[1,16], meanDataAMx[2,16], meanDataAMx[3,16], meanDataAMx[4,16]),
                                'radius_lunate_r'=c(meanDataAMx[1,17], meanDataAMx[2,17], meanDataAMx[3,17], meanDataAMx[4,17]),
                                'lunate_hand_r'=c(meanDataAMx[1,18], meanDataAMx[2,18], meanDataAMx[3,18], meanDataAMx[4,18]),
                                'fingers_r'=c(meanDataAMx[1,19], meanDataAMx[2,19], meanDataAMx[3,19], meanDataAMx[4,19]),
                                'arm_l'=c(meanDataAMx[1,20], meanDataAMx[2,20], meanDataAMx[3,20], meanDataAMx[4,20]),
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
                                'head'=c(meanDataAMy[1,13], meanDataAMy[2,13], meanDataAMy[3,13], meanDataAMy[4,13]),
                                'arm_r'=c(meanDataAMy[1,14], meanDataAMy[2,14], meanDataAMy[3,14], meanDataAMy[4,14]),
                                'elbow_r'=c(meanDataAMy[1,15], meanDataAMy[2,15], meanDataAMy[3,15], meanDataAMy[4,15]),
                                'radioulnar_r'=c(meanDataAMy[1,16], meanDataAMy[2,16], meanDataAMy[3,16], meanDataAMy[4,16]),
                                'radius_lunate_r'=c(meanDataAMy[1,17], meanDataAMy[2,17], meanDataAMy[3,17], meanDataAMy[4,17]),
                                'lunate_hand_r'=c(meanDataAMy[1,18], meanDataAMy[2,18], meanDataAMy[3,18], meanDataAMy[4,18]),
                                'fingers_r'=c(meanDataAMy[1,19], meanDataAMy[2,19], meanDataAMy[3,19], meanDataAMy[4,19]),
                                'arm_l'=c(meanDataAMy[1,20], meanDataAMy[2,20], meanDataAMy[3,20], meanDataAMy[4,20]),
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
                                'head'=c(meanDataAMz[1,13], meanDataAMz[2,13], meanDataAMz[3,13], meanDataAMz[4,13]),
                                'arm_r'=c(meanDataAMz[1,14], meanDataAMz[2,14], meanDataAMz[3,14], meanDataAMz[4,14]),
                                'elbow_r'=c(meanDataAMz[1,15], meanDataAMz[2,15], meanDataAMz[3,15], meanDataAMz[4,15]),
                                'radioulnar_r'=c(meanDataAMz[1,16], meanDataAMz[2,16], meanDataAMz[3,16], meanDataAMz[4,16]),
                                'radius_lunate_r'=c(meanDataAMz[1,17], meanDataAMz[2,17], meanDataAMz[3,17], meanDataAMz[4,17]),
                                'lunate_hand_r'=c(meanDataAMz[1,18], meanDataAMz[2,18], meanDataAMz[3,18], meanDataAMz[4,18]),
                                'fingers_r'=c(meanDataAMz[1,19], meanDataAMz[2,19], meanDataAMz[3,19], meanDataAMz[4,19]),
                                'arm_l'=c(meanDataAMz[1,20], meanDataAMz[2,20], meanDataAMz[3,20], meanDataAMz[4,20]),
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
barx = barplot(as.matrix(-land.means.x), main="Land Linear Momentum A-P",
               ylab=expression(kg %.% m %.% s^-1 %.% BW^-1),
               xlim=c(0,30),ylim=c(0.0,0.15),
               col=c("red","green","blue","yellow"),
               legend = c( "5%","20%", "40%", "100%"),  las=2, cex.names = 1) #beside=TRUE,xlab="joint",
rm(op)
# contribute: pelvis, thighs, legs, back, head, arms(-)

op = par(mar=c(8,4,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(land.means.y), main="Land Linear Momentum M-L",
               ylab=expression(kg %.% m %.% s^-1 %.% BM^-1),
               xlim=c(0,30),ylim=c(0.0,0.15),
               col=c("red","green","blue","yellow"),
               legend = c( "5%","20%", "40%", "100%"),  las=2, cex.names = 1) #beside=TRUE,xlab="joint",
rm(op)
# contribute: arms, forearms, hands, back, head, arms(-) (right sign opposed to left)

op = par(mar=c(8,4,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(land.means.z), main="Land Linear Momentum Vertical",
               ylab=expression(kg %.% m %.% s^-1 %.% BM^-1),
               xlim=c(0,30),ylim=c(0,-0.35),
               col=c("red","green","blue","yellow"),
               legend = c( "5%","20%", "40%", "100%"),  las=2, cex.names = 1) #beside=TRUE,xlab="joint",
rm(op)
# contribute: pelvis, thighs, legs, back, head, arms(-)


# unconmment to plot with SD
#arrows(barx,xx+er, barx,xx, angle=90, code=3, length=0.05)



# 
op = par(mar=c(8,5,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(land.means.xx), main="Land Angular Momentum X",
               ylab=expression(kg %.% m %.% s^-1 %.% BM^-1 %.% H),
               xlim=c(0,30),ylim=c(-0.02,0.01),
               col=c("red","green","blue","yellow"),
               legend = c( "5%","20%", "40%", "100%"),  las=2, cex.names = 1) #beside=TRUE,xlab="joint",
rm(op)


op = par(mar=c(8,5,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(land.means.yy), main="Land Angular Momentum Y",
               ylab=expression(kg %.% m %.% s^-1 %.% BM^-1 %.% H),
               xlim=c(0,30),ylim=c(-0.02,0.01),
               col=c("red","green","blue","yellow"),
               legend = c( "5%","20%", "40%", "100%"),  las=2, cex.names = 1) #beside=TRUE,xlab="joint",
rm(op)
# contribute: pelvis, thighs, legs, back, head


op = par(mar=c(8,5,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(land.means.zz), main="Land Angular Momentum Z",
               ylab=expression(kg %.% m %.% s^-1 %.% BM^-1 %.% H),
               xlim=c(0,30),ylim=c(-0.02,0.01),
               col=c("red","green","blue","yellow"),
               legend = c( "5%","20%", "40%", "100%"),  las=2, cex.names = 1) #beside=TRUE,xlab="joint",
rm(op)






#---------------------------------------------------------------------------------------------------------------------------
## simplified ****************************** 
simp_names = list('back','pelvis','thigh_r','thigh_l','head','leg_r','leg_l')
landing.means.x <- structure(list(
  'back'=c(meanDataLMx[1,12], meanDataLMx[2,12], meanDataLMx[3,12], meanDataLMx[4,12]),
  'pelvis'=c(meanDataLMx[1,1], meanDataLMx[2,1], meanDataLMx[3,1], meanDataLMx[4,1]),
  'thigh_r'=c(meanDataLMx[1,2], meanDataLMx[2,2], meanDataLMx[3,2], meanDataLMx[4,2]),
  'thigh_l'=c(meanDataLMx[1,7], meanDataLMx[2,7], meanDataLMx[3,7], meanDataLMx[4,7]),
  'head'=c(meanDataLMx[1,13], meanDataLMx[2,13], meanDataLMx[3,13], meanDataLMx[4,13]),
  'leg_r'=c(meanDataLMx[1,3], meanDataLMx[2,3], meanDataLMx[3,3], meanDataLMx[4,3]),
  'leg_l'=c(meanDataLMx[1,8], meanDataLMx[2,8], meanDataLMx[3,8], meanDataLMx[4,8])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -4L))

#
landing.stds.x <- structure(list(
  'back'=c(stdDataLMx[1,12], stdDataLMx[2,12], stdDataLMx[3,12], stdDataLMx[4,12]),
  'pelvis'=c(stdDataLMx[1,1], stdDataLMx[2,1], stdDataLMx[3,1], stdDataLMx[4,1]),
  'thigh_r'=c(stdDataLMx[1,2], stdDataLMx[2,2], stdDataLMx[3,2], stdDataLMx[4,2]),
  'thigh_l'=c(stdDataLMx[1,7], stdDataLMx[2,7], stdDataLMx[3,7], stdDataLMx[4,7]),
  'head'=c(stdDataLMx[1,13], stdDataLMx[2,13], stdDataLMx[3,13], stdDataLMx[4,13]),
  'leg_r'=c(stdDataLMx[1,3], stdDataLMx[2,3], stdDataLMx[3,3], stdDataLMx[4,3]),
  'leg_l'=c(stdDataLMx[1,8], stdDataLMx[2,8], stdDataLMx[3,8], stdDataLMx[4,8])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -4L))

landing.ci.x <- structure(list(
  'back'=c(t*stdDataLMx[1,12]/sqrt(nparticipants), t*stdDataLMx[2,12]/sqrt(nparticipants), t*stdDataLMx[3,12]/sqrt(nparticipants), t*stdDataLMx[4,12]/sqrt(nparticipants)),
  'pelvis'=c(t*stdDataLMx[1,1]/sqrt(nparticipants), t*stdDataLMx[2,1]/sqrt(nparticipants), t*stdDataLMx[3,1]/sqrt(nparticipants), t*stdDataLMx[4,1]/sqrt(nparticipants)),
  'thigh_r'=c(t*stdDataLMx[1,2]/sqrt(nparticipants), t*stdDataLMx[2,2]/sqrt(nparticipants), t*stdDataLMx[3,2]/sqrt(nparticipants), t*stdDataLMx[4,2]/sqrt(nparticipants)),
  'thigh_l'=c(t*stdDataLMx[1,7]/sqrt(nparticipants), t*stdDataLMx[2,7]/sqrt(nparticipants), t*stdDataLMx[3,7]/sqrt(nparticipants), t*stdDataLMx[4,7]/sqrt(nparticipants)),
  'head'=c(t*stdDataLMx[1,13]/sqrt(nparticipants), t*stdDataLMx[2,13]/sqrt(nparticipants), t*stdDataLMx[3,13]/sqrt(nparticipants), t*stdDataLMx[4,13]/sqrt(nparticipants)),
  'leg_r'=c(t*stdDataLMx[1,3]/sqrt(nparticipants), t*stdDataLMx[2,3]/sqrt(nparticipants), t*stdDataLMx[3,3]/sqrt(nparticipants), t*stdDataLMx[4,3]/sqrt(nparticipants)),
  'leg_l'=c(t*stdDataLMx[1,8]/sqrt(nparticipants), t*stdDataLMx[2,8]/sqrt(nparticipants), t*stdDataLMx[3,8]/sqrt(nparticipants), t*stdDataLMx[4,8]/sqrt(nparticipants))
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -4L))

op = par(mar=c(4,5,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(-landing.means.x), main="Landing Linear Momentum0 (A-P)",
               ylab=expression(kg %.% m %.% s^-1 %.% BW^-1),
               xlim=c(0,35),ylim=c(-0,0.06),
               col=c("red","green","blue","yellow"),
               legend = c( "5%","20%", "40%", "100%"),  
               las=2, cex.names = 1, beside=TRUE,args.legend = list(x=25,horiz=TRUE)) #beside=TRUE,xlab="joint",
rm(op)


xx=as.matrix(-landing.means.x)
er=as.matrix(landing.stds.x)
erci=as.matrix(landing.ci.x)
arrows(barx,xx+erci, barx,xx, angle=90, code=3, length=0.05)
arrows(barx,xx-erci, barx,xx, angle=90, code=3, length=0.05)




## vertical
simp_names = list('back','pelvis','head','arm_r','arm_l')
landing.means.z <- structure(list(
  'back'=c(meanDataLMz[1,12], meanDataLMz[2,12], meanDataLMz[3,12], meanDataLMz[4,12]),
  'pelvis'=c(meanDataLMz[1,1], meanDataLMz[2,1], meanDataLMz[3,1], meanDataLMz[4,1]),
  'head'=c(meanDataLMz[1,13], meanDataLMz[2,13], meanDataLMz[3,13], meanDataLMz[4,13]),
  'arm_r'=c(meanDataLMz[1,14], meanDataLMz[2,14], meanDataLMz[3,14], meanDataLMz[4,14]),
  'arm_l'=c(meanDataLMz[1,20], meanDataLMz[2,20], meanDataLMz[3,20], meanDataLMz[4,20])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -4L))

#
landing.stds.z <- structure(list(
  'back'=c(stdDataLMz[1,12], stdDataLMz[2,12], stdDataLMz[3,12], stdDataLMz[4,12]),
  'pelvis'=c(stdDataLMz[1,1], stdDataLMz[2,1], stdDataLMz[3,1], stdDataLMz[4,1]),
  'head'=c(stdDataLMz[1,13], stdDataLMz[2,13], stdDataLMz[3,13], stdDataLMz[4,13]),
  'arm_r'=c(stdDataLMz[1,14], stdDataLMz[2,14], stdDataLMz[3,14], stdDataLMz[4,14]),
  'arm_l'=c(stdDataLMz[1,20], stdDataLMz[2,20], stdDataLMz[3,20], stdDataLMz[4,20])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -4L))

landing.ci.z <- structure(list(
  'back'=c(t*stdDataLMz[1,12]/sqrt(nparticipants), t*stdDataLMz[2,12]/sqrt(nparticipants), t*stdDataLMz[3,12]/sqrt(nparticipants), t*stdDataLMz[4,12]/sqrt(nparticipants)),
  'pelvis'=c(t*stdDataLMz[1,1]/sqrt(nparticipants), t*stdDataLMz[2,1]/sqrt(nparticipants), t*stdDataLMz[3,1]/sqrt(nparticipants), t*stdDataLMz[4,1]/sqrt(nparticipants)),
  'head'=c(t*stdDataLMz[1,13]/sqrt(nparticipants), t*stdDataLMz[2,13]/sqrt(nparticipants), t*stdDataLMz[3,13]/sqrt(nparticipants), t*stdDataLMz[4,13]/sqrt(nparticipants)),
  'arm_r'=c(t*stdDataLMz[1,14]/sqrt(nparticipants), t*stdDataLMz[2,14]/sqrt(nparticipants), t*stdDataLMz[3,14]/sqrt(nparticipants), t*stdDataLMz[4,14]/sqrt(nparticipants)),
  'arm_l'=c(t*stdDataLMz[1,20]/sqrt(nparticipants), t*stdDataLMz[2,20]/sqrt(nparticipants), t*stdDataLMz[3,20]/sqrt(nparticipants), t*stdDataLMz[4,20]/sqrt(nparticipants))
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -4L))

op = par(mar=c(4,5,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(landing.means.z), main="Landing Linear Momentum0 (V)",
               ylab=expression(kg %.% m %.% s^-1 %.% BW^-1),
               xlim=c(0,35),ylim=c(-0.002,-0.15),
               col=c("red","green","blue","yellow"),
               legend = c( "5%","20%", "40%", "100%"),  las=2, cex.names = 1, beside=TRUE) #beside=TRUE,xlab="joint",
rm(op)


xx=as.matrix(landing.means.z)
er=as.matrix(landing.stds.z)
erci=as.matrix(landing.ci.z)
arrows(barx,xx+erci, barx,xx, angle=90, code=3, length=0.05)
arrows(barx,xx-erci, barx,xx, angle=90, code=3, length=0.05)





# PLOT PAPER
################ ordered by mass
## medial-lateral # contribute: arms, forearms, hands, back, head, arms(-) (right sign opposed to left)
simp_names = list('5%','20%','40%','100%')

landing.means.y <- structure(list(
  '5%'= c(meanDataLMy[1,14], meanDataLMy[1,20], meanDataLMy[1,15] + meanDataLMy[1,16], meanDataLMy[1,21] + meanDataLMy[1,22], meanDataLMy[1,18], meanDataLMy[1,24]),
  '20%' =c(meanDataLMy[2,14], meanDataLMy[2,20], meanDataLMy[2,15] + meanDataLMy[2,16], meanDataLMy[2,21] + meanDataLMy[2,22], meanDataLMy[2,18], meanDataLMy[2,24]),
  '40%' = c(meanDataLMy[3,14], meanDataLMy[3,20], meanDataLMy[3,15] + meanDataLMy[3,16] , meanDataLMy[3,21] + meanDataLMy[3,22], meanDataLMy[3,18], meanDataLMy[3,24]),
  '100%' = c(meanDataLMy[4,14], meanDataLMy[4,20], meanDataLMy[4,15] + meanDataLMy[4,16], meanDataLMy[4,21] +  meanDataLMy[4,22], meanDataLMy[4,18], meanDataLMy[4,24])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -6L))

#
landing.stds.y <- structure(list(
  '5%'= c(stdDataLMy[1,14], stdDataLMy[1,20], (stdDataLMy[1,15] +  stdDataLMy[1,16])/2, (stdDataLMy[1,21] + stdDataLMy[1,22])/2, stdDataLMy[1,18], stdDataLMy[1,24]),
  '20%' =c(stdDataLMy[2,14], stdDataLMy[2,20], (stdDataLMy[2,15] + stdDataLMy[2,16])/2, (stdDataLMy[2,21] + stdDataLMy[2,22])/2, stdDataLMy[2,18], stdDataLMy[2,24]),
  '40%' = c(stdDataLMy[3,14], stdDataLMy[3,20], (stdDataLMy[3,15] + stdDataLMy[3,16])/2, (stdDataLMy[3,21] + stdDataLMy[3,22])/2, stdDataLMy[3,18], stdDataLMy[3,24]),
  '100%' = c(stdDataLMy[4,14], stdDataLMy[4,20], (stdDataLMy[4,15] +  stdDataLMy[4,16])/2, (stdDataLMy[4,21] + stdDataLMy[4,22])/2, stdDataLMy[4,18], stdDataLMy[4,24])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -6L))

k=t/sqrt(nparticipants)
landing.ci.y <- structure(list(
  '5%'= c( k*stdDataLMy[1,14], k*stdDataLMy[1,20], k*((stdDataLMy[1,15] + stdDataLMy[1,16])/2), k*((stdDataLMy[1,21]+stdDataLMy[1,22])/2), k*stdDataLMy[1,18], k*stdDataLMy[1,24]),
  '20%' =c( k*stdDataLMy[2,14], k*stdDataLMy[2,20], k*((stdDataLMy[2,15] + stdDataLMy[2,16])/2), k*((stdDataLMy[2,21]+stdDataLMy[2,22])/2), k*stdDataLMy[2,18], k*stdDataLMy[2,24]),
  '40%' = c( k*stdDataLMy[3,14], k*stdDataLMy[3,20], k*((stdDataLMy[3,15] + stdDataLMy[3,16])/2), k*((stdDataLMy[3,21]+stdDataLMy[3,22])/2), k*stdDataLMy[3,18], k*stdDataLMy[3,24]),
  '100%' = c( k*stdDataLMy[4,14], k*stdDataLMy[4,20], k*((stdDataLMy[4,15] + stdDataLMy[4,16])/2), k*((stdDataLMy[4,21]+stdDataLMy[4,22])/2), k*stdDataLMy[4,18], k*stdDataLMy[4,24])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -6L))

op = par(mar=c(4,5,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(landing.means.y), main="Landing Linear Momentum (ML)",
               ylab=expression(kg %.% m %.% s^-1 %.% BW^-1),
               xlim=c(0,30),ylim=c(-0.01,0.01),
               col=c("red","green","blue","yellow","purple","azure2"),
               legend = c('arm_r','arm_l','forearm_r','forearm_l','hand_r','hand_l'), 
               las=2, cex.names = 1, beside=TRUE, args.legend = list(x=30,horiz=TRUE)) #beside=TRUE,xlab="joint",
rm(op)


xx=as.matrix(landing.means.y)
er=as.matrix(landing.stds.y)
erci=as.matrix(landing.ci.y)
arrows(barx,xx+erci, barx,xx, angle=90, code=3, length=0.05)
arrows(barx,xx-erci, barx,xx, angle=90, code=3, length=0.05)


## AP
## antero-posterior 
simp_names = list('5%','20%','40%','100%')
# contribute: pelvis, thighs, legs, back, head
landing.means.x <- structure(list(
  '1%'= c(meanDataLMx[1,12], meanDataLMx[1,1], meanDataLMx[1,2], meanDataLMx[1,7], meanDataLMx[1,13], meanDataLMx[1,3], meanDataLMx[1,8]),
  '40%' =c(meanDataLMx[2,12], meanDataLMx[2,1], meanDataLMx[2,2], meanDataLMx[2,7], meanDataLMx[2,13], meanDataLMx[2,3], meanDataLMx[2,8]),
  '70%' = c(meanDataLMx[3,12], meanDataLMx[3,1], meanDataLMx[3,2], meanDataLMx[3,7], meanDataLMx[3,13], meanDataLMx[3,3], meanDataLMx[3,8]),
  '100%' = c(meanDataLMx[4,12], meanDataLMx[4,1], meanDataLMx[4,2], meanDataLMx[4,7], meanDataLMx[4,13], meanDataLMx[4,3], meanDataLMx[4,8])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -7L))

#
landing.stds.x <- structure(list(
  '1%'= c(stdDataLMx[1,12], stdDataLMx[1,1], stdDataLMx[1,2], stdDataLMx[1,7], stdDataLMx[1,13], stdDataLMx[1,3], stdDataLMx[1,8]),
  '40%' =c(stdDataLMx[2,12], stdDataLMx[2,1], stdDataLMx[2,2], stdDataLMx[2,7], stdDataLMx[2,13], stdDataLMx[2,3], stdDataLMx[2,8]),
  '70%' = c(stdDataLMx[3,12], stdDataLMx[3,1], stdDataLMx[3,2], stdDataLMx[3,7], stdDataLMx[3,13], stdDataLMx[3,3], stdDataLMx[3,8]),
  '100%' = c(stdDataLMx[4,12], stdDataLMx[4,1], stdDataLMx[4,2], stdDataLMx[4,7], stdDataLMx[4,13], stdDataLMx[4,3], stdDataLMx[4,8])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -7L))

k=t/sqrt(nparticipants)
landing.ci.x <- structure(list(
  '1%'= c(k*stdDataLMx[1,12], k*stdDataLMx[1,1], k*stdDataLMx[1,2], k*stdDataLMx[1,7], k*stdDataLMx[1,13], k*stdDataLMx[1,3], k*stdDataLMx[1,8]),
  '40%' =c(k*stdDataLMx[2,12], k*stdDataLMx[2,1], k*stdDataLMx[2,2], k*stdDataLMx[2,7], k*stdDataLMx[2,13], k*stdDataLMx[2,3], k*stdDataLMx[2,8]),
  '70%' = c(k*stdDataLMx[3,12], k*stdDataLMx[3,1], k*stdDataLMx[3,2], k*stdDataLMx[3,7], k*stdDataLMx[3,13], k*stdDataLMx[3,3], k*stdDataLMx[3,8]),
  '100%' = c(k*stdDataLMx[4,12], k*stdDataLMx[4,1], k*stdDataLMx[4,2], k*stdDataLMx[4,7], k*stdDataLMx[4,13], k*stdDataLMx[4,3], k*stdDataLMx[4,8])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -7L))

op = par(mar=c(4,5,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(-landing.means.x), main="Landing Linear Momentum (AP)",
               ylab=expression(kg %.% m %.% s^-1 %.% BW^-1),
               xlim=c(0,35),ylim=c(-0.002,0.07),
               col=c("red","green","blue","yellow","purple","azure2","cadetblue"),
               legend = c( 'back','pelvis','thigh_r','thigh_l','head','leg_r','leg_l'), 
               las=2, cex.names = 1, beside=TRUE, args.legend = list(x=35,horiz=TRUE)) #beside=TRUE,xlab="joint",
rm(op)


xx=as.matrix(-landing.means.x)
er=as.matrix(landing.stds.x)
erci=as.matrix(landing.ci.x)
arrows(barx,xx+erci, barx,xx, angle=90, code=3, length=0.05)
arrows(barx,xx-erci, barx,xx, angle=90, code=3, length=0.05)


## vertical
simp_names = list('5%','20%','40%','100%')
landing.means.z <- structure(list(
  '5%'= c(meanDataLMz[1,12], meanDataLMz[1,1], meanDataLMz[1,13], meanDataLMz[1,14], meanDataLMz[1,20]),
  '20%' =c(meanDataLMz[2,12], meanDataLMz[2,1], meanDataLMz[2,13], meanDataLMz[2,14], meanDataLMz[2,20]),
  '40%' = c(meanDataLMz[3,12], meanDataLMz[3,1], meanDataLMz[3,13], meanDataLMz[3,14], meanDataLMz[3,20]),
  '100%' = c(meanDataLMz[4,12], meanDataLMz[4,1], meanDataLMz[4,13], meanDataLMz[4,14], meanDataLMz[4,20])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -5L))

#
landing.stds.z <- structure(list(
  '5%'= c(stdDataLMz[1,12], stdDataLMz[1,1], stdDataLMz[1,13], stdDataLMz[1,14], stdDataLMz[1,20]),
  '20%' =c(stdDataLMz[2,12], stdDataLMz[2,1], stdDataLMz[2,13], stdDataLMz[2,14], stdDataLMz[2,20]),
  '40%' = c(stdDataLMz[3,12], stdDataLMz[3,1], stdDataLMz[3,13], stdDataLMz[3,14], stdDataLMz[3,20]),
  '100%' = c(stdDataLMz[4,12], stdDataLMz[4,1], stdDataLMz[4,13], stdDataLMz[4,14], stdDataLMz[4,20])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -5L))

k=t/sqrt(nparticipants)
landing.ci.z <- structure(list(
  '5%'= c(k*stdDataLMz[1,12], k*stdDataLMz[1,1], k*stdDataLMz[1,13], k*stdDataLMz[1,14], k*stdDataLMz[1,20]),
  '20%' =c(k*stdDataLMz[2,12], k*stdDataLMz[2,1], k*stdDataLMz[2,13], k*stdDataLMz[2,14], k*stdDataLMz[2,20]),
  '40%' = c(k*stdDataLMz[3,12], k*stdDataLMz[3,1], k*stdDataLMz[3,13], k*stdDataLMz[3,14], k*stdDataLMz[3,20]),
  '100%' = c(k*stdDataLMz[4,12], k*stdDataLMz[4,1], k*stdDataLMz[4,13], k*stdDataLMz[4,14], k*stdDataLMz[4,20])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -5L))

op = par(mar=c(4,5,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(landing.means.z), main="Landing Linear Momentum (V)",
               ylab=expression(kg %.% m %.% s^-1 %.% BW^-1),
               xlim=c(0,25),ylim=c(-0.15,0),
               col=c("red","green","blue","yellow","purple"),
               legend = c( "back","pelvis", "head", "arm_r","arm_l"),  
               las=2, cex.names = 1, beside=TRUE,args.legend = list(x=25, y=-0.1,horiz=TRUE)) #beside=TRUE,xlab="joint",
rm(op)


xx=as.matrix(landing.means.z)
er=as.matrix(landing.stds.z)
erci=as.matrix(landing.ci.z)
arrows(barx,xx+erci, barx,xx, angle=90, code=3, length=0.05)
arrows(barx,xx-erci, barx,xx, angle=90, code=3, length=0.05)



## sagital torque
# contribute: pelvis, thighs, legs, back, head
simp_names = list('5%','20%','40%','100%')
landing.means.yy <- structure(list(
  '5%'= c(meanDataAMy[1,12], meanDataAMy[1,1], meanDataAMy[1,2], meanDataAMy[1,7], meanDataAMy[1,13], meanDataAMy[1,3], meanDataAMy[1,8]),
  '20%' =c(meanDataAMy[2,12], meanDataAMy[2,1], meanDataAMy[2,2], meanDataAMy[2,7], meanDataAMy[2,13], meanDataAMy[2,3], meanDataAMy[2,8]),
  '40%' = c(meanDataAMy[3,12], meanDataAMy[3,1], meanDataAMy[3,2], meanDataAMy[3,7], meanDataAMy[3,13], meanDataAMy[3,3], meanDataAMy[3,8]),
  '100%' = c(meanDataAMy[4,12], meanDataAMy[4,1], meanDataAMy[4,2], meanDataAMy[4,7], meanDataAMy[4,13], meanDataAMy[4,3], meanDataAMy[4,8])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -7L))

#
landing.stds.yy <- structure(list(
  '5%'= c(stdDataAMy[1,12], stdDataAMy[1,1], stdDataAMy[1,2], stdDataAMy[1,7], stdDataAMy[1,13], stdDataAMy[1,3], stdDataAMy[1,8]),
  '20%' =c(stdDataAMy[2,12], stdDataAMy[2,1], stdDataAMy[2,2], stdDataAMy[2,7], stdDataAMy[2,13], stdDataAMy[2,3], stdDataAMy[2,8]),
  '40%' = c(stdDataAMy[3,12], stdDataAMy[3,1], stdDataAMy[3,2], stdDataAMy[3,7], stdDataAMy[3,13], stdDataAMy[3,3], stdDataAMy[3,8]),
  '100%' = c(stdDataAMy[4,12], stdDataAMy[4,1], stdDataAMy[4,2], stdDataAMy[4,7], stdDataAMy[4,13], stdDataAMy[4,3], stdDataAMy[4,8])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -7L))

k=t/sqrt(nparticipants)
landing.ci.yy <- structure(list(
  '5%'= c(k*stdDataAMy[1,12], k*stdDataAMy[1,1], k*stdDataAMy[1,2], k*stdDataAMy[1,7], k*stdDataAMy[1,13], k*stdDataAMy[1,3], k*stdDataAMy[1,8]),
  '20%' =c(k*stdDataAMy[2,12], k*stdDataAMy[2,1], k*stdDataAMy[2,2], k*stdDataAMy[2,7], k*stdDataAMy[2,13], k*stdDataAMy[2,3], k*stdDataAMy[2,8]),
  '40%' = c(k*stdDataAMy[3,12], k*stdDataAMy[3,1], k*stdDataAMy[3,2], k*stdDataAMy[3,7], k*stdDataAMy[3,13], k*stdDataAMy[3,3], k*stdDataAMy[3,8]),
  '100%' = c(k*stdDataAMy[4,12], k*stdDataAMy[4,1], k*stdDataAMy[4,2], k*stdDataAMy[4,7], k*stdDataAMy[4,13], k*stdDataAMy[4,3], k*stdDataAMy[4,8])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -7L))

op = par(mar=c(5,5,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(-landing.means.yy), 
               ylab=expression(kg %.% m^2 %.% s^-1 %.% BW^-1 %.% H^-1),
               xlim=c(0,35),ylim=c(-0.005, 0.013),
               col=c("red","green","blue","yellow","purple","azure2","cadetblue"),
               legend = c( 'back','pelvis','thigh_r','thigh_l','head','leg_r','leg_l'),  
               las=2, cex.names = 1, beside=TRUE,args.legend = list(x=35,horiz=TRUE)) #beside=TRUE,xlab="joint",main="Landing Angular Momentum in Sagittal Plane",
rm(op)

xx=as.matrix(-landing.means.yy)
er=as.matrix(landing.stds.yy)
erci=as.matrix(landing.ci.yy)
arrows(barx,xx+erci, barx,xx, angle=90, code=3, length=0.05)
arrows(barx,xx-erci, barx,xx, angle=90, code=3, length=0.05)


#pairwise.t.test(IMPULSE$Momenta, IMPULSE$Phase, p.adj = "bonf",paired=TRUE)
#pairwise.t.test(IMPULSE$Momenta, IMPULSE$Coordinate, p.adj = "bonf",paired=TRUE)
#pairwise.t.test(IMPULSE$Momenta, IMPULSE$Segment, p.adj = "bonf",paired=TRUE)


