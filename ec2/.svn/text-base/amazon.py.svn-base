#!/usr/bin/python

import os


class EC2(object):

    def __init__(self,fstype='ext3'):
        mk_fstab(fstype)
        mk_networking()
       

    def mk_fstab(self, fstype='ext3'):
        self.fstab = """
/dev/sda1 / %s defaults 0 1 
/dev/sda2 /mnt %s defaults 1 2 
/dev/sda3 swap swap defaults 0 0"""  % (fstype,fstype)

    def mk_networking(self):
        self.networking = """
auto lo 
iface lo inet loopback 
auto eth0 
iface eth0 inet dhcp"""
