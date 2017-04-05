# Analysis of Variances from uncontrolled manifold and its orthogonal space
rm(list = ls())



# ------------------------------------------------------------------------
#    JUMP IMPULSE
# Task 1: impulsion through antero-posterior and vertical force
# Task 2: impulsion through antero posterior angular momentum (around M-L axis at the center of mass)
# ------------------------------------------------------------------------
p='/galo/devel/gepetto/motorg/motorog/' #home
#p='/local/gmaldona/devel/motorg/motorog/' #lab
nparticipants = 5
ddl=nparticipants-1
t = qt(.975,ddl)
names<- c('pelvis','hip_r','knee_r','ankle_r','subtalar_r','mtp_r','hip_l','knee_l','ankle_l','subtalar_l',
          'mtp_l','back','neck','acromial_r','elbow_r','radioulnar_r','radius_lunate_r','lunate_hand_r','fingers_r',
          'acromial_l','elbow_l','radioulnar_l','radius_lunate_l','lunate_hand_l','fingers_l')

# ---------------------- Read the data -----------------------------------
pathName = paste(p,'TableMomentaJump.csv',sep="")
IMPULSE = read.csv(pathName,
                       header = FALSE, 
                       col.names = list('Participant', 'Phase', 'Task', 'Coordinate' ,'Momenta'))
IMPULSE$Participant<-as.factor(IMPULSE$Participant)
IMPULSE$Phase<-as.factor(IMPULSE$Phase)
IMPULSE$Task<-as.factor(IMPULSE$Task)
IMPULSE$Coordinate<-as.factor(IMPULSE$Coordinate)


boxplot(IMPULSE$Momenta[IMPULSE$Task=="1" & IMPULSE$Phase=="0"] ~ IMPULSE$Coordinate[IMPULSE$Task=="1" & IMPULSE$Phase=="0"]) 

aovstats <-aov(IMPULSE$Momenta ~ 
                 (IMPULSE$Task+IMPULSE$Phase+IMPULSE$Coordinate) + 
                 Error(IMPULSE$Participant  / (IMPULSE$Task+IMPULSE$Phase+IMPULSE$Coordinate)), 
               data = IMPULSE)
summary(aovstats)
# joints are different
# phases are different
# joints are different
pairwise.t.test(IMPULSE$Momenta, IMPULSE$Task, p.adj = "bonf",paired=TRUE)
pairwise.t.test(IMPULSE$Momenta, IMPULSE$Phase, p.adj = "bonf",paired=TRUE)
pairwise.t.test(IMPULSE$Momenta, IMPULSE$Coordinate, p.adj = "bonf",paired=TRUE)

# ----------------------- Means - Std - Confidence Interval --------------------------
pathName = paste(p,'means/JumpLM.csv',sep="")
meanDataLM = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'means/JumpAM.csv',sep="")
meanDataAM = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'std/JumpLM.csv',sep="")
stdDataLM = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'std/JumpAM.csv',sep="")
stdDataAM = read.csv(pathName, header = FALSE, col.names = names)

