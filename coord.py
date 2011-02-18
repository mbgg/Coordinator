# coordinator which sends 
#
#

import socket

def preface():
	pass

def nwcom():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	s.bind(("", 51000)) 
	s.listen(1)

	try: 
		while True: 
			komm, addr = s.accept() 
			print "connection from %s" % addr[0]

			while True: 
				data = komm.recv(1024)

				if not data: 
					komm.close() 
					break

				#print "[%s] %s" % (addr[0], data) 	
				if data == "start":
					print "start recv"
					komm.send("check") 

				elif data == "rewind":
					print "rewind recv"
					komm.send("dorewind") 
				
				elif data == "exit":
					komm.close()
					s.close()
					return

	finally: 
		s.close()

print "coord started"
preface()

nwcom()



