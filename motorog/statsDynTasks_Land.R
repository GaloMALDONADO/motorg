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
pathName = paste(p,'TableCriteriaLand.csv',sep="")
SOT_LAND = read.csv(pathName, header = FALSE, col.names = list('Participant', 'Phase', 'Task', 'Ratio'))
SOT_LAND$Participant<-as.factor(SOT_LAND$Participant)
SOT_LAND$Phase<-as.factor(SOT_LAND$Phase)
SOT_LAND$Task<-as.factor(SOT_LAND$Task)


# -----------------  Assess Normality of the Data -------------------------
shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="4"])
# data normally distributed
shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="13"])
# data normally distributed
shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="20"])
# data normally distributed
shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="40"])
# data normally distributed
shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="97"])

shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="2" & SOT_LAND$Phase=="4"])
# data normally distributed
shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="2" & SOT_LAND$Phase=="13"])
# data normally distributed
shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="2" & SOT_LAND$Phase=="20"])
# data normally distributed
shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="2" & SOT_LAND$Phase=="40"])
shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="2" & SOT_LAND$Phase=="97"])

shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="3" & SOT_LAND$Phase=="4"])
# data normally distributed
shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="3" & SOT_LAND$Phase=="13"])
# data normally distributed
shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="3" & SOT_LAND$Phase=="20"])
# data normally distributed
shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="3" & SOT_LAND$Phase=="40"])
# data normally distributed
shapiro.test(SOT_LAND$Ratio[SOT_LAND$Task=="3" & SOT_LAND$Phase=="97"])

#variance equality



# -------------------------- Plot ------------------------------------------
# Plot means and std
boxplot(SOT_LAND$Ratio~SOT_LAND$Task)
# stability > Force > Tau
boxplot(SOT_LAND$Ratio~SOT_LAND$Phase)
# tasks are similarly controlled at all phases
boxplot(SOT_LAND$Ratio~SOT_LAND$Task:SOT_LAND$Phase)
# 4% -- force is more controlled.
# 20% -- stability is more controlled.
# 40% -- stability is more controlled. Tau is not controlled.
# 100% -- stability and force are more controlled. Tau is not controlled.

# Plot the means and stds/CI as error bars
meanForce4 = mean(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="4"])
stdForce4 = sd(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="4"])
ciForce4 = t * stdForce4 / sqrt(nparticipants)
ciPlusForce4 = meanForce4 + ciForce4 
ciMinForce4 = meanForce4 - ciForce4 

meanForce13 = mean(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="13"])
stdForce13 = sd(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="13"])
ciForce13 = (t * stdForce13 / sqrt(nparticipants))
ciPlusForce13 = (meanForce13 + ciForce13)
ciMinForce13 = (meanForce13 - ciForce13 )

meanForce20 = mean(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="20"])
stdForce20 = sd(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="20"])
ciForce20 = t * stdForce20 / sqrt(nparticipants)
ciPlusForce20 = meanForce20 + ciForce20 
ciMinForce20 = meanForce20 - ciForce20 

meanForce40= mean(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="40"])
stdForce40= sd(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="40"])
ciForce40 = t * stdForce40 / sqrt(nparticipants)
ciPlusForce40 = meanForce40 + ciForce40 
ciMinForce40 = meanForce40 - ciForce40 

meanForce100= mean(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="97"])
stdForce100= sd(SOT_LAND$Ratio[SOT_LAND$Task=="1" & SOT_LAND$Phase=="97"])
ciForce100 = t * stdForce100 / sqrt(nparticipants)
ciPlusForce100 = meanForce100 + ciForce100 
ciMinForce100 = meanForce100 - ciForce100 

#

meanStab4 = mean(SOT_LAND$Ratio[SOT_LAND$Task=="2" & SOT_LAND$Phase=="4"])
stdStab4 = sd(SOT_LAND$Ratio[SOT_LAND$Task=="2" & SOT_LAND$Phase=="4"])
ciStab4 = t * stdStab4 / sqrt(nparticipants)
ciPlusStab4 = meanStab4 + ciStab4 
ciMinStab4 = meanStab4 - ciStab4

meanStab13= mean(SOT_LAND$Ratio[SOT_LAND$Task=="2" & SOT_LAND$Phase=="13"])
stdStab13= sd(SOT_LAND$Ratio[SOT_LAND$Task=="2" & SOT_LAND$Phase=="13"])
ciStab13 = t * stdStab13 / sqrt(nparticipants)
ciPlusStab13 = meanStab13 + ciStab13 
ciMinStab13 = meanStab13 - ciStab13

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

meanStab100= mean(SOT_LAND$Ratio[SOT_LAND$Task=="2" & SOT_LAND$Phase=="97"])
stdStab100= sd(SOT_LAND$Ratio[SOT_LAND$Task=="2" & SOT_LAND$Phase=="97"])
ciStab100 = t * stdStab100 / sqrt(nparticipants)
ciPlusStab100 = meanStab100 + ciStab100 
ciMinStab100 = meanStab100 - ciStab100

