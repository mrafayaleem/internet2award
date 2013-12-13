'''
Created on Dec 12, 2013

@author: Waqar Ahmed
'''
from mininet.log import setLogLevel
from pyretic.sdx.scripts.traffic_offloading.mininet_handler import MininetHandler
from pygraph.classes.digraph import digraph
from pygraph.algorithms.searching import depth_first_search
from pyretic.sdx.lib.hispar import *
import json
import os

cwd=os.getcwd()

if __name__ == '__main__':
    gr=Grapher()
    gr.parse(cwd+"/../../topology/mininet.topo", cwd+"/../../policies/traffic_offloading/local.cfg")
    
    mn=MininetHandler()
    setLogLevel('info')
    (cli, controller)=mn.getArgs()     
    mn.simple(controller, gr)
    
    q=Quality(gr, mn)
    q.latency()
    