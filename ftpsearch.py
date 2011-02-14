import re
import sys
import argparse
from ftplib import FTP
import cPickle as pickle

class FtpFileFinder(object):
    ftp = None
    dirs = []
    files = []
    curDirs = []
    dirname = ''

    def __init__(self):
        super(FtpFileFinder, self).__init__()

    def openRemote(self, server, username, password):
        self.ftp = FTP(server)
        self.ftp.login(username, password)

    def closeRemote(self):
        self.ftp.quit()
        self.ftp = None

    def findFile(self, filename):
        for fname in self.files:
            if fname.find(filename)!=-1:
                print fname

    def saveToFile(self, filename):
        pickle.dump(self.files, open(filename, 'wb'))

    def loadFromFile(self, filename):
        self.files = pickle.load(open(filename, 'rb'))

    def listDir(self, dirname=''):
        if len(dirname) > 0 and len(self.dirname) == 0:
            self.dirname = dirname
        #print 'Listing dir ' + self.dirname
        self.ftp.cwd(self.dirname)
        self.ftp.retrlines('LIST', self.addFile)

        while len(self.curDirs) > 1:
            self.dirname = self.curDirs.pop()
            self.listDir()

    def addFile(self, line):
        arr = line.split(' ')
        fname = arr[len(arr)-1]

        m = re.match('^d.*', line)
        if m!= None:
            if fname!='.' and fname!='..':
                self.curDirs.append(self.dirname + '/' + fname)
        elif fname!='.' and fname!='..':
            self.files.append(self.dirname + '/' + fname)

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
        fff.saveToFile(args.server+'.arch')

    if args.arch!=None:
        fff.loadFromFile(args.arch)

    fff.findFile(args.filename)

if __name__ == '__main__':
    main()
