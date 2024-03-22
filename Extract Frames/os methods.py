
# The *os* and *os.path* modules include many functions to interact with the file system.
# Python-OS-Module Functions

# Here we will discuss some important functions of the Python os module :

#     Handling the Current Working Directory
#     Creating a Directory
#     Listing out Files and Directories with Python
#     Deleting Directory or Files using Python


# ====================================================================================
# Getting the Current working directory 

import os 
cwd = os.getcwd() 
print("Current working directory:", cwd) 

# ====================================================================================
# Changing the Current working directory

import os 
def current_path(): 
	print("Current working directory before") 
	print(os.getcwd()) 
	print() 
current_path() 
os.chdir('../') 
current_path()

# ====================================================================================
# Creating a Directory
# Using os.mkdir(): This method raises FileExistsError if the directory to be created already exists

import os
directory = "GeeksforGeeks"
parent_dir = "D:/Pycharm projects/"
path = os.path.join(parent_dir, directory)

os.mkdir(path)
print("Directory '% s' created" % directory)
directory = "Geeks"
parent_dir = "D:/Pycharm projects"
mode = 0o666	 # a specific mode (0o666) is provided, which grants read and write permissions. 
path = os.path.join(parent_dir, directory)
os.mkdir(path, mode)
print("Directory '% s' created" % directory)


# Using os.makedirs(): That means while making leaf directory if any intermediate-level directory is missing, 
# 	os.makedirs() method will create them all.

import os
directory = "Nikhil"
parent_dir = "D:/Pycharm projects/GeeksForGeeks/Authors"
path = os.path.join(parent_dir, directory)
os.makedirs(path)
print("Directory '% s' created" % directory)
directory = "c"
parent_dir = "D:/Pycharm projects/GeeksforGeeks/a/b"
mode = 0o666
path = os.path.join(parent_dir, directory)
os.makedirs(path, mode)
print("Directory '% s' created" % directory)

# ====================================================================================
# Listing out Files and Directories with Python

import os 
path = "/"
dir_list = os.listdir(path) 
print("Files and directories in '", path, "' :") 
print(dir_list) 

# ====================================================================================
# Deleting Directory or Files using Python

# Using os.remove() Method: os.remove() method in Python is used to remove or delete a file path. 
# 	This method can not remove or delete a directory.
# 	If the specified path is a directory then OSError will be raised by the method.

import os 
file = 'file1.txt'
location = "D:/Pycharm projects/GeeksforGeeks/Authors/Nikhil/"
path = os.path.join(location, file) 
os.remove(path) 


# Using os.rmdir(): os.rmdir() method in Python is used to remove or delete an empty directory. 
# 	OSError will be raised if the specified path is not an empty directory.

import os 
directory = "Geeks"
parent = "D:/Pycharm projects/"
path = os.path.join(parent, directory) 
os.rmdir(path)

# ====================================================================================
# Commonly Used Functions

# Using os.name function: This function gives the name of the operating system dependent module imported. 
import os
print(os.name)

# Using os.error Function: All functions in this module raise OSError in the case of invalid 
# 	or inaccessible file names and paths, or other arguments.
# 	os.error is an alias for built-in OSError exception.
import os
try:
	filename = 'GFG.txt'
	f = open(filename, 'rU')
	text = f.read()
	f.close()
except IOError:
    print('Problem reading: ' + filename)

# Using os.remove() Function: Using the Os module we can remove a file in our system
import os 
os.remove("file_name.txt") #removing the file.

# Using os.path.exists() Function: This method will check whether a file exists or not by passing the name of the file as a parameter.
import os 
result = os.path.exists("file_name") #giving the name of the file as a parameter.
print(result)

# Using os.path.getsize() Function: In os.path.getsize() function, python will give us the size of the file in bytes. 
import os #importing os module
size = os.path.getsize("filename")
print("Size of the file is", size," bytes.")


# ====================================================================================

# ====================================================================================

# ====================================================================================




