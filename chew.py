#!/usr/bin/python
import argparse
import os
import shutil
import urllib2
import json
import sys

# Constants
KITCHEN = '/usr/local/Kitchen'
BIN = '/usr/local/bin'

def parseArgs():
    parser = argparse.ArgumentParser(description='Copy a file from base/default into a user specified theme and commit the file.')
    parser.add_argument('Operation', metavar='operation', choices=['install', 'update', 'remove'],
                       help='the operation you wish to perform.')
    parser.add_argument('Package', metavar='package', 
                       help='the shortname for the package you wish to perform the operation on.')

    args = parser.parse_args()
    return args

def getRepoUrl(package):
    url = 'https://secure.meanbee.com/fridge/?' + package
    result = urllib2.urlopen(url).read()
    dict = json.loads(result)
    
    if dict['status'] == 'OK':
        return dict['content']
    else:
        writeErrorAndExit('Error while retrieving package: ' + dict['content'], 1)

def goToKitchen():
    # See if the Kitchen exists...
    if not os.path.isdir(KITCHEN):
        # It doesn't, lets make it
        os.makedirs(KITCHEN)

    # Change directory into the kitchen
    os.chdir(KITCHEN)

def cloneRepository(package, repo_url):
    if (os.path.isdir(package)):
        # The package already exists!
        writeErrorAndExit("Error while cloning the package: Package already exists. Did you mean update?", 2)

    os.system('git clone ' + repo_url + ' ' + package)
    writeSuccess("Package installed successfully!")

def goToBin():
    # See if the Kitchen exists...
    if not os.path.isdir(BIN):
        # It doesn't, lets make it
        os.makedirs(BIN)

    # Change directory into the bin folder
    os.chdir(BIN)

def writeSuccess(message):
    sys.stderr.write('\033[92m' + '[chew] Success: ' + message + '\033[0m' + '\n')

def writeError(message):
    sys.stderr.write('\033[91m' + '[chew] An error occurred: ' + message + '\033[0m' + '\n')
    
def writeErrorAndExit(message, exit_code = 1):
    writeError(message)
    sys.exit(exit_code)

def makeSymlink(package):
    #Make the symlink
    src = KITCHEN + '/' + package + '/' + package
    dest = BIN + '/' + package
    os.system('ln -s ' + src + ' ' + dest)


def removePackageFromKitchen(package):
    # Check if the package exists
    if not os.path.isdir(package):
        # It doesn't exist! :O Tell the user at once!
        writeErrorAndExit("Error while trying to remove the package: Package folder not found", 4)

    # Package file exists... Let's remove it
    shutil.rmtree(package)
    
def removeSymlink(package):
    os.remove(package)

def updatePackage(package):
    # Check if the package exists
    if not os.path.isdir(package):
        # It doesn't exist! :O Tell the user at once!
        writeErrorAndExit("Error while updating the package: Package folder not found", 5)

    # Package file exists... Let's update it
    os.chdir(package)
    os.system('git pull origin master')
    writeSuccess("Package updated successfully!")


# !!! SCRIPT STARTS HERE !!!

try:
    # Let's get some arguments
    args = parseArgs()
    package = args.Package
    op = args.Operation

    if op == 'install':
        # Get the git repository associated with this package
        repo_url = getRepoUrl(package)
    
        # Go to the Kitchen, it's time to bake!
        goToKitchen()
    
        # Let's get the repository
        cloneRepository(package, repo_url)
    
        # Cool, let's make a symlink to the bin folder
        goToBin()
        makeSymlink(package)
    
        # Done

    elif op == 'remove':
        # Let's go to the Kitchen to find the package
        goToKitchen()

        # Remove the package from here
        removePackageFromKitchen(package)

        # Remove the symlink also
        goToBin()
        removeSymlink(package)

        # Done

    elif op == 'update':
        # Go into the kitchen first of all
        goToKitchen()

        # Next, lets go into the package folder and update
        updatePackage(package)

        # Done

    else:
        # argparse should prevent anyone getting here.
        writeErrorAndExit("Unrecognised operation", 3)
except Exception as (errno, strerror):
    writeErrorAndExit("Unexpected error: " + strerror, 2)
