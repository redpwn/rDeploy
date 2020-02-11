import hashlib

def hash_file(path):
	BUF_SIZE = 65536

	sha1 = hashlib.sha1()

	with open(path, 'rb') as f:
		while True:
			data = f.read(BUF_SIZE)
			if not data:
					break
			sha1.update(data)
	return sha1.hexdigest()

def get_key(problem, baseDir):
	assert problem.startswith(baseDir)

	key = problem[len(baseDir):]

	if key[0] == '/':
		key = key[1:] 

	return key
