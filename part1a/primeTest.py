import random
import intCalc

smallPrimeUBound = 2001
smallPrimeList = (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997,1009,1013,1019,1021,1031,1033,1039,1049,1051,1061,1063,1069,1087,1091,1093,1097,1103,1109,1117,1123,1129,1151,1153,1163,1171,1181,1187,1193,1201,1213,1217,1223,1229,1231,1237,1249,1259,1277,1279,1283,1289,1291,1297,1301,1303,1307,1319,1321,1327,1361,1367,1373,1381,1399,1409,1423,1427,1429,1433,1439,1447,1451,1453,1459,1471,1481,1483,1487,1489,1493,1499,1511,1523,1531,1543,1549,1553,1559,1567,1571,1579,1583,1597,1601,1607,1609,1613,1619,1621,1627,1637,1657,1663,1667,1669,1693,1697,1699,1709,1721,1723,1733,1741,1747,1753,1759,1777,1783,1787,1789,1801,1811,1823,1831,1847,1861,1867,1871,1873,1877,1879,1889,1901,1907,1913,1931,1933,1949,1951,1973,1979,1987,1993,1997,1999)

##################################################
# used for Prime number test
##################################################

# Miller_Rabin alg for prime number test
rabin_test_times = 20

def isPrimeRabin(n):
    for i in range(0, rabin_test_times):
        a = random.randint(1, n - 1)
        if intCalc.montgomery(a, n - 1, n) != 1:
            return False
    return True
    
isPrime = isPrimeRabin


##################################################

# Find the smallest prime number greater than base
def nextPrime(base):
    if base < smallPrimeUBound:
        for i in smallPrimeList:
            if i > base:
                return i
    #print('Small prime list not enough.')
    i = base
    if i % 2 == 0: i += 1
    while True:
        i += 2
        if isPrime(i):
            return i

# generate random int with specified bits
def randomIntBits(bits):
    base1 = 1 << (bits - 1)
    base2 = (1 << bits) - 1
    #print('Random range: %d ~ %d.'%(base1, base2))
    return random.randint(base1, base2)

# generate random large prime with sepecified bits
def randomPrimeBits(bits):
    base1 = 1 << (bits - 1)
    base2 = (1 << bits) - 1
    i = random.randint(base1, base2)
    #print('Random range: %d ~ %d. Base: %d'%(base1, base2, i))
    if i % 2 == 0: i += 1
    while True:
        i += 2
        if i > base2:
            i = base1
        if isPrime(i):
            return i
        #print(i, flush=True)

# find the smallest coprime of n
def minRelativelyPrime(n, base = 1):
    i = base
    while True:
        i = nextPrime(i)
        if n % i != 0:
            return i

# pollard_rho alg for prime factorization
def pollard_rho(x, c):
    i, k = 1, 2
    x0 = random.randint(0, x)
    y = x0
    while True:
        i += 1
        x0 = (intCalc.mult_mod(x0, x0, x) + c) % x
        d = intCalc.gcd(y - x0, x)
        if d != 1 and d != x: return d
        if y == x0: return x
        if i == k:
            y = x0
            k += k
    pass

# call pollard_rho function for prime factorization
def findFactors(n):
    factors = []
    if isPrime(n):
        return [n]
    p = n
    while p >= n:
        p = pollard_rho(p, random.randint(1, n - 1))
    factors.extend(findFactors(p))
    factors.extend(findFactors(n//p))
    return factors



