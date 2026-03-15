from funcs import *
def chord(a, b, eps, f):
    xp = a
    k=0
    if(f(a)*f(b)>0):
        return extrem(a,b,eps,f)
    while True:
        k+=1
        x = a - (b - a) * f(a) / (f(b) - f(a))
        if abs(x - xp) <= eps:
            return x,k
        if f(a) * f(x) < 0:
            b = x
        else:
            a = x
        xp = x


def extrem(a, b, eps, f):
    k=1
    if(f(a)>0):
        k=-1
    i=0
    x=0
    while(i<=500):
        i+=1
        x=(a+b)/2
        dfx=k*df(f,x)
        if abs(f(x))<eps:
            return x,i
        if dfx>0:
            a=x
        else:
            b=x
