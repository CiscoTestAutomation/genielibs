class ManagementOutput(object):

    # Show Ipv4 Virtual Address Status output
    showIpv4VirtualAddressStatusOutput = '''
    VRF Name: default
    Virtual IP: 5.2.21.22/16
    Active Interface Name: MgmtEth0/RP0/CPU0/0
    Active Interface MAC Address: 88fc.5dc4.9d90
    
    VRF Node Create Timestamp   : .7337
    ARP Add Timestamp           : Sat Jul 01 2002241054 16:32:19.1471
    RIB Add Timestamp           : .7337
    SNMAC Add Timestamp         : N/A
    '''

    # Show Route Ipv4 output
    showRouteIpv4Output = '''
    Codes: C - connected, S - static, R - RIP, B - BGP, (>) - Diversion path
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
       i - ISIS, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, su - IS-IS summary null, * - candidate default
       U - per-user static route, o - ODR, L - local, G  - DAGR, l - LISP
       A - access/subscriber, a - Application route
       M - mobile route, r - RPL, t - Traffic Engineering, (!) - FRR Backup path
    Gateway of last resort is 5.4.0.1 to network 0.0.0.0
    
    S*   0.0.0.0/0 [1/0] via 5.4.0.1, 1w1d
    C    5.4.0.0/16 is directly connected, 1w1d, MgmtEth0/RP0/CPU0/0
                    is directly connected, 1w1d, MgmtEth0/RP1/CPU0/0
    L    5.4.23.20/32 is directly connected, 1w1d, MgmtEth0/RP0/CPU0/0
    L    5.4.23.22/32 [0/0] via 5.4.23.22, 1w1d, MgmtEth0/RP0/CPU0/0
    S    5.255.253.6/32 [1/0] via 5.4.0.1, 1w1d
    '''

    # Ops output
    ManagementOpsOutput = {
        'management': {
            'ipv4': {
                'virtual_address': '5.2.21.22/16'
            },
            'interface': 'MgmtEth0/RP0/CPU0/0',
            'vrf': 'default'
        },
        'routes': {
            'ipv4': {
                '5.255.253.6/32': {
                    'next_hop': '5.4.0.1',
                    'source_protocol': 'static'
                },
                '5.4.23.22/32': {
                    'next_hop': '5.4.23.22',
                    'source_protocol': 'local'
                },
                '0.0.0.0/0': {
                    'next_hop': '5.4.0.1',
                    'source_protocol': 'static'
                },
                '5.4.23.20/32': {
                    'source_protocol': 'local'
                },
                '5.4.0.0/16': {
                    'source_protocol': 'connected'
                }
            }
        }
    }