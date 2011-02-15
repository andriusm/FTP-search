#!/usr/bin/env python
"""
This script helps you find files on a remote FTP server.
It's also possible to search the cached version of the
site with no network access.
"""

import re
import sys
import anydbm
import argparse
from ftplib import FTP

__version__ = "0.1"
__author__ = "Andrius Miasnikovas"
__license__ = "psf"

class FtpFileFinder(object):
    db = None
    ftp = None
    dirs = []
    dirname = ''

    def __init__(self):
        super(FtpFileFinder, self).__init__()

    def openRemote(self, server, username, password):
        self.db = anydbm.open(server + '.arch', 'n')
        self.ftp = FTP(server)
        self.ftp.login(username, password)

    def closeRemote(self):
        self.ftp.quit()
        self.ftp = None
        self.db.sync()

    def findFile(self, filename):
        for k,v in self.db.items():
            if v.lower().find(filename) != -1:
                print k

    def loadFromFile(self, archfile):
        self.db = anydbm.open(archfile.name, 'r')

    def listDir(self, dirname=''):
        if len(dirname) > 0 and len(self.dirname) == 0:
            self.dirname = dirname
        self.ftp.cwd(self.dirname)
        self.ftp.retrlines('LIST', self.addFile)

        while len(self.dirs) > 1:
            self.dirname = self.dirs.pop()
            self.listDir()

    def addFile(self, line):
        arr = line.split(' ')
        fname = arr[len(arr)-1]
        absolute = self.dirname + '/' + fname

        m = re.match('^d.*', line)
        if m!= None:
            if fname!='.' and fname!='..':
                self.dirs.append(absolute)
        elif fname!='.' and fname!='..':
            self.db[absolute] = fname

def main():
    parser = argparse.ArgumentParser(description='Search remote FTP site for a file. If archive filename is specified the network connection is not used.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-s', '--server', help='Hostname or IP address of the FTP server')
    group.add_argument('-a', '--arch', type=file, help='Previously created archive file which contains the FTP site structure')
    parser.add_argument('filename', help='Filename to look for on the FTP site')
    parser.add_argument('-u', '--user', default='anonymous', help='Username for the FTP site (default - anonymous)')
    parser.add_argument('-p', '--pwd', default='', help='Password for the FTP site')
    parser.add_argument('-d', '--dir', default='/', help='Remote directory that denotes the root of the search tree, location must be absolute (default - /)')
    args = parser.parse_args()

    fff = FtpFileFinder()

    if args.server!=None:
        fff.openRemote(args.server, args.user, args.pwd)
        fff.listDir(args.dir)
        fff.closeRemote()

    if args.arch!=None:
        fff.loadFromFile(args.arch)

    fff.findFile(args.filename)

if __name__ == '__main__':
    main()
