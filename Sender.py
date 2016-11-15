#!/usr/bin/env python
import os, sys
import argparse
from time import sleep

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group( required = True )
group.add_argument( '--directory', '-d', help = 'Use all files in this directory in the * "ls" returns them (BEWARE: MUST BE WRITABLE)')
group.add_argument( '--files', '-f', help = 'Use the listed files as in the * they are given', nargs = '*')

parser.add_argument( '--delay', default = 0.5, type = float, help = "Set the delay between the chmod's")
parser.add_argument( 'message', help = 'Message to be transmitted. Can be the output of a shell command if you use backticks (`) or $() expression in double-quotes ("").\r\nExample: %s -d sample_files/ "$(cat /etc/passwd | head)"' % sys.argv[0])
args = parser.parse_args()


ENDLINE = '\x92'
# message = '''TheSuperASCII_Secret! ()!@#$%^&*_+-={}[];'\\:,./<>?~`|\n'''*4
message = args.message
delay = args.delay

files = args.files
if args.directory :
	files = [ (args.directory + x) for x in os.listdir( args.directory ) ]
file_num = len(files)
message += ENDLINE * file_num

initial_status = []							# Get the Initial State of all files
for f in files :
	initial_status.append( {'mod' : os.stat(f)[0], 'a_time' : os.stat(f)[-3], 'm_time' : os.stat(f)[-2], 'c_time' : os.stat(f)[-1]} )



def revert_chmod() :
	for f, st in zip(files, initial_status) :
		os.chmod(f, st['mod'])
		os.utime(f, (st['a_time'],  st['m_time']) )



tick = 1
def do_tick( file ) :						# Ticking mechanism.
	global tick 							# Toggle the Owner Read bit of First File in List
	mod = (os.stat(file)[0])				# 
	if (tick % 2) :
		mod |= (1<<8)
	os.chmod( file, mod )
	tick += 1

MessageEnded = False
try :

	items, chunk = message, file_num
	for c in zip(*[iter(items)]*chunk) :	# http://www.garyrobinson.net/2008/04/splitting-a-pyt.html
		
		if MessageEnded :
			break

		for char, file in zip(c, files) :	# pick a char and a file
			mod = ord(char)					# make the char an int
			os.chmod(file, mod)				# chmod the file with that int

			if char == '\n' :
				char = '\\n'
			print "{:5}	{:1} {:15}".format(mod, char, file)

			if char == ENDLINE :			# If we found the special character
				MessageEnded = True
				break						# The message is over

		do_tick(files[0])
		sleep( delay )



except KeyboardInterrupt :					# In case of Ctrl - C
	revert_chmod()							# Revert all files to initial state
	print 
	print "Aborted by user..."
	sys.exit(-1)							# Exit non-zero

revert_chmod()								# Revert files before exiting gracefully