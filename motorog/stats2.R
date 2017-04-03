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
pathName = paste(p,'TableCriteriaImpulse.csv',sep="")
SOT_IMPULSE = read.csv(pathName,
                      header = FALSE, 
                      col.names = list('Participant', 'Phase', 'Task', 'Ratio'))
SOT_IMPULSE$Participant<-as.factor(SOT_IMPULSE$Participant)
SOT_IMPULSE$Phase<-as.factor(SOT_IMPULSE$Phase)
SOT_IMPULSE$Task<-as.factor(SOT_IMPULSE$Task)

# -----------------  Assess Normality of the Data -------------------------
shapiro.test(SOT_IMPULSE$Ratio)
# p = 0.4278, p>0.05 => data is normal
shapiro.test(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="1" & SOT_IMPULSE$Phase=="0"])
# data normally distributed
shapiro.test(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="1" & SOT_IMPULSE$Phase=="40"])
# data normally distributed
shapiro.test(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="1" & SOT_IMPULSE$Phase=="70"])
# data normally distributed
shapiro.test(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="1" & SOT_IMPULSE$Phase=="99"])
# data normally distributed

shapiro.test(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="2" & SOT_IMPULSE$Phase=="0"])
# data normally distributed
shapiro.test(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="2" & SOT_IMPULSE$Phase=="40"])
# data normally distributed
shapiro.test(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="2" & SOT_IMPULSE$Phase=="70"])
# data normally distributed
shapiro.test(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="2" & SOT_IMPULSE$Phase=="99"])
# data normally distributed

#variance equality
# -------------------------- Plot ------------------------------------------
# Plot means and std
boxplot(SOT_IMPULSE$Ratio~SOT_IMPULSE$Task) # impulsionLM mean > impulsionAM mean 
boxplot(SOT_IMPULSE$Ratio~SOT_IMPULSE$Phase) # tasks are more controlled at 99% phase
boxplot(SOT_IMPULSE$Ratio~SOT_IMPULSE$Task:SOT_IMPULSE$Phase) # impulsionLM is more controlled than impulsionAM at all time
# AM is not controlled at 40% and 70%

# Plot the means and stds/CI as error bars
meanImpLM1 = mean(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="1" & SOT_IMPULSE$Phase=="0"])
stdImpLM1 = sd(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="1" & SOT_IMPULSE$Phase=="0"])
ciImpLM1 = t * stdImpLM1 / sqrt(nparticipants)
ciPlusImpLM1 = meanImpLM1 + ciImpLM1 
ciMinImpLM1 = meanImpLM1 - ciImpLM1 

meanImpLM40 = mean(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="1" & SOT_IMPULSE$Phase=="40"])
stdImpLM40 = sd(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="1" & SOT_IMPULSE$Phase=="40"])
ciImpLM40 = t * stdImpLM40 / sqrt(nparticipants)
ciPlusImpLM40 = meanImpLM40 + ciImpLM40 
ciMinImpLM40 = meanImpLM40 - ciImpLM40 

meanImpLM70 = mean(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="1"& SOT_IMPULSE$Phase=="70"])
stdImpLM70 = sd(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="1" & SOT_IMPULSE$Phase=="70"])
ciImpLM70 = t * stdImpLM70 / sqrt(nparticipants)
ciPlusImpLM70 = meanImpLM70 + ciImpLM70
ciMinImpLM70 = meanImpLM70 - ciImpLM70

meanImpLM100 = mean(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="1"& SOT_IMPULSE$Phase=="99"])
stdImpLM100 = sd(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="1" & SOT_IMPULSE$Phase=="99"])
ciImpLM100 = t * stdImpLM100 / sqrt(nparticipants)
ciPlusImpLM100 = meanImpLM100 + ciImpLM100
ciMinImpLM100 = meanImpLM100 - ciImpLM100

meanImpAM1 = mean(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="2" & SOT_IMPULSE$Phase=="0"])
stdImpAM1 = sd(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="2" & SOT_IMPULSE$Phase=="0"])
ciImpAM1 = t * stdImpAM1 / sqrt(nparticipants)
ciPlusImpAM1 = meanImpAM1 + ciImpAM1
ciMinImpAM1 = meanImpAM1 - ciImpAM1

meanImpAM40= mean(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="2" & SOT_IMPULSE$Phase=="40"])
stdImpAM40= sd(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="2" & SOT_IMPULSE$Phase=="40"])
ciImpAM40 = t * stdImpAM40 / sqrt(nparticipants)
ciPlusImpAM40 = meanImpAM40 + ciImpAM40
ciMinImpAM40 = meanImpAM40 - ciImpAM40

