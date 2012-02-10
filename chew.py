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
    parser.add_argument('Package', metavar='package', 
                       help='the shortname for the package you wish to install.')

    args = parser.parse_args()
    return args

def getRepoUrl(package):
    url = 'https://secure.meanbee.com/fridge/?' + package
    result = urllib2.urlopen(url).read()
    dict = json.loads(result)
    
    if dict['status'] == 'OK':
        return dict['content']
    else:
        sys.stderr.write('Error while retrieving package: ' + dict['content'] + '\n');
        sys.exit(1)

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
        sys.stderr.write('Error while cloning the package: Package already exists. Did you mean update?' + '\n');
        sys.exit(2)
        

    os.system('git clone ' + repo_url + ' ' + package)

def makeSymlink(package):
    # See if the Kitchen exists...
    if not os.path.isdir(BIN):
        # It doesn't, lets make it
        os.makedirs(BIN)

    # Change directory into the bin folder
    os.chdir(BIN)
        
    #Make the symlink
    src = KITCHEN + '/' + package + '/' + package
    dest = BIN + '/' + package
    os.system('ln -s ' + src + ' ' + dest)

    
    

# !!! SCRIPT STARTS HERE !!!

# Let's get some arguments
args = parseArgs()
package = args.Package

# Get the git repository associated with this package
repo_url = getRepoUrl(package)

# Go to the Kitchen, it's time to bake!
goToKitchen()

# Let's get the repository
cloneRepository(package, repo_url)

# Cool, let's make a symlink to the bin folder
makeSymlink(package)

# Done.
