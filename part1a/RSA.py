import intCalc
import primeTest
import hashlib

# gnerate two unequal rand large prime num
def _generatePQ(bits):
    bits >>= 1
    p = primeTest.randomPrimeBits(bits)
    q = primeTest.randomPrimeBits(bits)
    while p == q:
        q = primeTest.randomPrimeBits(bits)
    #print('random prime  %d, %d'%(p, q))
    return (p, q)

# calculate n, e, d from p and q
def _calcNED(p, q):
    t = (p - 1) * (q - 1)
    n = p * q
    e, d = _calcED(t)
    return (n, e, d)

# calculate e, and d
# usually will random an int for e which 1 < e < t and e & t is relatively prime
# I have three value for recommand, if the recommand is suitable then e will
# usually be 65537
# putting the larger number of e and d into pubkey will slow down the encry and verify
# otherwise will slow down the speed of decry and sign

def _calcED(t):
    recommand = (65537, 3, 17)
    e = 1
    
    # if e choose to be any prime will pass
    for i in recommand:
        if i < t:
            e = i
            break
    
    # will not execute, only for explain
    if e == 1: e = primeTest.getMinRelativelyPrime(t)
    
    d = intCalc.modular_linear_equation(e, 1, t)[0]
    return (e, d)   # default to be slower decry & sign
    #return (d, e)

# provide calls for common functions in primeTest
randomIntBits = primeTest.randomIntBits
findFactors = primeTest.findFactors
isPrime = primeTest.isPrime

def _bytesToInt(intBytes):
    return int.from_bytes(intBytes, 'big', signed=False)

def _intToBytes(num, length):
    return num.to_bytes(length, 'big', signed=False)

# get an int with at least n bits
def _integerBits(n):
    count = 0
    while n != 0:
        count += 1
        n >>= 1
    return count

# Generate key pair according to the specified # of bits
def generateKey(bits):
    p, q = _generatePQ(bits)
    n, e, d = _calcNED(p, q)
    return ((e,n), (d,n))

# Because the plaintext does not necessarily happen to be
# divided equally. So mark the length of the remaining
# section with n bytes at the beginning.
codeTitle = b"441_proj:"
codeLeftLen = 4

# use public key to do encryption
# return encrypted data
def encrypt(data, pubkey):
    if len(pubkey) != 2: raise ValueError('pubkey error.')
    n = pubkey[1]
    if isinstance(data, type(b'')):
        
        # When encrypting, for each segment,
        # the ciphertext is 1 byte more than the plaintext
        cipherLen = (_integerBits(n)-1) >> 3
        plainLen = cipherLen + 1
        
        # Find the number of segments and excess bytes base
        lenData = len(data)
        sectionCount = lenData // cipherLen
        base = lenData % cipherLen
        ret = bytearray()
        
        # Encrypt the first segment,
        # only if the plaintext cannot be divided into whole num
        if base > 0:
            a = int.from_bytes(data[0:base], 'big')
            b = intCalc.montgomery(a, pubkey[0], n)
            ret.extend(codeTitle)
            ret.extend(_intToBytes(base, codeLeftLen))
            ret.extend(_intToBytes(b, plainLen)) # Write the first ciphertext
        
        for i in range(base, lenData, cipherLen):
            sectionData = data[i : i + cipherLen]
            a = int.from_bytes(sectionData, 'big')
            b = intCalc.montgomery(a, pubkey[0], n)
            ret.extend(_intToBytes(b, plainLen))
        
        return bytes(ret)
    else:
        raise TypeError("data must be 'bytes'")

# decrypt using private key
# return decrypted data
def decrypt(data, prikey):
    if len(prikey) != 2: raise ValueError('prikey error.')
    n = prikey[1]
    if isinstance(data, type(b'')):
    
        # When decrypting, for each segment
        # the ciphertext is 1 byte more than the plaintext
        plainLen = (_integerBits(n)-1) >> 3
        cipherLen = plainLen + 1
        
        # Find the number of segments and excess bytes base
        lenData = len(data)
        ret = bytearray()
        
        # Decrypt the first ciphertext without full length
        pos = 0
        if data[0:len(codeTitle)] == codeTitle:
            pos = len(codeTitle)
            lena = int.from_bytes(data[pos:pos+codeLeftLen], 'big')
            pos += codeLeftLen
            a = int.from_bytes(data[pos:pos + cipherLen], 'big')
            pos += cipherLen
            b = intCalc.montgomery(a, prikey[0], n)
            ret.extend(_intToBytes(b, lena)) # Write the first decrypted plaintext
            #ret.extend(bytes(lena))
            
        for i in range(pos, lenData, cipherLen):
            sectionData = data[i : i + cipherLen]
            a = int.from_bytes(sectionData, 'big')
            b = intCalc.montgomery(a, prikey[0], n)
            ret.extend(_intToBytes(b, plainLen))
            
        return bytes(ret)
    else:
        raise TypeError("data must be 'bytes'")

#############################################################
# signiature and verify
# used hashlib to verify
# reference:
# https://docs.python.org/3.8/library/hashlib.html
# https://cryptobook.nakov.com/digital-signatures/rsa-sign-verify-examples
#############################################################

# private key signature
# Returns the byte array of the signature result
def sign(data, prikey):
    if len(prikey) != 2: raise ValueError('prikey error.')
    n = prikey[1]
    sha1calc = hashlib.sha1()
    sha1calc.update(data)
    return encrypt(sha1calc.digest(), (prikey[0], n))

# public key verification
# Pass the Verification returns True, Fail returns False
def verify(data, pubkey, signature):
    if len(pubkey) != 2: raise ValueError('pubkey error.')
    n = pubkey[1]
    sha1calc = hashlib.sha1()
    sha1calc.update(data)
    m = decrypt(signature, (pubkey[0], n))
    return sha1calc.digest() == m

#print('test')
#bits = 1024
#pubKey, priKey = generateKey(bits)
#pubfmt = '%x,%x'
#prifmt = '%x,%x'
#print('public key：' + pubfmt%pubKey)
#print('private：' + prifmt%priKey)
#M = 'I deserve a B'.encode('ascii')
#print('original message：(%d bytes)\n%s'%(len(M),M.decode('ascii')))

#C = encrypt(M, pubKey)
#print('cipher text：(%d bytes)\n%s'%(len(C),_bytesToInt(C)))

#m = decrypt(C, priKey)
#print('decoded msg：(%d bytes)\n%s'%(len(m),m.decode('ascii')))

#S = sign(M, priKey)
#print('sign：(%d bytes)\n%s'%(len(S),_bytesToInt(S)))

#R = verify(M, pubKey, S)
#print("Signature valid：%s"%R)