meanImpAM70= mean(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="2" & SOT_IMPULSE$Phase=="70"])
stdImpAM70= sd(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="2" & SOT_IMPULSE$Phase=="70"])
ciImpAM70 = t * stdImpAM70 / sqrt(nparticipants)
ciPlusImpAM70 = meanImpAM70 + ciImpAM70
ciMinImpAM70 = meanImpAM70 - ciImpAM70

meanImpAM100= mean(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="2" & SOT_IMPULSE$Phase=="99"])
stdImpAM100= sd(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="2" & SOT_IMPULSE$Phase=="99"])
ciImpAM100 = t * stdImpAM100 / sqrt(nparticipants)
ciPlusImpAM100 = meanImpAM100 + ciImpAM100
ciMinImpAM100 = meanImpAM100 - ciImpAM100

jump.means <- structure(list('1'=c(meanImpLM1,meanImpAM1),
                             '40'=c(meanImpLM40, meanImpAM40),
                             '70'=c(meanImpLM70, meanImpAM70),
                             '100'=c(meanImpLM100, meanImpAM100)), 
                              .Names = c("1%", "40%",  "70%", "100%"), 
                              class = "data.frame", row.names = c(NA, -2L))

barx = barplot(as.matrix(jump.means), main="Jump",
                xlab="Phase of the motion", ylab="Index of Motor Task Control",
                xlim=c(0,13),ylim=c(-2.5,4),
                col=c("blue","red"),
                legend = c( "Force Task","Torque Task"), beside=TRUE)

jump.stds <- structure(list('1'=c(stdImpLM1,stdImpAM1),
                             '40'=c(stdImpLM40, stdImpAM40),
                             '70'=c(stdImpLM70, stdImpAM70), 
                             '100'=c(stdImpLM100, stdImpAM100)),
                       .Names = c("1%", "40%",  "70%", "100%"),
                        class = "data.frame", row.names = c(NA, -2L))

jump.ci <- structure(list('1'=c(ciImpLM1, ciImpAM1),
                          '40'=c(ciImpLM40, ciImpAM40),
                          '70'=c(ciImpLM70, ciImpAM70), 
                         '100'=c(ciImpLM100, ciImpAM100)),
                     .Names = c("1%", "40%",  "70%", "100%"),
                     class = "data.frame", row.names = c(NA, -2L))

xx=as.matrix(jump.means)
er=as.matrix(jump.stds)
erci=as.matrix(jump.ci)
arrows(barx,xx+erci, barx,xx, angle=90, code=3, length=0.05)
arrows(barx,xx-erci, barx,xx, angle=90, code=3, length=0.05)

# unconmment to plot with SD
#arrows(barx,x+er, barx,xx, angle=90, code=3, length=0.05)


# --------- add significant effects to plot 
displayEffects <- function(x, y, offset1, offset2, s='*'){
  # draw first horizontal line
  lines(x[1:2],c(y, y), type = "l", pch=22, lty=2)
  # draw ticks
  lines(x[c(1,1)],c(y, y-offset1), type = "l", pch=22, lty=2)
  lines(x[c(2,2)],c(y, y-offset2), type = "l", pch=22, lty=2)
  # draw asterics
  text(x[1]+((x[2]-x[1])/2),y+offset,s)
}

# capture x coordinates of bars
x <- barx
# create the y coordinate of the line
y <- 2
# set an offset for tick lengths
offset1 <- 0.2
offset2 <- 0.2

displayEffects(x[1:2], 2.1, offset1, 1.3, '*')
displayEffects(x[3:4], 0.7, offset1, offset2, '*')
displayEffects(x[5:6], 1.5, offset1, 0.95, '*')
displayEffects(x[7:8], 2.5, offset1, 0.6, '*')

vector <- c((x[1]+x[2])/2, (x[7]+x[8])/2)
displayEffects(array(vector), -1.95, -1.7, -1.7, '**')
vector <- c((x[3]+x[4])/2, (x[7]+x[8])/2)
displayEffects(array(vector), -1.4, -1.15, -1.15, '**')
vector <- c((x[5]+x[6])/2, (x[7]+x[8])/2)
displayEffects(array(vector), -0.9, -0.65, -0.65, '**')

# ----------------------------- Repeated Measures Anova ---------------------------
# compute repetitive measures anova
aovstats <-aov(SOT_IMPULSE$Ratio ~ 
               (SOT_IMPULSE$Task*SOT_IMPULSE$Phase) + 
               Error(SOT_IMPULSE$Participant  / (SOT_IMPULSE$Task*SOT_IMPULSE$Phase)), 
               data = SOT_IMPULSE)
