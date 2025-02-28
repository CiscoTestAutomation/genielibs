class ManagementOutput(object):
    ShowIpRouteDistributor0000Output = """
Routing entry for 0.0.0.0/0, supernet
  Known via "static", distance 1, metric 0, candidate default path
  Routing Descriptor Blocks:
  * 10.85.84.1
      Route metric is 0, traffic share count is 1"""

    ShowIpRouteDistributorIPOutput = """
Routing entry for 10.85.84.0/24
  Known via "connected", distance 0, metric 0 (connected, via interface)
  Routing Descriptor Blocks:
  * directly connected, via Ethernet0
      Route metric is 0, traffic share count is 1"""

    ShowIpInterfaceEthernet0Output = """
Ethernet0 is up, line protocol is up
  Internet address is 10.85.84.48/24
  Broadcast address is 255.255.255.255
  Address determined by non-volatile memory
  MTU is 1500 bytes
  Helper address is not set
  Directed broadcast forwarding is disabled
  Outgoing access list is not set
  Inbound  access list is not set
  Proxy ARP is enabled
  Security level is default
  Split horizon is enabled
  ICMP redirects are always sent
  ICMP unreachables are always sent
  ICMP mask replies are never sent
  IP fast switching is disabled
  IP fast switching on the same interface is disabled
  IP Flow switching is disabled
  IP Null turbo vector
  IP multicast fast switching is disabled
  IP multicast distributed fast switching is disabled
  IP route-cache flags are None
  Router Discovery is disabled
  IP output packet accounting is disabled
  IP access violation accounting is disabled
  TCP/IP header compression is disabled
  RTP/IP header compression is disabled
  Probe proxy name replies are disabled
  Policy routing is disabled
  Network address translation is disabled
  WCCP Redirect outbound is disabled
  WCCP Redirect exclude is disabled
  BGP Policy Mapping is disabled"""

    ManagementOpsOutput = {'management': {'ipv4_gateway': '10.85.84.1',
  'interface': 'Ethernet0',
  'ipv4_address': '10.85.84.48/24'}}