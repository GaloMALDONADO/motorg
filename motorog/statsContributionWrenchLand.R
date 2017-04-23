# Analysis of Variances from uncontrolled manifold and its orthogonal space
rm(list = ls())


# ------------------------------------------------------------------------
p='/galo/devel/gepetto/motorg/motorog/tables/momenta/' #home
#p='/local/gmaldona/devel/motorg/motorog/tables/momenta/' #lab
nparticipants = 5
ddl=nparticipants-1
t = qt(.975,ddl)
names<- c('pelvis','thigh_r','leg_r','foot_flex_r','foot_r','toes_r','thigh_l','leg_l','foot_flex_l','foot_l',
          'toes_l','back','head','upper_arm_r','forearm_flex_r','forearm_rot_r','hand_deviation_r','hand_flex_r','fingers_r',
          'upper_arm_l','forearm_flex_l','forearm_rot_l','hand_deviation_l','hand_flex_l','fingers_l')

# ---------------------- Read the data -----------------------------------

# ----------------------- Means - Std - Confidence Interval --------------------------
pathName = paste(p,'mean/LandFLMx.csv',sep="")
meanDataLMx = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'mean/LandFLMy.csv',sep="")
meanDataLMy = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'mean/LandFLMz.csv',sep="")
meanDataLMz = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'std/LandFLMx.csv',sep="")
stdDataLMx = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'std/LandFLMy.csv',sep="")
stdDataLMy = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'std/LandFLMz.csv',sep="")
stdDataLMz = read.csv(pathName, header = FALSE, col.names = names)

pathName = paste(p,'mean/LandTAMx.csv',sep="")
meanDataAMx = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'mean/LandTAMy.csv',sep="")
meanDataAMy = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'mean/LandTAMz.csv',sep="")
meanDataAMz = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'std/LandTAMx.csv',sep="")
stdDataAMx = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'std/LandTAMy.csv',sep="")
stdDataAMy = read.csv(pathName, header = FALSE, col.names = names)
pathName = paste(p,'std/LandTAMz.csv',sep="")
stdDataAMz = read.csv(pathName, header = FALSE, col.names = names)



# MEANS
# Linear Momentum x
land.means.x <- structure(list('pelvis'=c(meanDataLMx[1,1], meanDataLMx[2,1], meanDataLMx[3,1], meanDataLMx[4,1], meanDataLMx[5,1]),
                               'thigh_r'=c(meanDataLMx[1,2], meanDataLMx[2,2], meanDataLMx[3,2], meanDataLMx[4,2], meanDataLMx[5,2]),
                               'leg_r'=c(meanDataLMx[1,3], meanDataLMx[2,3], meanDataLMx[3,3], meanDataLMx[4,3], meanDataLMx[5,3]),
                               'foot_flex_r'=c(meanDataLMx[1,4], meanDataLMx[2,4], meanDataLMx[3,4], meanDataLMx[4,4], meanDataLMx[5,4]),
                               'foot_r'=c(meanDataLMx[1,5], meanDataLMx[2,5], meanDataLMx[3,5], meanDataLMx[4,5], meanDataLMx[5,5]),
                               'toes_r'=c(meanDataLMx[1,6], meanDataLMx[2,6], meanDataLMx[3,6], meanDataLMx[4,6], meanDataLMx[5,6]),
                               'thigh_l'=c(meanDataLMx[1,7], meanDataLMx[2,7], meanDataLMx[3,7], meanDataLMx[4,7], meanDataLMx[5,7]),
                               'leg_l'=c(meanDataLMx[1,8], meanDataLMx[2,8], meanDataLMx[3,8], meanDataLMx[4,8], meanDataLMx[5,8]),
                               'foot_flex_l'=c(meanDataLMx[1,9], meanDataLMx[2,9], meanDataLMx[3,9], meanDataLMx[4,9], meanDataLMx[5,9]),
                               'foot_l'=c(meanDataLMx[1,10], meanDataLMx[2,10], meanDataLMx[3,10], meanDataLMx[4,10], meanDataLMx[5,10]),
                               'toes_l'=c(meanDataLMx[1,11], meanDataLMx[2,11], meanDataLMx[3,11], meanDataLMx[4,11], meanDataLMx[5,11]),
                               'back'=c(meanDataLMx[1,12], meanDataLMx[2,12], meanDataLMx[3,12], meanDataLMx[4,12], meanDataLMx[5,12]),
                               'head'=c(meanDataLMx[1,13], meanDataLMx[2,13], meanDataLMx[3,13], meanDataLMx[4,13], meanDataLMx[5,13]),
                               'upper_arm_r'=c(meanDataLMx[1,14], meanDataLMx[2,14], meanDataLMx[3,14], meanDataLMx[4,14], meanDataLMx[5,14]),
                               'forearm_flex_r'=c(meanDataLMx[1,15], meanDataLMx[2,15], meanDataLMx[3,15], meanDataLMx[4,15], meanDataLMx[5,15]),
                               'forearm_rot_r'=c(meanDataLMx[1,16], meanDataLMx[2,16], meanDataLMx[3,16], meanDataLMx[4,16], meanDataLMx[5,16]),
                               'hand_deviation_r'=c(meanDataLMx[1,17], meanDataLMx[2,17], meanDataLMx[3,17], meanDataLMx[4,17], meanDataLMx[5,17]),
                               'hand_flex_r'=c(meanDataLMx[1,18], meanDataLMx[2,18], meanDataLMx[3,18], meanDataLMx[4,18], meanDataLMx[5,18]),
                               'fingers_r'=c(meanDataLMx[1,19], meanDataLMx[2,19], meanDataLMx[3,19], meanDataLMx[4,19], meanDataLMx[5,19]),
                               'upper_arm_l'=c(meanDataLMx[1,20], meanDataLMx[2,20], meanDataLMx[3,20], meanDataLMx[4,20], meanDataLMx[5,20]),
                               'forearm_flex_l'=c(meanDataLMx[1,21], meanDataLMx[2,21], meanDataLMx[3,21], meanDataLMx[4,21], meanDataLMx[5,21]),
                               'forearm_rot_l'=c(meanDataLMx[1,22], meanDataLMx[2,22], meanDataLMx[3,22], meanDataLMx[4,22], meanDataLMx[5,22]),
                               'hand_deviation_l'=c(meanDataLMx[1,23], meanDataLMx[2,23], meanDataLMx[3,23], meanDataLMx[4,23], meanDataLMx[5,23]),
                               'hand_flex_l'=c(meanDataLMx[1,24], meanDataLMx[2,24], meanDataLMx[3,24], meanDataLMx[4,24], meanDataLMx[5,24]),
                               'fingers_l'=c(meanDataLMx[1,25], meanDataLMx[2,25], meanDataLMx[3,25], meanDataLMx[4,25], meanDataLMx[5,25])
), 
.Names = names, 
class = "data.frame", row.names = c(NA, -5L))



# Linear Momentum Y
land.means.y <- structure(list('pelvis'=c(meanDataLMy[1,1], meanDataLMy[2,1], meanDataLMy[3,1], meanDataLMy[4,1], meanDataLMy[5,1]),
                               'thigh_r'=c(meanDataLMy[1,2], meanDataLMy[2,2], meanDataLMy[3,2], meanDataLMy[4,2], meanDataLMy[5,2]),
                               'leg_r'=c(meanDataLMy[1,3], meanDataLMy[2,3], meanDataLMy[3,3], meanDataLMy[4,3], meanDataLMy[5,3]),
                               'foot_flex_r'=c(meanDataLMy[1,4], meanDataLMy[2,4], meanDataLMy[3,4], meanDataLMy[4,4], meanDataLMy[5,4]),
                               'foot_r'=c(meanDataLMy[1,5], meanDataLMy[2,5], meanDataLMy[3,5], meanDataLMy[4,5], meanDataLMy[5,5]),
                               'toes_r'=c(meanDataLMy[1,6], meanDataLMy[2,6], meanDataLMy[3,6], meanDataLMy[4,6], meanDataLMy[5,6]),
                               'thigh_l'=c(meanDataLMy[1,7], meanDataLMy[2,7], meanDataLMy[3,7], meanDataLMy[4,7], meanDataLMy[5,7]),
                               'leg_l'=c(meanDataLMy[1,8], meanDataLMy[2,8], meanDataLMy[3,8], meanDataLMy[4,8], meanDataLMy[5,8]),
                               'foot_flex_l'=c(meanDataLMy[1,9], meanDataLMy[2,9], meanDataLMy[3,9], meanDataLMy[4,9], meanDataLMy[5,9]),
                               'foot_l'=c(meanDataLMy[1,10], meanDataLMy[2,10], meanDataLMy[3,10], meanDataLMy[4,10], meanDataLMy[5,10]),
                               'toes_l'=c(meanDataLMy[1,11], meanDataLMy[2,11], meanDataLMy[3,11], meanDataLMy[4,11], meanDataLMy[5,11]),
                               'back'=c(meanDataLMy[1,12], meanDataLMy[2,12], meanDataLMy[3,12], meanDataLMy[4,12], meanDataLMy[5,12]),
                               'head'=c(meanDataLMy[1,13], meanDataLMy[2,13], meanDataLMy[3,13], meanDataLMy[4,13], meanDataLMy[5,13]),
                               'upper_arm_r'=c(meanDataLMy[1,14], meanDataLMy[2,14], meanDataLMy[3,14], meanDataLMy[4,14], meanDataLMy[5,14]),
                               'forearm_flex_r'=c(meanDataLMy[1,15], meanDataLMy[2,15], meanDataLMy[3,15], meanDataLMy[4,15], meanDataLMy[5,15]),
                               'forearm_rot_r'=c(meanDataLMy[1,16], meanDataLMy[2,16], meanDataLMy[3,16], meanDataLMy[4,16], meanDataLMy[5,16]),
                               'hand_deviation_r'=c(meanDataLMy[1,17], meanDataLMy[2,17], meanDataLMy[3,17], meanDataLMy[4,17], meanDataLMy[5,17]),
                               'hand_flex_r'=c(meanDataLMy[1,18], meanDataLMy[2,18], meanDataLMy[3,18], meanDataLMy[4,18], meanDataLMy[5,18]),
                               'fingers_r'=c(meanDataLMy[1,19], meanDataLMy[2,19], meanDataLMy[3,19], meanDataLMy[4,19], meanDataLMy[5,19]),
                               'upper_arm_l'=c(meanDataLMy[1,20], meanDataLMy[2,20], meanDataLMy[3,20], meanDataLMy[4,20], meanDataLMy[5,20]),
                               'forearm_flex_l'=c(meanDataLMy[1,21], meanDataLMy[2,21], meanDataLMy[3,21], meanDataLMy[4,21], meanDataLMy[5,21]),
                               'forearm_rot_l'=c(meanDataLMy[1,22], meanDataLMy[2,22], meanDataLMy[3,22], meanDataLMy[4,22], meanDataLMy[5,22]),
                               'hand_deviation_l'=c(meanDataLMy[1,23], meanDataLMy[2,23], meanDataLMy[3,23], meanDataLMy[4,23], meanDataLMy[5,23]),
                               'hand_flex_l'=c(meanDataLMy[1,24], meanDataLMy[2,24], meanDataLMy[3,24], meanDataLMy[4,24], meanDataLMy[5,24]),
                               'fingers_l'=c(meanDataLMy[1,25], meanDataLMy[2,25], meanDataLMy[3,25], meanDataLMy[4,25], meanDataLMy[5,25])
), 
.Names = names, 
class = "data.frame", row.names = c(NA, -5L))


