# Analysis of Variances from uncontrolled manifold and its orthogonal space
rm(list = ls())

#p='/galo/devel/gepetto/motorg/motorog/'
p='/local/gmaldona/devel/motorg/motorog/'


# ------------------------------------------------------------------------
#    JUMP IMPULSE
# Task 1: impulsion through antero-posterior and vertical linear momentum
# Task 2: impulsion through antero posterior angular momentum (around M-L axis)
# ------------------------------------------------------------------------
pathName = paste(p,'TableCriteriaImpulse.csv',sep="")
SOT_IMPULSE = read.csv(pathName,
                      header = FALSE, 
                      col.names = list('Participant', 'Phase', 'Task', 'Ratio'))
SOT_IMPULSE$Participant<-as.factor(SOT_IMPULSE$Participant)
SOT_IMPULSE$Phase<-as.factor(SOT_IMPULSE$Phase)
SOT_IMPULSE$Task<-as.factor(SOT_IMPULSE$Task)

boxplot(SOT_IMPULSE$Ratio~SOT_IMPULSE$Task)
# impulsionAM mean > impulsionLM mean 
boxplot(SOT_IMPULSE$Ratio~SOT_IMPULSE$Phase)
# tasks are more controlled at 1 and 50 % of the phase
boxplot(SOT_IMPULSE$Ratio~SOT_IMPULSE$Task:SOT_IMPULSE$Phase)
# impulsionLM is more controlled than impulsionAM at 1%
# impulsionAM is more controlled than impulsionLM at 50% and 100%
# impulsionLM decrease it is importance during the jump phase


# Plot the means and stds (error bars)
meanImpLM1 = mean(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="1"&
                                     SOT_IMPULSE$Phase=="1"])
stdImpLM1 = sd(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="1"&
                                 SOT_IMPULSE$Phase=="1"])
meanImpLM50= mean(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="1"&
                                      SOT_IMPULSE$Phase=="50"])
stdImpLM50= mean(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="1"&
                                      SOT_IMPULSE$Phase=="50"])
meanImpLM100= mean(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="1"&
                                      SOT_IMPULSE$Phase=="100"])
stdImpLM100= mean(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="1"&
                                       SOT_IMPULSE$Phase=="100"])
meanImpAM1 = mean(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="2"&
                                      SOT_IMPULSE$Phase=="1"])
stdImpAM1 = sd(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="2"&
                                      SOT_IMPULSE$Phase=="1"])
meanImpAM50= mean(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="2"&
                                      SOT_IMPULSE$Phase=="50"])
stdImpAM50= sd(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="2"&
                                      SOT_IMPULSE$Phase=="50"])
meanImpAM100= mean(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="2"&
                                       SOT_IMPULSE$Phase=="100"])
stdImpAM100= sd(SOT_IMPULSE$Ratio[SOT_IMPULSE$Task=="2"&
                                     SOT_IMPULSE$Phase=="100"])

jump.means <- structure(list('1'=c(meanImpLM1,meanImpAM1),
                             '50'=c(meanImpLM50, meanImpAM50),
                             '100'=c(meanImpLM100, meanImpAM100)), 
                              .Names = c("1%", "50%", "100%"), 
                              class = "data.frame", row.names = c(NA, -2L))
barx = barplot(as.matrix(jump.means), main="Jump",
        xlab="Phase of the motion", ylab="Index of Motor Task Control",
        xlim=c(0,10),ylim=c(0,8),
        col=c("darkblue","red"),
        legend = c( "Impulsion Linear Momentum","Impulsion Angular Mommentum"), beside=TRUE)

jump.stds <- structure(list('1'=c(stdImpLM1,stdImpAM1),
                             '50'=c(stdImpLM50, stdImpAM50),
                             '100'=c(stdImpLM100, stdImpAM100)), 
                        .Names = c("1%", "50%", "100%"), 
                        class = "data.frame", row.names = c(NA, -2L))
xx=as.matrix(jump.means)
er=as.matrix(jump.stds)
arrows(barx,xx+er, barx,xx, angle=90, code=3, length=0.05)


