######################################################
# RSA Mathematical calculation lib for large intergers
# Montgomery algorithm
# Euclidean algorithm and extended Euclidean algorithm
######################################################


#######################################################
# Newton's method of infinite approximation for the int
# part of the square root
#######################################################
def sqrtInt(x):
    if x < 4: return 1
    
    g1 = x
    g2 = x >> 1
    count = 0
    
    while g2 < g1:
        count += 1
        g1 = g2
        g2 = (g1 + x // g1) >> 1
        
    # print('sqrtInt(%d) loop %d times.'%(x, count))
    # print('check sqrtInt() result: %s.'%(g1 * g1 <= x and x < (g1+1) * (g1+1)))
    return g1

######################################################
# Fast multiplication mod calculation
# (a * b) % c
######################################################
def mult_mod(a, b, c):
    a %= c
    b %= c
    ret = 0
    
    while b != 0:
        if 0 != (b & 1):
            ret += a
            ret %= c
        a <<= 1
        if a >= c:
            a %= c
        b >>= 1
    return ret

######################################################
# Montgomery algorithm
# calculate the value of (n ^ p)% m
######################################################
def montgomery(n, p, m):
    k = 1
    n %= m
    while p != 1:
        if 0 != (p & 1):
            k = (k * n) % m
        n = (n * n) % m
        p >>= 1
    return (k * n) % m

##########################################################
# Euclidean algorithm and extended Euclidean algorithm
# reference:http://ce.sharif.edu/courses/86-87/2/ce115-2/resources/root/CLRS.pdf
##########################################################

# Find the greatest common divisor
def gcd(a, b):
    while b != 0:
        r = b
        b = a % b
        a = r
    return a


# calculate one solution for gcd(a,b)=ax+by
def exgcd(a, b):
    x0, y0 = 1, 0
    x1, y1 = 0, 1
    x, y = 0, 1
    r = a % b
    q = (a - r) // b
    while r != 0:
        x = x0 - q * x1
        y = y0 - q * y1
        x0, y0 = x1, y1
        x1, y1 = x, y
        a = b
        b = r
        r = a % b
        q = (a - r) // b
    return (b, x, y)

# the congruent equation ax≡b (mod n)
# has a solution to the unknown x if and only if gcd(a, n) | b
# if the equation has a solution, the equation has gcd (a, n) solutions
def modular_linear_equation(a, b, n):
    r = []
    d, x, y = exgcd(a, n)
    if b % d != 0:
        return r
    
    x0 = x * (b // d) % n   # particular solution
    r.append(x0)
    for i in range(1, d):   # residual solution
        r.append((x0+i*(n-d))%n)
    return r