# Linear Momentum Z
land.means.z <- structure(list('pelvis'=c(meanDataLMz[1,1], meanDataLMz[2,1], meanDataLMz[3,1], meanDataLMz[4,1], meanDataLMz[5,1]),
                               'thigh_r'=c(meanDataLMz[1,2], meanDataLMz[2,2], meanDataLMz[3,2], meanDataLMz[4,2], meanDataLMz[5,2]),
                               'leg_r'=c(meanDataLMz[1,3], meanDataLMz[2,3], meanDataLMz[3,3], meanDataLMz[4,3], meanDataLMz[5,3]),
                               'foot_flex_r'=c(meanDataLMz[1,4], meanDataLMz[2,4], meanDataLMz[3,4], meanDataLMz[4,4], meanDataLMz[5,4]),
                               'foot_r'=c(meanDataLMz[1,5], meanDataLMz[2,5], meanDataLMz[3,5], meanDataLMz[4,5], meanDataLMz[5,5]),
                               'toes_r'=c(meanDataLMz[1,6], meanDataLMz[2,6], meanDataLMz[3,6], meanDataLMz[4,6], meanDataLMz[5,6]),
                               'thigh_l'=c(meanDataLMz[1,7], meanDataLMz[2,7], meanDataLMz[3,7], meanDataLMz[4,7], meanDataLMz[5,7]),
                               'leg_l'=c(meanDataLMz[1,8], meanDataLMz[2,8], meanDataLMz[3,8], meanDataLMz[4,8], meanDataLMz[5,8]),
                               'foot_flex_l'=c(meanDataLMz[1,9], meanDataLMz[2,9], meanDataLMz[3,9], meanDataLMz[4,9], meanDataLMz[5,9]),
                               'foot_l'=c(meanDataLMz[1,10], meanDataLMz[2,10], meanDataLMz[3,10], meanDataLMz[4,10], meanDataLMz[5,10]),
                               'toes_l'=c(meanDataLMz[1,11], meanDataLMz[2,11], meanDataLMz[3,11], meanDataLMz[4,11], meanDataLMz[5,11]),
                               'back'=c(meanDataLMz[1,12], meanDataLMz[2,12], meanDataLMz[3,12], meanDataLMz[4,12], meanDataLMz[5,12]),
                               'head'=c(meanDataLMz[1,13], meanDataLMz[2,13], meanDataLMz[3,13], meanDataLMz[4,13], meanDataLMz[5,13]),
                               'upper_arm_r'=c(meanDataLMz[1,14], meanDataLMz[2,14], meanDataLMz[3,14], meanDataLMz[4,14], meanDataLMz[5,14]),
                               'forearm_flex_r'=c(meanDataLMz[1,15], meanDataLMz[2,15], meanDataLMz[3,15], meanDataLMz[4,15], meanDataLMz[5,15]),
                               'forearm_rot_r'=c(meanDataLMz[1,16], meanDataLMz[2,16], meanDataLMz[3,16], meanDataLMz[4,16], meanDataLMz[5,16]),
                               'hand_deviation_r'=c(meanDataLMz[1,17], meanDataLMz[2,17], meanDataLMz[3,17], meanDataLMz[4,17], meanDataLMz[5,17]),
                               'hand_flex_r'=c(meanDataLMz[1,18], meanDataLMz[2,18], meanDataLMz[3,18], meanDataLMz[4,18], meanDataLMz[5,18]),
                               'fingers_r'=c(meanDataLMz[1,19], meanDataLMz[2,19], meanDataLMz[3,19], meanDataLMz[4,19], meanDataLMz[5,19]),
                               'upper_arm_l'=c(meanDataLMz[1,20], meanDataLMz[2,20], meanDataLMz[3,20], meanDataLMz[4,20], meanDataLMz[5,20]),
                               'forearm_flex_l'=c(meanDataLMz[1,21], meanDataLMz[2,21], meanDataLMz[3,21], meanDataLMz[4,21], meanDataLMz[5,21]),
                               'forearm_rot_l'=c(meanDataLMz[1,22], meanDataLMz[2,22], meanDataLMz[3,22], meanDataLMz[4,22], meanDataLMz[5,22]),
                               'hand_deviation_l'=c(meanDataLMz[1,23], meanDataLMz[2,23], meanDataLMz[3,23], meanDataLMz[4,23], meanDataLMz[5,23]),
                               'hand_flex_l'=c(meanDataLMz[1,24], meanDataLMz[2,24], meanDataLMz[3,24], meanDataLMz[4,24], meanDataLMz[5,24]),
                               'fingers_l'=c(meanDataLMz[1,25], meanDataLMz[2,25], meanDataLMz[3,25], meanDataLMz[4,25], meanDataLMz[5,25])
), 
.Names = names, 
class = "data.frame", row.names = c(NA, -5L))


# 
# Angular Momentum x
land.means.xx <- structure(list('pelvis'=c(meanDataAMx[1,1], meanDataAMx[2,1], meanDataAMx[3,1], meanDataAMx[4,1], meanDataAMx[5,1]),
                               'thigh_r'=c(meanDataAMx[1,2], meanDataAMx[2,2], meanDataAMx[3,2], meanDataAMx[4,2], meanDataAMx[5,2]),
                               'leg_r'=c(meanDataAMx[1,3], meanDataAMx[2,3], meanDataAMx[3,3], meanDataAMx[4,3], meanDataAMx[5,3]),
                               'foot_flex_r'=c(meanDataAMx[1,4], meanDataAMx[2,4], meanDataAMx[3,4], meanDataAMx[4,4], meanDataAMx[5,4]),
                               'foot_r'=c(meanDataAMx[1,5], meanDataAMx[2,5], meanDataAMx[3,5], meanDataAMx[4,5], meanDataAMx[5,5]),
                               'toes_r'=c(meanDataAMx[1,6], meanDataAMx[2,6], meanDataAMx[3,6], meanDataAMx[4,6], meanDataAMx[5,6]),
                               'thigh_l'=c(meanDataAMx[1,7], meanDataAMx[2,7], meanDataAMx[3,7], meanDataAMx[4,7], meanDataAMx[5,7]),
                               'leg_l'=c(meanDataAMx[1,8], meanDataAMx[2,8], meanDataAMx[3,8], meanDataAMx[4,8], meanDataAMx[5,8]),
                               'foot_flex_l'=c(meanDataAMx[1,9], meanDataAMx[2,9], meanDataAMx[3,9], meanDataAMx[4,9], meanDataAMx[5,9]),
                               'foot_l'=c(meanDataAMx[1,10], meanDataAMx[2,10], meanDataAMx[3,10], meanDataAMx[4,10], meanDataAMx[5,10]),
                               'toes_l'=c(meanDataAMx[1,11], meanDataAMx[2,11], meanDataAMx[3,11], meanDataAMx[4,11], meanDataAMx[5,11]),
                               'back'=c(meanDataAMx[1,12], meanDataAMx[2,12], meanDataAMx[3,12], meanDataAMx[4,12], meanDataAMx[5,12]),
                               'head'=c(meanDataAMx[1,13], meanDataAMx[2,13], meanDataAMx[3,13], meanDataAMx[4,13], meanDataAMx[5,13]),
                               'upper_arm_r'=c(meanDataAMx[1,14], meanDataAMx[2,14], meanDataAMx[3,14], meanDataAMx[4,14], meanDataAMx[5,14]),
                               'forearm_flex_r'=c(meanDataAMx[1,15], meanDataAMx[2,15], meanDataAMx[3,15], meanDataAMx[4,15], meanDataAMx[5,15]),
                               'forearm_rot_r'=c(meanDataAMx[1,16], meanDataAMx[2,16], meanDataAMx[3,16], meanDataAMx[4,16], meanDataAMx[5,16]),
                               'hand_deviation_r'=c(meanDataAMx[1,17], meanDataAMx[2,17], meanDataAMx[3,17], meanDataAMx[4,17], meanDataAMx[5,17]),
                               'hand_flex_r'=c(meanDataAMx[1,18], meanDataAMx[2,18], meanDataAMx[3,18], meanDataAMx[4,18], meanDataAMx[5,18]),
                               'fingers_r'=c(meanDataAMx[1,19], meanDataAMx[2,19], meanDataAMx[3,19], meanDataAMx[4,19], meanDataAMx[5,19]),
                               'upper_arm_l'=c(meanDataAMx[1,20], meanDataAMx[2,20], meanDataAMx[3,20], meanDataAMx[4,20], meanDataAMx[5,20]),
                               'forearm_flex_l'=c(meanDataAMx[1,21], meanDataAMx[2,21], meanDataAMx[3,21], meanDataAMx[4,21], meanDataAMx[5,21]),
                               'forearm_rot_l'=c(meanDataAMx[1,22], meanDataAMx[2,22], meanDataAMx[3,22], meanDataAMx[4,22], meanDataAMx[5,22]),
                               'hand_deviation_l'=c(meanDataAMx[1,23], meanDataAMx[2,23], meanDataAMx[3,23], meanDataAMx[4,23], meanDataAMx[5,23]),
                               'hand_flex_l'=c(meanDataAMx[1,24], meanDataAMx[2,24], meanDataAMx[3,24], meanDataAMx[4,24], meanDataAMx[5,24]),
                               'fingers_l'=c(meanDataAMx[1,25], meanDataAMx[2,25], meanDataAMx[3,25], meanDataAMx[4,25], meanDataAMx[5,25])
), 
.Names = names, 
class = "data.frame", row.names = c(NA, -5L))



# Angular Momentum Y
land.means.yy <- structure(list('pelvis'=c(meanDataAMy[1,1], meanDataAMy[2,1], meanDataAMy[3,1], meanDataAMy[4,1], meanDataAMy[5,1]),
                               'thigh_r'=c(meanDataAMy[1,2], meanDataAMy[2,2], meanDataAMy[3,2], meanDataAMy[4,2], meanDataAMy[5,2]),
                               'leg_r'=c(meanDataAMy[1,3], meanDataAMy[2,3], meanDataAMy[3,3], meanDataAMy[4,3], meanDataAMy[5,3]),
                               'foot_flex_r'=c(meanDataAMy[1,4], meanDataAMy[2,4], meanDataAMy[3,4], meanDataAMy[4,4], meanDataAMy[5,4]),
                               'foot_r'=c(meanDataAMy[1,5], meanDataAMy[2,5], meanDataAMy[3,5], meanDataAMy[4,5], meanDataAMy[5,5]),
                               'toes_r'=c(meanDataAMy[1,6], meanDataAMy[2,6], meanDataAMy[3,6], meanDataAMy[4,6], meanDataAMy[5,6]),
                               'thigh_l'=c(meanDataAMy[1,7], meanDataAMy[2,7], meanDataAMy[3,7], meanDataAMy[4,7], meanDataAMy[5,7]),
                               'leg_l'=c(meanDataAMy[1,8], meanDataAMy[2,8], meanDataAMy[3,8], meanDataAMy[4,8], meanDataAMy[5,8]),
                               'foot_flex_l'=c(meanDataAMy[1,9], meanDataAMy[2,9], meanDataAMy[3,9], meanDataAMy[4,9], meanDataAMy[5,9]),
                               'foot_l'=c(meanDataAMy[1,10], meanDataAMy[2,10], meanDataAMy[3,10], meanDataAMy[4,10], meanDataAMy[5,10]),
                               'toes_l'=c(meanDataAMy[1,11], meanDataAMy[2,11], meanDataAMy[3,11], meanDataAMy[4,11], meanDataAMy[5,11]),
                               'back'=c(meanDataAMy[1,12], meanDataAMy[2,12], meanDataAMy[3,12], meanDataAMy[4,12], meanDataAMy[5,12]),
                               'head'=c(meanDataAMy[1,13], meanDataAMy[2,13], meanDataAMy[3,13], meanDataAMy[4,13], meanDataAMy[5,13]),
                               'upper_arm_r'=c(meanDataAMy[1,14], meanDataAMy[2,14], meanDataAMy[3,14], meanDataAMy[4,14], meanDataAMy[5,14]),
                               'forearm_flex_r'=c(meanDataAMy[1,15], meanDataAMy[2,15], meanDataAMy[3,15], meanDataAMy[4,15], meanDataAMy[5,15]),
                               'forearm_rot_r'=c(meanDataAMy[1,16], meanDataAMy[2,16], meanDataAMy[3,16], meanDataAMy[4,16], meanDataAMy[5,16]),
                               'hand_deviation_r'=c(meanDataAMy[1,17], meanDataAMy[2,17], meanDataAMy[3,17], meanDataAMy[4,17], meanDataAMy[5,17]),
                               'hand_flex_r'=c(meanDataAMy[1,18], meanDataAMy[2,18], meanDataAMy[3,18], meanDataAMy[4,18], meanDataAMy[5,18]),
                               'fingers_r'=c(meanDataAMy[1,19], meanDataAMy[2,19], meanDataAMy[3,19], meanDataAMy[4,19], meanDataAMy[5,19]),
                               'upper_arm_l'=c(meanDataAMy[1,20], meanDataAMy[2,20], meanDataAMy[3,20], meanDataAMy[4,20], meanDataAMy[5,20]),
                               'forearm_flex_l'=c(meanDataAMy[1,21], meanDataAMy[2,21], meanDataAMy[3,21], meanDataAMy[4,21], meanDataAMy[5,21]),
                               'forearm_rot_l'=c(meanDataAMy[1,22], meanDataAMy[2,22], meanDataAMy[3,22], meanDataAMy[4,22], meanDataAMy[5,22]),
                               'hand_deviation_l'=c(meanDataAMy[1,23], meanDataAMy[2,23], meanDataAMy[3,23], meanDataAMy[4,23], meanDataAMy[5,23]),
                               'hand_flex_l'=c(meanDataAMy[1,24], meanDataAMy[2,24], meanDataAMy[3,24], meanDataAMy[4,24], meanDataAMy[5,24]),
                               'fingers_l'=c(meanDataAMy[1,25], meanDataAMy[2,25], meanDataAMy[3,25], meanDataAMy[4,25], meanDataAMy[5,25])
), 
.Names = names, 
class = "data.frame", row.names = c(NA, -5L))