# compute repetitive measures anova
aovstats <-aov(SOT_IMPULSE$Ratio ~ 
               SOT_IMPULSE$Task*SOT_IMPULSE$Phase + 
                Error(SOT_IMPULSE$Participant / SOT_IMPULSE$Task*SOT_IMPULSE$Phase), 
              data = SOT_IMPULSE)
summary(aovstats)
# tasks are significantly differents p - 0.0385
# tasks and phase are significantly differents p=0.000493

# Effect Size
# of the tasks
etacarrePartiel<-16.435/(16.435+7.127)
# 70% of the variance of tha ratios explains the variation of the tasks
ftailleEffet<-sqrt(etacarrePartiel/(1-etacarrePartiel))
# effect fort : ftaill = 1.51. Effect is independent of the size
# of the tasks and phase interaction
etacarrePartiel<-21.161/(21.161+3.704)
# 85% of the variance of tha ratios explains the variation of the tasks
ftailleEffet<-sqrt(etacarrePartiel/(1-etacarrePartiel))
# strong effect 2.39/ Effect independent of the size

# POST-HOC
# Compare tasks
pairwise.t.test(SOT_IMPULSE$Ratio, 
                SOT_IMPULSE$Task, 
                p.adj = "bonf",paired=TRUE)
# impulsionLM and impulsionAM are significantly different p = 0.018
# Angular Momentum > Linear Momentum
pairwise.t.test(SOT_IMPULSE$Ratio, 
                SOT_IMPULSE$Phase, 
                p.adj = "bonf",paired=TRUE)
# at 50% both tasks are more controlled p = 0.0039
pairwise.t.test(SOT_IMPULSE$Ratio, 
                SOT_IMPULSE$Task:SOT_IMPULSE$Phase, 
                p.adj = "bonf",paired=TRUE)
# impulsionLM is significantly less controlled at 100% than at 50%


# ----------------------------------------------
#                 Flying
# Task 1: vision
# Task 2: pelvis
# ----------------------------------------------
rm(list = ls())
p='/galo/devel/gepetto/motorg/motorog/'

pathName = paste(p,'TableCriteriaFly.csv',sep="")
SOT_FLY = read.csv(pathName,
                   header = FALSE, 
                    col.names = list('Participant',
                                     'Phase',
                                     'Task',
                                     'Ratio'))

SOT_FLY$Participant<-as.factor(SOT_FLY$Participant)
SOT_FLY$Phase<-as.factor(SOT_FLY$Phase)
SOT_FLY$Task<-as.factor(SOT_FLY$Task)

boxplot(SOT_FLY$Ratio~SOT_FLY$Task)
# vision mean > pelvis mean 
boxplot(SOT_FLY$Ratio~SOT_FLY$Phase)
# tasks are more controlled at 50 % of the phase
boxplot(SOT_FLY$Ratio~SOT_FLY$Task:SOT_FLY$Phase)
# vision is more controlled than pelvis at all phases
# pelvis is almost invariant


# Plot the means and stds (error bars)
meanVis1 = mean(SOT_FLY$Ratio[SOT_FLY$Task=="1"&
                                SOT_FLY$Phase=="1"])
stdVis1 = sd(SOT_FLY$Ratio[SOT_FLY$Task=="1"&
                             SOT_FLY$Phase=="1"])
meanVis50= mean(SOT_FLY$Ratio[SOT_FLY$Task=="1"&
                                SOT_FLY$Phase=="50"])
stdVis50= mean(SOT_FLY$Ratio[SOT_FLY$Task=="1"&
                               SOT_FLY$Phase=="50"])
meanVis100= mean(SOT_FLY$Ratio[SOT_FLY$Task=="1"&
                                 SOT_FLY$Phase=="100"])
stdVis100= mean(SOT_FLY$Ratio[SOT_FLY$Task=="1"&
                                SOT_FLY$Phase=="100"])
meanPelv1 = mean(SOT_FLY$Ratio[SOT_FLY$Task=="2"&
                                 SOT_FLY$Phase=="1"])
stdPelv1 = sd(SOT_FLY$Ratio[SOT_FLY$Task=="2"&
                              SOT_FLY$Phase=="1"])
