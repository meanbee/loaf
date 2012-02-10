#!/usr/bin/python
import argparse
import os
import shutil

def parseArgs():
    parser = argparse.ArgumentParser(description='Copy a file from base/default into a user specified theme and commit the file.')
    parser.add_argument('Package', metavar='package', 
                       help='the shortname for the package you wish to install.')

    args = parser.parse_args()
    return args

#TODO unstub this
def getRepoUrl(package):
    return 'git@codebasehq.com:meanbee/general/dac.git'

# Commence the running!
args = parseArgs()
package = args.Package

# Get the git repository associated with this package
repo_url = getRepoUrl(package)

