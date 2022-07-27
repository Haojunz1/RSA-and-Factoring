##############################
# Libaray used in this program
# gmpy2 can be used as multiprecision lib stated in the piazza @56
##############################
from gmpy2 import *
from math import log, ceil
import sys
from random import *
import time

###############################
# helper functions
###############################

# =============================
# add factors to factor list
# for this situation, the num
# of factor will only be 2 which
# is prime and q
# =============================
def add_fs(prime, f_s, value=1):
	if f_s.get(prime) is None:
		f_s[prime] = value
	else:
		f_s[prime] += value

# =============================
# generate prime table for
# interval A to B
# =============================

def  primeRange (A,B) :
	pTable = [2]
	for i in range(3,B,2):
		if (is_prime(i)):
			pTable.append(i)

	return pTable

# =============================
# return nth root
# =============================
def nthroot(k, n):
    u, ret = n, n+1
    while u < ret:
        ret = u
        a = (k-1) * ret + n // pow(ret, k-1)
        u = a // k
    if isinstance(ret,int):
    	return ret
    else:
    	return None

# ===============================
# check if it is a power of prime
# ===============================
def is_power(n, B=10**6+3):

	exp = ceil(log(n, B))
    
	for ex in range(exp, 2, -1):
    
		prime = nthroot(n, ex)
        
		if prime != None:
			return prime, ex
            
	return None, None
    
############################################
# extended euclidean algorithm
# mod inverse
# reference:
# https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
############################################
def exgcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = exgcd(b % a, a)
        return (g, x - (b // a) * y, y)

def mod_inverse(a, m):
    g, x, y = exgcd(a, m)
    if g != 1:
        raise Exception('>>> modular inverse does not exist')
    else:
        return x % m

##############################################
# trial division
# basically never used in this project
#############################################
def trial_divison(n, B = 10**6, f_s = {}):

	ret = n
	for prime in primeRange(2, B):
		exp = 0
        
		while ret % prime == 0:
			ret //= prime
			exp += 1
            
		if exp > 0:
			add_fs(prime, f_s, exp)
            
	return ret

###############################################
# pollard_rho
##############################################
def rho(n):
	n = mpz(n)
	x = mpz(2)
	y = x**2 + 1

	for i in range(n):
		prime = gcd(y-x,n)

		if prime != 1:
			return prime

		else: 
			#x = (pow(x,2)+1)%n
			#y = (pow(y,2)+1)%n
			#y = (pow(y,2)+1)%n
			y = (((y ** 2 + 1) % n)** 2 + 1) % n
			x = (x ** 2 + 1) % n
	return None  

#############################################
# pollard p - 1
#############################################
def pm1(a,	r = 2):
	B = 10**6

	b = r

	for prime in primeRange(2, B):

		m = int(log(a, prime))
		b = pow(b, pow(prime, m), a)

		g = gcd(b - 1, a)
		if 1 < g < a:
			return g
	return None

def factor(n , num_of_digits , f_s = {}, times = 1):

	# 1. check if the num already a prime
	print(">>> Checking if the number is already a prime")

	tic = time.perf_counter()
	if is_prime(n):
		add_fs(n, f_s, times)
		return
	toc = time.perf_counter()
	print(f">>> Checking if the int is prime used {toc - tic:0.4f} seconds")
	# 2. trial division
	n_tmp = n
	print(">>> Using trial division method...")

	tic = time.perf_counter()
	n = trial_divison(n, f_s=f_s)
    
	if n < n_tmp:
		print(">>> Found factor:", n_tmp // n)
	
	if n == 1:
		return
	elif is_prime(n):
		add_fs(n, f_s, times)
		return
	toc = time.perf_counter()
	print(f">>> Trial_divison used {toc - tic:0.4f} seconds")

	# 3. pollard's prime - 1 method

	seed = randint(2, 10)
	print(">>> Using Pollard's p - 1 Method...")

	tic = time.perf_counter()
	f = pm1(n,r = seed)
	toc = time.perf_counter()

	print(f">>> P - 1 used {toc - tic:0.4f} seconds")

	if f is not None:
		n //= f
		if is_prime(f):
			print(">>> Found prime: ", f)
			add_fs(f, f_s, times)

		if is_prime(n):
			add_fs(n, f_s, times)
			return

	# 4. pollard rho's method

	print(">>> Using pollard rho Method...")

	tic = time.perf_counter()
	f = rho(n)
	toc = time.perf_counter()
	print(f">>> Pollard rho used  {toc - tic:0.4f} seconds")

	if f is not None:
		n //= f
		if is_prime(n):
			print(">>> Found prime: ", f)
			add_fs(f, f_s, times)

		if is_prime(n):
			add_fs(n, f_s, times)
			return
    
def main(n):

	# Fully factored part
	f_s = {}
	
	unknown = {}
	
	num_of_digits = len(str(n))
	try:
		factor(n,num_of_digits = num_of_digits,f_s = f_s)
	except KeyboardInterrupt:
    
		for prime, ex in f_s.items():
			n //= prime**ex
		add_fs(n, unknown)
	return f_s, unknown       
					
def userPromotion(argv=[]):
	n = 1
	print("==== Enter postive number you want to factorize =====\
		\n=== Use 'quit' or 'exit' to terminate the program ===")

	while True:
		userInput = input("\n>>> ")
		if userInput == "quit" or userInput == "exit":
			break
		else:
			try:
				n = eval(userInput)
			except:
				print(">>> Unknown Command")
				continue
		if n <= 1 or type(n) is not int:
			print(">>> Please enter positive int larger than 1")
			continue
		num_of_digits = len(str(n))
		print(">>> Factoring: ", n, " ("+str(num_of_digits)+" digits in decimal)")
	
		f_s, unknown = main(n)
	
		print("\nThe results are as follows:")
		for prime, ex in f_s.items():
			if prime < n:
				if ex == 1:
					print("    Prime factor: = ", prime)
				elif ex > 1:
					print("Prime power factor: =", prime, " i = ", ex)
			else:
				print(str(n)+" is prime")
	
		if unknown != {}:
		
			for c, ex in unknown.items():
				if c == n:
					print(str(n)+" cannot be factored at this time")

if __name__ == '__main__':
	userPromotion(sys.argv)
