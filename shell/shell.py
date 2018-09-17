#!/usr/bin/env python3 
import os, sys, re

pid = os.getpid()

# Function that forks a child process. @param args takes array of args passed by user.
def process(args):
    rc = os.fork()
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:
        for dir in re.split(":", os.environ['PATH']): # try each directory in path
            path = "%s/%s" % (dir, args[0]) 
            try:
                 # try to exec program
                 os.execve(path, args, os.environ)
            except FileNotFoundError:             # ...expected
                pass 
        print("command not found")
        sys.exit()
    else:  
        os.wait()

while True:
    args = input('$ ')
    #args = input(u'💥' + ' ')
    args = args.split()
    #print(args)
    if not args:
        continue
    if args[0] == "exit":
        break 
    elif args[0] == "cd": #handle a change directory command
        if len(args) == 1:
            os.chdir(os.getenv('HOME'))
        else:
            try:
                if args[1] == '~':
                    os.chdir(os.getenv('HOME'))
                else:
                    os.chdir(args[1])
            except:
                print("No such file or directory: ", args[1])
    else:
        process(args)