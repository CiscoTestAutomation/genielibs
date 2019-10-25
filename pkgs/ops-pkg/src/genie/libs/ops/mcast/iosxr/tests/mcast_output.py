''' 
Mcast Genie Ops Object Outputs for IOSXR.
'''


class McastOutput(object):

    ShowVrfAllDetail = {
        "default": {
            "description": "not set",
            "vrf_mode": "regular",
            "address_family": {
                 "ipv6 unicast": {
                      "route_target": {
                           "400:1": {
                                "rt_type": "import",
                                "route_target": "400:1"},
                           "300:1": {
                                "rt_type": "import",
                                "route_target": "300:1"},
                           "200:1": {
                                "rt_type": "both",
                                "route_target": "200:1"},
                           "200:2": {
                                "rt_type": "import",
                                "route_target": "200:2"}}},
                 "ipv4 unicast": {
                      "route_target": {
                           "400:1": {
                                "rt_type": "import",
                                "route_target": "400:1"},
                           "300:1": {
                                "rt_type": "import",
                                "route_target": "300:1"},
                           "200:1": {
                                "rt_type": "both",
                                "route_target": "200:1"},
                           "200:2": {
                                "rt_type": "import",
                                "route_target": "200:2"}}}},
            "route_distinguisher": "200:1",
            "interfaces": ["GigabitEthernet0/0/0/1"]},
        "VRF1": {
            "description": "not set",
            "vrf_mode": "regular",
            "address_family": {
                 "ipv6 unicast": {
                      "route_target": {
                           "400:1": {
                                "rt_type": "import",
                                "route_target": "400:1"},
                           "300:1": {
                                "rt_type": "import",
                                "route_target": "300:1"},
                           "200:1": {
                                "rt_type": "both",
                                "route_target": "200:1"},
                           "200:2": {
                                "rt_type": "import",
                                "route_target": "200:2"}}},
                 "ipv4 unicast": {
                      "route_target": {
                           "400:1": {
                                "rt_type": "import",
                                "route_target": "400:1"},
                           "300:1": {
                                "rt_type": "import",
                                "route_target": "300:1"},
                           "200:1": {
                                "rt_type": "both",
                                "route_target": "200:1"},
                           "200:2": {
                                "rt_type": "import",
                                "route_target": "200:2"}}}},
            "route_distinguisher": "200:1",
            "interfaces": ["GigabitEthernet0/0/0/1"]}}

    ############################################
    #           INFO - VRF: default 
    ############################################

    PimVrfDefaultIpv4Mstatic = '''\
        RP/0/0/CPU0:R2# show pim vrf default ipv4 mstatic
        Mon May 29 14:37:05.732 UTC
        IP Multicast Static Routes Information

        * 10.10.10.10/32 via GigabitEthernet0/0/0/0 with nexthop 192.168.1.0 and distance 10
        * 10.10.10.11/32 via GigabitEthernet0/0/0/1 with nexthop 192.168.1.1 and distance 11
        * 10.10.10.12/32 via GigabitEthernet0/0/0/2 with nexthop 192.168.1.2 and distance 12
        * 10.10.10.13/32 via GigabitEthernet0/0/0/3 with nexthop 192.168.1.3 and distance 13
        * 10.10.10.14/32 via GigabitEthernet0/0/0/4 with nexthop 192.168.1.4 and distance 14
        * 10.10.10.15/32 via GigabitEthernet0/0/0/5 with nexthop 192.168.1.5 and distance 15
        * 10.10.10.16/32 via GigabitEthernet0/0/0/6 with nexthop 192.168.1.6 and distance 16
        * 10.10.10.17/32 via GigabitEthernet0/0/0/7 with nexthop 192.168.1.7 and distance 17
        '''

    PimVrfDefaultIpv6Mstatic = '''\
        RP/0/0/CPU0:R2# show pim vrf default ipv6 mstatic
        Mon May 29 14:37:26.421 UTC
        IP Multicast Static Routes Information

         * 2001:10:10::10/128 via GigabitEthernet0/0/0/0 with nexthop 2001:11:11::10 and distance 10 
         * 2001:10:10::11/128 via GigabitEthernet0/0/0/1 with nexthop 2001:11:11::11 and distance 11 
         * 2001:10:10::12/128 via GigabitEthernet0/0/0/2 with nexthop 2001:11:11::12 and distance 12
         * 2001:10:10::13/128 via GigabitEthernet0/0/0/3 with nexthop 2001:11:11::13 and distance 13
         * 2001:10:10::14/128 via GigabitEthernet0/0/0/4 with nexthop 2001:11:11::14 and distance 14
         * 2001:10:10::15/128 via GigabitEthernet0/0/0/5 with nexthop 2001:11:11::15 and distance 15
        '''

    PimVrfDefaultIpv4InterfaceDetail = '''\
        RP/0/0/CPU0:R2#show pim vrf default ipv4 interface detail
        Mon May 29 14:41:28.444 UTC

        PIM interfaces in VRF default
        IP PIM Multicast Interface State
        Flag: B - Bidir enabled, NB - Bidir disabled
              P - PIM Proxy enabled, NP - PIM Proxy disabled
              V - Virtual Interface
        BFD State - State/Interval/Multiplier

        Interface                  PIM  Nbr   Hello  DR
                                        Count Intvl  Prior

        Loopback0                   on   1     30     1     
            Primary Address : 10.16.2.2
                      Flags : B P V
                        BFD : Off/150 ms/3
                         DR : this system
          Propagation delay : 500
          Override Interval : 2500
                Hello Timer : 00:00:15
            Neighbor Filter : -

        GigabitEthernet0/0/0/0      on   1     30     1     
            Primary Address : 10.2.3.2
                      Flags : B P 
                        BFD : Off/150 ms/3
                         DR : this system
          Propagation delay : 500
          Override Interval : 2500
                Hello Timer : 00:00:01
            Neighbor Filter : -

        GigabitEthernet0/0/0/1      on   2     30     1     
            Primary Address : 10.1.2.2
                      Flags : NB P 
                        BFD : Off/150 ms/3
                         DR : this system
          Propagation delay : 500
          Override Interval : 2500
                Hello Timer : 00:00:07
            Neighbor Filter : -
        '''

    PimVrfDefaultIpv6InterfaceDetail = '''\
        RP/0/0/CPU0:R2#show pim vrf default ipv6 interface detail
        Mon May 29 14:41:52.972 UTC

        PIM interfaces in VRF default
        IP PIM Multicast Interface State
        Flag: B - Bidir enabled, NB - Bidir disabled
              P - PIM Proxy enabled, NP - PIM Proxy disabled
              A - PIM Assert batching capable, NA - PIM Assert batching incapable
              V - Virtual Interface

        Interface                  PIM  Nbr   Hello  DR
                                        Count Intvl  Prior

        Loopback0                   on   1     30     1     
            Primary Address : fe80::85c6:bdff:fe62:61e
                    Address : 2001:db8:2:2::2
                      Flags : B P NA V
                        BFD : Off/150 ms/3
                         DR : this system

          Propagation delay : 500
          Override Interval : 2500
                Hello Timer : 00:00:19
            Neighbor Filter : -

        GigabitEthernet0/0/0/0      on   1     30     1     
            Primary Address : fe80::5054:ff:fee4:f669
                    Address : 2001:db8:2:3::2
                      Flags : B P NA 
                        BFD : Off/150 ms/3
                         DR : this system

          Propagation delay : 500
          Override Interval : 2500
                Hello Timer : 00:00:22
            Neighbor Filter : -

        GigabitEthernet0/0/0/1      on   1     30     1     
            Primary Address : fe80::5054:ff:feac:64b3
                    Address : 2001:db8:1:2::2
                      Flags : B P NA 
                        BFD : Off/150 ms/3
                         DR : this system

          Propagation delay : 500
          Override Interval : 2500
                Hello Timer : 00:00:02
            Neighbor Filter : -
        '''

    PimVrfDefaultIpv4RpfSummary = '''\
        RP/0/0/CPU0:R2#show pim vrf default ipv4 rpf summary 
        Mon May 29 14:42:47.569 UTC
            ISIS Mcast Topology Not configured
            MoFRR Flow-based    Not configured
            MoFRR RIB           Not configured
            RUMP MuRIB          Not enabled

        PIM RPFs registered with Unicast RIB table

        Default RPF Table: IPv4-Unicast-default
        RIB Convergence Timeout Value: 00:30:00
        RIB Convergence Time Left:     00:00:00
        Multipath RPF Selection is Enabled

        Table: IPv4-Unicast-default
            PIM RPF Registrations = 1
            RIB Table converged
        '''

    PimVrfDefaultIpv6RpfSummary = '''\
        RP/0/0/CPU0:R2#show pim vrf default ipv6 rpf summary 
        Mon May 29 14:42:53.538 UTC
            ISIS Mcast Topology Not configured
            MoFRR Flow-based    Not configured
            MoFRR RIB           Not configured
            RUMP MuRIB          Not enabled

        PIM RPFs registered with Unicast RIB table

        Default RPF Table: IPv6-Unicast-default
        RIB Convergence Timeout Value: 00:30:00
        RIB Convergence Time Left:     00:00:00
        Multipath RPF Selection is Enabled

        Table: IPv6-Unicast-default
            PIM RPF Registrations = 0
            RIB Table converged
        '''

    ############################################
    #           INFO - VRF: VRF1
    ############################################

    PimVrfVRF1Ipv4Mstatic = '''\
        RP/0/0/CPU0:R2# show pim vrf VRF1 ipv4 mstatic
        Mon May 29 14:37:05.732 UTC
        IP Multicast Static Routes Information

        * 10.135.10.10/32 via GigabitEthernet1/0/0/0 with nexthop 192.168.1.0 and distance 10
        * 10.135.10.11/32 via GigabitEthernet1/0/0/1 with nexthop 192.168.1.1 and distance 11
        * 10.135.10.12/32 via GigabitEthernet1/0/0/2 with nexthop 192.168.1.2 and distance 12
        * 10.135.10.13/32 via GigabitEthernet1/0/0/3 with nexthop 192.168.1.3 and distance 13
        * 10.135.10.14/32 via GigabitEthernet1/0/0/4 with nexthop 192.168.1.4 and distance 14
        * 10.135.10.15/32 via GigabitEthernet1/0/0/5 with nexthop 192.168.1.5 and distance 15
        * 10.135.10.16/32 via GigabitEthernet1/0/0/6 with nexthop 192.168.1.6 and distance 16
        * 10.135.10.17/32 via GigabitEthernet1/0/0/7 with nexthop 192.168.1.7 and distance 17
        '''

    PimVrfVRF1Ipv6Mstatic = '''\
        RP/0/0/CPU0:R2# show pim vrf VRF1 ipv6 mstatic
        Mon May 29 14:37:26.421 UTC
        IP Multicast Static Routes Information

         * 2001:db8:6a27:100::10/128 via GigabitEthernet1/0/0/0 with nexthop 2001:11:11::10 and distance 10 
         * 2001:db8:6a27:100::11/128 via GigabitEthernet1/0/0/1 with nexthop 2001:11:11::11 and distance 11 
         * 2001:db8:6a27:100::12/128 via GigabitEthernet1/0/0/2 with nexthop 2001:11:11::12 and distance 12
         * 2001:db8:6a27:100::13/128 via GigabitEthernet1/0/0/3 with nexthop 2001:11:11::13 and distance 13
         * 2001:db8:6a27:100::14/128 via GigabitEthernet1/0/0/4 with nexthop 2001:11:11::14 and distance 14
         * 2001:db8:6a27:100::15/128 via GigabitEthernet1/0/0/5 with nexthop 2001:11:11::15 and distance 15
        '''

    PimVrfVRF1Ipv4InterfaceDetail = '''\
        RP/0/0/CPU0:R2#show pim vrf VRF1 ipv4 interface detail
        Mon May 29 14:41:28.444 UTC

        PIM interfaces in VRF VRF1
        IP PIM Multicast Interface State
        Flag: B - Bidir enabled, NB - Bidir disabled
              P - PIM Proxy enabled, NP - PIM Proxy disabled
              V - Virtual Interface
        BFD State - State/Interval/Multiplier

        Interface                  PIM  Nbr   Hello  DR
                                        Count Intvl  Prior

        Loopback0                   on   1     30     1     
            Primary Address : 10.16.2.2
                      Flags : B P V
                        BFD : Off/150 ms/3
                         DR : this system
          Propagation delay : 500
          Override Interval : 2500
                Hello Timer : 00:00:15
            Neighbor Filter : -

        GigabitEthernet0/0/0/0      on   1     30     1     
            Primary Address : 10.2.3.2
                      Flags : B P 
                        BFD : Off/150 ms/3
                         DR : this system
          Propagation delay : 500
          Override Interval : 2500
                Hello Timer : 00:00:01
            Neighbor Filter : -

        GigabitEthernet0/0/0/1      on   2     30     1     
            Primary Address : 10.1.2.2
                      Flags : NB P 
                        BFD : Off/150 ms/3
                         DR : this system
          Propagation delay : 500
          Override Interval : 2500
                Hello Timer : 00:00:07
            Neighbor Filter : -
        '''

    PimVrfVRF1Ipv6InterfaceDetail = '''\
        RP/0/0/CPU0:R2#show pim vrf VRF1 ipv6 interface detail
        Mon May 29 14:41:52.972 UTC

        PIM interfaces in VRF VRF1
        IP PIM Multicast Interface State
        Flag: B - Bidir enabled, NB - Bidir disabled
              P - PIM Proxy enabled, NP - PIM Proxy disabled
              A - PIM Assert batching capable, NA - PIM Assert batching incapable
              V - Virtual Interface

        Interface                  PIM  Nbr   Hello  DR
                                        Count Intvl  Prior

        Loopback0                   on   1     30     1     
            Primary Address : fe80::85c6:bdff:fe62:61e
                    Address : 2001:db8:2:2::2
                      Flags : B P NA V
                        BFD : Off/150 ms/3
                         DR : this system

          Propagation delay : 500
          Override Interval : 2500
                Hello Timer : 00:00:19
            Neighbor Filter : -

        GigabitEthernet0/0/0/0      on   1     30     1     
            Primary Address : fe80::5054:ff:fee4:f669
                    Address : 2001:db8:2:3::2
                      Flags : B P NA 
                        BFD : Off/150 ms/3
                         DR : this system

          Propagation delay : 500
          Override Interval : 2500
                Hello Timer : 00:00:22
            Neighbor Filter : -

        GigabitEthernet0/0/0/1      on   1     30     1     
            Primary Address : fe80::5054:ff:feac:64b3
                    Address : 2001:db8:1:2::2
                      Flags : B P NA 
                        BFD : Off/150 ms/3
                         DR : this system

          Propagation delay : 500
          Override Interval : 2500
                Hello Timer : 00:00:02
            Neighbor Filter : -
        '''

    PimVrfVRF1Ipv4RpfSummary = '''\
        RP/0/0/CPU0:R2#show pim VRF1 default ipv4 rpf summary 
        Mon May 29 14:42:47.569 UTC
            ISIS Mcast Topology Not configured
            MoFRR Flow-based    Not configured
            MoFRR RIB           Not configured
            RUMP MuRIB          Not enabled

        PIM RPFs registered with Unicast RIB table

        Default RPF Table: IPv4-Unicast-default
        RIB Convergence Timeout Value: 00:30:00
        RIB Convergence Time Left:     00:00:00
        Multipath RPF Selection is Enabled

        Table: IPv4-Unicast-default
            PIM RPF Registrations = 1
            RIB Table converged
        '''

    PimVrfVRF1Ipv6RpfSummary = '''\
        RP/0/0/CPU0:R2#show pim vrf VRF1 ipv6 rpf summary 
        Mon May 29 14:42:53.538 UTC
            ISIS Mcast Topology Not configured
            MoFRR Flow-based    Not configured
            MoFRR RIB           Not configured
            RUMP MuRIB          Not enabled

        PIM RPFs registered with Unicast RIB table

        Default RPF Table: IPv6-Unicast-default
        RIB Convergence Timeout Value: 00:30:00
        RIB Convergence Time Left:     00:00:00
        Multipath RPF Selection is Enabled

        Table: IPv6-Unicast-default
            PIM RPF Registrations = 0
            RIB Table converged
        '''

    ############################################
    #          TABLE - VRF: default 
    ############################################

    MribVrfDefaultIpv4Route = '''\
        RP/0/1/CPU0:rtr1#show mrib vrf default ipv4 route
        Mon Nov  2 15:26:01.015 PST

        IP Multicast Routing Information Base
        Entry flags: L - Domain-Local Source, E - External Source to the Domain,
        C - Directly-Connected Check, S - Signal, IA - Inherit Accept,
        IF - Inherit From, D - Drop, ME - MDT Encap, EID - Encap ID,
        MD - MDT Decap, MT - MDT Threshold Crossed, MH - MDT interface handle
        CD - Conditional Decap, MPLS - MPLS Decap, EX - Extranet
        MoFE - MoFRR Enabled, MoFS - MoFRR State, MoFP - MoFRR Primary
        MoFB - MoFRR Backup, RPFID - RPF ID Set, X - VXLAN
        Interface flags: F - Forward, A - Accept, IC - Internal Copy,
        NS - Negate Signal, DP - Don't Preserve, SP - Signal Present,
        II - Internal Interest, ID - Internal Disinterest, LI - Local Interest,
        LD - Local Disinterest, DI - Decapsulation Interface
        EI - Encapsulation Interface, MI - MDT Interface, LVIF - MPLS Encap,
        EX - Extranet, A2 - Secondary Accept, MT - MDT Threshold Crossed,
        MA - Data MDT Assigned, LMI - mLDP MDT Interface, TMI - P2MP-TE MDT Interface
        IRMI - IR MDT Interface

        (*,224.0.0.0/4) RPF nbr: 0.0.0.0 Flags: C RPF P
            Up: 00:00:58

        (*,224.0.0.0/24) Flags: D P
            Up: 00:00:58

        (*,224.0.1.39) Flags: S P
            Up: 00:00:58

        (*,227.1.1.1) RPF nbr: 0.0.0.0 Flags: C RPF MD MH CD
            MVPN TID: 0xe000001f
            MVPN Remote TID: 0x0
            MVPN Payload: IPv4
            MDT IFH: 0x803380
            Up: 00:00:54
            Outgoing Interface List
                Loopback0 Flags: F NS, Up: 00:00:54

        (192.168.0.12,227.1.1.1) RPF nbr: 192.168.0.12 Flags: RPF ME MH
            MVPN TID: 0xe000001f
            MVPN Remote TID: 0x0
            MVPN Payload: IPv4
            MDT IFH: 0x803380
            Up: 00:00:54
            Incoming Interface List
                Loopback0 Flags: F NS, Up: 00:00:58
            Outgoing Interface List
                Loopback0 Flags: F A, Up: 00:00:54

        (*,232.0.0.0/8) Flags: D P
            Up: 00:00:58

        (*,236.5.5.5) RPF nbr: 0.0.0.0 Flags: C RPF MD MH CD
            MVPN TID: 0xe0000018
            MVPN Remote TID: 0xe0800018
            MVPN Payload: IPv4 IPv6
            MDT IFH: 0x803480
            Up: 00:00:54
            Outgoing Interface List
                Loopback0 Flags: F NS, Up: 00:00:54

        (192.168.0.12,236.5.5.5) RPF nbr: 192.168.0.12 Flags: RPF ME MH
            MVPN TID: 0xe0000018
            MVPN Remote TID: 0xe0800018
            MVPN Payload: IPv4 IPv6
            MDT IFH: 0x803480
            Up: 00:00:54
            Incoming Interface List
                Loopback0 Flags: F A, Up: 00:00:54
            Outgoing Interface List
                Loopback0 Flags: F A, Up: 00:00:54

        (192.168.0.22,236.5.5.5) RPF nbr: 10.121.1.22 Flags: C RPF MD MH CD
            MVPN TID: 0xe0000018
            MVPN Remote TID: 0xe0800018
            MVPN Payload: IPv4 IPv6
            MDT IFH: 0x803480
            Up: 00:00:13
            Outgoing Interface List
                Loopback0 Flags: F NS, Up: 00:00:13
                GigabitEthernet0/1/0/1 Flags: NS, Up: 00:00:01
        '''

    MribVrfDefaultIpv6Route = '''\
        RP/0/1/CPU0:rtr1#show mrib vrf default ipv6 route  
        Mon Nov  2 15:26:01.015 PST

        IP Multicast Routing Information Base
        Entry flags: L - Domain-Local Source, E - External Source to the Domain,
            C - Directly-Connected Check, S - Signal, IA - Inherit Accept,
            IF - Inherit From, D - Drop, ME - MDT Encap, EID - Encap ID,
            MD - MDT Decap, MT - MDT Threshold Crossed, MH - MDT interface handle
            CD - Conditional Decap, MPLS - MPLS Decap, EX - Extranet
            MoFE - MoFRR Enabled, MoFS - MoFRR State, MoFP - MoFRR Primary
            MoFB - MoFRR Backup, RPFID - RPF ID Set, X - VXLAN
        Interface flags: F - Forward, A - Accept, IC - Internal Copy,
            NS - Negate Signal, DP - Don't Preserve, SP - Signal Present,
            II - Internal Interest, ID - Internal Disinterest, LI - Local Interest,
            LD - Local Disinterest, DI - Decapsulation Interface
            EI - Encapsulation Interface, MI - MDT Interface, LVIF - MPLS Encap,
            EX - Extranet, A2 - Secondary Accept, MT - MDT Threshold Crossed,
            MA - Data MDT Assigned, LMI - mLDP MDT Interface, TMI - P2MP-TE MDT Interface
            IRMI - IR MDT Interface

        (*,ff00::/8)
          RPF nbr: 2001:db8:b901:0:150:150:150:150 Flags: L C RPF P
          Up: 00:04:45
          Outgoing Interface List
            Decaps6tunnel0 Flags: NS DI, Up: 00:04:40

        (*,ff00::/15)
          Flags: D P
          Up: 00:04:45

        (*,ff02::/16)
          Flags: D P
          Up: 00:04:45

        (*,ff10::/15)
          Flags: D P
          Up: 00:04:45

        (*,ff12::/16)
          Flags: D P
          Up: 00:04:45

        (2001:db8:1:0:1:1:1:2,ff15::1:1)
          RPF nbr: 2001:db8:1:0:1:1:1:2 Flags: L RPF MT
          MT Slot: 0/2/CPU0
          Up: 00:02:53
          Incoming Interface List
            GigabitEthernet150/0/0/6 Flags: A, Up: 00:02:53
          Outgoing Interface List
            mdtvpn1 Flags: F NS MI MT MA, Up: 00:02:53

        (2001:db8:10:0:4:4:4:5,ff15::2:1)
          RPF nbr: ::ffff:192.168.195.200 Flags: L RPF
          Up: 00:03:59
          Incoming Interface List
            mdtvpn1 Flags: A MI, Up: 00:03:35
          Outgoing Interface List
            GigabitEthernet150/0/0/6 Flags: F NS, Up: 00:03:59

        (*,ff20::/15)
          Flags: D P
          Up: 00:04:45

        (*,ff22::/16)
          Flags: D P
          Up: 00:04:45
        '''

    ############################################
    #          TABLE - VRF: VRF1
    ############################################

    MribVrfVRF1Ipv4Route = '''\
        RP/0/1/CPU0:rtr1#show mrib vrf VRF1 ipv4 route
        Mon Nov  2 15:26:01.015 PST

        IP Multicast Routing Information Base
        Entry flags: L - Domain-Local Source, E - External Source to the Domain,
        C - Directly-Connected Check, S - Signal, IA - Inherit Accept,
        IF - Inherit From, D - Drop, ME - MDT Encap, EID - Encap ID,
        MD - MDT Decap, MT - MDT Threshold Crossed, MH - MDT interface handle
        CD - Conditional Decap, MPLS - MPLS Decap, EX - Extranet
        MoFE - MoFRR Enabled, MoFS - MoFRR State, MoFP - MoFRR Primary
        MoFB - MoFRR Backup, RPFID - RPF ID Set, X - VXLAN
        Interface flags: F - Forward, A - Accept, IC - Internal Copy,
        NS - Negate Signal, DP - Don't Preserve, SP - Signal Present,
        II - Internal Interest, ID - Internal Disinterest, LI - Local Interest,
        LD - Local Disinterest, DI - Decapsulation Interface
        EI - Encapsulation Interface, MI - MDT Interface, LVIF - MPLS Encap,
        EX - Extranet, A2 - Secondary Accept, MT - MDT Threshold Crossed,
        MA - Data MDT Assigned, LMI - mLDP MDT Interface, TMI - P2MP-TE MDT Interface
        IRMI - IR MDT Interface

        (*,234.0.0.0/4) RPF nbr: 0.0.0.1 Flags: MD RPF P
            Up: 00:01:28

        (*,10.76.0.0/32) Flags: P D
            Up: 00:01:38

        (*,10.76.1.40) Flags: S P
            Up: 00:00:46

        (172.16.154.15,192.168.21.1) RPF nbr: 192.168.0.12 Flags: RPF ME MH
            MVPN TID: 0xe000001f
            MVPN Remote TID: 0x0
            MVPN Payload: IPv4
            MDT IFH: 0x803380
            Up: 00:00:54
            Incoming Interface List
                GigabitEthernet0/0/0/1 Flags: F NS, Up: 00:01:38
            Outgoing Interface List
                GigabitEthernet0/0/0/2 Flags: F A, Up: 00:01:24
        '''

    MribVrfVRF1Ipv6Route = '''\
        RP/0/1/CPU0:rtr1#show mrib vrf VRF1 ipv6 route  
        Mon Nov  2 15:26:01.015 PST

        IP Multicast Routing Information Base
        Entry flags: L - Domain-Local Source, E - External Source to the Domain,
            C - Directly-Connected Check, S - Signal, IA - Inherit Accept,
            IF - Inherit From, D - Drop, ME - MDT Encap, EID - Encap ID,
            MD - MDT Decap, MT - MDT Threshold Crossed, MH - MDT interface handle
            CD - Conditional Decap, MPLS - MPLS Decap, EX - Extranet
            MoFE - MoFRR Enabled, MoFS - MoFRR State, MoFP - MoFRR Primary
            MoFB - MoFRR Backup, RPFID - RPF ID Set, X - VXLAN
        Interface flags: F - Forward, A - Accept, IC - Internal Copy,
            NS - Negate Signal, DP - Don't Preserve, SP - Signal Present,
            II - Internal Interest, ID - Internal Disinterest, LI - Local Interest,
            LD - Local Disinterest, DI - Decapsulation Interface
            EI - Encapsulation Interface, MI - MDT Interface, LVIF - MPLS Encap,
            EX - Extranet, A2 - Secondary Accept, MT - MDT Threshold Crossed,
            MA - Data MDT Assigned, LMI - mLDP MDT Interface, TMI - P2MP-TE MDT Interface
            IRMI - IR MDT Interface

        (*,ff70::/12)
          RPF nbr: :: Flags: C RPF P
          Up: 00:04:45

        (*,ff70::/15)
          Flags: D P
          Up: 00:04:45

        (*,ff72::/16)
          Flags: D P
          Up: 00:04:45

        (*,ff80::/15)
          Flags: D P
          Up: 00:04:45

        (*,ff82::/16)
          Flags: D P
          Up: 00:04:45

        (*,ff90::/15)
          Flags: D P
          Up: 00:04:45
        '''

    McastInfo = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'enable': True,
                        'mroute': 
                            {'10.135.10.10/32': 
                                {'path': 
                                    {'192.168.1.0 GigabitEthernet1/0/0/0 10': 
                                        {'admin_distance': 10,
                                        'interface_name': 'GigabitEthernet1/0/0/0',
                                        'neighbor_address': '192.168.1.0'}}},
                            '10.135.10.11/32': 
                                {'path': 
                                    {'192.168.1.1 GigabitEthernet1/0/0/1 11': 
                                        {'admin_distance': 11,
                                        'interface_name': 'GigabitEthernet1/0/0/1',
                                        'neighbor_address': '192.168.1.1'}}},
                            '10.135.10.12/32': 
                                {'path': 
                                    {'192.168.1.2 GigabitEthernet1/0/0/2 12': 
                                        {'admin_distance': 12,
                                        'interface_name': 'GigabitEthernet1/0/0/2',
                                        'neighbor_address': '192.168.1.2'}}},
                            '10.135.10.13/32': 
                                {'path': 
                                    {'192.168.1.3 GigabitEthernet1/0/0/3 13': 
                                        {'admin_distance': 13,
                                        'interface_name': 'GigabitEthernet1/0/0/3',
                                        'neighbor_address': '192.168.1.3'}}},
                            '10.135.10.14/32': 
                                {'path': 
                                    {'192.168.1.4 GigabitEthernet1/0/0/4 14': 
                                        {'admin_distance': 14,
                                        'interface_name': 'GigabitEthernet1/0/0/4',
                                        'neighbor_address': '192.168.1.4'}}},
                            '10.135.10.15/32': 
                                {'path': 
                                    {'192.168.1.5 GigabitEthernet1/0/0/5 15': 
                                        {'admin_distance': 15,
                                        'interface_name': 'GigabitEthernet1/0/0/5',
                                        'neighbor_address': '192.168.1.5'}}},
                            '10.135.10.16/32': 
                                {'path': 
                                    {'192.168.1.6 GigabitEthernet1/0/0/6 16': 
                                        {'admin_distance': 16,
                                        'interface_name': 'GigabitEthernet1/0/0/6',
                                        'neighbor_address': '192.168.1.6'}}},
                            '10.135.10.17/32': 
                                {'path': 
                                    {'192.168.1.7 GigabitEthernet1/0/0/7 17': 
                                        {'admin_distance': 17,
                                        'interface_name': 'GigabitEthernet1/0/0/7',
                                        'neighbor_address': '192.168.1.7'}}}},
                        'multipath': True},
                    'ipv6': 
                        {'enable': True,
                        'mroute': 
                            {'2001:db8:6a27:100::10/128': 
                                {'path': 
                                    {'2001:11:11::10 GigabitEthernet1/0/0/0 10': 
                                        {'admin_distance': 10,
                                        'interface_name': 'GigabitEthernet1/0/0/0',
                                        'neighbor_address': '2001:11:11::10'}}},
                                    '2001:db8:6a27:100::11/128': 
                                        {'path': 
                                            {'2001:11:11::11 GigabitEthernet1/0/0/1 11': 
                                                {'admin_distance': 11,
                                                'interface_name': 'GigabitEthernet1/0/0/1',
                                                'neighbor_address': '2001:11:11::11'}}},
                                    '2001:db8:6a27:100::12/128': 
                                        {'path': 
                                            {'2001:11:11::12 GigabitEthernet1/0/0/2 12': 
                                                {'admin_distance': 12,
                                                'interface_name': 'GigabitEthernet1/0/0/2',
                                                'neighbor_address': '2001:11:11::12'}}},
                                    '2001:db8:6a27:100::13/128': 
                                        {'path': 
                                            {'2001:11:11::13 GigabitEthernet1/0/0/3 13': 
                                                {'admin_distance': 13,
                                                'interface_name': 'GigabitEthernet1/0/0/3',
                                                'neighbor_address': '2001:11:11::13'}}},
                                    '2001:db8:6a27:100::14/128': 
                                        {'path': 
                                            {'2001:11:11::14 GigabitEthernet1/0/0/4 14': 
                                                {'admin_distance': 14,
                                                'interface_name': 'GigabitEthernet1/0/0/4',
                                                'neighbor_address': '2001:11:11::14'}}},
                                    '2001:db8:6a27:100::15/128': 
                                        {'path': 
                                            {'2001:11:11::15 GigabitEthernet1/0/0/5 15': 
                                                {'admin_distance': 15,
                                                'interface_name': 'GigabitEthernet1/0/0/5',
                                                'neighbor_address': '2001:11:11::15'}}}},
                        'multipath': True}}},
            'default': 
                {'address_family': 
                    {'ipv4': 
                        {'enable': True,
                        'mroute': 
                            {'10.10.10.10/32': 
                                {'path': 
                                    {'192.168.1.0 GigabitEthernet0/0/0/0 10': 
                                        {'admin_distance': 10,
                                        'interface_name': 'GigabitEthernet0/0/0/0',
                                        'neighbor_address': '192.168.1.0'}}},
                            '10.10.10.11/32': 
                                {'path': 
                                    {'192.168.1.1 GigabitEthernet0/0/0/1 11': 
                                        {'admin_distance': 11,
                                        'interface_name': 'GigabitEthernet0/0/0/1',
                                        'neighbor_address': '192.168.1.1'}}},
                            '10.10.10.12/32': 
                                {'path': 
                                    {'192.168.1.2 GigabitEthernet0/0/0/2 12': 
                                        {'admin_distance': 12,
                                        'interface_name': 'GigabitEthernet0/0/0/2',
                                        'neighbor_address': '192.168.1.2'}}},
                            '10.10.10.13/32': 
                                {'path': 
                                    {'192.168.1.3 GigabitEthernet0/0/0/3 13': 
                                        {'admin_distance': 13,
                                        'interface_name': 'GigabitEthernet0/0/0/3',
                                        'neighbor_address': '192.168.1.3'}}},
                            '10.10.10.14/32': 
                                {'path': 
                                    {'192.168.1.4 GigabitEthernet0/0/0/4 14': 
                                        {'admin_distance': 14,
                                        'interface_name': 'GigabitEthernet0/0/0/4',
                                        'neighbor_address': '192.168.1.4'}}},
                            '10.10.10.15/32': 
                                {'path': 
                                    {'192.168.1.5 GigabitEthernet0/0/0/5 15': 
                                        {'admin_distance': 15,
                                        'interface_name': 'GigabitEthernet0/0/0/5',
                                        'neighbor_address': '192.168.1.5'}}},
                            '10.10.10.16/32': 
                                {'path': 
                                    {'192.168.1.6 GigabitEthernet0/0/0/6 16': 
                                        {'admin_distance': 16,
                                        'interface_name': 'GigabitEthernet0/0/0/6',
                                        'neighbor_address': '192.168.1.6'}}},
                            '10.10.10.17/32': 
                                {'path': 
                                    {'192.168.1.7 GigabitEthernet0/0/0/7 17': 
                                        {'admin_distance': 17,
                                        'interface_name': 'GigabitEthernet0/0/0/7',
                                        'neighbor_address': '192.168.1.7'}}}},
                        'multipath': True},
                    'ipv6': 
                        {'enable': True,
                        'mroute': 
                            {'2001:10:10::10/128': 
                                {'path': 
                                    {'2001:11:11::10 GigabitEthernet0/0/0/0 10': 
                                        {'admin_distance': 10,
                                        'interface_name': 'GigabitEthernet0/0/0/0',
                                        'neighbor_address': '2001:11:11::10'}}},
                                    '2001:10:10::11/128': 
                                        {'path': 
                                            {'2001:11:11::11 GigabitEthernet0/0/0/1 11': 
                                                {'admin_distance': 11,
                                                'interface_name': 'GigabitEthernet0/0/0/1',
                                                'neighbor_address': '2001:11:11::11'}}},
                                    '2001:10:10::12/128': 
                                        {'path': 
                                            {'2001:11:11::12 GigabitEthernet0/0/0/2 12': 
                                                {'admin_distance': 12,
                                                'interface_name': 'GigabitEthernet0/0/0/2',
                                                'neighbor_address': '2001:11:11::12'}}},
                                    '2001:10:10::13/128': 
                                        {'path': 
                                            {'2001:11:11::13 GigabitEthernet0/0/0/3 13': 
                                                {'admin_distance': 13,
                                                'interface_name': 'GigabitEthernet0/0/0/3',
                                                'neighbor_address': '2001:11:11::13'}}},
                                    '2001:10:10::14/128': 
                                        {'path': 
                                            {'2001:11:11::14 GigabitEthernet0/0/0/4 14': 
                                                {'admin_distance': 14,
                                                'interface_name': 'GigabitEthernet0/0/0/4',
                                                'neighbor_address': '2001:11:11::14'}}},
                                    '2001:10:10::15/128': 
                                        {'path': 
                                            {'2001:11:11::15 GigabitEthernet0/0/0/5 15': 
                                                {'admin_distance': 15,
                                                'interface_name': 'GigabitEthernet0/0/0/5',
                                                'neighbor_address': '2001:11:11::15'}}}},
                        'multipath': True}}}}}

    McastTable = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'multicast_group': 
                            {'10.76.0.0/32': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'P D',
                                        'uptime': '00:01:38'}}},
                            '10.76.1.40': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'S P',
                                        'uptime': '00:00:46'}}},
                            '192.168.21.1': 
                                {'source_address': 
                                    {'172.16.154.15': 
                                        {'flags': 'RPF ME MH',
                                        'incoming_interface_list': 
                                            {'GigabitEthernet0/0/0/1': 
                                                {'rpf_nbr': '192.168.0.12'}},
                                        'outgoing_interface_list': 
                                            {'GigabitEthernet0/0/0/2': 
                                                {'flags': 'F A',
                                                'uptime': '00:01:24'}},
                                        'uptime': '00:00:54'}}},
                            '234.0.0.0/4': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'MD RPF P',
                                        'uptime': '00:01:28'}}}}},
                    'ipv6': 
                        {'multicast_group': 
                            {'ff70::/12': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'C RPF P',
                                        'uptime': '00:04:45'}}},
                            'ff70::/15': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'D P',
                                        'uptime': '00:04:45'}}},
                            'ff72::/16': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'D P',
                                        'uptime': '00:04:45'}}},
                            'ff80::/15': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'D P',
                                        'uptime': '00:04:45'}}},
                            'ff82::/16': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'D P',
                                        'uptime': '00:04:45'}}},
                            'ff90::/15': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'D P',
                                        'uptime': '00:04:45'}}}}}}},
            'default': 
                {'address_family': 
                    {'ipv4': 
                        {'multicast_group': 
                            {'224.0.0.0/24': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'D P',
                                        'uptime': '00:00:58'}}},
                                    '224.0.0.0/4': 
                                        {'source_address': 
                                            {'*': 
                                                {'flags': 'C RPF P',
                                                'uptime': '00:00:58'}}},
                                    '224.0.1.39': 
                                        {'source_address': 
                                            {'*': 
                                                {'flags': 'S P',
                                                'uptime': '00:00:58'}}},
                                    '227.1.1.1': 
                                        {'source_address': 
                                            {'*': 
                                                {'flags': 'C RPF MD MH CD',
                                                'outgoing_interface_list': 
                                                    {'Loopback0': 
                                                        {'flags': 'F NS',
                                                        'uptime': '00:00:54'}},
                                                'uptime': '00:00:54'},
                                            '192.168.0.12': 
                                                {'flags': 'RPF ME MH',
                                                'incoming_interface_list': 
                                                    {'Loopback0': 
                                                        {'rpf_nbr': '192.168.0.12'}},
                                                'outgoing_interface_list': 
                                                    {'Loopback0': 
                                                        {'flags': 'F A',
                                                        'uptime': '00:00:54'}},
                                                'uptime': '00:00:54'}}},
                                    '232.0.0.0/8': 
                                        {'source_address': 
                                            {'*': 
                                                {'flags': 'D P',
                                                'uptime': '00:00:58'}}},
                                    '236.5.5.5': 
                                        {'source_address': 
                                            {'*': 
                                                {'flags': 'C RPF MD MH CD',
                                                'outgoing_interface_list': 
                                                    {'Loopback0': 
                                                        {'flags': 'F NS',
                                                        'uptime': '00:00:54'}},
                                                'uptime': '00:00:54'},
                                            '192.168.0.12': 
                                                {'flags': 'RPF ME MH',
                                                'incoming_interface_list': 
                                                    {'Loopback0': 
                                                        {'rpf_nbr': '192.168.0.12'}},
                                                'outgoing_interface_list': 
                                                    {'Loopback0': 
                                                        {'flags': 'F A',
                                                        'uptime': '00:00:54'}},
                                                'uptime': '00:00:54'},
                                            '192.168.0.22': 
                                                {'flags': 'C RPF MD MH CD',
                                                'outgoing_interface_list': 
                                                    {'GigabitEthernet0/1/0/1': 
                                                        {'flags': 'NS',
                                                        'uptime': '00:00:01'},
                                                    'Loopback0': {'flags': 'F NS',
                                                    'uptime': '00:00:13'}},
                                                'uptime': '00:00:13'}}}}},
                    'ipv6': 
                        {'multicast_group': 
                            {'ff00::/15': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'D P',
                                        'uptime': '00:04:45'}}},
                            'ff00::/8': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'L C RPF P',
                                        'outgoing_interface_list': 
                                            {'Decaps6tunnel0': 
                                                {'flags': 'NS DI',
                                                'uptime': '00:04:40'}},
                                        'uptime': '00:04:45'}}},
                            'ff02::/16': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'D P',
                                        'uptime': '00:04:45'}}},
                            'ff10::/15': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'D P',
                                        'uptime': '00:04:45'}}},
                            'ff12::/16': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'D P',
                                        'uptime': '00:04:45'}}},
                            'ff15::1:1': 
                                {'source_address': 
                                    {'2001:db8:1:0:1:1:1:2': 
                                        {'flags': 'L RPF MT',
                                        'incoming_interface_list': 
                                            {'GigabitEthernet150/0/0/6': 
                                                {'rpf_nbr': '2001:db8:1:0:1:1:1:2'}},
                                        'outgoing_interface_list': 
                                            {'mdtvpn1': 
                                                {'flags': 'F NS MI MT MA',
                                                'uptime': '00:02:53'}},
                                            'uptime': '00:02:53'}}},
                            'ff15::2:1': 
                                {'source_address': 
                                    {'2001:db8:10:0:4:4:4:5': 
                                        {'flags': 'L RPF',
                                        'incoming_interface_list': 
                                            {'mdtvpn1': 
                                                {'rpf_nbr': '::ffff:192.168.195.200'}},
                                        'outgoing_interface_list': 
                                            {'GigabitEthernet150/0/0/6': 
                                                {'flags': 'F NS',
                                                'uptime': '00:03:59'}},
                                        'uptime': '00:03:59'}}},
                            'ff20::/15': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'D P',
                                        'uptime': '00:04:45'}}},
                            'ff22::/16': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'D P',
                                        'uptime': '00:04:45'}}}}}}}}}