meanPelv50= mean(SOT_FLY$Ratio[SOT_FLY$Task=="2"&
                                 SOT_FLY$Phase=="50"])
stdPelv50= sd(SOT_FLY$Ratio[SOT_FLY$Task=="2"&
                              SOT_FLY$Phase=="50"])
meanPelv100= mean(SOT_FLY$Ratio[SOT_FLY$Task=="2"&
                                  SOT_FLY$Phase=="100"])
stdPelv100= sd(SOT_FLY$Ratio[SOT_FLY$Task=="2"&
                               SOT_FLY$Phase=="100"])

fly.means <- structure(list('1'=c(meanVis1,meanPelv1),
                             '50'=c(meanVis50, meanPelv50),
                             '100'=c(meanVis100, meanPelv100)), 
                        .Names = c("1%", "50%", "100%"), 
                        class = "data.frame", row.names = c(NA, -2L))
barx = barplot(as.matrix(fly.means), main="Fly",
               xlab="Phase of the motion", ylab="Index of Motor Task Control",
               xlim=c(0,10),ylim=c(0,11),
               col=c("darkblue","red"),
               legend = c( "Vision","Pelvis"), beside=TRUE)

fly.stds <- structure(list('1'=c(stdVis1,stdPelv1),
                            '50'=c(stdVis50, stdPelv50),
                            '100'=c(stdVis100, stdPelv100)), 
                       .Names = c("1%", "50%", "100%"), 
                       class = "data.frame", row.names = c(NA, -2L))
xx=as.matrix(fly.means)
er=as.matrix(fly.stds)
arrows(barx,xx+er, barx,xx, angle=90, code=3, length=0.05)


# compute repetitive measures anova
aovstats <-aov(SOT_FLY$Ratio ~ 
                 SOT_FLY$Task*SOT_FLY$Phase + 
                 Error(SOT_FLY$Participant / SOT_FLY$Task*SOT_FLY$Phase), 
               data = SOT_FLY)
summary(aovstats)
# tasks are significantly differents p = 0.000564
# tasks and phase are significantly differents p=0.0108

# Effect Size
# of the tasks
etacarrePartiel<-37.70/(37.70+1.51 )
# 96% of the variance of tha ratios explains the variation of the tasks
ftailleEffet<-sqrt(etacarrePartiel/(1-etacarrePartiel))
# effect fort : ftaill = 4.99. Effect is independent of the size
# of the tasks and phase interaction
etacarrePartiel<-6.242/(6.242+2.973)
# 67% of the variance of tha ratios explains the variation of the tasks
ftailleEffet<-sqrt(etacarrePartiel/(1-etacarrePartiel))
# strong effect 1.448. Effect independent of the size

# POST-HOC
# Compare tasks
pairwise.t.test(SOT_FLY$Ratio, 
                SOT_FLY$Task, 
                p.adj = "bonf",paired=TRUE)
# vision and pelvis are significantly different p = 6.1e-06
# Vision > Pelvis
pairwise.t.test(SOT_FLY$Ratio, 
                SOT_FLY$Phase, 
                p.adj = "bonf",paired=TRUE)
# not signifficant diferents of the phases
pairwise.t.test(SOT_FLY$Ratio, 
                SOT_FLY$Task:SOT_FLY$Phase, 
                p.adj = "bonf",paired=TRUE)
# vision is significantly more controlled than pelvis at 50% and 100%

# ----------------------------------------------
#                 Landing
# Task 1: damping
# Task 2: stifness
# Task 3: stability of center of mass x,y
# Task 4: stability through angular momentum
# ----------------------------------------------
rm(list = ls())
p='/galo/devel/gepetto/motorg/motorog/'
pathName = paste(p,'TableCriteriaLand.csv',sep="")
SOT_LAND = read.csv(pathName,
                    header = FALSE, 
                    col.names = list('Participant',
                                     'Phase',
                                      'Task',
                                      'Ratio'))

SOT_LAND$Participant<-as.factor(SOT_LAND$Participant)
SOT_LAND$Phase<-as.factor(SOT_LAND$Phase)
SOT_LAND$Task<-as.factor(SOT_LAND$Task)

