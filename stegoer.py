
import os
from time import sleep




ENDLINE = '\x92'
message = '''TheSuperASCII_Secret! ()!@#$%^&*_+-={}[];'\\:,./<>?~`|\n'''*4
# message = 'secret'
message += ENDLINE*4

delay = 0.4

files = ['/tmp/upl.gif', '/tmp/upl2.gif', '/tmp/upl3.gif', '/tmp/upl4.gif']
file_num = len(files)

initial_status = []

for f in files :
	initial_status.append( {'mod' : os.stat(f)[0], 'a_time' : os.stat(f)[-3], 'm_time' : os.stat(f)[-2], 'c_time' : os.stat(f)[-1]} )

tick = 1
def do_tick( file ) :
	global tick 		# ticking mechanism. XOR with 1 or 0 the MS
	mod = (os.stat(file)[0])
	if (tick % 2) :
		mod |= (1<<8)	# set the R user bit
	os.chmod( file, mod )
	# os.system( 'ls -l %s' % file )
	tick += 1


items, chunk = message, file_num
for c in zip(*[iter(items)]*chunk) :	# http://www.garyrobinson.net/2008/04/splitting-a-pyt.html
	
	for char, file in zip(c, files) :
		mod = ord(char)
		os.chmod(file, mod)
		print "{:5}	{:1} {:15}".format(mod, char, file)
		if char == ENDLINE :
			break

	do_tick(files[0])
	sleep( delay )


for f, st in zip(files, initial_status) :
	print st
	os.chmod(f, st['mod'])
	os.utime(f, (st['a_time'],  st['m_time']) )