# Angular Momentum Z
land.means.zz <- structure(list('pelvis'=c(meanDataAMz[1,1], meanDataAMz[2,1], meanDataAMz[3,1], meanDataAMz[4,1], meanDataAMz[5,1]),
                               'thigh_r'=c(meanDataAMz[1,2], meanDataAMz[2,2], meanDataAMz[3,2], meanDataAMz[4,2], meanDataAMz[5,2]),
                               'leg_r'=c(meanDataAMz[1,3], meanDataAMz[2,3], meanDataAMz[3,3], meanDataAMz[4,3], meanDataAMz[5,3]),
                               'foot_flex_r'=c(meanDataAMz[1,4], meanDataAMz[2,4], meanDataAMz[3,4], meanDataAMz[4,4], meanDataAMz[5,4]),
                               'foot_r'=c(meanDataAMz[1,5], meanDataAMz[2,5], meanDataAMz[3,5], meanDataAMz[4,5], meanDataAMz[5,5]),
                               'toes_r'=c(meanDataAMz[1,6], meanDataAMz[2,6], meanDataAMz[3,6], meanDataAMz[4,6], meanDataAMz[5,6]),
                               'thigh_l'=c(meanDataAMz[1,7], meanDataAMz[2,7], meanDataAMz[3,7], meanDataAMz[4,7], meanDataAMz[5,7]),
                               'leg_l'=c(meanDataAMz[1,8], meanDataAMz[2,8], meanDataAMz[3,8], meanDataAMz[4,8], meanDataAMz[5,8]),
                               'foot_flex_l'=c(meanDataAMz[1,9], meanDataAMz[2,9], meanDataAMz[3,9], meanDataAMz[4,9], meanDataAMz[5,9]),
                               'foot_l'=c(meanDataAMz[1,10], meanDataAMz[2,10], meanDataAMz[3,10], meanDataAMz[4,10], meanDataAMz[5,10]),
                               'toes_l'=c(meanDataAMz[1,11], meanDataAMz[2,11], meanDataAMz[3,11], meanDataAMz[4,11], meanDataAMz[5,11]),
                               'back'=c(meanDataAMz[1,12], meanDataAMz[2,12], meanDataAMz[3,12], meanDataAMz[4,12], meanDataAMz[5,12]),
                               'head'=c(meanDataAMz[1,13], meanDataAMz[2,13], meanDataAMz[3,13], meanDataAMz[4,13], meanDataAMz[5,13]),
                               'upper_arm_r'=c(meanDataAMz[1,14], meanDataAMz[2,14], meanDataAMz[3,14], meanDataAMz[4,14], meanDataAMz[5,14]),
                               'forearm_flex_r'=c(meanDataAMz[1,15], meanDataAMz[2,15], meanDataAMz[3,15], meanDataAMz[4,15], meanDataAMz[5,15]),
                               'forearm_rot_r'=c(meanDataAMz[1,16], meanDataAMz[2,16], meanDataAMz[3,16], meanDataAMz[4,16], meanDataAMz[5,16]),
                               'hand_deviation_r'=c(meanDataAMz[1,17], meanDataAMz[2,17], meanDataAMz[3,17], meanDataAMz[4,17], meanDataAMz[5,17]),
                               'hand_flex_r'=c(meanDataAMz[1,18], meanDataAMz[2,18], meanDataAMz[3,18], meanDataAMz[4,18], meanDataAMz[5,18]),
                               'fingers_r'=c(meanDataAMz[1,19], meanDataAMz[2,19], meanDataAMz[3,19], meanDataAMz[4,19], meanDataAMz[5,19]),
                               'upper_arm_l'=c(meanDataAMz[1,20], meanDataAMz[2,20], meanDataAMz[3,20], meanDataAMz[4,20], meanDataAMz[5,20]),
                               'forearm_flex_l'=c(meanDataAMz[1,21], meanDataAMz[2,21], meanDataAMz[3,21], meanDataAMz[4,21], meanDataAMz[5,21]),
                               'forearm_rot_l'=c(meanDataAMz[1,22], meanDataAMz[2,22], meanDataAMz[3,22], meanDataAMz[4,22], meanDataAMz[5,22]),
                               'hand_deviation_l'=c(meanDataAMz[1,23], meanDataAMz[2,23], meanDataAMz[3,23], meanDataAMz[4,23], meanDataAMz[5,23]),
                               'hand_flex_l'=c(meanDataAMz[1,24], meanDataAMz[2,24], meanDataAMz[3,24], meanDataAMz[4,24], meanDataAMz[5,24]),
                               'fingers_l'=c(meanDataAMz[1,25], meanDataAMz[2,25], meanDataAMz[3,25], meanDataAMz[4,25], meanDataAMz[5,25])
), 
.Names = names, 
class = "data.frame", row.names = c(NA, -5L))



# ----------- BARPLOT
colors = c("red","green","blue","yellow","pink")
slegend = c( "7%","16%","30%", "40%", "100%")

