'''
Created on Dec 12, 2013

@author: root
'''

'''
Created on Dec 12, 2013

@author: mininet
'''

from pygraph.classes.digraph import digraph
from pygraph.algorithms.searching import depth_first_search
import json

class Grapher(object):
    def parse(self, topo_file, IPs_file):
        self.graph = digraph()
        
        #Temporary path
        topo=json.load(open(topo_file, 'r'))
        self.IPdict=json.load(open(IPs_file, 'r'))
        
        for key in topo.keys():
            self.graph.add_node(key, self.IPdict[key])
            
        for key in topo.keys():
            for peer in topo[key]["Peers"]:
                self.graph.add_edge((key, peer))
                
    def get_all_reachable(self, node):
        st, pre, post = depth_first_search(self.graph, root=node)
        return st.keys()
    
class Quality(object):
    PING_COUNT=4
    
    def __init__(self, gr, mn):
        self.gr=gr
        self.mn=mn
        
    def latency(self):
        for node in self.gr.graph.nodes():
            for reachable in self.gr.get_all_reachable(node):
                if(reachable!=node):
                    print node + " -> " + reachable + ": " + self.mn.latency(node, reachable, Quality.PING_COUNT)
            