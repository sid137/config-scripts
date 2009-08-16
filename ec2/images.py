#!/usr/bin/python
"""Module contains class definitions for creating disk images, and installing
    Debian and Ubuntu systems with debootstrap"""


import os
from linux import *
from optparse import OptionParser

    
class Image:

    def __init__(self, name, size=1024, fstype='reiserfs', target=''):
        self.name = name
        self.size = size
        self.fstype = fstype
        self.target = target or os.path.basename(os.path.splitext(name)[0])+'_chroot'
        
    def create(self):
        """Creates a new disk image with the specified name, and
            size in megabytes"""
        
        print "Creating new image %s..." % self.name
        os.system('dd if=/dev/zero of=%s bs=1M status=noxfer count=%d ' % (self.name, self.size))

    def make_fs(self, fstype='reiserfs'):
        """ Formats image with specified filesystem.  Created image if it doesn't exist"""
        if fstype == 'ext3':
            cmd = 'mke2fs -F -j -q'
        elif fstype == 'reiserfs':
            cmd = 'mkreiserfs -f -q'
        elif fstype == 'reiser4':
            # sudo apt-get install  reiser4progs libreiser4-dev
            cmd = 'mkreiser4 -f -y'
        elif fstype == 'xfs':
            # sudo apt-get install  xfslibs-dev xfsdump xfsprogs
            cmd = 'mkfs.xfs -f -q'
        elif fstype == 'jfs':
            #  sudo apt-get install jfsutils
            cmd = 'mkfs.jfs -q'
            
        if not os.path.exists(self.name):
            self.create()
        print "Formatting %s as %s filesystem..." % (self.name, fstype)
        os.system(cmd+' '+self.name)

    def mount(self):
        if not os.path.isdir(self.target):
            os.mkdir(self.target)
        cmd = 'sudo mount -o loop %s %s' % (self.name, self.target)
        os.system(cmd)

    def install(self, distribution=Debian()):
        """Installs the distribution which is passed as an argument.
        Defaults to Debian stable"""
        distribution.install(self)
        self.unmount()

    def unmount(self):
        """Unmount image from mount point"""
        print "Unmounting %s..." % self.name
        cmd = 'sudo umount %s' % self.name
        os.system(cmd)
        os.removedirs(self.target)
        
    def setup(self):
        self.create()
        self.make_fs()
        self.mount()
        self.install()
        
    def chroot(self):
        """Chroot to target directory of image"""
        os.system('sudo chroot %s /bin/bash' % os.path.realpath(self.target))

def main():
    parser = OptionParser()
    parser.set_defaults(name='debian.fs', create_image=False)
    parser.add_option('-n', '--name', help="Displays this help message")
    parser.add_option('-c', '--create_image', action="store_true", help="Create a new disk image")
    parser.add_option('-f', '--filesystem', help='Filesystem type to write to image')
    parser.add_option('-m', '--mount', help='Mount point for image')
    parser.add_option('-s', '--size', help='Size of disk image in megabytes')
    parser.add_option('-a', '--all', help='Run all steps to create disk image and install OS')
    (options, args) = parser.parse_args()



    name = options.name
    image = Image(name)

    image.make_fs('ext3')
    Debian(release='lenny').install(image)
    image.chroot()
    os.system('echo `pwd` > test')
    os.system('exit')
    image.unmount()

if __name__ == "__main__":
    main()



