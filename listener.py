import os
from time import sleep
from sys import stdout

ENDLINE = '\x92'
# print ord(ENDLINE)
files = ['/tmp/upl.gif', '/tmp/upl2.gif', '/tmp/upl3.gif', '/tmp/upl4.gif']



Delivered = False
message = ''

def tick(file) :
	return (os.stat(file)[0] % 512) ^ 512 


last_state = tick(files[0])
while not Delivered :



	cur_state = tick(files[0])
	# print cur_state
	while cur_state == last_state :
		sleep (0.2)
		cur_state = tick(files[0])
		# print cur_state,


	for f in files :

		mod = (os.stat(f)[0])
		char = chr(mod % 256)
		# message += char
		if char == (ENDLINE) :
			# print "End<>"
			Delivered = True
			break
		stdout.write(str(char))
		stdout.flush()

	last_state = cur_state
