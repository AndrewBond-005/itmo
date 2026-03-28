def simps(f,a,b,n,k):
    h = (b - a) / n
    x = []
    i = a
    while i <= b:
        x.append(i)
        i += h
    ans=f(x[0])+f(x[n])
    for i in range(1,n):
        if i%2==0:
            ans+=2*f(x[i])
        else:
            ans+=4*f(x[i])
    ans*=h/3
    return ans