import math
def check_one_root(f, a, b):
    n = 1000
    step = (b - a) / n
    sign_changes = 0
    prev=0
    if a<1e-10:
       if math.copysign(1, f(a+1e-10))!=math.copysign(1, f(a-1e-10)):
           sign_changes+=1
       prev = f(a+1e-10)
    else:
        prev = f(a)
    for i in range(1, n + 1):
        x = a + i * step
        curr = f(x)
        if prev * curr <= 0:
            sign_changes += 1
        prev = curr
    return sign_changes