jump.means <- structure(list('pelvis'=c(meanDataLM[1,1], meanDataLM[2,1], meanDataLM[3,1], meanDataLM[4,1]),
                             'hip_r'=c(meanDataLM[1,2], meanDataLM[2,2], meanDataLM[3,2], meanDataLM[4,2]),
                             'knee_r'=c(meanDataLM[1,3], meanDataLM[2,3], meanDataLM[3,3], meanDataLM[4,3]),
                             'ankle_r'=c(meanDataLM[1,4], meanDataLM[2,4], meanDataLM[3,4], meanDataLM[4,4]),
                             'subtalar_r'=c(meanDataLM[1,5], meanDataLM[2,5], meanDataLM[3,5], meanDataLM[4,5]),
                             'mtp_r'=c(meanDataLM[1,6], meanDataLM[2,6], meanDataLM[3,6], meanDataLM[4,6]),
                             'hip_l'=c(meanDataLM[1,7], meanDataLM[2,7], meanDataLM[3,7], meanDataLM[4,7]),
                             'knee_l'=c(meanDataLM[1,8], meanDataLM[2,8], meanDataLM[3,8], meanDataLM[4,8]),
                             'ankle_l'=c(meanDataLM[1,9], meanDataLM[2,9], meanDataLM[3,9], meanDataLM[4,9]),
                             'subtalar_l'=c(meanDataLM[1,10], meanDataLM[2,10], meanDataLM[3,10], meanDataLM[4,10]),
                             'mtp_l'=c(meanDataLM[1,11], meanDataLM[2,11], meanDataLM[3,11], meanDataLM[4,11]),
                             'back'=c(meanDataLM[1,12], meanDataLM[2,12], meanDataLM[3,12], meanDataLM[4,12]),
                             'neck'=c(meanDataLM[1,13], meanDataLM[2,13], meanDataLM[3,13], meanDataLM[4,13]),
                             'acromial_r'=c(meanDataLM[1,14], meanDataLM[2,14], meanDataLM[3,14], meanDataLM[4,14]),
                             'elbow_r'=c(meanDataLM[1,15], meanDataLM[2,15], meanDataLM[3,15], meanDataLM[4,15]),
                             'radioulnar_r'=c(meanDataLM[1,16], meanDataLM[2,16], meanDataLM[3,16], meanDataLM[4,16]),
                             'radius_lunate_r'=c(meanDataLM[1,17], meanDataLM[2,17], meanDataLM[3,17], meanDataLM[4,17]),
                             'lunate_hand_r'=c(meanDataLM[1,18], meanDataLM[2,18], meanDataLM[3,18], meanDataLM[4,18]),
                             'fingers_r'=c(meanDataLM[1,19], meanDataLM[2,19], meanDataLM[3,19], meanDataLM[4,19]),
                             'acromial_l'=c(meanDataLM[1,20], meanDataLM[2,20], meanDataLM[3,20], meanDataLM[4,20]),
                             'elbow_l'=c(meanDataLM[1,21], meanDataLM[2,21], meanDataLM[3,21], meanDataLM[4,21]),
                             'radioulnar_l'=c(meanDataLM[1,22], meanDataLM[2,22], meanDataLM[3,22], meanDataLM[4,22]),
                             'radius_lunate_l'=c(meanDataLM[1,23], meanDataLM[2,23], meanDataLM[3,23], meanDataLM[4,23]),
                             'lunate_hand_l'=c(meanDataLM[1,24], meanDataLM[2,24], meanDataLM[3,24], meanDataLM[4,24]),
                             'fingers_l'=c(meanDataLM[1,25], meanDataLM[2,25], meanDataLM[3,25], meanDataLM[4,25])
                              ), 
                        .Names = names, 
                        class = "data.frame", row.names = c(NA, -4L))