summary(aovstats)
# tasks are significantly differents p = 0.00425 ** <0.01
# phases are significantly differents p = 6.15e-06 *** < 0.05
# task:phases interactions are not significantly different

# Effect Size
# of the tasks
aov_sum_sq = 5.779
aov_resid = 0.674
etacarrePartiel<-aov_sum_sq/(aov_sum_sq+aov_resid)
# 89% of the variance of tha ratios explains the variation of the tasks
ftailleEffet<-sqrt(etacarrePartiel/(1-etacarrePartiel))
# effect fort : ftaill = 2.928 (f/2 = 1.464). Effect is independent of the size

# of phases
aov_sum_sq = 8.662
aov_resid = 1.035
etacarrePartiel<-aov_sum_sq/(aov_sum_sq+aov_resid)
# 89.3% of the variance of tha ratios explains the variation of the tasks
ftailleEffet<-sqrt(etacarrePartiel/(1-etacarrePartiel))
# strong effect : ftail = 2.89 (f/2 = 1.445). Effect is independent of the size

# POST-HOC
# Compare tasks
pairwise.t.test(SOT_IMPULSE$Ratio, SOT_IMPULSE$Task, p.adj = "bonf",paired=TRUE)
# impulsionLM and impulsionAM are significantly different p = 6.2e-06
# Linear Momentum > Angular Momentum

# compare phases
pairwise.t.test(SOT_IMPULSE$Ratio, SOT_IMPULSE$Phase, p.adj = "bonf",paired=TRUE)
# 0 diff than 99, p=0.0116
# 40 diff than 99, p=5.5e-05
# 70 diff than 99, p=0.0014












# ----------------------------------------------
#                 Landing
# Task 1: vertical force 
# Task 2: M-L and A-P force. Stability
# Task 3: Torque around M-L axis at the CoM
# ----------------------------------------------
rm(list = ls())
#p='/galo/devel/gepetto/motorg/motorog/' #home
p='/local/gmaldona/devel/motorg/motorog/' #lab
nparticipants = 5
ddl=nparticipants-1
t = qt(.975,ddl)

# ---------------------- Read the data -----------------------------------
pathName = paste(p,'TableCriteriaLand.csv',sep="")
SOT_LAND = read.csv(pathName, header = FALSE, col.names = list('Participant', 'Phase', 'Task', 'Ratio'))
SOT_LAND$Participant<-as.factor(SOT_LAND$Participant)
SOT_LAND$Phase<-as.factor(SOT_LAND$Phase)
SOT_LAND$Task<-as.factor(SOT_LAND$Task)


# -----------------  Assess Normality of the Data -------------------------
shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="5"])
# data normally distributed
shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="20"])
# data normally distributed
shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="40"])
# data normally distributed
shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="99"])
# data normally distributed

shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="2" & SOT_LAND$Phase=="5"])
# data normally distributed
shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="2" & SOT_LAND$Phase=="20"])
# data normally distributed
shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="2" & SOT_LAND$Phase=="40"])
# data normally distributed
shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="2" & SOT_LAND$Phase=="99"])
# data not ormally distributed ***************

shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="3" & SOT_LAND$Phase=="5"])
# data normally distributed
shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="3" & SOT_LAND$Phase=="20"])
# data normally distributed
shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="3" & SOT_LAND$Phase=="40"])
# data normally distributed
shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="3" & SOT_LAND$Phase=="99"])
# data normally distributed


#variance equality



# -------------------------- Plot ------------------------------------------
# Plot means and std
boxplot(SOT_LAND$Ratio~SOT_LAND$Task)
# stability > Force > Tau
boxplot(SOT_LAND$Ratio~SOT_LAND$Phase)
# tasks are similarly controlled at all phases
boxplot(SOT_LAND$Ratio~SOT_LAND$Task:SOT_LAND$Phase)
# 5% -- force is more controlled.
# 20% -- stability is more controlled.
# 40% -- stability is more controlled. Tau is not controlled.
# 100% -- stability and force are more controlled. Tau is not controlled.

# Plot the means and stds/CI as error bars
meanForce5 = mean(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="5"])
stdForce5 = sd(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="5"])
ciForce5 = t * stdForce5 / sqrt(nparticipants)
ciPlusForce5 = meanForce5 + ciForce5 
ciMinForce5 = meanForce5 - ciForce5 