op = par(mar=c(8,5,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(-land.means.x), main="A-P Force",
               ylab=expression(kg %.% m %.% s^-1 %.% BW^-1),
               xlim=c(0,30),ylim=c(-0.8,0.2),
               col=colors,
               legend = slegend ,  las=2, cex.names = 1) #beside=TRUE,xlab="joint",
rm(op)
# contribute: pelvis, thighs, legs, back, head

op = par(mar=c(8,4,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(-land.means.y), main="M-L Force",
               ylab=expression(kg %.% m %.% s^-1 %.% BM^-1),
               xlim=c(0,30),ylim=c(-0.2,0.2),
               col=colors,
               legend = slegend,  las=2, cex.names = 1) #beside=TRUE,xlab="joint",
rm(op)
# contribute: arms, forearms, hands, back, head, arms(-) (right sign opposed to left)
# thigh legh foot

op = par(mar=c(8,4,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(land.means.z), main="Land Vertical Force",
               ylab=expression(kg %.% m %.% s^-1 %.% BW^-1),
               xlim=c(0,30),ylim=c(-0.1,1.5),
               col=colors,
               legend = slegend,  las=2, cex.names = 1) #beside=TRUE,xlab="joint",
rm(op)
# contribute: pelvis, thighs, legs, back, head, arms(-)


# 
op = par(mar=c(8,5,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(land.means.xx), main="Land Angular Momentum X",
               ylab=expression(kg %.% m %.% s^-1 %.% BM^-1 %.% H),
               xlim=c(0,30),ylim=c(-0.1,0.1),
               col=colors,
               legend = slegend,  las=2, cex.names = 1) #beside=TRUE,xlab="joint",
rm(op)


op = par(mar=c(8,5,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(-land.means.yy), main="Land Angular Momentum Y",
               ylab=expression(kg %.% m %.% s^-1 %.% BM^-1 %.% H),
               xlim=c(0,30),ylim=c(-0.1,0.1),
               col=colors,
               legend = slegend,  las=2, cex.names = 1) #beside=TRUE,xlab="joint",
rm(op)
# contribute: pelvis, thighs, legs, back, head


op = par(mar=c(8,5,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(land.means.zz), main="Land Angular Momentum Z",
               ylab=expression(kg %.% m %.% s^-1 %.% BM^-1 %.% H),
               xlim=c(0,30),ylim=c(-0.1,0.1),
               col=colors,
               legend = slegend,  las=2, cex.names = 1) #beside=TRUE,xlab="joint",
rm(op)



# -------------------------------------------------------------------------
#  Angular Momentum A-P axis 
#  Type of analysis: Right vs Left
#  Justification : segmental cancelletaion of R and L might be an stability strategy
#  Segmens: thigh R, thihg L, legR, legL, foot R, foot L, arm R, arm L
# -------------------------------------------------------------------------
# names<- c('1 pelvis','2 thigh_r','3 leg_r','4foot_flex_r','5 foot_r','6 toes_r','7 thigh_l','8 leg_l','9 foot_flex_l','10 foot_l',
#'11 toes_l','12 back','13 head','14 arm_r','15 forearm_flex_r','16 forearm_rot_r','17 hand_deviation_r','18 hand_flex_r','19 fingers_r',
#'20 arm_l','21 forearm_flex_l','22 forearm_rot_l','23 hand_deviation_l','24 hand_flex_l','25 fingers_l')


# thigh + leg
# foot + toes
# forearm and hand
# contribute: pelvis, thighs, legs, back, head
simp_names = list('7%','16%','30%','40%','100%')
landing.means.xx <- structure(list(
  '7%'= c(meanDataAMx[1,2]+meanDataAMx[1,3], meanDataAMx[1,7]+meanDataAMx[1,8],
          meanDataAMx[1,4]+meanDataAMx[1,5]+meanDataAMx[1,6], meanDataAMx[1,9]+meanDataAMx[1,10]+meanDataAMx[1,11], 
          meanDataAMx[1,14]+meanDataAMx[1,17]+meanDataAMx[1,18]+meanDataAMx[1,19], meanDataAMx[1,20]+meanDataAMx[1,23]+meanDataAMx[1,24]+meanDataAMx[1,25], 
          meanDataAMx[1,15]+meanDataAMx[1,16], meanDataAMx[1,21]+meanDataAMx[1,22]),
  '16%' =c(meanDataAMx[2,2]+meanDataAMx[2,3], meanDataAMx[2,7]+meanDataAMx[2,8], 
           meanDataAMx[2,4]+meanDataAMx[2,5]+meanDataAMx[2,6], meanDataAMx[2,9]+meanDataAMx[2,10]+meanDataAMx[2,11], 
           meanDataAMx[2,14]+meanDataAMx[2,17]+meanDataAMx[2,18]+meanDataAMx[2,19], meanDataAMx[2,20]+meanDataAMx[2,23]+meanDataAMx[2,24]+meanDataAMx[2,25], 
           meanDataAMx[2,15]+meanDataAMx[2,16], meanDataAMx[2,21]+meanDataAMx[2,22]),
  '30%' = c(meanDataAMx[3,2]+meanDataAMx[3,3], meanDataAMx[3,7]+meanDataAMx[3,8],
            meanDataAMx[3,4]+meanDataAMx[3,5]+meanDataAMx[3,6], meanDataAMx[3,9]+meanDataAMx[3,10]+meanDataAMx[3,11], 
            meanDataAMx[3,14]+meanDataAMx[3,17]+meanDataAMx[3,18]+meanDataAMx[3,19], meanDataAMx[3,20]+meanDataAMx[3,23]+meanDataAMx[3,24]+meanDataAMx[3,25], 
            meanDataAMx[3,15]+meanDataAMx[3,16], meanDataAMx[3,21]+meanDataAMx[3,22]),
  '40%' = c(meanDataAMx[4,2]+meanDataAMx[4,3], meanDataAMx[4,7]+meanDataAMx[4,8], 
             meanDataAMx[4,4]+meanDataAMx[4,5]+meanDataAMx[4,6], meanDataAMx[4,9]+meanDataAMx[4,10]+meanDataAMx[4,11], 
             meanDataAMx[4,14]+meanDataAMx[4,17]+meanDataAMx[4,18]+meanDataAMx[4,19], meanDataAMx[4,20]+meanDataAMx[4,23]+meanDataAMx[4,24]+meanDataAMx[4,25], 
             meanDataAMx[4,15]+meanDataAMx[4,16], meanDataAMx[4,21]+meanDataAMx[4,22]),
  '100%' = c(meanDataAMx[5,2]+meanDataAMx[5,3], meanDataAMx[5,7]+meanDataAMx[5,8], 
            meanDataAMx[5,4]+meanDataAMx[5,5]+meanDataAMx[5,6], meanDataAMx[5,9]+meanDataAMx[5,10]+meanDataAMx[5,11], 
            meanDataAMx[5,14]+meanDataAMx[5,17]+meanDataAMx[5,18]+meanDataAMx[5,19], meanDataAMx[5,20]+meanDataAMx[5,23]+meanDataAMx[5,24]+meanDataAMx[5,25], 
            meanDataAMx[5,15]+meanDataAMx[5,16], meanDataAMx[5,21]+meanDataAMx[5,22])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -8L))

#
landing.stds.xx <- structure(list(
  '7%'= c((stdDataAMx[1,2]+stdDataAMx[1,3])/2, (stdDataAMx[1,7]+stdDataAMx[1,8])/2,
          (stdDataAMx[1,4]+stdDataAMx[1,5]+stdDataAMx[1,6])/3, (stdDataAMx[1,9]+stdDataAMx[1,10]+stdDataAMx[1,11])/3, 
          (stdDataAMx[1,14]+stdDataAMx[1,17]+stdDataAMx[1,18]+stdDataAMx[1,19])/4, (stdDataAMx[1,20]+stdDataAMx[1,23]+stdDataAMx[1,24]+stdDataAMx[1,25])/4, 
          (stdDataAMx[1,15]+stdDataAMx[1,16])/2, (stdDataAMx[1,21]+stdDataAMx[1,22]))/2,
  '16%' =c((stdDataAMx[2,2]+stdDataAMx[2,3])/2, (stdDataAMx[2,7]+stdDataAMx[2,8])/2, 
           (stdDataAMx[2,4]+stdDataAMx[2,5]+stdDataAMx[2,6])/3, (stdDataAMx[2,9]+stdDataAMx[2,10]+stdDataAMx[2,11])/3, 
           (stdDataAMx[2,14]+stdDataAMx[2,17]+stdDataAMx[2,18]+stdDataAMx[2,19])/2, (stdDataAMx[2,20]+stdDataAMx[2,23]+stdDataAMx[2,24]+stdDataAMx[2,25])/4, 
           (stdDataAMx[2,15]+stdDataAMx[2,16])/2, (stdDataAMx[2,21]+stdDataAMx[2,22])/2),
  '30%' = c((stdDataAMx[3,2]+stdDataAMx[3,3])/2, (stdDataAMx[3,7]+stdDataAMx[3,8])/2,
            (stdDataAMx[3,4]+stdDataAMx[3,5]+stdDataAMx[3,6])/3, (stdDataAMx[3,9]+stdDataAMx[3,10]+stdDataAMx[3,11])/3, 
            (stdDataAMx[3,14]+stdDataAMx[3,17]+stdDataAMx[3,18]+stdDataAMx[3,19])/4, (stdDataAMx[3,20]+stdDataAMx[3,23]+stdDataAMx[3,24]+stdDataAMx[3,25])/4, 
            (stdDataAMx[3,15]+stdDataAMx[3,16])/2, (stdDataAMx[3,21]+stdDataAMx[3,22])/2),
  '40%' = c((stdDataAMx[4,2]+stdDataAMx[4,3])/2, (stdDataAMx[4,7]+stdDataAMx[4,8])/2, 
            (stdDataAMx[4,4]+stdDataAMx[4,5]+stdDataAMx[4,6])/3, (stdDataAMx[4,9]+stdDataAMx[4,10]+stdDataAMx[4,11])/3, 
            (stdDataAMx[4,14]+stdDataAMx[4,17]+stdDataAMx[4,18]+stdDataAMx[4,19])/4, (stdDataAMx[4,20]+stdDataAMx[4,23]+stdDataAMx[4,24]+stdDataAMx[4,25])/4, 
            (stdDataAMx[4,15]+stdDataAMx[4,16])/2, (stdDataAMx[4,21]+stdDataAMx[4,22])/2),
  '100%' = c((stdDataAMx[5,2]+stdDataAMx[5,3])/2, (stdDataAMx[5,7]+stdDataAMx[5,8])/2, 
             (stdDataAMx[5,4]+stdDataAMx[5,5]+stdDataAMx[5,6])/3, (stdDataAMx[5,9]+stdDataAMx[5,10]+stdDataAMx[5,11])/3, 
             (stdDataAMx[5,14]+stdDataAMx[5,17]+stdDataAMx[5,18]+stdDataAMx[5,19])/4, (stdDataAMx[5,20]+stdDataAMx[5,23]+stdDataAMx[5,24]+stdDataAMx[5,25])/4, 
             (stdDataAMx[5,15]+stdDataAMx[5,16])/2, (stdDataAMx[5,21]+stdDataAMx[5,22])/2)
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -8L))


k=t/sqrt(nparticipants)
landing.ci.xx <- structure(list(
  '7%'= c(k*stdDataAMx[1,2]+k*stdDataAMx[1,3], k*stdDataAMx[1,7]+k*stdDataAMx[1,8],
          k*stdDataAMx[1,4]+k*stdDataAMx[1,5]+k*stdDataAMx[1,6], k*stdDataAMx[1,9]+k*stdDataAMx[1,10]+k*stdDataAMx[1,11], 
          k*stdDataAMx[1,14]+k*stdDataAMx[1,17]+k*stdDataAMx[1,18]+k*stdDataAMx[1,19], k*stdDataAMx[1,20]+k*stdDataAMx[1,23]+k*stdDataAMx[1,24]+k*stdDataAMx[1,25], 
          k*stdDataAMx[1,15]+k*stdDataAMx[1,16], k*stdDataAMx[1,21]+k*stdDataAMx[1,22]),
  '16%' =c(k*stdDataAMx[2,2]+k*stdDataAMx[2,3], k*stdDataAMx[2,7]+k*stdDataAMx[2,8], 
           k*stdDataAMx[2,4]+k*stdDataAMx[2,5]+k*stdDataAMx[2,6], k*stdDataAMx[2,9]+k*stdDataAMx[2,10]+k*stdDataAMx[2,11], 
           k*stdDataAMx[2,14]+k*stdDataAMx[2,17]+k*stdDataAMx[2,18]+k*stdDataAMx[2,19], k*stdDataAMx[2,20]+k*stdDataAMx[2,23]+k*stdDataAMx[2,24]+k*stdDataAMx[2,25], 
           k*stdDataAMx[2,15]+k*stdDataAMx[2,16], k*stdDataAMx[2,21]+k*stdDataAMx[2,22]),
  '30%' = c(k*stdDataAMx[3,2]+k*stdDataAMx[3,3], k*stdDataAMx[3,7]+k*stdDataAMx[3,8],
            k*stdDataAMx[3,4]+k*stdDataAMx[3,5]+k*stdDataAMx[3,6], k*stdDataAMx[3,9]+k*stdDataAMx[3,10]+k*stdDataAMx[3,11], 
            k*stdDataAMx[3,14]+k*stdDataAMx[3,17]+k*stdDataAMx[3,18]+k*stdDataAMx[3,19], k*stdDataAMx[3,20]+k*stdDataAMx[3,23]+k*stdDataAMx[3,24]+k*stdDataAMx[3,25], 
            k*stdDataAMx[3,15]+k*stdDataAMx[3,16], k*stdDataAMx[3,21]+k*stdDataAMx[3,22]),
  '40%' = c(k*stdDataAMx[4,2]+k*stdDataAMx[4,3], k*stdDataAMx[4,7]+k*stdDataAMx[4,8], 
            k*stdDataAMx[4,4]+k*stdDataAMx[4,5]+k*stdDataAMx[4,6], k*stdDataAMx[4,9]+k*stdDataAMx[4,10]+k*stdDataAMx[4,11], 
            k*stdDataAMx[4,14]+k*stdDataAMx[4,17]+k*stdDataAMx[4,18]+k*stdDataAMx[4,19], k*stdDataAMx[4,20]+k*stdDataAMx[4,23]+k*stdDataAMx[4,24]+k*stdDataAMx[4,25], 
            k*stdDataAMx[4,15]+k*stdDataAMx[4,16], k*stdDataAMx[4,21]+k*stdDataAMx[4,22]),
  '100%' = c(k*stdDataAMx[5,2]+k*stdDataAMx[5,3], k*stdDataAMx[5,7]+k*stdDataAMx[5,8], 
             k*stdDataAMx[5,4]+k*stdDataAMx[5,5]+k*stdDataAMx[5,6], k*stdDataAMx[5,9]+k*stdDataAMx[5,10]+k*stdDataAMx[5,11], 
             k*stdDataAMx[5,14]+k*stdDataAMx[5,17]+k*stdDataAMx[5,18]+k*stdDataAMx[5,19], k*stdDataAMx[5,20]+k*stdDataAMx[5,23]+k*stdDataAMx[5,24]+k*stdDataAMx[5,25], 
             k*stdDataAMx[5,15]+k*stdDataAMx[5,16], k*stdDataAMx[5,21]+k*stdDataAMx[5,22])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -8L))


headers = c('thigh_leg_r','thigh_leg_l','foot_r','foot_l',
            'upper arm_r','upper arm_l','forearm_hand_r','forearm_hand_l')
colors = c("red","green","blue","yellow","purple","azure2","cadetblue",
           "coral") #,"forestgreen","deeppink","cyan","rosybrown1","beige","aquamarine")
op = par(mar=c(5,5,5,1)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(-landing.means.xx), 
               ylab=expression(Nm %.% BW^-1 %.% H^-1),
               xlim=c(0,50),ylim=c(-0.025, 0.025), 
               col=colors,
               legend = headers,  
               las=2, cex.names = 1.4,  pch=19, cex.lab=1.4,
               beside=TRUE,args.legend = list(x=45,y=0.035,horiz=FALSE, ncol=3, cex=1.4)) #beside=TRUE,xlab="joint",main="Landing Angular Momentum in Sagittal Plane",
rm(op)

xx=as.matrix(-landing.means.xx)
er=as.matrix(-landing.stds.xx)
erci=as.matrix(-landing.ci.xx)
arrows(barx,xx+er, barx,xx, angle=90, code=3, length=0.05)
arrows(barx,xx-er, barx,xx, angle=90, code=3, length=0.05)


# -------------------------------------------------------------------------
#  Angular Momentum M-L axis 
#  Type of analysis: Right vs Left
#  Justification : segmental cancelletaion of R and L might be an stability strategy
#  Segmens: 
# -------------------------------------------------------------------------
# names<- c('1 pelvis','2 thigh_r','3 leg_r','4foot_flex_r','5 foot_r','6 toes_r','7 thigh_l','8 leg_l','9 foot_flex_l','10 foot_l',
#'11 toes_l','12 back','13 head','14 arm_r','15 forearm_flex_r','16 forearm_rot_r','17 hand_deviation_r','18 hand_flex_r','19 fingers_r',
#'20 arm_l','21 forearm_flex_l','22 forearm_rot_l','23 hand_deviation_l','24 hand_flex_l','25 fingers_l')

# contribute: pelvis, thighs, legs, back, head
simp_names = list('7%','16%','30%','40%','100%')
upper_limbs1 = meanDataAMy[1,14] + meanDataAMy[1,15] + meanDataAMy[1,16] + meanDataAMy[1,17] + meanDataAMy[1,18] + meanDataAMy[1,19] + meanDataAMy[1,20] + meanDataAMy[1,21] + meanDataAMy[1,22] + meanDataAMy[1,23] + meanDataAMy[1,24] + meanDataAMy[1,25]
upper_limbs2 = meanDataAMy[2,14] + meanDataAMy[2,15] + meanDataAMy[2,16] + meanDataAMy[2,17] + meanDataAMy[2,18] + meanDataAMy[2,19] + meanDataAMy[2,20] + meanDataAMy[2,21] + meanDataAMy[2,22] + meanDataAMy[2,23] + meanDataAMy[2,24] + meanDataAMy[2,25]
upper_limbs3 = meanDataAMy[3,14] + meanDataAMy[3,15] + meanDataAMy[3,16] + meanDataAMy[3,17] + meanDataAMy[3,18] + meanDataAMy[3,19] + meanDataAMy[3,20] + meanDataAMy[3,21] + meanDataAMy[3,22] + meanDataAMy[3,23] + meanDataAMy[3,24] + meanDataAMy[3,25]
upper_limbs4 = meanDataAMy[4,14] + meanDataAMy[4,15] + meanDataAMy[4,16] + meanDataAMy[4,17] + meanDataAMy[4,18] + meanDataAMy[4,19] + meanDataAMy[4,20] + meanDataAMy[4,21] + meanDataAMy[4,22] + meanDataAMy[4,23] + meanDataAMy[4,24] + meanDataAMy[4,25]
upper_limbs5 = meanDataAMy[5,14] + meanDataAMy[5,15] + meanDataAMy[5,16] + meanDataAMy[5,17] + meanDataAMy[5,18] + meanDataAMy[5,19] + meanDataAMy[5,20] + meanDataAMy[5,21] + meanDataAMy[5,22] + meanDataAMy[5,23] + meanDataAMy[5,24] + meanDataAMy[5,25]
lower_limbs1 = meanDataAMy[1,2] + meanDataAMy[1,3] + meanDataAMy[1,4] + meanDataAMy[1,5] + meanDataAMy[1,6] + meanDataAMy[1,7] + meanDataAMy[1,8] + meanDataAMy[1,9] + meanDataAMy[1,10] 
lower_limbs2 = meanDataAMy[2,2] + meanDataAMy[2,3] + meanDataAMy[2,4] + meanDataAMy[2,5] + meanDataAMy[2,6] + meanDataAMy[2,7] + meanDataAMy[2,8] + meanDataAMy[2,9] + meanDataAMy[2,10] 
lower_limbs3 = meanDataAMy[3,2] + meanDataAMy[3,3] + meanDataAMy[3,4] + meanDataAMy[3,5] + meanDataAMy[3,6] + meanDataAMy[3,7] + meanDataAMy[3,8] + meanDataAMy[3,9] + meanDataAMy[3,10] 
lower_limbs4 = meanDataAMy[4,2] + meanDataAMy[4,3] + meanDataAMy[4,4] + meanDataAMy[4,5] + meanDataAMy[4,6] + meanDataAMy[4,7] + meanDataAMy[4,8] + meanDataAMy[4,9] + meanDataAMy[4,10] 
lower_limbs5 = meanDataAMy[5,2] + meanDataAMy[5,3] + meanDataAMy[5,4] + meanDataAMy[5,5] + meanDataAMy[5,6] + meanDataAMy[5,7] + meanDataAMy[5,8] + meanDataAMy[5,9] + meanDataAMy[5,10] 
#
upper_limbs1_std = (stdDataAMy[1,14] + stdDataAMy[1,15] + stdDataAMy[1,16] + stdDataAMy[1,17] + stdDataAMy[1,18] + stdDataAMy[1,19] + stdDataAMy[1,20] + stdDataAMy[1,21] + stdDataAMy[1,22] + stdDataAMy[1,23] + stdDataAMy[1,24] + stdDataAMy[1,25])/12
upper_limbs2_std = (stdDataAMy[2,14] + stdDataAMy[2,15] + stdDataAMy[2,16] + stdDataAMy[2,17] + stdDataAMy[2,18] + stdDataAMy[2,19] + stdDataAMy[2,20] + stdDataAMy[2,21] + stdDataAMy[2,22] + stdDataAMy[2,23] + stdDataAMy[2,24] + stdDataAMy[2,25])/12
upper_limbs3_std = (stdDataAMy[3,14] + stdDataAMy[3,15] + stdDataAMy[3,16] + stdDataAMy[3,17] + stdDataAMy[3,18] + stdDataAMy[3,19] + stdDataAMy[3,20] + stdDataAMy[3,21] + stdDataAMy[3,22] + stdDataAMy[3,23] + stdDataAMy[3,24] + stdDataAMy[3,25])/12
upper_limbs4_std = (stdDataAMy[4,14] + stdDataAMy[4,15] + stdDataAMy[4,16] + stdDataAMy[4,17] + stdDataAMy[4,18] + stdDataAMy[4,19] + stdDataAMy[4,20] + stdDataAMy[4,21] + stdDataAMy[4,22] + stdDataAMy[4,23] + stdDataAMy[4,24] + stdDataAMy[4,25])/12
upper_limbs5_std = (stdDataAMy[5,14] + stdDataAMy[5,15] + stdDataAMy[5,16] + stdDataAMy[5,17] + stdDataAMy[5,18] + stdDataAMy[5,19] + stdDataAMy[5,20] + stdDataAMy[5,21] + stdDataAMy[5,22] + stdDataAMy[5,23] + stdDataAMy[5,24] + stdDataAMy[5,25])/12
lower_limbs1_std = (stdDataAMy[1,2] + stdDataAMy[1,3] + stdDataAMy[1,4] + stdDataAMy[1,5] + stdDataAMy[1,6] + stdDataAMy[1,7] + stdDataAMy[1,8] + stdDataAMy[1,9] + stdDataAMy[1,10])/9
lower_limbs2_std = (stdDataAMy[2,2] + stdDataAMy[2,3] + stdDataAMy[2,4] + stdDataAMy[2,5] + stdDataAMy[2,6] + stdDataAMy[2,7] + stdDataAMy[2,8] + stdDataAMy[2,9] + stdDataAMy[2,10])/9 
lower_limbs3_std = (stdDataAMy[3,2] + stdDataAMy[3,3] + stdDataAMy[3,4] + stdDataAMy[3,5] + stdDataAMy[3,6] + stdDataAMy[3,7] + stdDataAMy[3,8] + stdDataAMy[3,9] + stdDataAMy[3,10])/9
lower_limbs4_std = (stdDataAMy[4,2] + stdDataAMy[4,3] + stdDataAMy[4,4] + stdDataAMy[4,5] + stdDataAMy[4,6] + stdDataAMy[4,7] + stdDataAMy[4,8] + stdDataAMy[4,9] + stdDataAMy[4,10])/9
lower_limbs5_std = (stdDataAMy[5,2] + stdDataAMy[5,3] + stdDataAMy[5,4] + stdDataAMy[5,5] + stdDataAMy[5,6] + stdDataAMy[5,7] + stdDataAMy[5,8] + stdDataAMy[5,9] + stdDataAMy[5,10])/9

landing.means.yy <- structure(list(
  '7%'= c(lower_limbs1, meanDataAMy[1,1], meanDataAMy[1,12], meanDataAMy[1,13], upper_limbs1),
  '16%' =c(lower_limbs2, meanDataAMy[2,1], meanDataAMy[2,12], meanDataAMy[2,13], upper_limbs2),
  '30%' = c(lower_limbs3, meanDataAMy[3,1], meanDataAMy[3,12], meanDataAMy[3,13], upper_limbs3),
  '40%' = c(lower_limbs4, meanDataAMy[4,1], meanDataAMy[4,12], meanDataAMy[4,13], upper_limbs4),
  '100%' = c(lower_limbs5, meanDataAMy[5,1], meanDataAMy[5,12], meanDataAMy[5,13], upper_limbs5)
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -5L))

landing.stds.yy <- structure(list(
  '7%'= c(lower_limbs1_std, stdDataAMy[1,1], stdDataAMy[1,12], stdDataAMy[1,13], upper_limbs1_std),
  '16%' =c(lower_limbs2_std, stdDataAMy[2,1], stdDataAMy[2,12], stdDataAMy[2,13], upper_limbs2_std),
  '30%' = c(lower_limbs3_std, stdDataAMy[3,1], stdDataAMy[3,12], stdDataAMy[3,13], upper_limbs3_std),
  '40%' = c(lower_limbs4_std, stdDataAMy[4,1], stdDataAMy[4,12], stdDataAMy[4,13], upper_limbs4_std),
  '100%' = c(lower_limbs5_std, stdDataAMy[5,1], stdDataAMy[5,12], stdDataAMy[5,13], upper_limbs5_std)
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -5L))

landing.ci.yy <- structure(list(
  '7%'= c(k*lower_limbs1_std, k*stdDataAMy[1,1], k*stdDataAMy[1,12], k*stdDataAMy[1,13], k*upper_limbs1_std),
  '16%' =c(k*lower_limbs2_std, k*stdDataAMy[2,1], k*stdDataAMy[2,12], k*stdDataAMy[2,13], k*upper_limbs2_std),
  '30%' = c(k*lower_limbs3_std, k*stdDataAMy[3,1], k*stdDataAMy[3,12], k*stdDataAMy[3,13], k*upper_limbs3_std),
  '40%' = c(k*lower_limbs4_std, k*stdDataAMy[4,1], k*stdDataAMy[4,12], k*stdDataAMy[4,13], k*upper_limbs4_std),
  '100%' = c(k*lower_limbs5_std, k*stdDataAMy[5,1], k*stdDataAMy[5,12], k*stdDataAMy[5,13], k*upper_limbs5_std)
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -5L))

headers = c('lower limbs','pelvis','torso','head','upper limbs')
colors = c("red","green","blue","yellow","purple")
op = par(mar=c(5,5,5,2)) # c(bottom, left, top, right) which gives the number of lines of margin
bary = barplot(as.matrix(-landing.means.yy), 
               ylab=expression(Nm %.% BW^-1 %.% H^-1),
               xlim=c(0,30),ylim=c(-0.02, 0.15),
               col=colors,
               legend = headers,  
               las=2, cex.names = 1.4,  pch=19, cex.lab=1.4, 
               beside=TRUE,args.legend = list(x=25,y=0.19,horiz=FALSE, cex=1.4,ncol=3)) #beside=TRUE,xlab="joint",main="Landing Angular Momentum in Sagittal Plane",
rm(op)

yy=as.matrix(-landing.means.yy)
er=as.matrix(-landing.stds.yy)
erci=as.matrix(-landing.ci.yy)
arrows(bary,yy+er, bary,yy, angle=90, code=3, length=0.05)
arrows(bary,yy-er, bary,yy, angle=90, code=3, length=0.05)


# -------------------------------------------------------------------------
#  Angular Momentum Z axis 
#  Type of analysis: Right vs Left
#  Justification : segmental cancelletaion of R and L might be an stability strategy
#  Segmens: 
# -------------------------------------------------------------------------
landing.means.zz <- structure(list(
  '7%'= c(meanDataAMx[1,2]+meanDataAMx[1,3]+meanDataAMx[1,4]+meanDataAMx[1,5]+meanDataAMx[1,6], 
          meanDataAMx[1,7]+meanDataAMx[1,8]+meanDataAMx[1,9]+meanDataAMx[1,10]+meanDataAMx[1,11], 
          meanDataAMx[1,14]+meanDataAMx[1,15]+meanDataAMx[1,16]+meanDataAMx[1,17]+meanDataAMx[1,18]+meanDataAMx[1,19], 
          meanDataAMx[1,20]+meanDataAMx[1,21]+meanDataAMx[1,22]+meanDataAMx[1,23]+meanDataAMx[1,24]+meanDataAMx[1,25]),
  '16%' =c(meanDataAMx[2,2]+meanDataAMx[2,3]+meanDataAMx[2,4]+meanDataAMx[2,5]+meanDataAMx[2,6], 
           meanDataAMx[2,7]+meanDataAMx[2,8]+meanDataAMx[2,9]+meanDataAMx[2,10]+meanDataAMx[2,11], 
           meanDataAMx[2,14]+meanDataAMx[2,15]+meanDataAMx[2,16]+meanDataAMx[2,17]+meanDataAMx[2,18]+meanDataAMx[2,19], 
           meanDataAMx[2,20]+meanDataAMx[2,21]+meanDataAMx[2,22]+meanDataAMx[2,23]+meanDataAMx[2,24]+meanDataAMx[2,25]),
  '30%' = c(meanDataAMx[3,2]+meanDataAMx[3,3]+meanDataAMx[3,4]+meanDataAMx[3,5]+meanDataAMx[3,6],
            meanDataAMx[3,7]+meanDataAMx[3,8]+meanDataAMx[3,9]+meanDataAMx[3,10]+meanDataAMx[3,11], 
            meanDataAMx[3,14]+meanDataAMx[3,15]+meanDataAMx[3,16]+meanDataAMx[3,17]+meanDataAMx[3,18]+meanDataAMx[3,19], 
            meanDataAMx[3,20]+meanDataAMx[3,21]+meanDataAMx[3,22]+meanDataAMx[3,23]+meanDataAMx[3,24]+meanDataAMx[3,25]),
  '40%' = c(meanDataAMx[4,2]+meanDataAMx[4,3]+meanDataAMx[4,4]+meanDataAMx[4,5]+meanDataAMx[4,6],
            meanDataAMx[4,7]+meanDataAMx[4,8]+meanDataAMx[4,9]+meanDataAMx[4,10]+meanDataAMx[4,11], 
            meanDataAMx[4,14]+meanDataAMx[4,15]+meanDataAMx[4,16]+meanDataAMx[4,17]+meanDataAMx[4,18]+meanDataAMx[4,19], 
            meanDataAMx[4,20]+meanDataAMx[4,21]+meanDataAMx[4,22]+meanDataAMx[4,23]+meanDataAMx[4,24]+meanDataAMx[4,25]),
  '100%' = c(meanDataAMx[5,2]+meanDataAMx[5,3]+meanDataAMx[5,4]+meanDataAMx[5,5]+meanDataAMx[5,6], 
             meanDataAMx[5,7]+meanDataAMx[5,8]+meanDataAMx[5,9]+meanDataAMx[5,10]+meanDataAMx[5,11], 
             meanDataAMx[5,14]+meanDataAMx[5,15]+meanDataAMx[5,16]+meanDataAMx[5,17]+meanDataAMx[5,18]+meanDataAMx[5,19], 
             meanDataAMx[5,20]+meanDataAMx[5,23]+meanDataAMx[5,24]+meanDataAMx[5,25]+meanDataAMx[5,21]+meanDataAMx[5,22])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -4L))

#
landing.stds.zz <- structure(list(
  '7%'= c((stdDataAMx[1,2]+stdDataAMx[1,3]+stdDataAMx[1,4]+stdDataAMx[1,5]+stdDataAMx[1,6])/5, 
          (stdDataAMx[1,7]+stdDataAMx[1,8]+stdDataAMx[1,9]+stdDataAMx[1,10]+stdDataAMx[1,11])/5, 
          (stdDataAMx[1,14]+stdDataAMx[1,15]+stdDataAMx[1,16]+stdDataAMx[1,17]+stdDataAMx[1,18]+stdDataAMx[1,19])/6, 
          (stdDataAMx[1,20]+stdDataAMx[1,21]+stdDataAMx[1,22]+stdDataAMx[1,23]+stdDataAMx[1,24]+stdDataAMx[1,25])/6),
  '16%' =c((stdDataAMx[2,2]+stdDataAMx[2,3]+stdDataAMx[2,4]+stdDataAMx[2,5]+stdDataAMx[2,6])/5, 
           (stdDataAMx[2,7]+stdDataAMx[2,8]+stdDataAMx[2,9]+stdDataAMx[2,10]+stdDataAMx[2,11])/5, 
           (stdDataAMx[2,14]+stdDataAMx[2,15]+stdDataAMx[2,16]+stdDataAMx[2,17]+stdDataAMx[2,18]+stdDataAMx[2,19])/6, 
           (stdDataAMx[2,20]+stdDataAMx[2,21]+stdDataAMx[2,22]+stdDataAMx[2,23]+stdDataAMx[2,24]+stdDataAMx[2,25])/6),
  '30%' = c((stdDataAMx[3,2]+stdDataAMx[3,3]+stdDataAMx[3,4]+stdDataAMx[3,5]+stdDataAMx[3,6])/5,
            (stdDataAMx[3,7]+stdDataAMx[3,8]+stdDataAMx[3,9]+stdDataAMx[3,10]+stdDataAMx[3,11])/5, 
            (stdDataAMx[3,14]+stdDataAMx[3,15]+stdDataAMx[3,16]+stdDataAMx[3,17]+stdDataAMx[3,18]+stdDataAMx[3,19])/6, 
            (stdDataAMx[3,20]+stdDataAMx[3,21]+stdDataAMx[3,22]+stdDataAMx[3,23]+stdDataAMx[3,24]+stdDataAMx[3,25])/6),
  '40%' = c((stdDataAMx[4,2]+stdDataAMx[4,3]+stdDataAMx[4,4]+stdDataAMx[4,5]+stdDataAMx[4,6])/5,
            (stdDataAMx[4,7]+stdDataAMx[4,8]+stdDataAMx[4,9]+stdDataAMx[4,10]+stdDataAMx[4,11])/5, 
            (stdDataAMx[4,14]+stdDataAMx[4,15]+stdDataAMx[4,16]+stdDataAMx[4,17]+stdDataAMx[4,18]+stdDataAMx[4,19])/6, 
            (stdDataAMx[4,20]+stdDataAMx[4,21]+stdDataAMx[4,22]+stdDataAMx[4,23]+stdDataAMx[4,24]+stdDataAMx[4,25])/6),
  '100%' = c((stdDataAMx[5,2]+stdDataAMx[5,3]+stdDataAMx[5,4]+stdDataAMx[5,5]+stdDataAMx[5,6])/5, 
             (stdDataAMx[5,7]+stdDataAMx[5,8]+stdDataAMx[5,9]+stdDataAMx[5,10]+stdDataAMx[5,11])/5, 
             (stdDataAMx[5,14]+stdDataAMx[5,15]+stdDataAMx[5,16]+stdDataAMx[5,17]+stdDataAMx[5,18]+stdDataAMx[5,19])/6, 
             (stdDataAMx[5,20]+stdDataAMx[5,23]+stdDataAMx[5,24]+stdDataAMx[5,25]+stdDataAMx[5,21]+stdDataAMx[5,22])/6)
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -4L))

#
k=t/sqrt(nparticipants)
landing.ci.zz <- structure(list(
  '7%'= c(k*stdDataAMx[1,2]+k*stdDataAMx[1,3]+k*stdDataAMx[1,4]+k*stdDataAMx[1,5]+k*stdDataAMx[1,6], 
          k*stdDataAMx[1,7]+k*stdDataAMx[1,8]+k*stdDataAMx[1,9]+k*stdDataAMx[1,10]+k*stdDataAMx[1,11], 
          k*stdDataAMx[1,14]+k*stdDataAMx[1,15]+k*stdDataAMx[1,16]+k*stdDataAMx[1,17]+k*stdDataAMx[1,18]+k*stdDataAMx[1,19], 
          k*stdDataAMx[1,20]+k*stdDataAMx[1,21]+k*stdDataAMx[1,22]+k*stdDataAMx[1,23]+k*stdDataAMx[1,24]+k*stdDataAMx[1,25]),
  '16%' =c(k*stdDataAMx[2,2]+k*stdDataAMx[2,3]+k*stdDataAMx[2,4]+k*stdDataAMx[2,5]+k*stdDataAMx[2,6], 
           k*stdDataAMx[2,7]+k*stdDataAMx[2,8]+k*stdDataAMx[2,9]+k*stdDataAMx[2,10]+k*stdDataAMx[2,11], 
           k*stdDataAMx[2,14]+k*stdDataAMx[2,15]+k*stdDataAMx[2,16]+k*stdDataAMx[2,17]+k*stdDataAMx[2,18]+k*stdDataAMx[2,19], 
           k*stdDataAMx[2,20]+k*stdDataAMx[2,21]+k*stdDataAMx[2,22]+k*stdDataAMx[2,23]+k*stdDataAMx[2,24]+k*stdDataAMx[2,25]),
  '30%' = c(k*stdDataAMx[3,2]+k*stdDataAMx[3,3]+k*stdDataAMx[3,4]+k*stdDataAMx[3,5]+k*stdDataAMx[3,6],
            k*stdDataAMx[3,7]+k*stdDataAMx[3,8]+k*stdDataAMx[3,9]+k*stdDataAMx[3,10]+k*stdDataAMx[3,11], 
            k*stdDataAMx[3,14]+k*stdDataAMx[3,15]+k*stdDataAMx[3,16]+k*stdDataAMx[3,17]+k*stdDataAMx[3,18]+k*stdDataAMx[3,19], 
            k*stdDataAMx[3,20]+k*stdDataAMx[3,21]+k*stdDataAMx[3,22]+k*stdDataAMx[3,23]+k*stdDataAMx[3,24]+k*stdDataAMx[3,25]),
  '40%' = c(k*stdDataAMx[4,2]+k*stdDataAMx[4,3]+k*stdDataAMx[4,4]+k*stdDataAMx[4,5]+k*stdDataAMx[4,6],
            k*stdDataAMx[4,7]+k*stdDataAMx[4,8]+k*stdDataAMx[4,9]+k*stdDataAMx[4,10]+k*stdDataAMx[4,11], 
            k*stdDataAMx[4,14]+k*stdDataAMx[4,15]+k*stdDataAMx[4,16]+k*stdDataAMx[4,17]+k*stdDataAMx[4,18]+k*stdDataAMx[4,19], 
            k*stdDataAMx[4,20]+k*stdDataAMx[4,21]+k*stdDataAMx[4,22]+k*stdDataAMx[4,23]+k*stdDataAMx[4,24]+k*stdDataAMx[4,25]),
  '100%' = c(k*stdDataAMx[5,2]+k*stdDataAMx[5,3]+k*stdDataAMx[5,4]+k*stdDataAMx[5,5]+k*stdDataAMx[5,6], 
             k*stdDataAMx[5,7]+k*stdDataAMx[5,8]+k*stdDataAMx[5,9]+k*stdDataAMx[5,10]+k*stdDataAMx[5,11], 
             k*stdDataAMx[5,14]+k*stdDataAMx[5,15]+k*stdDataAMx[5,16]+k*stdDataAMx[5,17]+k*stdDataAMx[5,18]+k*stdDataAMx[5,19], 
             k*stdDataAMx[5,20]+k*stdDataAMx[5,23]+k*stdDataAMx[5,24]+k*stdDataAMx[5,25]+k*stdDataAMx[5,21]+k*stdDataAMx[5,22])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -4L))

headers = c('lower_limbs_r','lower_limbs_l','upper_limbs_r','upper_limbs_l')
colors = c("red","green","blue","yellow") #,"forestgreen","deeppink","cyan","rosybrown1","beige","aquamarine")
op = par(mar=c(5,5,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barz = barplot(as.matrix(landing.means.zz), 
               ylab=expression(Nm %.% BW^-1 %.% H^-1),
               xlim=c(0,30),ylim=c(-0.035, 0.035),
               col=colors,
               legend = headers,  
               las=2, cex.names = 1.4,  pch=19, cex.lab=1.4,  
               beside=TRUE,args.legend = list(x=32,y=0.045,horiz=FALSE, ncol=4, cex=1.4)) #beside=TRUE,xlab="joint",main="Landing Angular Momentum in Sagittal Plane",
rm(op)

zz=as.matrix(landing.means.zz)
er=as.matrix(landing.stds.zz)
erci=as.matrix(landing.ci.zz)
arrows(barz,zz+er, barz,zz, angle=90, code=3, length=0.05)
arrows(barz,zz-er, barz,zz, angle=90, code=3, length=0.05)






























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
simp_names = list('back','pelvis','head','upper_arm_r','upper_arm_l')
landing.means.z <- structure(list(
  'back'=c(meanDataLMz[1,12], meanDataLMz[2,12], meanDataLMz[3,12], meanDataLMz[4,12]),
  'pelvis'=c(meanDataLMz[1,1], meanDataLMz[2,1], meanDataLMz[3,1], meanDataLMz[4,1]),
  'head'=c(meanDataLMz[1,13], meanDataLMz[2,13], meanDataLMz[3,13], meanDataLMz[4,13]),
  'upper_arm_r'=c(meanDataLMz[1,14], meanDataLMz[2,14], meanDataLMz[3,14], meanDataLMz[4,14]),
  'upper_arm_l'=c(meanDataLMz[1,20], meanDataLMz[2,20], meanDataLMz[3,20], meanDataLMz[4,20])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -4L))

#
landing.stds.z <- structure(list(
  'back'=c(stdDataLMz[1,12], stdDataLMz[2,12], stdDataLMz[3,12], stdDataLMz[4,12]),
  'pelvis'=c(stdDataLMz[1,1], stdDataLMz[2,1], stdDataLMz[3,1], stdDataLMz[4,1]),
  'head'=c(stdDataLMz[1,13], stdDataLMz[2,13], stdDataLMz[3,13], stdDataLMz[4,13]),
  'upper_arm_r'=c(stdDataLMz[1,14], stdDataLMz[2,14], stdDataLMz[3,14], stdDataLMz[4,14]),
  'upper_arm_l'=c(stdDataLMz[1,20], stdDataLMz[2,20], stdDataLMz[3,20], stdDataLMz[4,20])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -4L))

landing.ci.z <- structure(list(
  'back'=c(t*stdDataLMz[1,12]/sqrt(nparticipants), t*stdDataLMz[2,12]/sqrt(nparticipants), t*stdDataLMz[3,12]/sqrt(nparticipants), t*stdDataLMz[4,12]/sqrt(nparticipants)),
  'pelvis'=c(t*stdDataLMz[1,1]/sqrt(nparticipants), t*stdDataLMz[2,1]/sqrt(nparticipants), t*stdDataLMz[3,1]/sqrt(nparticipants), t*stdDataLMz[4,1]/sqrt(nparticipants)),
  'head'=c(t*stdDataLMz[1,13]/sqrt(nparticipants), t*stdDataLMz[2,13]/sqrt(nparticipants), t*stdDataLMz[3,13]/sqrt(nparticipants), t*stdDataLMz[4,13]/sqrt(nparticipants)),
  'upper_arm_r'=c(t*stdDataLMz[1,14]/sqrt(nparticipants), t*stdDataLMz[2,14]/sqrt(nparticipants), t*stdDataLMz[3,14]/sqrt(nparticipants), t*stdDataLMz[4,14]/sqrt(nparticipants)),
  'upper_arm_l'=c(t*stdDataLMz[1,20]/sqrt(nparticipants), t*stdDataLMz[2,20]/sqrt(nparticipants), t*stdDataLMz[3,20]/sqrt(nparticipants), t*stdDataLMz[4,20]/sqrt(nparticipants))
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



# -------------------------------------------------------------------------
#  Angular Momentum Z axis 
#  Type of analysis: Right vs Left
#  Justification : segmental cancelletaion of R and L might be an stability strategy
#  Segmens: thigh R, thihg L, legR, legL, foot R, foot L, arm R, arm L
# -------------------------------------------------------------------------
# names<- c('1 pelvis','2 thigh_r','3 leg_r','4foot_flex_r','5 foot_r','6 toes_r','7 thigh_l','8 leg_l','9 foot_flex_l','10 foot_l',
#'11 toes_l','12 back','13 head','14 arm_r','15 forearm_flex_r','16 forearm_rot_r','17 hand_deviation_r','18 hand_flex_r','19 fingers_r',
#'20 arm_l','21 forearm_flex_l','22 forearm_rot_l','23 hand_deviation_l','24 hand_flex_l','25 fingers_l')

# contribute: pelvis, thighs, legs, back, head
simp_names = list('5%','20%','40%','100%')
landing.means.zz <- structure(list(
  '5%'= c(meanDataAMz[1,2], meanDataAMz[1,7], 
          meanDataAMz[1,3], meanDataAMz[1,8], 
          meanDataAMz[1,4]+meanDataAMz[1,5], meanDataAMz[1,9]+meanDataAMz[1,10], 
          meanDataAMz[1,6], meanDataAMz[1,11], 
          meanDataAMz[1,14], meanDataAMz[1,20], 
          meanDataAMz[1,15]+meanDataAMz[1,16], meanDataAMz[1,21]+meanDataAMz[1,22], 
          meanDataAMz[1,17]+meanDataAMz[1,18]+meanDataAMz[1,19], meanDataAMz[1,23]+meanDataAMz[1,24]+meanDataAMz[1,25]),
  '20%' =c(meanDataAMz[2,2], meanDataAMz[2,7], 
           meanDataAMz[2,3], meanDataAMz[2,8], 
           meanDataAMz[2,4]+meanDataAMz[2,5], meanDataAMz[2,9]+meanDataAMz[2,10], 
           meanDataAMz[1,6], meanDataAMz[1,11], 
           meanDataAMz[2,14], meanDataAMz[2,20], 
           meanDataAMz[2,15]+meanDataAMz[2,16], meanDataAMz[2,21]+meanDataAMz[2,22], 
           meanDataAMz[2,17]+meanDataAMz[2,18]+meanDataAMz[2,19], meanDataAMz[2,23]+meanDataAMz[2,24]+meanDataAMz[2,25]),
  '40%' = c(meanDataAMz[3,2], meanDataAMz[3,7], 
            meanDataAMz[3,3], meanDataAMz[3,8], 
            meanDataAMz[3,4]+meanDataAMz[3,5], meanDataAMz[3,9]+meanDataAMz[3,10], 
            meanDataAMz[1,6], meanDataAMz[1,11], 
            meanDataAMz[3,14], meanDataAMz[3,20], 
            meanDataAMz[3,15]+meanDataAMz[3,16], 
            meanDataAMz[3,21]+meanDataAMz[3,22], 
            meanDataAMz[3,17]+meanDataAMz[3,18]+meanDataAMz[3,19], 
            meanDataAMz[3,23]+meanDataAMz[3,24]+meanDataAMz[3,25]),
  '100%' = c(meanDataAMz[4,2], meanDataAMz[4,7], 
             meanDataAMz[4,3], meanDataAMz[4,8], 
             meanDataAMz[4,4]+meanDataAMz[4,5], meanDataAMz[4,9]+meanDataAMz[4,10], 
             meanDataAMz[1,6], meanDataAMz[1,11], 
             meanDataAMz[4,14], meanDataAMz[4,20], 
             meanDataAMz[4,15]+meanDataAMz[4,16], meanDataAMz[4,21]+meanDataAMz[4,22], 
             meanDataAMz[4,17]+meanDataAMz[4,18]+meanDataAMz[4,19], meanDataAMz[4,23]+meanDataAMz[4,24]+meanDataAMz[4,25])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -14L))

#
landing.stds.zz <- structure(list(
  '5%'= c(stdDataAMz[1,2], stdDataAMz[1,7], 
          stdDataAMz[1,3], stdDataAMz[1,8], 
          (stdDataAMz[1,4]+stdDataAMz[1,5])/2, (stdDataAMz[1,9]+stdDataAMz[1,10])/2, 
          stdDataAMz[1,6], stdDataAMz[1,11], 
          stdDataAMz[1,14], stdDataAMz[1,20], 
          (stdDataAMz[1,15]+stdDataAMz[1,16])/2, (stdDataAMz[1,21]+stdDataAMz[1,22])/2, 
          (stdDataAMz[1,17]+stdDataAMz[1,18]+stdDataAMz[1,19])/3, (stdDataAMz[1,23]+stdDataAMz[1,24]+stdDataAMz[1,25])/3),
  '20%' =c(stdDataAMz[2,2], stdDataAMz[2,7], 
           stdDataAMz[2,3], stdDataAMz[2,8], 
           (stdDataAMz[2,4]+stdDataAMz[2,5])/2, (stdDataAMz[2,9]+stdDataAMz[2,10])/2, 
           stdDataAMz[1,6], stdDataAMz[1,11], 
           stdDataAMz[2,14], stdDataAMz[2,20], 
           (stdDataAMz[2,15]+stdDataAMz[2,16])/2, (stdDataAMz[2,21]+stdDataAMz[2,22])/2, 
           (stdDataAMz[2,17]+stdDataAMz[2,18]+stdDataAMz[2,19])/3, (stdDataAMz[2,23]+stdDataAMz[2,24]+stdDataAMz[2,25])/3),
  '40%' = c(stdDataAMz[3,2], stdDataAMz[3,7], 
            stdDataAMz[3,3], stdDataAMz[3,8], 
            (stdDataAMz[3,4]+stdDataAMz[3,5])/2, (stdDataAMz[3,9]+stdDataAMz[3,10])/2, 
            stdDataAMz[1,6], stdDataAMz[1,11], 
            stdDataAMz[3,14], stdDataAMz[3,20], 
            stdDataAMz[3,15]+stdDataAMz[3,16], 
            stdDataAMz[3,21]+stdDataAMz[3,22], 
            (stdDataAMz[3,17]+stdDataAMz[3,18]+stdDataAMz[3,19])/3, 
            (stdDataAMz[3,23]+stdDataAMz[3,24]+stdDataAMz[3,25])/3),
  '100%' = c(stdDataAMz[4,2], stdDataAMz[4,7], 
             stdDataAMz[4,3], stdDataAMz[4,8], 
             (stdDataAMz[4,4]+stdDataAMz[4,5])/2, (stdDataAMz[4,9]+stdDataAMz[4,10])/2, 
             stdDataAMz[1,6], stdDataAMz[1,11], 
             stdDataAMz[4,14], stdDataAMz[4,20], 
             (stdDataAMz[4,15]+stdDataAMz[4,16])/2, (stdDataAMz[4,21]+stdDataAMz[4,22])/2, 
             (stdDataAMz[4,17]+stdDataAMz[4,18]+stdDataAMz[4,19])/3, (stdDataAMz[4,23]+stdDataAMz[4,24]+stdDataAMz[4,25])/3)
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -14L))

k=t/sqrt(nparticipants)
landing.ci.zz <- structure(list(
  '5%'= c(k*stdDataAMz[1,2], k*stdDataAMz[1,7], 
          k*stdDataAMz[1,3], k*stdDataAMz[1,8], 
          k*stdDataAMz[1,4]+k*stdDataAMz[1,5], k*stdDataAMz[1,9]+k*stdDataAMz[1,10], 
          k*stdDataAMz[1,6], k*stdDataAMz[1,11], 
          k*stdDataAMz[1,14], k*stdDataAMz[1,20], 
          k*stdDataAMz[1,15]+k*stdDataAMz[1,16], k*stdDataAMz[1,21]+k*stdDataAMz[1,22], 
          k*stdDataAMz[1,17]+k*stdDataAMz[1,18]+k*stdDataAMz[1,19], k*stdDataAMz[1,23]+k*stdDataAMz[1,24]+k*stdDataAMz[1,25]),
  '20%' =c(k*stdDataAMz[2,2], k*stdDataAMz[2,7], 
           k*stdDataAMz[2,3], k*stdDataAMz[2,8], 
           k*stdDataAMz[2,4]+k*stdDataAMz[2,5], k*stdDataAMz[2,9]+k*stdDataAMz[2,10], 
           k*stdDataAMz[1,6], k*stdDataAMz[1,11], 
           k*stdDataAMz[2,14], k*stdDataAMz[2,20], 
           k*stdDataAMz[2,15]+k*stdDataAMz[2,16], k*stdDataAMz[2,21]+k*stdDataAMz[2,22], 
           k*stdDataAMz[2,17]+k*stdDataAMz[2,18]+k*stdDataAMz[2,19], k*stdDataAMz[2,23]+k*stdDataAMz[2,24]+k*stdDataAMz[2,25]),
  '40%' = c(k*stdDataAMz[3,2], k*stdDataAMz[3,7], 
            k*stdDataAMz[3,3], k*stdDataAMz[3,8], 
            k*stdDataAMz[3,4]+k*stdDataAMz[3,5], k*stdDataAMz[3,9]+k*stdDataAMz[3,10], 
            k*stdDataAMz[1,6], k*stdDataAMz[1,11], 
            k*stdDataAMz[3,14], k*stdDataAMz[3,20], 
            k*stdDataAMz[3,15]+k*stdDataAMz[3,16], 
            k*stdDataAMz[3,21]+k*stdDataAMz[3,22], 
            k*stdDataAMz[3,17]+k*stdDataAMz[3,18]+k*stdDataAMz[3,19], 
            k*stdDataAMz[3,23]+k*stdDataAMz[3,24]+k*stdDataAMz[3,25]),
  '100%' = c(k*stdDataAMz[4,2], k*stdDataAMz[4,7], 
             k*stdDataAMz[4,3], k*stdDataAMz[4,8], 
             k*stdDataAMz[4,4]+k*stdDataAMz[4,5], k*stdDataAMz[4,9]+k*stdDataAMz[4,10], 
             k*stdDataAMz[1,6], k*stdDataAMz[1,11], 
             k*stdDataAMz[4,14], k*stdDataAMz[4,20], 
             k*stdDataAMz[4,15]+k*stdDataAMz[4,16], k*stdDataAMz[4,21]+k*stdDataAMz[4,22], 
             k*stdDataAMz[4,17]+k*stdDataAMz[4,18]+k*stdDataAMz[4,19], k*stdDataAMz[4,23]+k*stdDataAMz[4,24]+k*stdDataAMz[4,25])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -14L))


headers = c('thigh_r','thigh_l','leg_r','leg_l','foot_r','foot_l','toes_r','toes_l',
            'upper arm_r','upper arm_l','forearm_r','forearm_l','hand_r','hand_l')
colors = c("red","green","blue","yellow","purple","azure2","cadetblue",
           "coral","forestgreen","deeppink","cyan","rosybrown1","beige","aquamarine")
op = par(mar=c(5,5,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barz = barplot(as.matrix(landing.means.zz), 
               ylab=expression(Nm %.% BW^-1 %.% H^-1),
               xlim=c(0,60),ylim=c(-0.02, 0.02),
               col=colors,
               legend = headers,  
               las=2, cex.names = 1, beside=TRUE,args.legend = list(x=60,y=0.022,horiz=FALSE, ncol=5)) #beside=TRUE,xlab="joint",main="Landing Angular Momentum in Sagittal Plane",
rm(op)

zz=as.matrix(landing.means.zz)
er=as.matrix(landing.stds.zz)
erci=as.matrix(landing.ci.zz)
arrows(barz,zz+er, barz,zz, angle=90, code=3, length=0.05)
arrows(barz,zz-er, barz,zz, angle=90, code=3, length=0.05)
















# PLOT PAPER
################ ordered by mass
## medial-lateral # contribute: arms, forearms, hands, back, head, arms(-) (right sign opposed to left)
#'back','thigh_r','thigh_l','leg_r','leg_l','upper_arm_r','upper_arm_l','forearm_r','forearm_l','hand_r','hand_l'
simp_names = list('5%','20%','40%','100%')

landing.means.y <- structure(list(
  '5%'= c(meanDataLMy[1,12], meanDataLMy[1,2], meanDataLMy[1,7], meanDataLMy[1,3], meanDataLMy[1,8], meanDataLMy[1,14], meanDataLMy[1,20], meanDataLMy[1,15] + meanDataLMy[1,16], meanDataLMy[1,21] + meanDataLMy[1,22], meanDataLMy[1,18], meanDataLMy[1,24]),
  '20%' =c(meanDataLMy[1,12], meanDataLMy[1,2], meanDataLMy[1,7], meanDataLMy[1,3], meanDataLMy[1,8], meanDataLMy[2,14], meanDataLMy[2,20], meanDataLMy[2,15] + meanDataLMy[2,16], meanDataLMy[2,21] + meanDataLMy[2,22], meanDataLMy[2,18], meanDataLMy[2,24]),
  '40%' = c(meanDataLMy[1,12], meanDataLMy[1,2], meanDataLMy[1,7], meanDataLMy[1,3], meanDataLMy[1,8], meanDataLMy[3,14], meanDataLMy[3,20], meanDataLMy[3,15] + meanDataLMy[3,16] , meanDataLMy[3,21] + meanDataLMy[3,22], meanDataLMy[3,18], meanDataLMy[3,24]),
  '100%' = c(meanDataLMy[1,12], meanDataLMy[1,2], meanDataLMy[1,7], meanDataLMy[1,3], meanDataLMy[1,8], meanDataLMy[4,14], meanDataLMy[4,20], meanDataLMy[4,15] + meanDataLMy[4,16], meanDataLMy[4,21] +  meanDataLMy[4,22], meanDataLMy[4,18], meanDataLMy[4,24])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -11L))

#
landing.stds.y <- structure(list(
  '5%'= c(stdDataLMy[1,12], stdDataLMy[1,2], stdDataLMy[1,7], stdDataLMy[1,3], stdDataLMy[1,8], stdDataLMy[1,14], stdDataLMy[1,20], (stdDataLMy[1,15] +  stdDataLMy[1,16])/2, (stdDataLMy[1,21] + stdDataLMy[1,22])/2, stdDataLMy[1,18], stdDataLMy[1,24]),
  '20%' =c(stdDataLMy[2,12], stdDataLMy[2,2], stdDataLMy[2,7], stdDataLMy[2,3], stdDataLMy[2,8], stdDataLMy[2,14], stdDataLMy[2,20], (stdDataLMy[2,15] + stdDataLMy[2,16])/2, (stdDataLMy[2,21] + stdDataLMy[2,22])/2, stdDataLMy[2,18], stdDataLMy[2,24]),
  '40%' = c(stdDataLMy[3,12], stdDataLMy[3,2], stdDataLMy[3,7], stdDataLMy[3,3], stdDataLMy[3,8], stdDataLMy[3,14], stdDataLMy[3,20], (stdDataLMy[3,15] + stdDataLMy[3,16])/2, (stdDataLMy[3,21] + stdDataLMy[3,22])/2, stdDataLMy[3,18], stdDataLMy[3,24]),
  '100%' = c(stdDataLMy[4,12], stdDataLMy[4,2], stdDataLMy[4,7], stdDataLMy[4,3], stdDataLMy[4,8], stdDataLMy[4,14], stdDataLMy[4,20], (stdDataLMy[4,15] +  stdDataLMy[4,16])/2, (stdDataLMy[4,21] + stdDataLMy[4,22])/2, stdDataLMy[4,18], stdDataLMy[4,24])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -11L))

k=t/sqrt(nparticipants)
landing.ci.y <- structure(list(
  '5%'= c( k*stdDataLMy[1,12], k*stdDataLMy[1,2], k*stdDataLMy[1,7], k*stdDataLMy[1,3], k*stdDataLMy[1,8], k*stdDataLMy[1,14], k*stdDataLMy[1,20], k*((stdDataLMy[1,15] + stdDataLMy[1,16])/2), k*((stdDataLMy[1,21]+stdDataLMy[1,22])/2), k*stdDataLMy[1,18], k*stdDataLMy[1,24]),
  '20%' =c( k*stdDataLMy[1,12], k*stdDataLMy[1,2], k*stdDataLMy[1,7], k*stdDataLMy[1,3], k*stdDataLMy[1,8], k*stdDataLMy[2,14], k*stdDataLMy[2,20], k*((stdDataLMy[2,15] + stdDataLMy[2,16])/2), k*((stdDataLMy[2,21]+stdDataLMy[2,22])/2), k*stdDataLMy[2,18], k*stdDataLMy[2,24]),
  '40%' = c( k*stdDataLMy[1,12], k*stdDataLMy[1,2], k*stdDataLMy[1,7], k*stdDataLMy[1,3], k*stdDataLMy[1,8], k*stdDataLMy[3,14], k*stdDataLMy[3,20], k*((stdDataLMy[3,15] + stdDataLMy[3,16])/2), k*((stdDataLMy[3,21]+stdDataLMy[3,22])/2), k*stdDataLMy[3,18], k*stdDataLMy[3,24]),
  '100%' = c( k*stdDataLMy[1,12], k*stdDataLMy[1,2], k*stdDataLMy[1,7], k*stdDataLMy[1,3], k*stdDataLMy[1,8], k*stdDataLMy[4,14], k*stdDataLMy[4,20], k*((stdDataLMy[4,15] + stdDataLMy[4,16])/2), k*((stdDataLMy[4,21]+stdDataLMy[4,22])/2), k*stdDataLMy[4,18], k*stdDataLMy[4,24])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -11L))

op = par(mar=c(4,5,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(-landing.means.y), main="Force (ML)",
               ylab=expression(N %.% BW^-1),
               xlim=c(0,60),ylim=c(-0.15,0.15),
               col=c("red","green","blue","yellow","purple","azure2","beige","cyan","cadetblue4","brown","deeppink"),
               legend = c('back','thigh_r','thigh_l','leg_r','leg_l','upper_arm_r','upper_arm_l','forearm_r','forearm_l','hand_r','hand_l'), 
               las=2, cex.names = 1, beside=TRUE, args.legend = list(x=60,y=0.1,horiz=FALSE)) #beside=TRUE,xlab="joint",
rm(op)


xx=as.matrix(-landing.means.y)
er=as.matrix(-landing.stds.y)
erci=as.matrix(-landing.ci.y)
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
barx = barplot(as.matrix(-landing.means.x), main="Landing Force (AP)",
               ylab=expression(kg %.% m %.% s^-1 %.% BW^-1),
               xlim=c(0,35),ylim=c(-0.35,0.3),
               col=c("red","green","blue","yellow","purple","azure2","cadetblue"),
               legend = c( 'back','pelvis','thigh_r','thigh_l','head','leg_r','leg_l'), 
               las=2, cex.names = 1, beside=TRUE, args.legend = list(x=35,horiz=TRUE)) #beside=TRUE,xlab="joint",
rm(op)


xx=as.matrix(-landing.means.x)
er=as.matrix(-landing.stds.x)
erci=as.matrix(-landing.ci.x)
arrows(barx,xx+erci, barx,xx, angle=90, code=3, length=0.05)
arrows(barx,xx-erci, barx,xx, angle=90, code=3, length=0.05)


## vertical
simp_names = list('5%','20%','40%','100%')
landing.means.z <- structure(list(
  '5%'= c(meanDataLMz[1,12], meanDataLMz[1,1], meanDataLMz[1,13], meanDataLMz[1,5], meanDataLMz[1,10], meanDataLMz[1,6], meanDataLMz[1,11]),
  '20%' =c(meanDataLMz[2,12], meanDataLMz[2,1], meanDataLMz[2,13], meanDataLMz[1,5], meanDataLMz[1,10], meanDataLMz[1,6], meanDataLMz[1,11]),
  '40%' = c(meanDataLMz[3,12], meanDataLMz[3,1], meanDataLMz[3,13], meanDataLMz[1,5], meanDataLMz[1,10], meanDataLMz[1,6], meanDataLMz[1,11]),
  '100%' = c(meanDataLMz[4,12], meanDataLMz[4,1], meanDataLMz[4,13], meanDataLMz[1,5], meanDataLMz[1,10], meanDataLMz[1,6], meanDataLMz[1,11])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -7L))

#
landing.stds.z <- structure(list(
  '5%'= c(stdDataLMz[1,12], stdDataLMz[1,1], stdDataLMz[1,13], stdDataLMz[1,5], stdDataLMz[1,10], stdDataLMz[1,6], stdDataLMz[1,11]),
  '20%' =c(stdDataLMz[2,12], stdDataLMz[2,1], stdDataLMz[2,13], stdDataLMz[2,5], stdDataLMz[2,10], stdDataLMz[1,6], stdDataLMz[1,11]),
  '40%' = c(stdDataLMz[3,12], stdDataLMz[3,1], stdDataLMz[3,13], stdDataLMz[3,5], stdDataLMz[3,10], stdDataLMz[1,6], stdDataLMz[1,11]),
  '100%' = c(stdDataLMz[4,12], stdDataLMz[4,1], stdDataLMz[4,13], stdDataLMz[4,5], stdDataLMz[4,10], stdDataLMz[1,6], stdDataLMz[1,11])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -7L))

k=t/sqrt(nparticipants)
landing.ci.z <- structure(list(
  '5%'= c(k*stdDataLMz[1,12], k*stdDataLMz[1,1], k*stdDataLMz[1,13], k*stdDataLMz[1,5], k*stdDataLMz[1,10], k*stdDataLMz[1,6], k*stdDataLMz[1,11]),
  '20%' =c(k*stdDataLMz[2,12], k*stdDataLMz[2,1], k*stdDataLMz[2,13], k*stdDataLMz[1,5], k*stdDataLMz[2,10], k*stdDataLMz[2,6], k*stdDataLMz[2,11]),
  '40%' = c(k*stdDataLMz[3,12], k*stdDataLMz[3,1], k*stdDataLMz[3,13], k*stdDataLMz[1,5], k*stdDataLMz[3,10], k*stdDataLMz[3,6], k*stdDataLMz[3,11]),
  '100%' = c(k*stdDataLMz[4,12], k*stdDataLMz[4,1], k*stdDataLMz[4,13], k*stdDataLMz[1,5], k*stdDataLMz[4,10], k*stdDataLMz[4,6], k*stdDataLMz[4,11])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -7L))

op = par(mar=c(4,5,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(landing.means.z), main="Landing Force (V)",
               ylab=expression(N %.% BW^-1),
               xlim=c(0,35),ylim=c(-0.5,0.75),
               col=c("red","green","blue","yellow","purple","coral","cadetblue"),
               legend = c( "back","pelvis", "head", "foot_r","foot_l",'toes_r',"toes_l"),  
               las=2, cex.names = 1, beside=TRUE,args.legend = list(x=35, y=0.8,horiz=TRUE)) #beside=TRUE,xlab="joint",
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
               xlim=c(0,35),ylim=c(-0.08, 0.05),
               col=c("red","green","blue","yellow","purple","azure2","cadetblue"),
               legend = c( 'back','pelvis','thigh_r','thigh_l','head','leg_r','leg_l'),  
               las=2, cex.names = 1, beside=TRUE,args.legend = list(x=35,horiz=TRUE)) #beside=TRUE,xlab="joint",main="Landing Angular Momentum in Sagittal Plane",
rm(op)

xx=as.matrix(-landing.means.yy)
er=as.matrix(landing.stds.yy)
erci=as.matrix(landing.ci.yy)
arrows(barx,xx+erci, barx,xx, angle=90, code=3, length=0.05)
arrows(barx,xx-erci, barx,xx, angle=90, code=3, length=0.05)




## vertical torque
# contribute: pelvis, thighs, legs, back, head
simp_names = list('5%','20%','40%','100%')
landing.means.zz <- structure(list(
  '5%'= c(meanDataAMz[1,12], meanDataAMz[1,1], meanDataAMz[1,2], meanDataAMz[1,7], meanDataAMz[1,13], meanDataAMz[1,3], meanDataAMz[1,8]),
  '20%' =c(meanDataAMz[2,12], meanDataAMz[2,1], meanDataAMz[2,2], meanDataAMz[2,7], meanDataAMz[2,13], meanDataAMz[2,3], meanDataAMz[2,8]),
  '40%' = c(meanDataAMz[3,12], meanDataAMz[3,1], meanDataAMz[3,2], meanDataAMz[3,7], meanDataAMz[3,13], meanDataAMz[3,3], meanDataAMz[3,8]),
  '100%' = c(meanDataAMz[4,12], meanDataAMz[4,1], meanDataAMz[4,2], meanDataAMz[4,7], meanDataAMz[4,13], meanDataAMz[4,3], meanDataAMz[4,8])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -7L))

#
landing.stds.zz <- structure(list(
  '5%'= c(stdDataAMz[1,12], stdDataAMz[1,1], stdDataAMz[1,2], stdDataAMz[1,7], stdDataAMz[1,13], stdDataAMz[1,3], stdDataAMz[1,8]),
  '20%' =c(stdDataAMz[2,12], stdDataAMz[2,1], stdDataAMz[2,2], stdDataAMz[2,7], stdDataAMz[2,13], stdDataAMz[2,3], stdDataAMz[2,8]),
  '40%' = c(stdDataAMz[3,12], stdDataAMz[3,1], stdDataAMz[3,2], stdDataAMz[3,7], stdDataAMz[3,13], stdDataAMz[3,3], stdDataAMz[3,8]),
  '100%' = c(stdDataAMz[4,12], stdDataAMz[4,1], stdDataAMz[4,2], stdDataAMz[4,7], stdDataAMz[4,13], stdDataAMz[4,3], stdDataAMz[4,8])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -7L))

k=t/sqrt(nparticipants)
landing.ci.zz <- structure(list(
  '5%'= c(k*stdDataAMz[1,12], k*stdDataAMz[1,1], k*stdDataAMz[1,2], k*stdDataAMz[1,7], k*stdDataAMz[1,13], k*stdDataAMz[1,3], k*stdDataAMz[1,8]),
  '20%' =c(k*stdDataAMz[2,12], k*stdDataAMz[2,1], k*stdDataAMz[2,2], k*stdDataAMz[2,7], k*stdDataAMz[2,13], k*stdDataAMz[2,3], k*stdDataAMz[2,8]),
  '40%' = c(k*stdDataAMz[3,12], k*stdDataAMz[3,1], k*stdDataAMz[3,2], k*stdDataAMz[3,7], k*stdDataAMz[3,13], k*stdDataAMz[3,3], k*stdDataAMz[3,8]),
  '100%' = c(k*stdDataAMz[4,12], k*stdDataAMz[4,1], k*stdDataAMz[4,2], k*stdDataAMz[4,7], k*stdDataAMz[4,13], k*stdDataAMz[4,3], k*stdDataAMz[4,8])
), 
.Names = simp_names, 
class = "data.frame", row.names = c(NA, -7L))

op = par(mar=c(5,5,4,2)) # c(bottom, left, top, right) which gives the number of lines of margin
barx = barplot(as.matrix(landing.means.zz), 
               ylab=expression(kg %.% m^2 %.% s^-1 %.% BW^-1 %.% H^-1),
               xlim=c(0,35),ylim=c(-0.02, 0.02),
               col=c("red","green","blue","yellow","purple","azure2","cadetblue"),
               legend = c( 'back','pelvis','thigh_r','thigh_l','head','leg_r','leg_l'),  
               las=2, cex.names = 1, beside=TRUE,args.legend = list(x=35,horiz=TRUE)) #beside=TRUE,xlab="joint",main="Landing Angular Momentum in Sagittal Plane",
rm(op)

xx=as.matrix(landing.means.zz)
er=as.matrix(landing.stds.zz)
erci=as.matrix(landing.ci.zz)
arrows(barx,xx+erci, barx,xx, angle=90, code=3, length=0.05)
arrows(barx,xx-erci, barx,xx, angle=90, code=3, length=0.05)