boxplot(SOT_LAND$Ratio~SOT_LAND$Task)
# stability AngMom mean > damping mean > stability CM mean > stifness mean
boxplot(SOT_LAND$Ratio~SOT_LAND$Phase)
# tasks are similarly controlled at all phases
boxplot(SOT_LAND$Ratio~SOT_LAND$Task:SOT_LAND$Phase)
# damping is less controlled at each phase increment
# stifness is more controlled at each phase increment
# stability CM and stability AngMom are similarly controlled in all phases
# damping is more controlled than stifness at all phases
# stifness is almost invariant


# Plot the means and stds (error bars)
meanDamp1 = mean(SOT_LAND$Ratio[SOT_LAND$Task=="1"&
                                 SOT_LAND$Phase=="1"])
stdDamp1 = sd(SOT_LAND$Ratio[SOT_LAND$Task=="1"&
                              SOT_LAND$Phase=="1"])
meanDamp50= mean(SOT_LAND$Ratio[SOT_LAND$Task=="1"&
                                 SOT_LAND$Phase=="50"])
stdDamp50= mean(SOT_LAND$Ratio[SOT_LAND$Task=="1"&
                                SOT_LAND$Phase=="50"])
meanDamp100= mean(SOT_LAND$Ratio[SOT_LAND$Task=="1"&
                                  SOT_LAND$Phase=="100"])
stdDamp100= mean(SOT_LAND$Ratio[SOT_LAND$Task=="1"&
                                 SOT_LAND$Phase=="100"])
meanStiff1 = mean(SOT_LAND$Ratio[SOT_LAND$Task=="2"&
                                  SOT_LAND$Phase=="1"])
stdStiff1 = sd(SOT_LAND$Ratio[SOT_LAND$Task=="2"&
                               SOT_LAND$Phase=="1"])
meanStiff50= mean(SOT_LAND$Ratio[SOT_LAND$Task=="2"&
                                  SOT_LAND$Phase=="50"])
stdStiff50= sd(SOT_LAND$Ratio[SOT_LAND$Task=="2"&
                               SOT_LAND$Phase=="50"])
meanStiff100= mean(SOT_LAND$Ratio[SOT_LAND$Task=="2"&
                                   SOT_LAND$Phase=="100"])
stdStiff100= sd(SOT_LAND$Ratio[SOT_LAND$Task=="2"&
                                SOT_LAND$Phase=="100"])

meanStabCM1 = mean(SOT_LAND$Ratio[SOT_LAND$Task=="3"&
                                   SOT_LAND$Phase=="1"])
stdStabCM1 = sd(SOT_LAND$Ratio[SOT_LAND$Task=="3"&
                                SOT_LAND$Phase=="1"])
meanStabCM50= mean(SOT_LAND$Ratio[SOT_LAND$Task=="3"&
                                   SOT_LAND$Phase=="50"])
stdStabCM50= sd(SOT_LAND$Ratio[SOT_LAND$Task=="3"&
                                SOT_LAND$Phase=="50"])
meanStabCM100= mean(SOT_LAND$Ratio[SOT_LAND$Task=="3"&
                                    SOT_LAND$Phase=="100"])
stdStabCM100= sd(SOT_LAND$Ratio[SOT_LAND$Task=="3"&
                                 SOT_LAND$Phase=="100"])

meanStabAM1 = mean(SOT_LAND$Ratio[SOT_LAND$Task=="4"&
                                    SOT_LAND$Phase=="1"])
stdStabAM1 = sd(SOT_LAND$Ratio[SOT_LAND$Task=="4"&
                                 SOT_LAND$Phase=="1"])
meanStabAM50= mean(SOT_LAND$Ratio[SOT_LAND$Task=="4"&
                                    SOT_LAND$Phase=="50"])
stdStabAM50= sd(SOT_LAND$Ratio[SOT_LAND$Task=="4"&
                                SOT_LAND$Phase=="50"])
meanStabAM100= mean(SOT_LAND$Ratio[SOT_LAND$Task=="4"&
                                     SOT_LAND$Phase=="100"])
