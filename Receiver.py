#!/usr/bin/env python
import os
from time import sleep
from sys import stdout, exit
import argparse


ENDLINE = '\x92'

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group( required = True )
group.add_argument( '--directory', '-d', help = 'Use all files in this directory in the * "ls" returns them (BEWARE: MUST BE WRITABLE)')
group.add_argument( '--files', '-f', help = 'Use the listed files as in the * they are given', nargs = '*')

args = parser.parse_args()
# print args

files = args.files
if args.directory :
	files = [ (args.directory + x) for x in os.listdir( args.directory ) ]

# print files
Delivered = False

def tick(file) :							# Returns the "Tick bit" (First file's Owner Read bit)
	return (os.stat(file)[0] % 512) ^ 512 	# as boolean


def consume_char( char ) :

		stdout.write(str(char))				# Print Char without newlines
		stdout.flush()						# Flush the output stream


last_state = tick(files[0])					# Gets the state of Tick Bit
while not Delivered :

	cur_state = tick(files[0])				# Saves the current Tick Bit
	while cur_state == last_state :			# If the current and previous Tick bits are same
		sleep (0.1)							# Wait a while
		cur_state = tick(files[0])			# Get new Tick bit in case it changed
											# Spin-Lock until Tick bit Changes


	for f in files :						# Tick happened - New data in file privileges!

		mod = (os.stat(f)[0])				# Get the privilege int
		char = chr(mod % 256)				# Strip it to 1 byte and save it as ASCII Character
		if char == (ENDLINE) :				# If it is the Special Character
			Delivered = True				# The Message has been delivered
			break

		consume_char( char )				# Consume char in some way. Default: print it.

	last_state = cur_state
