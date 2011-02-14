import re
import sys
from ftplib import FTP

class FtpFileFinder(object):
    ftp = None
    dirs = []
    files = []
    curDirs = []
    dirname = ''

    def __init__(self, server, username='anonymous', password=''):
        super(FtpFileFinder, self).__init__()
        self.ftp = FTP(server)
        self.ftp.login(username, password)

        self.listDir()
       
        self.ftp.quit()
        for fname in self.files:
            if fname.find('htaccess')!=-1:
                print fname

    def listDir(self):
        #print 'Listing dir ' + self.dirname
        self.ftp.cwd(self.dirname)
        self.ftp.retrlines('LIST', self.findFile)

        while len(self.curDirs) > 1:
            self.dirname = self.curDirs.pop()
            self.listDir()

    def findFile(self, line):
        arr = line.split(' ')
        fname = arr[len(arr)-1]

        m = re.match('^d.*', line)
        if m!= None and fname!='.' and fname!='..':
            self.curDirs.append(self.dirname + '/' + fname)
        else:
            self.files.append(self.dirname + '/' + fname)

def usage():
    print 'Usage: python ftpsearch.py servername [username] [password]'
    exit(1)

def main():
    server = ''
    username = ''
    password = ''

    if len(sys.argv) < 2:
        usage()
    if len(sys.argv) > 1:
        server = sys.argv[1]
    if len(sys.argv) > 2:
        username = sys.argv[2]
    if len(sys.argv) > 3:
        password = sys.argv[3]

    fff = FtpFileFinder(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == '__main__':
    main()
