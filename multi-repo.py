#!/bin/python
#
# Author: 001100010010011110100001101101110011 
#
# Run this script in a folder which contains subfolders that are GIT repositories.
# This script can be used to check status, fetch, push or pull all the found repositories at once. 
#
# Originally this was a shell script but I decided to recreate it in Python due to the portability of python. 
# Heavy improvements are still needed especially in regards to input validation.  

# src: http://stackoverflow.com/questions/3497123/run-git-pull-over-all-subdirectories 
#
#######
# Script usage.
#######
# calling script:
#       $ python multi-repo.py [directory] [command]
#       
#       Directory is optional
#               When no directory is specified the current working directory will be used!
#
#       Command is required.
#               Command can be anything defined in the val_cmd variable, at the moment this is:
#                pull, push, fetch or status
#
# The example below also indicate some risk when running the script. 
# Examples:
#       $ python multi-repo.py / push
# This runs git push in all repos found starting from the root of the filesystem, this is quite likely to break and will take a long time.
#

#####

import sys # For parsing commandline arguments.
import subprocess # To start shell processes and the like.
import os # OS to enable passing enviroment variables 


# Declare default variables. 
directory = os.getcwd() # Default directory is cwd.
command = "" # Command is empty! This ensures the script will not run when no parameters are passed.


# Function to validate variable content.
def val_vars(directory, command):
	validated = "no" # If checks are successfully completed this will be yes.
	val_cmd = ['pull','push','status','fetch'] # List of valid commands.
	
        # Check to ensure content of var directory is a valid path. 
	if os.path.isdir(directory):
		print "Directory:", directory
		if command in val_cmd:  # Check to ensure that the content of command is in list val_cmd
			# print "Command:", command # debug.
			validated = "yes" # If both directory and command checks are true set validated to yes.
			return validated # Give validated status back as result of function.
		else:
			print "Command", command, "not valid." # Print content of command to help verify why it is not valid.
			#quit()	
	else:
		# print directory # Print directory to help verify contents.
		print "Directory", directory, "does not exist!"
		#quit()

	return validated # if either directory or command checks are unsuccessfull validated is returend as "no".


def gitcmd(repodir, command): # Executes the passed command on the passed directory.. 
	cmd = ['git', command] # build the actual git command. 
	#print cmd, command # Debug
	p = subprocess.Popen(cmd, cwd=repodir) # spawn process, also allows for password entry or key validation.
	p.wait() # wait for spawned proces, this ensures multiple calls to this function don't interfere with eachother.
	
def findrepo(directory):
	# Use Popen with stdout pipe to enable p.communicate to print the output.
	repopath = [] # List for storing repository paths.
	
	# Spawn a find subprocess to iterate through `directory` looking for .git directories.	
	p_find = subprocess.Popen(["find", directory, "-name", ".git" ], stdout=subprocess.PIPE)
	p_find.wait # Wait for previous process to finish. 	

	find_lines = p_find.stdout.readlines() 
	for line in find_lines:
		#print str(line)
		repopath.append(str(line).rstrip('.git\n'))
		#print line.rstrip('.git\n')

	#return find_lines;
	return repopath


# Validate passed arguments, set the content for directory and command variables depending on the passed command line arguments. 
if len(sys.argv) > 3 or len(sys.argv) < 2: # scriptnaam is first argument therefore >3 and <2.
	print "More than three of or less than one argument supplied!"
	quit()

elif len(sys.argv) == 3: # If 2 variables are passed total equals 3, because the script itself is also seen as one:
	directory = sys.argv[1] # store argv1 content in directory.
	command = sys.argv[2] # store argv2 content in command.

elif len(sys.argv) == 2: # If 1 variable is passed total equals 2.
	command = sys.argv[1] # Store argv1 in command.
	# print "whoa" # Debug

else:	
        # If neither condition above is met print "Unknown error". 
	print "Unknown error!" 
	quit() # Extra break, normally this should not be hit, needs cleanup. 

	
# Call validated function to ensure variable content is valid.
validated = val_vars(directory, command);

# if validated was returned as yes then proceed with the rest of the script. 
if validated == "yes":
	print "proceeding with script."
	repos = findrepo(directory)
 	#	
	for repo in repos:
                print "###############"
		print repo		
		os.chdir(repo)
		#print os.getcwd()
		gitcmd(repo, command)
                print "---------------\n"
		os.chdir(directory)
		#os.chdir("/mnt/c/Users/beheerder")
	#print os.getcwd()
 	#print subprocess.call("ls")
else:
	print "something went wrong!"
	quit()

