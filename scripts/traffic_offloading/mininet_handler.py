#!/usr/bin/python
################################################################################
#
#  <website link>
#
#  File:
#        sdx_mininet_traffic_offloading.py
#
#  Project:
#        Software Defined Exchange (SDX)
#
#  Author:
#        Muhammad Shahbaz
#        Arpit Gupta
#        Laurent Vanbever
#
#  Copyright notice:
#        Copyright (C) 2012, 2013 Georgia Institute of Technology
#              Network Operations and Internet Security Lab
#
#  License:
#        This file is part of the SDX development base package.
#
#        This file is free code: you can redistribute it and/or modify it under
#        the terms of the GNU Lesser General Public License version 2.1 as
#        published by the Free Software Foundation.
#
#        This package is distributed in the hope that it will be useful, but
#        WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#        Lesser General Public License for more details.
#
#        You should have received a copy of the GNU Lesser General Public
#        License along with the SDX source package.  If not, see
#        http://www.gnu.org/licenses/.
#

import sys, getopt
from mininet.topo import SingleSwitchTopo
from mininet.net import Mininet
from mininet.node import RemoteController
from pyretic.sdx.lib.hispar import *

class MininetHandler(object):
    def getArgs(self):
        cli = False;
        controller = '127.0.0.1'
        
        try:
            opts, args = getopt.getopt(sys.argv[1:],"h",["help", "cli", "controller="])
        except getopt.GetoptError:
            print 'sdx_mininet_simple.py [--cli --controller <ip address>]'
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                
                print 'sdx_mininet_simple.py [--cli --controller <ip address>]'
                sys.exit()
            elif opt == '--cli':
                cli = True
            elif opt == '--controller':
                controller = arg
        return (cli, controller)
       
    def simple(self, controllerIP, grapher):
        "Create and test SDX Simple Module"
        self.AS_to_host={}
        self.grapher=grapher
         
        print "Creating the topology with one IXP switch and three participating ASs\n\n" 
        topo = SingleSwitchTopo(k=3)
        self.net = Mininet(topo, controller=lambda name: RemoteController( 'c0', controllerIP ), autoSetMacs=True) #, autoStaticArp=True)
        self.net.start()
        self.hosts=self.net.hosts
        print "Configuring participating ASs\n\n"
        for host in self.hosts:
            if host.name=='h1':
                self.AS_to_host["A"]=host
                host.cmd('ifconfig lo:40 110.0.0.1 netmask 255.255.255.0 up')
                host.cmd('route add -net 120.0.0.0 netmask 255.255.255.0 gw 10.0.0.2 h1-eth0')
                host.cmd('route add -net 130.0.0.0 netmask 255.255.255.0 gw 10.0.0.2 h1-eth0')
            if host.name=='h2':
                self.AS_to_host["B"]=host
                host.cmd('route add -net 110.0.0.0 netmask 255.255.255.0 gw 10.0.0.1 h2-eth0')
                host.cmd('ifconfig lo:40 120.0.0.1 netmask 255.255.255.0 up')
                host.cmd('route add -net 130.0.0.0 netmask 255.255.255.0 gw 10.0.0.3 h2-eth0')
            if host.name=='h3':
                self.AS_to_host["C"]=host
                host.cmd('route add -net 110.0.0.0 netmask 255.255.255.0 gw 10.0.0.2 h3-eth0')
                host.cmd('route add -net 120.0.0.0 netmask 255.255.255.0 gw 10.0.0.2 h3-eth0')
                host.cmd('ifconfig lo:40 130.0.0.1 netmask 255.255.255.0 up')
            
            self.AS_to_host["A"].cmd("ping -c 2 -I 110.0.0.1 120.0.0.1")    
            
        
    def latency(self, AS1, AS2, count):
        #print self.AS_to_host["A"].cmd("ping -c 5 -I 110.0.0.1 120.0.0.1")
        "Returns latency between AS1 and AS2"
        command = "ping -c " + str(count) + " -I " + self.grapher.graph.node_attr[AS1]["IP"][0] + " " + self.grapher.graph.node_attr[AS2]["IP"][0] + " | tail -1| awk '{print $4}' | cut -d '/' -f 2"
        return self.AS_to_host[AS1].cmd(command)