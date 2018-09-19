#!/usr/bin/env python3 
import os, sys, re

pid = os.getpid()

# Function that forks a child process. @param args takes array of args passed by user.
def process(args):
    #this code is inspired by Dr. Freudenthal from the os-demos repo
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

def redirect(agrs1, args2):
    rc = os.fork()

    if rc == 0: 
        os.close(1)    # redirect child's stdout
        sys.stdout = open(args2, "w")
        os.set_inheritable(1, True)

        for dir in re.split(":", os.environ['PATH']): # try each directory in path
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args1, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly 

        sys.exit(1) 
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
        if len(args) == 1: #if user types in 'cd' change to home directory like bash
            os.chdir(os.getenv('HOME'))
        else:
            try:
                if args[1] == '~': #type 'cd ~' to get to home directory
                    os.chdir(os.getenv('HOME'))
                else:
                    os.chdir(args[1]) #handle a directory change
            except: #handle an unknown directory
                print("No such file or directory: ", args[1])
    elif ">" in args:
        args1 = []
        for i in args:
            if i == ">":
                break
            else:
                args1.append(i)
        args2 = args[len(args) - 1]
        redirect(args1, args2)
    else:
        process(args)