#
jump.stds <- structure(list('pelvis'=c(stdDataLM[1,1], stdDataLM[2,1], stdDataLM[3,1], stdDataLM[4,1]),
                             'hip_r'=c(stdDataLM[1,2], stdDataLM[2,2], stdDataLM[3,2], stdDataLM[4,2]),
                             'knee_r'=c(stdDataLM[1,3], stdDataLM[2,3], stdDataLM[3,3], stdDataLM[4,3]),
                             'ankle_r'=c(stdDataLM[1,4], stdDataLM[2,4], stdDataLM[3,4], stdDataLM[4,4]),
                             'subtalar_r'=c(stdDataLM[1,5], stdDataLM[2,5], stdDataLM[3,5], stdDataLM[4,5]),
                             'mtp_r'=c(stdDataLM[1,6], stdDataLM[2,6], stdDataLM[3,6], stdDataLM[4,6]),
                             'hip_l'=c(stdDataLM[1,7], stdDataLM[2,7], stdDataLM[3,7], stdDataLM[4,7]),
                             'knee_l'=c(stdDataLM[1,8], stdDataLM[2,8], stdDataLM[3,8], stdDataLM[4,8]),
                             'ankle_l'=c(stdDataLM[1,9], stdDataLM[2,9], stdDataLM[3,9], stdDataLM[4,9]),
                             'subtalar_l'=c(stdDataLM[1,10], stdDataLM[2,10], stdDataLM[3,10], stdDataLM[4,10]),
                             'mtp_l'=c(stdDataLM[1,11], stdDataLM[2,11], stdDataLM[3,11], stdDataLM[4,11]),
                             'back'=c(stdDataLM[1,12], stdDataLM[2,12], stdDataLM[3,12], stdDataLM[4,12]),
                             'neck'=c(stdDataLM[1,13], stdDataLM[2,13], stdDataLM[3,13], stdDataLM[4,13]),
                             'acromial_r'=c(stdDataLM[1,14], stdDataLM[2,14], stdDataLM[3,14], stdDataLM[4,14]),
                             'elbow_r'=c(stdDataLM[1,15], stdDataLM[2,15], stdDataLM[3,15], stdDataLM[4,15]),
                             'radioulnar_r'=c(stdDataLM[1,16], stdDataLM[2,16], stdDataLM[3,16], stdDataLM[4,16]),
                             'radius_lunate_r'=c(stdDataLM[1,17], stdDataLM[2,17], stdDataLM[3,17], stdDataLM[4,17]),
                             'lunate_hand_r'=c(stdDataLM[1,18], stdDataLM[2,18], stdDataLM[3,18], stdDataLM[4,18]),
                             'fingers_r'=c(stdDataLM[1,19], stdDataLM[2,19], stdDataLM[3,19], stdDataLM[4,19]),
                             'acromial_l'=c(stdDataLM[1,20], stdDataLM[2,20], stdDataLM[3,20], stdDataLM[4,20]),
                             'elbow_l'=c(stdDataLM[1,21], stdDataLM[2,21], stdDataLM[3,21], stdDataLM[4,21]),
                             'radioulnar_l'=c(stdDataLM[1,22], stdDataLM[2,22], stdDataLM[3,22], stdDataLM[4,22]),
                             'radius_lunate_l'=c(stdDataLM[1,23], stdDataLM[2,23], stdDataLM[3,23], stdDataLM[4,23]),
                             'lunate_hand_l'=c(stdDataLM[1,24], stdDataLM[2,24], stdDataLM[3,24], stdDataLM[4,24]),
                             'fingers_l'=c(stdDataLM[1,25], stdDataLM[2,25], stdDataLM[3,25], stdDataLM[4,25])
                              ), 
                          .Names = names, 
                          class = "data.frame", row.names = c(NA, -4L))

