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


