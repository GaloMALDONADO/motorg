# --------------------------------------------------------------------------
# Analysis of Variances from uncontrolled manifold and its orthogonal space
# --------------------------------------------------------------------------
# - Task 1: DLM "Derivative of linear momentum" 
# - Task 2: DAM "Derivative of angular momentum"
# ----------------------------------------------------
# IV: Variance
# DV1: Good variability and bad variability
# DV2: Phase of the motion 
# ----------------------------------------------------

rm(list = ls())
#p='/galo/devel/gepetto/motorg/motorog/' #home
p='/local/gmaldona/devel/motorg/motorog/' #lab
nparticipants = 5
ddl=nparticipants-1
t = qt(.975,ddl)

# ------------------------------------------------------------------------
# --------------------       Main          -------------------------------
# ------------------------------------------------------------------------
# Takeoff
# DLM
pathName = paste(p,'TableVariancesImpulseLM.csv',sep="")
TAKEOFF_DLM = read.csv(pathName, header = FALSE, col.names = list('Participant', 'Phase', 'Variability' ,'Variance'))
TAKEOFF_DLM$Participant<-as.factor(TAKEOFF_DLM$Participant)
TAKEOFF_DLM$Phase<-as.factor(TAKEOFF_DLM$Phase)

TAKEOFF_DLM$Variability = gsub("1", "GoodV", TAKEOFF_DLM$Variability)
TAKEOFF_DLM$Variability = gsub("2", "BadV", TAKEOFF_DLM$Variability)
TAKEOFF_DLM$Variability<-as.factor(TAKEOFF_DLM$Variability)
TAKEOFF_DLM$Variability<-as.factor(TAKEOFF_DLM$Variability)
# repetitive measures anova
statsTAKEOFF_DLM <-aov(TAKEOFF_DLM$Variance ~ (TAKEOFF_DLM$Phase*TAKEOFF_DLM$Variability) + 
                         Error(TAKEOFF_DLM$Participant / (TAKEOFF_DLM$Phase*TAKEOFF_DLM$Variability)), 
                       data = TAKEOFF_DLM)
summary(statsTAKEOFF_DLM)
# F(3, 30.82) *** p<0.0001 -- all effects
# F(1, 30.76) ** p<0.001 -- variability
# F(3, 26.15) *** p<0.0001 -- interaction
# ------------------------------------------------------------------------
# DAM
pathName = paste(p,'TableVariancesImpulseAM.csv',sep="")
TAKEOFF_DAM = read.csv(pathName, header = FALSE, col.names = list('Participant', 'Phase', 'Variability' ,'Variance'))
TAKEOFF_DAM$Participant<-as.factor(TAKEOFF_DAM$Participant)
TAKEOFF_DAM$Phase<-as.factor(TAKEOFF_DAM$Phase)
TAKEOFF_DAM$Variability<-as.factor(TAKEOFF_DAM$Variability)
TAKEOFF_DAM$Variability = gsub("1", "GoodV", TAKEOFF_DAM$Variability)
TAKEOFF_DAM$Variability = gsub("2", "BadV", TAKEOFF_DAM$Variability)
TAKEOFF_DAM$Variability<-as.factor(TAKEOFF_DAM$Variability)
# repetitive measures anova
statsTAKEOFF_DAM <-aov(TAKEOFF_DAM$Variance ~ (TAKEOFF_DAM$Phase*TAKEOFF_DAM$Variability) + 
                         Error(TAKEOFF_DAM$Participant / (TAKEOFF_DAM$Phase*TAKEOFF_DAM$Variability)), 
                       data = TAKEOFF_DAM)
summary(statsTAKEOFF_DAM)
# ------------------------------------------------------------------------
# Landing
# Vertical LDM
pathName = paste(p,'TableVariancesLandVDLM.csv',sep="")
LAND_VDLM = read.csv(pathName, header = FALSE, col.names = list('Participant', 'Phase', 'Variability' ,'Variance'))
LAND_VDLM$Participant<-as.factor(LAND_VDLM$Participant)
LAND_VDLM$Phase<-as.factor(LAND_VDLM$Phase)
LAND_VDLM$Variability<-as.factor(LAND_VDLM$Variability)
LAND_VDLM$Variability = gsub("1", "GoodV", LAND_VDLM$Variability)
LAND_VDLM$Variability = gsub("2", "BadV", LAND_VDLM$Variability)
LAND_VDLM$Variability<-as.factor(LAND_VDLM$Variability)
# repetitive measures anova
statsLAND_VDLM <-aov(LAND_VDLM$Variance ~ (LAND_VDLM$Phase*LAND_VDLM$Variability) + 
                         Error(LAND_VDLM$Participant / (LAND_VDLM$Phase*LAND_VDLM$Variability)), 
                       data = LAND_VDLM)
summary(statsLAND_VDLM)
pairwise.t.test(LAND_VDLM$Variance, LAND_VDLM$Variability:LAND_VDLM$Phase, p.adj = "bonf",paired=TRUE)

# ------------------------------------------------------------------------
# Stability LDM
pathName = paste(p,'TableVariancesLandStabDLM.csv',sep="")
LAND_SDLM = read.csv(pathName, header = FALSE, col.names = list('Participant', 'Phase', 'Variability' ,'Variance'))
LAND_SDLM$Participant<-as.factor(LAND_SDLM$Participant)
LAND_SDLM$Phase<-as.factor(LAND_SDLM$Phase)
LAND_SDLM$Variability<-as.factor(LAND_SDLM$Variability)
LAND_SDLM$Variability = gsub("1", "GoodV", LAND_SDLM$Variability)
LAND_SDLM$Variability = gsub("2", "BadV", LAND_SDLM$Variability)
LAND_SDLM$Variability<-as.factor(LAND_SDLM$Variability)
# repetitive measures anova
statsLAND_SDLM <-aov(LAND_SDLM$Variance ~ (LAND_SDLM$Phase*LAND_SDLM$Variability) + 
                       Error(LAND_SDLM$Participant / (LAND_SDLM$Phase*LAND_SDLM$Variability)), 
                     data = LAND_SDLM)
summary(statsLAND_SDLM)
pairwise.t.test(LAND_SDLM$Variance, LAND_SDLM$Variability:LAND_SDLM$Phase, p.adj = "bonf",paired=TRUE)

# ------------------------------------------------------------------------
# Stability ADM
pathName = paste(p,'TableVariancesLandStabDAM.csv',sep="")
LAND_SDAM = read.csv(pathName, header = FALSE, col.names = list('Participant', 'Phase', 'Variability' ,'Variance'))
LAND_SDAM$Participant<-as.factor(LAND_SDAM$Participant)
LAND_SDAM$Phase<-as.factor(LAND_SDAM$Phase)
LAND_SDAM$Variability<-as.factor(LAND_SDAM$Variability)
LAND_SDAM$Variability = gsub("1", "GoodV", LAND_SDAM$Variability)
LAND_SDAM$Variability = gsub("2", "BadV", LAND_SDAM$Variability)
LAND_SDAM$Variability<-as.factor(LAND_SDAM$Variability)
# repetitive measures anova
statsLAND_SDAM<-aov(LAND_SDAM$Variance ~ (LAND_SDAM$Phase*LAND_SDAM$Variability) + 
                       Error(LAND_SDAM$Participant / (LAND_SDAM$Phase*LAND_SDAM$Variability)), 
                     data = LAND_SDAM)
summary(statsLAND_SDAM)
pairwise.t.test(LAND_SDAM$Variance, LAND_SDAM$Variability:LAND_SDAM$Phase, p.adj = "bonf",paired=TRUE)
