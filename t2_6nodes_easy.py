#!/usr/bin/python

"""

"""

from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.topo import Topo
from mininet.log import lg, info
from mininet.util import irange, quietRun
from mininet.link import TCLink
from mininet.cli import CLI

import sys
flush = sys.stdout.flush

class ExampleTestTopo( Topo ):
    
    def __init__( self, **params ):

        # Initialize topology
        Topo.__init__( self, **params )

        # Create switches and hosts
        N = 6
        hosts = [ self.addHost( 'h%s' % h ) for h in irange( 1, N ) ]
        switches = [ self.addSwitch( 's%s' % s ) for s in irange( 1, N ) ]

        # Wire up switches
        self.addLink( switches[1], switches[0], bw=5, delay='1ms', loss=0, use_htb=True )
        self.addLink( switches[1], switches[2], bw=4, delay='1ms', loss=0, use_htb=True )
        self.addLink( switches[1], switches[4], bw=2, delay='1ms', loss=0, use_htb=True )
        self.addLink( switches[3], switches[5], bw=5, delay='1ms', loss=0, use_htb=True )
        self.addLink( switches[3], switches[2], bw=10, delay='1ms', loss=0, use_htb=True )
        self.addLink( switches[3], switches[4], bw=10, delay='1ms', loss=0, use_htb=True )
      
        # Wire up hosts
        for host, switch in zip( hosts, switches ):
            self.addLink( host, switch )


def bandwidthTest():
   
    # Select TCP Reno
    #output = quietRun( 'sysctl -w net.ipv4.tcp_congestion_control=reno' )
    #assert 'reno' in output
    
    # create network
    print "*** creating network topology"
    topo = ExampleTestTopo()
    sw = OVSKernelSwitch
    c0 = RemoteController( 'c0', ip='127.0.0.1', port=6633 )

    net = Mininet( topo=topo, switch=sw, controller=c0, waitConnected=True,
                   link=TCLink, autoSetMacs=True, autoStaticArp=False )
    net.start()
   
    CLI(net)
    net.stop()




if __name__ == '__main__':
    lg.setLogLevel( 'info' )
    
    print "*** Run traffic demands in example topo"
    bandwidthTest()
