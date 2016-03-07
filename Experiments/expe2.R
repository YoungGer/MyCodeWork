library(pid)
help('manufacture')
manufacture(P=0.75,T=325)
manufacture(P=0.5,T=320)

P1 = c(0.75,0.5,1,0.5,1)
T1 = c(325,320,320,330,330)
Y0 = c(407,193,468,310,571)

P1 = c(0,-1,1,-1,1)
T1 = c(0,-1,-1,1,1)
Y1 = c(407,193,468,310,571)
Y0 = c(390,197,472,314,575)
model.base.1 = lm(Y1~P1*T1)
summary(model.base.1)

contourPlot(model.base.1,'P1','T1')

new.df = data.frame(P1=P1,T1=T1)

predict(model.base.1,new.df)
