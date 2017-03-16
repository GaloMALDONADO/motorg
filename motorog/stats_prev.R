# Analysis of Variances from uncontrolled manifold and its orthogonal space
SOT = read.csv('/local/gmaldona/devel/motorg/motorog/TableCriteria.csv',
                header = FALSE, 
                col.names = list('Participant','Phase','Task','Ratio'))
SOT$Participant<-as.factor(SOT$Participant)
SOT$Phase<-as.factor(SOT$Phase)
SOT$Task<-as.factor(SOT$Task)

stats <-aov(SOT$Ratio ~ SOT$Task*SOT$Phase + Error(SOT$Participant / SOT$Task*SOT$Phase), data = SOT)
summary(stats)

pairwise.t.test(SOT$Ratio, SOT$Task, p.adj = "bonf",paired=TRUE)
pairwise.t.test(SOT$Ratio, SOT$Task:SOT$Phase, p.adj = "bonf",paired=TRUE)