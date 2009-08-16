#!/usr/bin/python 
"""
This script is meant to handle automated downloads, extraction, compilation,
and installation of files from source, or from apt-repositories.

File package information is specified in a .yaml file, which is sent as input.  The
yaml file is processed, and for each package installation, information is extracted
such as the package or svn location, compiler directives, special compilation
commands and environment variables, Apt source repositories

Requires several packages utilities first:
python python-yaml subversion bzip2 unzip tar sed sudo

These should be installed at initial system setup, and allow this program to continue from there
"""
import os, re
import threading
import yaml
from fileutils import *
from utils import *

#on archive
archive = re.compile(".*/(.*)").match
ext =  re.compile("(.*)\.(gz|bz2|tgz|zip)$").match

    
class Package(yaml.YAMLObject):
    def __init__(self, source='', flags='', env=None, cmd='', tmp='', file='',  dir='', \
                 svn='', apt_src='', apt_pkg='', proxy_user='', proxy_pass='', targ_dir = '/usr/local/src'):
         
        initFromArgs(self)
        try:  #process environment vars if specified as string
            self.env =  dict(v.split('=') for v in env)
        except (AttributeError, TypeError, ValueError): pass
        self.build = ''
        if apt_src:
            ensure_present(apt_src, '/etc/apt/source.list', True)
            run_cmd('sudo apt-get update')
        if apt_pkg:
            print "Installing packages: ", apt_pkg
            run_cmd( 'sudo apt-get install --assume-yes --allow-unauthenticated --fix-broken %s' % apt_pkg)
           
        self.source = source
        self.flags = flags   
        self.cmd = cmd
        self.tmp = tmp
        self.file = file
        self.dir = dir
        self.svn = svn
       
        self.proxy_user = proxy_user
        self.proxy_pass = proxy_pass
        self.targ_dir = targ_dir
         
        
    def download_source(self):
        archive_name = archive(self.source).group(1)
        self.file = os.path.join(self.targ_dir, archive_name)
        print "Saving %s to: %s" % (self.source, self.file)
        run_cmd('sudo wget %s --timestamping --directory-prefix=%s --retr-symlinks  \
            --proxy-user=%s --proxy-password=%s --no-check-certificate '  \
                        % (self.source, self.targ_dir, self.proxy_user, self.proxy_pass))

    def download_dir(self):
        dirname = os.path.basename(self.dir)
        self.build = os.path.join(self.targ_dir, dirname)    
        run_cmd('sudo cp --recursive --preserve --target-directory %s --update --force %s' \
                  % (self.targ_dir, self.dir))
  
    def download_svn(self):
        self.svn, dirname = self.svn.split()
        self.build = os.path.join(self.targ_dir, dirname)
        print "Checking out %s to: %s" % (self.svn, self.build)
        run_cmd('sudo svn co %s %s' % (self.svn, self.build))
    
    def download(self):
        """Downloads package via svn, or http GET
        First checks to see if local file or directory is specified and  exists, if not,
        it then attempts SVN download.  Finally tries source tarball dl
        """
        
        if os.path.isdir(self.dir):
            self.download_dir()
        elif self.svn:
            self.download_svn()
        elif self.source:
            self.download_source()

    
    def extract(self):
        if self.file:  
#            assert os.path.isfile(self.file)

            extension = ext(self.file).group(2)
            tar = {'gz':'-zxvf', 'tgz':'-zxvf','bz2':'-jxvf'}

            #doesn't handle badly packaged archives
            if extension in tar:
                cmd = "sudo tar %s %s -C %s | tail -n1 | sed -e 's/\([^/]*\).*/\\1/'" % (tar[extension], self.file, self.targ_dir)
            elif extension == 'zip':
                cmd = "sudo unzip -d %s %s | tail -n1 | sed -e 's/.*: \([^/]*\).*/\\1/'" % (self.targ_dir, self.file)

            base_dir = run_cmd(cmd).strip()
            self.build = os.path.join(self.targ_dir, base_dir)
            print "Extracted %s to: %s " % (self.file, self.build)

    def install(self):
        """Downloads, extracts, compiles and installs source code represented by the
        'package' config
        """
        
        if self.cmd:
            cmd = self.cmd
        elif os.path.isfile(os.path.join(self.build,'configure')):
            cmd = ' sudo ./configure %s && sudo make && sudo make install' % self.flags
        elif os.path.isfile(os.path.join(self.build,'setup.py')):
            cmd = 'sudo python setup.py build; sudo python setup.py install'
        elif os.path.isfile(os.path.join(self.build,'autogen.sh')):
            cmd = """
 	    sudo mkdir build && cd build
 	    sudo ./configure %s
 	    sudo make all install
            """ % self.flags
 	else:
            cmd = 'sudo make && sudo make install'
        run_cmd(cmd, env=self.env, cwd=self.build)

def main(filename):
    sequence = []
    for config in yaml.load(open(filename)):
        print config
        sequence.append(Package(**config)) # serial 

    for package in sequence:
        package.download() #threaded

    for package in sequence:
        package.extract() # threaded
    exit()
    for package in sequence:
        print package
        package.install()
        
if __name__ == "__main__":
    main('soft.yaml')