#

meanTau4 = mean(SOT_LAND$Ratio[SOT_LAND$Task=="3" & SOT_LAND$Phase=="4"])
stdTau4 = sd(SOT_LAND$Ratio[SOT_LAND$Task=="3" & SOT_LAND$Phase=="4"])
ciTau4 = t * stdTau4 / sqrt(nparticipants)
ciPlusTau4 = meanTau4 + ciTau4 
ciMinTau4 = meanTau4 - ciTau4 

meanTau13 = mean(SOT_LAND$Ratio[SOT_LAND$Task=="3" & SOT_LAND$Phase=="13"])
stdTau13 = sd(SOT_LAND$Ratio[SOT_LAND$Task=="3" & SOT_LAND$Phase=="13"])
ciTau13 = t * stdTau13 / sqrt(nparticipants)
ciPlusTau13 = meanTau13 + ciTau13 
ciMinTau13 = meanTau13 - ciTau13


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

meanTau100 = mean(SOT_LAND$Ratio[SOT_LAND$Task=="3" & SOT_LAND$Phase=="97"])
stdTau100 = sd(SOT_LAND$Ratio[SOT_LAND$Task=="3" & SOT_LAND$Phase=="97"])
ciTau100 = t * stdTau100 / sqrt(nparticipants)
ciPlusTau100 = meanTau100 + ciTau100 
ciMinTau100 = meanTau100 - ciTau100 



land.means <- structure(list('4'=c(meanForce4,  meanStab4, meanTau4),
                             '13'=c(meanForce13, meanStab13, meanTau13),
                            '20'=c(meanForce20, meanStab20, meanTau20),
                            '40'=c(meanForce40, meanStab40, meanTau40),
                            '100'=c(meanForce100, meanStab100, meanTau100)), 
                       .Names = c("4%", "13%", "20%", "40%","100%"), 
                       class = "data.frame", row.names = c(NA, -3L))

land.stds <- structure(list('4'=c(stdForce4,  stdStab4, stdTau4),
                            '20'=c(stdForce13, stdStab13, stdTau13),
                            '13'=c(stdForce20, stdStab20, stdTau20),
                            '40'=c(stdForce40, stdStab40, stdTau40),
                            '100'=c(stdForce100, stdStab100, stdTau100)), 
                       .Names = c("4%","13%" ,"20%", "40%","100%"), 
                       class = "data.frame", row.names = c(NA, -3L))

land.ci <- structure(list('4'=c(ciForce4,  ciStab4, ciTau4),
                          '13'=c(ciForce13, ciStab13, ciTau13),
                          '20'=c(ciForce20, ciStab20, ciTau20),
                          '40'=c(ciForce40, ciStab40, ciTau40),
                          '100'=c(ciForce100, ciStab100, ciTau100)), 
                       .Names = c("4%","13%","20%", "40%","100%"), 
                       class = "data.frame", row.names = c(NA, -3L))


# plot settings
angle1 <- rep(c(45,135,90), length.out=3)
density1 <- seq(10,25,length.out=3)
op = par(mar=c(5,5,5,1)) # c(bottom, left, top, right) which gives the number of lines of margin
# plot -6 15 max(land.means)
barx = barplot(as.matrix(land.means), 
               xlab="Phase of the motion", ylab="Index of Motor Task Control",
               xlim=c(0,20),ylim=c(0,max(land.means)+(abs(max(land.means))*0.80)), 
               las=1, cex.names = 1.6,  cex.lab=1.8, cex.main =2,
               col=c("red","green","blue"), angle=angle1, density=density1,
               legend = c( "Vertical","Stability LM","AM"), beside=TRUE,
               args.legend = list(cex=1.4, horiz=FALSE, ncol=3, x.intersp=.6, y=13.5))

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
  text(x[1]+((x[2]-x[1])/2),y+0.2,s)
}


# capture x coordinates of bars
x <- barx
# ---------- tasks ---------
# - 4%
# task 1 different than task 3 p=0.025
# task 2 different than task 3 p=0.014
displayEffects(x[2:3], 8.2, 0.2, 0.4, '*')
displayEffects( c(x[1],x[3] ),  9.5, .2, 3.2, '*')
# - 40%
# task 2 different than task 3 p=0.011
displayEffects(x[11:12], 7.4, 0.2, 1.5, '*')
# - 97%
# task 1 different than task 3 p=0.022
# task 2 different than task 3 p=0.00061
displayEffects( c(x[13],x[15] ),  7.7, 1.7, 3.4, '*')
displayEffects(x[14:15], 7, 0.2, 1.5, '*')

# ---------- phases
# Compare phases
# task 1 = phase 100% is significantly different than phase 4% and 13%
vector <- c((x[1]), (x[13]))
displayEffects(array(vector), -1.5, -1.2, -1.2, '**')
vector <- c((x[4]), (x[13]))
displayEffects(array(vector), -2.5, -2.2, -2.2, '**')
# Task 2: phases are not different 

