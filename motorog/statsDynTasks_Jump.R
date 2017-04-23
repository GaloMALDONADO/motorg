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
#----------------------------------------*********************+5fasd
t.test(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="1" & SOT_IMPULSE$Phase=="0"], mu = 0)

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
#----------------------------------------*********************+5fasd
t.test(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="2" & SOT_IMPULSE$Phase=="0"], mu = 0)

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

barx = barplot(as.matrix(jump.means), main="Takeoff",
                xlab="Phase of the motion", ylab="Index of Motor Task Control",
                xlim=c(0,13),ylim=c(-0.5,8),
                col=c("blue","red"),
                legend = c( "Force task","Torque task"), beside=TRUE)

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
  text(x[1]+((x[2]-x[1])/2),y+0.2,s)
}

# capture x coordinates of bars
x <- barx
# create the y coordinate of the line
y <- 2
# set an offset for tick lengths
offset1 <- 0.2
offset2 <- 0.2

displayEffects(x[1:2], 7.1, offset1, 3.5, '*')
displayEffects(x[3:4], 4.8, offset1, 2.2, '*')
displayEffects(x[5:6], 6.1, offset1, 4, '*')
displayEffects(x[7:8], 4.7, offset1, 0.9, '*')

#vector <- c((x[1]+x[2])/2, (x[7]+x[8])/2)
#displayEffects(array(vector), -1.95, -1.7, -1.7, '**')
#vector <- c((x[3]+x[4])/2, (x[7]+x[8])/2)
#displayEffects(array(vector), -1.4, -1.15, -1.15, '**')
#vector <- c((x[5]+x[6])/2, (x[7]+x[8])/2)
#displayEffects(array(vector), -0.9, -0.65, -0.65, '**')

# ----------------------------- Repeated Measures Anova ---------------------------
# compute repetitive measures anova
aovstats <-aov(SOT_IMPULSE$Ratio ~ 
               (SOT_IMPULSE$Task+SOT_IMPULSE$Phase) + 
               Error(SOT_IMPULSE$Participant  / (SOT_IMPULSE$Task+SOT_IMPULSE$Phase)), 
               data = SOT_IMPULSE)
summary(aovstats)
# tasks are significantly differents p = 0.00425 ** <0.01
# phases are not significantly differents p = 6.15e-06 *** < 0.05


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

