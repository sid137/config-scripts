#!/usr/bin/python

import os

class Script(object):
    def __init__(self, cmds):
        try:
            for cmd in cmds.split('\n'):
                os.system(cmd)
        except Exception:
            os.system(cmds)
    
class Linux(object): pass

class RedHat(Linux): pass
class CentOS(RedHat): pass
class FedoraCore(RedHat): pass

class Debian(Linux):
    """Class to mange Debian installations via debootstrap
    sudo apt get install debootstrap"""

    releases = {'stable': 'etch', 'testing': 'lenny', 'unstable': 'sid'}
    architectures = ['alpha', 'amd64', 'arm', 'hppa', 'hurd-i386', 'i386', \
                              'ia64', 'm68k', 'mips', 'mipsel', 'powerpc', 's390',  'sparc']
    repos = "ftp://ftp.fr.debian.org/debian"
    
    def __init__(self,  arch='amd64', release='stable'):      
        self.arch = arch
        self.release = release

    def install(self, dest):
        try:
            dest.mount()
            target = dest.target
        except TypeError:
            target = dest
        print "Installing base system.."
      
        cmd = 'sudo debootstrap --arch %s  %s %s %s' % (self.arch, self.release, target, self.repos)
        os.system(cmd)
        return
        
class Ubuntu(Debian):
    repos = "http://archive.ubuntu.com/ubuntu"
    releases = ['edgy', 'feisty', 'gutsy']

    def __init__(self,   arch='amd64', release='gutsy'):        
        super(Ubuntu, self).__init__(arch, release)
     
