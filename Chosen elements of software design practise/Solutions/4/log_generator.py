from random import randrange


with open('log.txt', 'w') as log:
	ips = []

	for _ in range(100):
		ips += [str(randrange(256)) + '.' + str(randrange(256)) + '.' + str(randrange(256)) + '.' + str(randrange(256))]
		
	for _ in range(1000):
		log.write(str(randrange(24)) + ':' + str(randrange(60)) + ':' + str(randrange(60)) + ' ' + ips[randrange(100)] + ' GET /res/foo.bar 200\n')