jump.ci <- structure(list('pelvis'=c(t*stdDataLM[1,1]/sqrt(nparticipants), t*stdDataLM[2,1]/sqrt(nparticipants), t*stdDataLM[3,1]/sqrt(nparticipants), t*stdDataLM[4,1]/sqrt(nparticipants)),
                            'hip_r'=c(t*stdDataLM[1,2]/sqrt(nparticipants), t*stdDataLM[2,2]/sqrt(nparticipants), t*stdDataLM[3,2]/sqrt(nparticipants), t*stdDataLM[4,2]/sqrt(nparticipants)),
                            'knee_r'=c(t*stdDataLM[1,3]/sqrt(nparticipants), t*stdDataLM[2,3]/sqrt(nparticipants), t*stdDataLM[3,3]/sqrt(nparticipants), t*stdDataLM[4,3]/sqrt(nparticipants)),
                            'ankle_r'=c(t*stdDataLM[1,4]/sqrt(nparticipants), t*stdDataLM[2,4]/sqrt(nparticipants), t*stdDataLM[3,4]/sqrt(nparticipants), t*stdDataLM[4,4]/sqrt(nparticipants)),
                            'subtalar_r'=c(t*stdDataLM[1,5]/sqrt(nparticipants), t*stdDataLM[2,5]/sqrt(nparticipants), t*stdDataLM[3,5]/sqrt(nparticipants), t*stdDataLM[4,5]/sqrt(nparticipants)),
                            'mtp_r'=c(t*stdDataLM[1,6]/sqrt(nparticipants), t*stdDataLM[2,6]/sqrt(nparticipants), t*stdDataLM[3,6]/sqrt(nparticipants), t*stdDataLM[4,6]/sqrt(nparticipants)),
                            'hip_l'=c(t*stdDataLM[1,7]/sqrt(nparticipants), t*stdDataLM[2,7]/sqrt(nparticipants), t*stdDataLM[3,7]/sqrt(nparticipants), t*stdDataLM[4,7]/sqrt(nparticipants)),
                            'knee_l'=c(t*stdDataLM[1,8]/sqrt(nparticipants), t*stdDataLM[2,8]/sqrt(nparticipants), t*stdDataLM[3,8]/sqrt(nparticipants), t*stdDataLM[4,8]/sqrt(nparticipants)),
                            'ankle_l'=c(t*stdDataLM[1,9]/sqrt(nparticipants), t*stdDataLM[2,9]/sqrt(nparticipants), t*stdDataLM[3,9]/sqrt(nparticipants), t*stdDataLM[4,9]/sqrt(nparticipants)),
                            'subtalar_l'=c(t*stdDataLM[1,10]/sqrt(nparticipants), t*stdDataLM[2,10]/sqrt(nparticipants), t*stdDataLM[3,10]/sqrt(nparticipants), t*stdDataLM[4,10]/sqrt(nparticipants)),
                            'mtp_l'=c(t*stdDataLM[1,11]/sqrt(nparticipants), t*stdDataLM[2,11]/sqrt(nparticipants), t*stdDataLM[3,11]/sqrt(nparticipants), t*stdDataLM[4,11]/sqrt(nparticipants)),
                            'back'=c(t*stdDataLM[1,12]/sqrt(nparticipants), t*stdDataLM[2,12]/sqrt(nparticipants), t*stdDataLM[3,12]/sqrt(nparticipants), t*stdDataLM[4,12]/sqrt(nparticipants)),
                            'neck'=c(t*stdDataLM[1,13]/sqrt(nparticipants), t*stdDataLM[2,13]/sqrt(nparticipants), t*stdDataLM[3,13]/sqrt(nparticipants), t*stdDataLM[4,13]/sqrt(nparticipants)),
                            'acromial_r'=c(t*stdDataLM[1,14]/sqrt(nparticipants), t*stdDataLM[2,14]/sqrt(nparticipants), t*stdDataLM[3,14]/sqrt(nparticipants), t*stdDataLM[4,14]/sqrt(nparticipants)),
                            'elbow_r'=c(t*stdDataLM[1,15]/sqrt(nparticipants), t*stdDataLM[2,15]/sqrt(nparticipants), t*stdDataLM[3,15]/sqrt(nparticipants), t*stdDataLM[4,15]/sqrt(nparticipants)),
                            'radioulnar_r'=c(t*stdDataLM[1,16]/sqrt(nparticipants), t*stdDataLM[2,16]/sqrt(nparticipants), t*stdDataLM[3,16]/sqrt(nparticipants), t*stdDataLM[4,16]/sqrt(nparticipants)),
                            'radius_lunate_r'=c(t*stdDataLM[1,17]/sqrt(nparticipants), t*stdDataLM[2,17]/sqrt(nparticipants), t*stdDataLM[3,17]/sqrt(nparticipants), t*stdDataLM[4,17]/sqrt(nparticipants)),
                            'lunate_hand_r'=c(t*stdDataLM[1,18]/sqrt(nparticipants), t*stdDataLM[2,18]/sqrt(nparticipants), t*stdDataLM[3,18]/sqrt(nparticipants), t*stdDataLM[4,18]/sqrt(nparticipants)),
                            'fingers_r'=c(t*stdDataLM[1,19]/sqrt(nparticipants), t*stdDataLM[2,19]/sqrt(nparticipants), t*stdDataLM[3,19]/sqrt(nparticipants), t*stdDataLM[4,19]/sqrt(nparticipants)),
                            'acromial_l'=c(t*stdDataLM[1,20]/sqrt(nparticipants), t*stdDataLM[2,20]/sqrt(nparticipants), t*stdDataLM[3,20]/sqrt(nparticipants), t*stdDataLM[4,20]/sqrt(nparticipants)),
                            'elbow_l'=c(t*stdDataLM[1,21]/sqrt(nparticipants), t*stdDataLM[2,21]/sqrt(nparticipants), t*stdDataLM[3,21]/sqrt(nparticipants), t*stdDataLM[4,21]/sqrt(nparticipants)),
                            'radioulnar_l'=c(t*stdDataLM[1,22]/sqrt(nparticipants), t*stdDataLM[2,22]/sqrt(nparticipants), t*stdDataLM[3,22]/sqrt(nparticipants), t*stdDataLM[4,22]/sqrt(nparticipants)),
                            'radius_lunate_l'=c(t*stdDataLM[1,23]/sqrt(nparticipants), t*stdDataLM[2,23]/sqrt(nparticipants), t*stdDataLM[3,23]/sqrt(nparticipants), t*stdDataLM[4,23]/sqrt(nparticipants)),
                            'lunate_hand_l'=c(t*stdDataLM[1,24]/sqrt(nparticipants), t*stdDataLM[2,24]/sqrt(nparticipants), t*stdDataLM[3,24]/sqrt(nparticipants), t*stdDataLM[4,24]/sqrt(nparticipants)),
                            'fingers_l'=c(t*stdDataLM[1,25]/sqrt(nparticipants), t*stdDataLM[2,25]/sqrt(nparticipants), t*stdDataLM[3,25]/sqrt(nparticipants), t*stdDataLM[4,25]/sqrt(nparticipants))
                            ), 
                            .Names = names, 
                            class = "data.frame", row.names = c(NA, -4L))


