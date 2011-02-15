FTP search
==========

Overview
--------

In short it's a script that allows one to search a specified FTP site for files.

Because of the FTP protocol's synchronous nature the site is first crawled by
the script and an in-memory list of all files is created. Only then this list
is checked for the file in question. To conserve network bandwidth and cut down
search time the file list is stored as a dbm file after the site crawling is
done.

Invocation
----------

Usage: ftpsearch.py [-h] (-s SERVER | -a ARCH) [-u USER] [-p PWD] [-d DIR] filename

Search remote FTP site for a file. If archive filename is specified the network connection is not used.

positional arguments:
  filename              Filename to look for on the FTP site

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER  Hostname or IP address of the FTP server
  -a ARCH, --arch ARCH        Previously created archive file which contains the FTP site structure
  -u USER, --user USER        Username for the FTP site (default - anonymous)
  -p PWD, --pwd PWD           Password for the FTP site
  -d DIR, --dir DIR           Remote directory that denotes the root of the search tree, location must be absolute (default - /)

First run example:

    ftpsearch.py -s ftp.example.org -u myuser -p pwd123 -d /public/myweb index.html

This will connect to the server ftp.example.org using the account myuser and password pwd123,
traverse the site starting at /public/myweb (remember that remote path must be absolute) and
then look for files named index.html (multiple matches are possible). After a successful run
a new archive (.arch) file will be created that represents the list of remote files. It can
be used later to search the same site by specifying the local archive file instead of a
remote FTP server. Just keep in mind that the results might not be as accurate if someone
else has updated the site.

Subsequent run example:

    ftpsearch.py -a ftp.example.org.arch index.php

This will open a local archive file ftp.example.org.arch (automatically named after the FTP
server) and search for a file named index.php. In this scenario no network connections will
be created so the search will be much master.

Contacts
--------

URL: http://andrius.miasnikovas.lt
Andrejus Miasnikovas <andriusms@gmail.com>

