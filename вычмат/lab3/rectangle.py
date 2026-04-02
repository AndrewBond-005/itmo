def rect(f,a,b,n,k):
    h=(b-a)/n
    x=[]
    i=a+k*h
    j=0
    while j<n:
        j+=1
        x.append(i)
        i+=h
    ans=0
    for i in range(len(x)):
        ans += f(x[i]) * h
    return ans