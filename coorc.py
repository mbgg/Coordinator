import socket

print "coorc started"

#ip = raw_input("IP-Adresse: ") 
ip = '172.20.6.100'#127.0.0.1'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((ip, 51000))
s.send("start") 

try: 
	while True: 
#		msg = raw_input("Nachricht: ") 
		response = s.recv(1024) 
		print "[%s] %s" % (ip,response) 
		if response == "check":
			s.send("rewind")
			
		elif response == "dorewind":
			s.send("exit")
			s.close()
			break

finally: 
	s.close()