stdStabAM100= sd(SOT_LAND$Ratio[SOT_LAND$Task=="4"&
                                  SOT_LAND$Phase=="100"])


land.means <- structure(list('1'=c(meanDamp1,meanStiff1,meanStabCM1,meanStabAM1),
                            '50'=c(meanDamp50, meanStiff50,meanStabCM50,meanStabAM50),
                            '100'=c(meanDamp100, meanStiff100,meanStabCM100,meanStabAM100)), 
                       .Names = c("1%", "50%", "100%"), 
                       class = "data.frame", row.names = c(NA, -4L))
barx = barplot(as.matrix(land.means), main="Landing",
               xlab="Phase of the motion", ylab="Index of Motor Task Control",
               xlim=c(0,15),ylim=c(0,10),
               col=c("darkblue","red","green","yellow"),
               legend = c( "Damping","Stiffness","Stability CoM","Stability Angular Momentum"), beside=TRUE)

land.stds <- structure(list('1'=c(stdDamp1,stdStiff1,stdStabCM1,stdStabAM1),
                           '50'=c(stdDamp50, stdStiff50,stdStabCM50,stdStabAM50),
                           '100'=c(stdDamp100, stdStiff100,stdStabCM100,stdStabAM100)), 
                      .Names = c("1%", "50%", "100%"), 
                      class = "data.frame", row.names = c(NA, -4L))
xx=as.matrix(land.means)
er=as.matrix(land.stds)
arrows(barx,xx+er, barx,xx, angle=90, code=3, length=0.05)


# compute repetitive measures anova
statsaov2 <-aov(SOT_LAND$Ratio ~ 
              SOT_LAND$Task*SOT_LAND$Phase + 
              Error(SOT_LAND$Participant / SOT_LAND$Task*SOT_LAND$Phase), 
              data = SOT_LAND)
summary(statsaov2)
# tasks are significantly differents p = 1.05e-06
# tasks and phase are significantly differents p=2.77e-08

# Effect Size
# of the tasks
etacarrePartiel<-102.98/(102.98+9.54 )
# 91% of the variance of tha ratios explains the variation of the tasks
ftailleEffet<-sqrt(etacarrePartiel/(1-etacarrePartiel))
# effect fort : ftaill = 3.28. Effect is independent of the size
# of the tasks and phase interaction
etacarrePartiel<-7.566/(7.566+1.501)
# 83% of the variance of tha ratios explains the variation of the tasks
ftailleEffet<-sqrt(etacarrePartiel/(1-etacarrePartiel))
# strong effect 2.245. Effect independent of the size

# POST-HOC
# Compare tasks
pairwise.t.test(SOT_LAND$Ratio, 
                SOT_LAND$Task, 
                p.adj = "bonf",paired=TRUE)
# damping and stifness are significantly different p = 5.5e-07
# stifness and stability CM are significantly different p = 1.2e-13
# stifness and stability AngMom are significantly different p = 1.1e-11
# stability CM and stability AngMom are significantly different p = 5.7e-06
# Not significant difference between damping and tasks 3 and 4


# POST-HOC
# Compare tasks
pairwise.t.test(SOT_LAND$Ratio, 
                SOT_LAND$Task, 
                p.adj = "bonf",paired=TRUE)
# damping and stifness are not significantly different p = 0.48
# damping and stability CM are significantly different p = 0.00094
# stifness and stability CM are significantly different p = 6.3e-07
# Angular Momentum >> Stability CM > Damping
# stability through angular momentum > Damping > stability of center of mass x,y > stifness

pairwise.t.test(SOT_LAND$Ratio, 
                SOT_LAND$Phase, 
                p.adj = "bonf",paired=TRUE)
# not signifficant diferents of the phases

pairwise.t.test(SOT_LAND$Ratio, 
                SOT_LAND$Task:SOT_LAND$Phase, 
                p.adj = "bonf",paired=TRUE)
# damping is significantly different at 50 % than at 100%
# damping is significantly different than stifness at 50% each
# stifness is significantly different thant stability CM at 1%, 50$ at 100% each
# stifness is significantly different thant stability AngMom 50% and 100%
# stability CM is significantly different than stability AngMom at 100%


