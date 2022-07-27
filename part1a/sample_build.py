import RSA
def main():
	print('sample build for 441 proj')
	bits = 1024

	pubKey, priKey = RSA.generateKey(bits)

	pubfmt = '%x,%x'
	prifmt = '%x,%x'

	print('public key：' + pubfmt%pubKey)
	print('private：' + prifmt%priKey)

	M = 'I deserve a B'.encode('ascii')
	print('original message：(%d bytes)\n%s'%(len(M),M.decode('ascii')))

	C = RSA.encrypt(M, pubKey)
	print('cipher text：(%d bytes)\n%s'%(len(C),RSA._bytesToInt(C)))

	m = RSA.decrypt(C, priKey)
	print('decoded msg：(%d bytes)\n%s'%(len(m),m.decode('ascii')))

	S = RSA.sign(M, priKey)
	print('sign：(%d bytes)\n%s'%(len(S),RSA._bytesToInt(S)))

	R = RSA.verify(M, pubKey, S)
	print("Signature valid：%s"%R)

main()