meanForce20 = mean(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="20"])
stdForce20 = mean(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="20"])
ciForce20 = t * stdForce20 / sqrt(nparticipants)
ciPlusForce5 = meanForce20 + ciForce20 
ciMinForce5 = meanForce20 - ciForce20 

meanForce40= mean(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="40"])
stdForce40= mean(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="40"])
ciForce40 = t * stdForce40 / sqrt(nparticipants)
ciPlusForce40 = meanForce40 + ciForce40 
ciMinForce40 = meanForce40 - ciForce40 

meanForce100= mean(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="99"])
stdForce100= mean(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="99"])
ciForce100 = t * stdForce5 / sqrt(nparticipants)
ciPlusForce100 = meanForce100 + ciForce100 
ciMinForce100 = meanForce100 - ciForce100 

#

meanStab5 = mean(SOT_LAND$Ratio[SOT_LAND$Task=="2" & SOT_LAND$Phase=="5"])
stdStab5 = sd(SOT_LAND$Ratio[SOT_LAND$Task=="2" & SOT_LAND$Phase=="5"])
ciStab5 = t * stdStab5 / sqrt(nparticipants)
ciPlusStab5 = meanStab5 + ciStab5 
ciMinStab5 = meanStab5 - ciStab5

meanStab20= mean(SOT_LAND$Ratio[SOT_LAND$Task=="2" & SOT_LAND$Phase=="20"])
stdStab20= sd(SOT_LAND$Ratio[SOT_LAND$Task=="2" & SOT_LAND$Phase=="20"])
ciStab20 = t * stdStab20 / sqrt(nparticipants)
ciPlusStab20 = meanStab20 + ciStab20 
ciMinStab20 = meanStab20 - ciStab20

meanStab40= mean(SOT_LAND$Ratio[SOT_LAND$Task=="2" & SOT_LAND$Phase=="40"])
stdStab40= sd(SOT_LAND$Ratio[SOT_LAND$Task=="2" & SOT_LAND$Phase=="40"])
ciStab40 = t * stdStab40 / sqrt(nparticipants)
ciPlusStab40 = meanStab40 + ciStab40 
ciMinStab40 = meanStab40 - ciStab40

meanStab100= mean(SOT_LAND$Ratio[SOT_LAND$Task=="2" & SOT_LAND$Phase=="99"])
stdStab100= mean(SOT_LAND$Ratio[SOT_LAND$Task=="2" & SOT_LAND$Phase=="99"])
ciStab100 = t * stdStab100 / sqrt(nparticipants)
ciPlusStab100 = meanStab100 + ciStab100 
ciMinStab100 = meanStab100 - ciStab100

#

meanTau5 = mean(SOT_LAND$Ratio[SOT_LAND$Task=="3" & SOT_LAND$Phase=="5"])
stdTau5 = sd(SOT_LAND$Ratio[SOT_LAND$Task=="3" & SOT_LAND$Phase=="5"])
ciTau5 = t * stdTau5 / sqrt(nparticipants)
ciPlusTau5 = meanTau5 + ciTau5 
ciMinTau5 = meanTau5 - ciTau5 

meanTau20 = mean(SOT_LAND$Ratio[SOT_LAND$Task=="3" & SOT_LAND$Phase=="20"])
stdTau20 = sd(SOT_LAND$Ratio[SOT_LAND$Task=="3" & SOT_LAND$Phase=="20"])
ciTau20 = t * stdTau20 / sqrt(nparticipants)
ciPlusTau20 = meanTau20 + ciTau20 
ciMinTau20 = meanTau20 - ciTau20 

meanTau40 = mean(SOT_LAND$Ratio[SOT_LAND$Task=="3" & SOT_LAND$Phase=="40"])
stdTau40 = sd(SOT_LAND$Ratio[SOT_LAND$Task=="3" & SOT_LAND$Phase=="40"])
ciTau40 = t * stdTau40 / sqrt(nparticipants)
ciPlusTau40 = meanTau40 + ciTau40 
ciMinTau40 = meanTau40 - ciTau40 

meanTau100 = mean(SOT_LAND$Ratio[SOT_LAND$Task=="3" & SOT_LAND$Phase=="99"])
stdTau100 = mean(SOT_LAND$Ratio[SOT_LAND$Task=="3" & SOT_LAND$Phase=="99"])
ciTau100 = t * stdTau100 / sqrt(nparticipants)
ciPlusTau100 = meanTau100 + ciTau100 
ciMinTau100 = meanTau100 - ciTau100 



