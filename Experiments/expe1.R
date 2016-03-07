a = c(-1,+1,-1,+1)
b = c(-1,-1,1,1)
y = c(52,74,62,80)

p = lm(y~a+b+a*b)


a = b = c = c(-1,1)
design = expand.grid(a=a,b=b,c=c)
a = design$a
b = design$b
c = design$c

y = c(80,91,78,93,85,93,87,90)



d = a*b
e = a*c
f = b*c
g = a*b*c

a = c(-1,1,-1,1)
b = c(-1,-1,1,1)
c = c(1,-1,-1,1)
y = c(3,9,3,7)


y = c(320,276,306,290,272,274,290,255)

m1 = lm(y~a*b*c*d)

summary(m1)

 library(pid)
help("tradeOffTable")
paretoPlot(m1)


help(popcorn)

r = c(-1,1,-1,1)
f = c(-1,-1,1,1)
p = c(1,-1,-1,1)

y = c(1,0.75,2,1.25)

lm(y~r*f*p)


f = t = s = c(-1,1)
design = expand.grid(f=f,t=t,s=s)
f = design$f
t = design$t
s = design$s

y = c(80,91,78,93,85,93,87,90)

lm(y~f*t*s)



a = b = c = c(-1,1)
design = expand.grid(a=a,b=b,c=c)
a = design$a
b = design$b
c = design$c
d = a*b
e = a*c
f = b*c

y = c(325,330,326,300,272,265,300,275)
m = lm(y~a*b*c*d*e*f)

m
paretoPlot(m)