# Task 3: phases 100% is significantly different than phases 13% and 20% 
vector <- c((x[6]), (x[15]))
displayEffects(array(vector), -4.75, -4.25, -4.25, '**')
vector <- c((x[9]), (x[15]))
displayEffects(array(vector), -5.75, -5.25, -5.25, '**')


# ----------------------------- Repeated Measures Anova ---------------------------
# compute repetitive measures anova
statsaov2 <-aov(SOT_LAND$Ratio ~ (SOT_LAND$Task:SOT_LAND$Phase) + 
                  Error(SOT_LAND$Participant / (SOT_LAND$Task:SOT_LAND$Phase)), 
                data = SOT_LAND)
summary(statsaov2) 
# tasks are significantly differents p = 1.96e-06 ***
# phases are not significantly differents
# tasks:phase interactions are significant p=7.9e-08 ***
interaction.plot(SOT_LAND$Phase,SOT_LAND$Task, SOT_LAND$Ratio,
                 type="b",col=c("red","green","blue"),leg.bty="o",leg.bg="beige",
                 cex.lab=1.8, legend=F,lwd=2,pch=c(18,24),
                 xlab="Phase of the motion",ylab="Index of Motor Task Control")
legend("bottomleft",c("Vertical LDLM","Stability LDLM","TDAM"),bty="n",lty=c(1,2),lwd=2, cex=1.4, pch=c(18,24), col=c("red","green","blue"))
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
pairwise.t.test(SOT_LAND$Ratio, SOT_LAND$Phase, p.adj = "bonf",paired=TRUE)
# 5 diff than 20, 40, 97
# 

pairwise.t.test(SOT_LAND$Ratio, SOT_LAND$Task:SOT_LAND$Phase, p.adj = "bonf",paired=TRUE)
# 1:97 with 3:97, p = 0.025
# 2:20 with 1:20, p = 0.05
# 2:20 with 3:40, p = 0.019
# 2:20 with 3:97, p = 0.042
# 2:40 with 3:40, p = 0.019
# 2:97 with 3:97, p = 0.022


# Compare phases
pairwise.t.test(SOT_LAND$Ratio[SOT_LAND$Task=="1"], 
                SOT_LAND$Task[SOT_LAND$Task=="1"]:SOT_LAND$Phase[SOT_LAND$Task=="1"], p.adj = "bonf",paired=TRUE)
# phase 100% is significantly different than phase 4% and 13%
pairwise.t.test(SOT_LAND$Ratio[SOT_LAND$Task=="2"], 
                SOT_LAND$Task[SOT_LAND$Task=="2"]:SOT_LAND$Phase[SOT_LAND$Task=="2"], p.adj = "bonf",paired=TRUE)
# phases are not different 
pairwise.t.test(SOT_LAND$Ratio[SOT_LAND$Task=="3"], 
                SOT_LAND$Task[SOT_LAND$Task=="3"]:SOT_LAND$Phase[SOT_LAND$Task=="3"], p.adj = "bonf",paired=TRUE)
# phases 100% is significantly different than phases 13% and 20% 



#Compare tasks
pairwise.t.test(SOT_LAND$Ratio[SOT_LAND$Phase=="4"], 
                SOT_LAND$Task[SOT_LAND$Phase=="4"]:SOT_LAND$Phase[SOT_LAND$Phase=="4"], p.adj = "bonf",paired=TRUE)
# task 1 different than task 3 p=0.025
# task 2 different than task 3 p=0.014

pairwise.t.test(SOT_LAND$Ratio[SOT_LAND$Phase=="13"], 
                SOT_LAND$Task[SOT_LAND$Phase=="13"]:SOT_LAND$Phase[SOT_LAND$Phase=="13"], p.adj = "bonf",paired=TRUE)
# no difference
pairwise.t.test(SOT_LAND$Ratio[SOT_LAND$Phase=="20"], 
                SOT_LAND$Task[SOT_LAND$Phase=="20"]:SOT_LAND$Phase[SOT_LAND$Phase=="20"], p.adj = "bonf",paired=TRUE)
# no difference
pairwise.t.test(SOT_LAND$Ratio[SOT_LAND$Phase=="40"], 
                SOT_LAND$Task[SOT_LAND$Phase=="40"]:SOT_LAND$Phase[SOT_LAND$Phase=="40"], p.adj = "bonf",paired=TRUE)
# task 2 different than task 3 p=0.011
pairwise.t.test(SOT_LAND$Ratio[SOT_LAND$Phase=="97"], 
                SOT_LAND$Task[SOT_LAND$Phase=="97"]:SOT_LAND$Phase[SOT_LAND$Phase=="97"], p.adj = "bonf",paired=TRUE)
# task 1 different than task 3 p=0.022
# task 2 different than task 3 p=0.00061


