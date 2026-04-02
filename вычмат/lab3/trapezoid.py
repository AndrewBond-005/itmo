def trap(f,a,b,n,k):
    h = (b - a) / n
    x = []
    i = a
    while i <= b or abs(i-b)<10**(-8):
        x.append(i)
        i += h
    ans=f(x[0])+f(x[n])
    for i in range(1,n):
        ans+=2*f(x[i])
    ans*=h/2
    return ans