barx = barplot(as.matrix(jump.means), main="Jump Linear Momentum",
               xlab="joint", ylab="kg.m/s",
               xlim=c(0,115),ylim=c(-20,50),
               col=c("red","green","blue","yellow"),
               legend = c( "1%","40%", "70%", "100%"), beside=TRUE, las=2)

xx=as.matrix(jump.means)
er=as.matrix(jump.stds)
erci=as.matrix(jump.ci)
arrows(barx,xx+erci, barx,xx, angle=90, code=3, length=0.05)
arrows(barx,xx-erci, barx,xx, angle=90, code=3, length=0.05)

# unconmment to plot with SD
#arrows(barx,xx+er, barx,xx, angle=90, code=3, length=0.05)

pairwise.t.test(IMPULSE$Momenta[IMPULSE$Task=="1" & IMPULSE$Phase=="0"], IMPULSE$Coordinate, p.adj = "bonf",paired=TRUE)

#1%
barx = barplot(as.matrix(jump.means)[1,], main="Jump Linear Momentum 1%",
               xlab="joint", ylab="kg.m/s",
               xlim=c(0,30),ylim=c(-20,50),
               col=c("blue"),
               beside=TRUE, las=2)
xx=as.matrix(jump.means)[1,]
er=as.matrix(jump.stds)[1,]
erci=as.matrix(jump.ci)[1,]
arrows(barx,xx+erci, barx,xx, angle=90, code=3, length=0.05)
arrows(barx,xx-erci, barx,xx, angle=90, code=3, length=0.05)

#40%
barx = barplot(as.matrix(jump.means)[2,], main="Jump Linear Momentum 40%",
               xlab="joint", ylab="kg.m/s",
               xlim=c(0,30),ylim=c(-20,50),
               col=c("blue"),
               beside=TRUE, las=2)
xx=as.matrix(jump.means)[2,]
er=as.matrix(jump.stds)[2,]
erci=as.matrix(jump.ci)[2,]
arrows(barx,xx+erci, barx,xx, angle=90, code=3, length=0.05)
arrows(barx,xx-erci, barx,xx, angle=90, code=3, length=0.05)

#70%
barx = barplot(as.matrix(jump.means)[3,], main="Jump Linear Momentum 70%",
               xlab="joint", ylab="kg.m/s",
               xlim=c(0,30),ylim=c(-20,50),
               col=c("blue"),
               beside=TRUE, las=2)
xx=as.matrix(jump.means)[3,]
er=as.matrix(jump.stds)[3,]
erci=as.matrix(jump.ci)[3,]
arrows(barx,xx+erci, barx,xx, angle=90, code=3, length=0.05)
arrows(barx,xx-erci, barx,xx, angle=90, code=3, length=0.05)

#99%
barx = barplot(as.matrix(jump.means)[4,], main="Jump Linear Momentum 100%",
               xlab="joint", ylab="kg.m/s",
               xlim=c(0,30),ylim=c(-20,50),
               col=c("blue"),
               beside=TRUE, las=2)
xx=as.matrix(jump.means)[4,]
er=as.matrix(jump.stds)[4,]
erci=as.matrix(jump.ci)[4,]
arrows(barx,xx+erci, barx,xx, angle=90, code=3, length=0.05)
arrows(barx,xx-erci, barx,xx, angle=90, code=3, length=0.05)