land.means <- structure(list('5'=c(meanForce5,  meanStab5, meanTau5),
                            '20'=c(meanForce20, meanStab20, meanTau20),
                            '40'=c(meanForce40, meanStab40, meanTau40),
                            '100'=c(meanForce100, meanStab100, meanTau100)), 
                       .Names = c("5%", "20%", "40%","100%"), 
                       class = "data.frame", row.names = c(NA, -3L))
barx = barplot(as.matrix(land.means), main="Landing",
               xlab="Phase of the motion", ylab="Index of Motor Task Control",
               xlim=c(0,15),ylim=c(0,4.5),
               col=c("red","green","blue"),
               legend = c( "Vertical Force","Stability Forces","Torque CoM"), beside=TRUE)

land.stds <- structure(list('5'=c(stdForce5,  stdStab5, stdTau5),
                            '20'=c(stdForce20, stdStab20, stdTau20),
                            '40'=c(stdForce40, stdStab40, stdTau40),
                            '100'=c(stdForce100, stdStab100, stdTau100)), 
                       .Names = c("5%", "20%", "40%","100%"), 
                       class = "data.frame", row.names = c(NA, -3L))

land.ci <- structure(list('5'=c(ciForce5,  ciStab5, ciTau5),
                            '20'=c(ciForce20, ciStab20, ciTau20),
                            '40'=c(ciForce40, ciStab40, ciTau40),
                            '100'=c(ciForce100, ciStab100, ciTau100)), 
                       .Names = c("5%", "20%", "40%","100%"), 
                       class = "data.frame", row.names = c(NA, -3L))

xx=as.matrix(land.means)
er=as.matrix(land.stds)
erci=as.matrix(land.ci)
arrows(barx,xx+erci, barx,xx, angle=90, code=3, length=0.05)
arrows(barx,xx-erci, barx,xx, angle=90, code=3, length=0.05)
# unconmment to plot with SD
#arrows(barx,x+er, barx,xx, angle=90, code=3, length=0.05)


# --------- add significant effects to plot 
displayEffects <- function(x, y, offset1, offset2, s='*'){
  # draw first horizontal line
  lines(x[1:2],c(y, y), type = "l", pch=22, lty=2)
  # draw ticks
  lines(x[c(1,1)],c(y, y-offset1), type = "l", pch=22, lty=2)
  lines(x[c(2,2)],c(y, y-offset2), type = "l", pch=22, lty=2)
  # draw asterics
  text(x[1]+((x[2]-x[1])/2),y+offset,s)
}



# ----------------------------- Repeated Measures Anova ---------------------------
# compute repetitive measures anova
statsaov2 <-aov(SOT_LAND$Ratio ~ (SOT_LAND$Task*SOT_LAND$Phase) + 
                  Error(SOT_LAND$Participant / (SOT_LAND$Task*SOT_LAND$Phase)), 
                data = SOT_LAND)
summary(statsaov2) 
# tasks are significantly differents p = 1.96e-06 ***
# phases are not significantly differents
# tasks:phase interactions are significant p=7.9e-08 ***


# Effect Size
# of the tasks
aov_sum_sq = 11.149
aov_resid = 0.433
etacarrePartiel<-aov_sum_sq/(aov_sum_sq+aov_resid)
# 96% of the variance of tha ratios explains the variation of the tasks 
ftailleEffet<-sqrt(etacarrePartiel/(1-etacarrePartiel))
# strong effect : ftaill = 5.074 (f/3 = 1.69). Effect is independent of the size

# of phases
aov_sum_sq = 6.398
aov_resid = 1.416
etacarrePartiel<-aov_sum_sq/(aov_sum_sq+aov_resid)
# 81.8% of the variance of tha ratios explains the variation of the tasks with the phases
ftailleEffet<-sqrt(etacarrePartiel/(1-etacarrePartiel))
# strong effect: ftaill = 2.125 (f/3 = 0.70). Effect is independent of the size

# POST-HOC
# Compare tasks
pairwise.t.test(SOT_LAND$Ratio, SOT_LAND$Task, p.adj = "bonf",paired=TRUE)
# task 1 (V force) signifficantly different from task 3 (Torque CoM)
# task 2 (Stability Forces) signifficantly different from task 3 (Torque CoM)
# task 1 (V force) signifficantly different from task 2 (Stability Forces) 

# compare phases
pairwise.t.test(SOT_LAND$Ratio, SOT_LAND$Task:SOT_LAND$Phase, p.adj = "bonf",paired=TRUE)
# 1:99 with 3:99, p = 0.025
# 2:20 with 1:20, p = 0.05
# 2:20 with 3:40, p = 0.019
# 2:20 with 3:99, p = 0.042
# 2:40 with 3:40, p = 0.019
# 2:99 with 3:99, p = 0.022


