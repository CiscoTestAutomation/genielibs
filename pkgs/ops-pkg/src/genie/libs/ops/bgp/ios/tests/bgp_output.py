''' 
BGP Genie Ops Object Outputs for IOS.
'''


class BgpOutput(object):

    show_bgp_all_summary = '''\
        show bgp all summary
        For address family: IPv4 Unicast
        BGP router identifier 1.1.1.1, local AS number 65000
        BGP table version is 4, main routing table version 4
        3 network entries using 744 bytes of memory
        3 path entries using 408 bytes of memory
        3/3 BGP path/bestpath attribute entries using 840 bytes of memory
        2 BGP extended community entries using 500 bytes of memory
        0 BGP route-map cache entries using 0 bytes of memory
        0 BGP filter-list cache entries using 0 bytes of memory
        BGP using 2492 total bytes of memory
        BGP activity 12/0 prefixes, 12/0 paths, scan interval 60 secs

        Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
        2.2.2.2         4        65000   27420   30189        4    0    0 2w5d            1
        3.3.3.3         4        65000   27430   30165        4    0    0 2w5d            1

        For address family: IPv6 Unicast
        BGP router identifier 1.1.1.1, local AS number 65000
        BGP table version is 5, main routing table version 5
        3 network entries using 816 bytes of memory
        3 path entries using 456 bytes of memory
        3/3 BGP path/bestpath attribute entries using 840 bytes of memory
        2 BGP extended community entries using 500 bytes of memory
        0 BGP route-map cache entries using 0 bytes of memory
        0 BGP filter-list cache entries using 0 bytes of memory
        BGP using 2612 total bytes of memory
        BGP activity 12/0 prefixes, 12/0 paths, scan interval 60 secs

        Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
        2001:2:2:2::2   4        65000   27420   30190        5    0    0 2w5d            1
        2001:3:3:3::3   4        65000   27430   30181        5    0    0 2w5d            1

        For address family: VPNv4 Unicast
        BGP router identifier 1.1.1.1, local AS number 65000
        BGP table version is 4, main routing table version 4
        3 network entries using 768 bytes of memory
        3 path entries using 408 bytes of memory
        3/3 BGP path/bestpath attribute entries using 888 bytes of memory
        2 BGP extended community entries using 500 bytes of memory
        0 BGP route-map cache entries using 0 bytes of memory
        0 BGP filter-list cache entries using 0 bytes of memory
        BGP using 2564 total bytes of memory
        BGP activity 12/0 prefixes, 12/0 paths, scan interval 60 secs

        Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
        2.2.2.2         4        65000   27420   30177        4    0    0 2w5d            1
        3.3.3.3         4        65000   27431   30188        4    0    0 2w5d            1

        For address family: VPNv6 Unicast
        BGP router identifier 1.1.1.1, local AS number 65000
        BGP table version is 5, main routing table version 5
        3 network entries using 840 bytes of memory
        3 path entries using 468 bytes of memory
        3/3 BGP path/bestpath attribute entries using 888 bytes of memory
        2 BGP extended community entries using 500 bytes of memory
        0 BGP route-map cache entries using 0 bytes of memory
        0 BGP filter-list cache entries using 0 bytes of memory
        BGP using 2696 total bytes of memory
        BGP activity 12/0 prefixes, 12/0 paths, scan interval 60 secs

        Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
        2001:2:2:2::2   4        65000   27420   30187        5    0    0 2w5d            1
        2001:3:3:3::3   4        65000   27430   30169        5    0    0 2w5d            1
        R1_xe#
    '''
    
    show_vrf_detail = '''\
        show vrf detail | inc \(VRF
        VRF Mgmt-intf (VRF Id = 1); default RD <not set>; default VPNID <not set>
        VRF VRF1 (VRF Id = 2); default RD 65000:1; default VPNID <not set>
    '''

    show_bgp_all_cluster_ids = '''\
        show bgp all cluster-ids
        Global cluster-id: 1.1.1.1 (configured: 0.0.0.0)
        BGP client-to-client reflection:         Configured    Used
        all (inter-cluster and intra-cluster): ENABLED
        intra-cluster:                         ENABLED       ENABLED

        List of cluster-ids:
        Cluster-id     #-neighbors C2C-rfl-CFG C2C-rfl-USE
    '''

    show_bgp_all_neighbors = '''\
        show bgp all neighbors
        For address family: IPv4 Unicast
        BGP neighbor is 2.2.2.2,  remote AS 65000, internal link
        BGP version 4, remote router ID 2.2.2.2
        BGP state = Established, up for 2w5d
        Last read 00:00:17, last write 00:00:39, hold time is 180, keepalive interval is 60 seconds
        Neighbor sessions:
            1 active, is not multisession capable (disabled)
        Neighbor capabilities:
            Route refresh: advertised and received(new)
            Four-octets ASN Capability: advertised and received
            Address family IPv4 Unicast: advertised and received
            Enhanced Refresh Capability: advertised
            Multisession Capability:
            Stateful switchover support enabled: NO for session 1
        Message statistics:
            InQ depth is 0
            OutQ depth is 0

                                Sent       Rcvd
            Opens:                  1          1
            Notifications:          0          0
            Updates:                2          2
            Keepalives:         30186      27417
            Route Refresh:          0          0
            Total:              30189      27420
        Do log neighbor state changes (via global configuration)
        Default minimum time between advertisement runs is 0 seconds

        Address tracking is enabled, the RIB does have a route to 2.2.2.2
        Route to peer address reachability Up: 1; Down: 0
            Last notification 2w5d
        Connections established 1; dropped 0
        Last reset never
        Interface associated: (none) (peering address NOT in same link)
        Transport(tcp) path-mtu-discovery is enabled
        Graceful-Restart is disabled
        SSO is disabled
        Connection state is ESTAB, I/O status: 1, unread input bytes: 0
        Connection is ECN Disabled, Mininum incoming TTL 0, Outgoing TTL 255
        Local host: 1.1.1.1, Local port: 179
        Foreign host: 2.2.2.2, Foreign port: 25026
        Connection tableid (VRF): 0
        Maximum output segment queue size: 50

        Enqueued packets for retransmit: 0, input: 0  mis-ordered: 0 (0 bytes)

        Event Timers (current time is 0x621EDEF8):
        Timer          Starts    Wakeups            Next
        Retrans         30188          0             0x0
        TimeWait            0          0             0x0
        AckHold         27419      26858             0x0
        SendWnd             0          0             0x0
        KeepAlive           0          0             0x0
        GiveUp              0          0             0x0
        PmtuAger            0          0             0x0
        DeadWait            0          0             0x0
        Linger              0          0             0x0
        ProcessQ            0          0             0x0

        iss:  402897367  snduna:  403471038  sndnxt:  403471038
        irs: 3455343999  rcvnxt: 3455865077

        sndwnd:  32236  scale:      0  maxrcvwnd:  16384
        rcvwnd:  15719  scale:      0  delrcvwnd:    665

        SRTT: 1000 ms, RTTO: 1003 ms, RTV: 3 ms, KRTT: 0 ms
        minRTT: 1 ms, maxRTT: 1000 ms, ACK hold: 200 ms
        uptime: 1645068668 ms, Sent idletime: 17155 ms, Receive idletime: 17356 ms
        Status Flags: passive open, gen tcbs
        Option Flags: nagle, path mtu capable
        IP Precedence value : 6

        Datagrams (max data segment is 1240 bytes):
        Rcvd: 57653 (out of order: 0), with data: 27419, total data bytes: 521077
        Sent: 57603 (retransmit: 0, fastretransmit: 0, partialack: 0, Second Congestion: 0), with data: 30188, total data bytes: 573670

        Packets received in fast path: 0, fast processed: 0, slow path: 0
        fast lock acquisition failures: 0, slow path: 0
        TCP Semaphore      0x7F23C7640538  FREE

        BGP neighbor is 3.3.3.3,  remote AS 65000, internal link
        BGP version 4, remote router ID 3.3.3.3
        BGP state = Established, up for 2w5d
        Last read 00:00:02, last write 00:00:22, hold time is 180, keepalive interval is 60 seconds
        Neighbor sessions:
            1 active, is not multisession capable (disabled)
        Neighbor capabilities:
            Route refresh: advertised and received(new)
            Four-octets ASN Capability: advertised and received
            Address family IPv4 Unicast: advertised and received
            Graceful Restart Capability: received
            Remote Restart timer is 120 seconds
            Address families advertised by peer:
                IPv4 Unicast (was not preserved
            Enhanced Refresh Capability: advertised
            Multisession Capability:
            Stateful switchover support enabled: NO for session 1
        Message statistics:
            InQ depth is 0
            OutQ depth is 0

                                Sent       Rcvd
            Opens:                  1          1
            Notifications:          0          0
            Updates:                2          2
            Keepalives:         30162      27427
            Route Refresh:          0          0
            Total:              30165      27430
        Do log neighbor state changes (via global configuration)
        Default minimum time between advertisement runs is 0 seconds

        Address tracking is enabled, the RIB does have a route to 3.3.3.3
        Route to peer address reachability Up: 1; Down: 0
            Last notification 2w5d
        Connections established 1; dropped 0
        Last reset never
        Interface associated: (none) (peering address NOT in same link)
        Transport(tcp) path-mtu-discovery is enabled
        Graceful-Restart is disabled
        SSO is disabled
        Connection state is ESTAB, I/O status: 1, unread input bytes: 0
        Connection is ECN Disabled, Mininum incoming TTL 0, Outgoing TTL 255
        Local host: 1.1.1.1, Local port: 11084
        Foreign host: 3.3.3.3, Foreign port: 179
        Connection tableid (VRF): 0
        Maximum output segment queue size: 50

        Enqueued packets for retransmit: 0, input: 0  mis-ordered: 0 (0 bytes)

        Event Timers (current time is 0x621EDEFB):
        Timer          Starts    Wakeups            Next
        Retrans         30165          0             0x0
        TimeWait            0          0             0x0
        AckHold         27429      26944             0x0
        SendWnd             0          0             0x0
        KeepAlive           0          0             0x0
        GiveUp              0          0             0x0
        PmtuAger      1636295    1636294      0x621EE25B
        DeadWait            0          0             0x0
        Linger              0          0             0x0
        ProcessQ            0          0             0x0

        iss: 4151727173  snduna: 4152300388  sndnxt: 4152300388
        irs: 3770309714  rcvnxt: 3770830970

        sndwnd:  29200  scale:      0  maxrcvwnd:  16384
        rcvwnd:  15966  scale:      0  delrcvwnd:    418

        SRTT: 1000 ms, RTTO: 1003 ms, RTV: 3 ms, KRTT: 0 ms
        minRTT: 1 ms, maxRTT: 1000 ms, ACK hold: 200 ms
        uptime: 1645729685 ms, Sent idletime: 2470 ms, Receive idletime: 2670 ms
        Status Flags: active open
        Option Flags: nagle, path mtu capable
        IP Precedence value : 6

        Datagrams (max data segment is 1460 bytes):
        Rcvd: 57650 (out of order: 0), with data: 27428, total data bytes: 521255
        Sent: 57523 (retransmit: 0, fastretransmit: 0, partialack: 0, Second Congestion: 0), with data: 30164, total data bytes: 573214

        Packets received in fast path: 0, fast processed: 0, slow path: 0
        fast lock acquisition failures: 0, slow path: 0
        TCP Semaphore      0x7F23C7494520  FREE


        For address family: IPv6 Unicast
        BGP neighbor is 2001:2:2:2::2,  remote AS 65000, internal link
        BGP version 4, remote router ID 2.2.2.2
        BGP state = Established, up for 2w5d
        Last read 00:00:17, last write 00:00:00, hold time is 180, keepalive interval is 60 seconds
        Neighbor sessions:
            1 active, is not multisession capable (disabled)
        Neighbor capabilities:
            Route refresh: advertised and received(new)
            Four-octets ASN Capability: advertised and received
            Address family IPv6 Unicast: advertised and received
            Enhanced Refresh Capability: advertised
            Multisession Capability:
            Stateful switchover support enabled: NO for session 1
        Message statistics:
            InQ depth is 0
            OutQ depth is 0

                                Sent       Rcvd
            Opens:                  1          1
            Notifications:          0          0
            Updates:                2          2
            Keepalives:         30188      27417
            Route Refresh:          0          0
            Total:              30191      27420
        Do log neighbor state changes (via global configuration)
        Default minimum time between advertisement runs is 0 seconds

        Address tracking is enabled, the RIB does have a route to 2001:2:2:2::2
        Route to peer address reachability Up: 2; Down: 0
            Last notification 2w5d
        Connections established 1; dropped 0
        Last reset never
        Interface associated: (none) (peering address NOT in same link)
        Transport(tcp) path-mtu-discovery is enabled
        Graceful-Restart is disabled
        SSO is disabled
        Connection state is ESTAB, I/O status: 1, unread input bytes: 0
        Connection is ECN Disabled, Mininum incoming TTL 0, Outgoing TTL 255
        Local host: 2001:1:1:1::1, Local port: 179
        Foreign host: 2001:2:2:2::2, Foreign port: 52223
        Connection tableid (VRF): 0
        Maximum output segment queue size: 50

        Enqueued packets for retransmit: 0, input: 0  mis-ordered: 0 (0 bytes)

        Event Timers (current time is 0x621EDEFE):
        Timer          Starts    Wakeups            Next
        Retrans         30190          0             0x0
        TimeWait            0          0             0x0
        AckHold         27419      26861             0x0
        SendWnd             0          0             0x0
        KeepAlive           0          0             0x0
        GiveUp              0          0             0x0
        PmtuAger            0          0             0x0
        DeadWait            0          0             0x0
        Linger              0          0             0x0
        ProcessQ            0          0             0x0

        iss:  723831891  snduna:  724405635  sndnxt:  724405635
        irs: 2052291678  rcvnxt: 2052812792

        sndwnd:  32141  scale:      0  maxrcvwnd:  16384
        rcvwnd:  15206  scale:      0  delrcvwnd:   1178

        SRTT: 1000 ms, RTTO: 1003 ms, RTV: 3 ms, KRTT: 0 ms
        minRTT: 1 ms, maxRTT: 1000 ms, ACK hold: 200 ms
        uptime: 1645067186 ms, Sent idletime: 315 ms, Receive idletime: 106 ms
        Status Flags: passive open, gen tcbs
        Option Flags: nagle, path mtu capable
        IP Precedence value : 6

        Datagrams (max data segment is 1220 bytes):
        Rcvd: 57654 (out of order: 0), with data: 27419, total data bytes: 521113
        Sent: 57613 (retransmit: 0, fastretransmit: 0, partialack: 0, Second Congestion: 0), with data: 57613, total data bytes: 2878271

        Packets received in fast path: 0, fast processed: 0, slow path: 0
        fast lock acquisition failures: 0, slow path: 0
        TCP Semaphore      0x7F23C76402C8  FREE

        BGP neighbor is 2001:3:3:3::3,  remote AS 65000, internal link
        BGP version 4, remote router ID 3.3.3.3
        BGP state = Established, up for 2w5d
        Last read 00:00:02, last write 00:00:10, hold time is 180, keepalive interval is 60 seconds
        Neighbor sessions:
            1 active, is not multisession capable (disabled)
        Neighbor capabilities:
            Route refresh: advertised and received(new)
            Four-octets ASN Capability: advertised and received
            Address family IPv6 Unicast: advertised and received
            Graceful Restart Capability: received
            Remote Restart timer is 120 seconds
            Address families advertised by peer:
                IPv6 Unicast (was not preserved
            Enhanced Refresh Capability: advertised
            Multisession Capability:
            Stateful switchover support enabled: NO for session 1
        Message statistics:
            InQ depth is 0
            OutQ depth is 0

                                Sent       Rcvd
            Opens:                  1          1
            Notifications:          0          0
            Updates:                2          2
            Keepalives:         30178      27427
            Route Refresh:          0          0
            Total:              30181      27430
        Do log neighbor state changes (via global configuration)
        Default minimum time between advertisement runs is 0 seconds

        Address tracking is enabled, the RIB does have a route to 2001:3:3:3::3
        Route to peer address reachability Up: 1; Down: 0
            Last notification 2w5d
        Connections established 1; dropped 0
        Last reset never
        Interface associated: (none) (peering address NOT in same link)
        Transport(tcp) path-mtu-discovery is enabled
        Graceful-Restart is disabled
        SSO is disabled
        Connection state is ESTAB, I/O status: 1, unread input bytes: 0
        Connection is ECN Disabled, Mininum incoming TTL 0, Outgoing TTL 255
        Local host: 2001:1:1:1::1, Local port: 179
        Foreign host: 2001:3:3:3::3, Foreign port: 47133
        Connection tableid (VRF): 0
        Maximum output segment queue size: 50

        Enqueued packets for retransmit: 0, input: 0  mis-ordered: 0 (0 bytes)

        Event Timers (current time is 0x621EDF01):
        Timer          Starts    Wakeups            Next
        Retrans         30180          0             0x0
        TimeWait            0          0             0x0
        AckHold         27429      26963             0x0
        SendWnd             0          0             0x0
        KeepAlive           0          0             0x0
        GiveUp              0          0             0x0
        PmtuAger            0          0             0x0
        DeadWait            0          0             0x0
        Linger              0          0             0x0
        ProcessQ            0          0             0x0

        iss: 1399948803  snduna: 1400522357  sndnxt: 1400522357
        irs: 1512650626  rcvnxt: 1513171918

        sndwnd:  28800  scale:      0  maxrcvwnd:  16384
        rcvwnd:  16384  scale:      0  delrcvwnd:      0

        SRTT: 1000 ms, RTTO: 1003 ms, RTV: 3 ms, KRTT: 0 ms
        minRTT: 1 ms, maxRTT: 1000 ms, ACK hold: 200 ms
        uptime: 1645725071 ms, Sent idletime: 2676 ms, Receive idletime: 2676 ms
        Status Flags: passive open, gen tcbs
        Option Flags: nagle, path mtu capable
        IP Precedence value : 6

        Datagrams (max data segment is 1440 bytes):
        Rcvd: 57664 (out of order: 0), with data: 27428, total data bytes: 521291
        Sent: 57560 (retransmit: 0, fastretransmit: 0, partialack: 0, Second Congestion: 0), with data: 57560, total data bytes: 2875961

        Packets received in fast path: 0, fast processed: 0, slow path: 0
        fast lock acquisition failures: 0, slow path: 0
        TCP Semaphore      0x7F23C7494380  FREE


        For address family: VPNv4 Unicast
        BGP neighbor is 2.2.2.2,  vrf VRF1,  remote AS 65000, internal link
        BGP version 4, remote router ID 2.2.2.2
        BGP state = Established, up for 2w5d
        Last read 00:00:13, last write 00:00:44, hold time is 180, keepalive interval is 60 seconds
        Neighbor sessions:
            1 active, is not multisession capable (disabled)
        Neighbor capabilities:
            Route refresh: advertised and received(new)
            Four-octets ASN Capability: advertised and received
            Address family IPv4 Unicast: advertised and received
            Enhanced Refresh Capability: advertised
            Multisession Capability:
            Stateful switchover support enabled: NO for session 1
        Message statistics:
            InQ depth is 0
            OutQ depth is 0

                                Sent       Rcvd
            Opens:                  1          1
            Notifications:          0          0
            Updates:                2          2
            Keepalives:         30174      27417
            Route Refresh:          0          0
            Total:              30177      27420
        Do log neighbor state changes (via global configuration)
        Default minimum time between advertisement runs is 0 seconds

        Address tracking is enabled, the RIB does have a route to 2.2.2.2
        Route to peer address reachability Up: 2; Down: 0
            Last notification 2w5d
        Connections established 1; dropped 0
        Last reset never
        Interface associated: (none) (peering address NOT in same link)
        Transport(tcp) path-mtu-discovery is enabled
        Graceful-Restart is disabled
        SSO is disabled
        Connection state is ESTAB, I/O status: 1, unread input bytes: 0
        Connection is ECN Disabled, Mininum incoming TTL 0, Outgoing TTL 255
        Local host: 1.1.1.1, Local port: 179
        Foreign host: 2.2.2.2, Foreign port: 50426
        Connection tableid (VRF): 2
        Maximum output segment queue size: 50

        Enqueued packets for retransmit: 0, input: 0  mis-ordered: 0 (0 bytes)

        Event Timers (current time is 0x621EDF03):
        Timer          Starts    Wakeups            Next
        Retrans         30180          4             0x0
        TimeWait            0          0             0x0
        AckHold         27420      26856             0x0
        SendWnd             0          0             0x0
        KeepAlive           0          0             0x0
        GiveUp              0          0             0x0
        PmtuAger            0          0             0x0
        DeadWait            0          0             0x0
        Linger              0          0             0x0
        ProcessQ            0          0             0x0

        iss: 3028094276  snduna: 3028667719  sndnxt: 3028667719
        irs:  568735500  rcvnxt:  569256556

        sndwnd:  32483  scale:      0  maxrcvwnd:  16384
        rcvwnd:  15738  scale:      0  delrcvwnd:    646

        SRTT: 1000 ms, RTTO: 1003 ms, RTV: 3 ms, KRTT: 0 ms
        minRTT: 1 ms, maxRTT: 1000 ms, ACK hold: 200 ms
        uptime: 1645068163 ms, Sent idletime: 13180 ms, Receive idletime: 13380 ms
        Status Flags: passive open, gen tcbs
        Option Flags: VRF id set, nagle, path mtu capable
        IP Precedence value : 6

        Datagrams (max data segment is 1240 bytes):
        Rcvd: 57669 (out of order: 0), with data: 27420, total data bytes: 521055
        Sent: 57610 (retransmit: 4, fastretransmit: 0, partialack: 0, Second Congestion: 0), with data: 30176, total data bytes: 573442

        Packets received in fast path: 0, fast processed: 0, slow path: 0
        fast lock acquisition failures: 0, slow path: 0
        TCP Semaphore      0x7F23C7640468  FREE

        BGP neighbor is 3.3.3.3,  vrf VRF1,  remote AS 65000, internal link
        BGP version 4, remote router ID 3.3.3.3
        BGP state = Established, up for 2w5d
        Last read 00:00:02, last write 00:00:40, hold time is 180, keepalive interval is 60 seconds
        Neighbor sessions:
            1 active, is not multisession capable (disabled)
        Neighbor capabilities:
            Route refresh: advertised and received(new)
            Four-octets ASN Capability: advertised and received
            Address family IPv4 Unicast: advertised and received
            Graceful Restart Capability: received
            Remote Restart timer is 120 seconds
            Address families advertised by peer:
                IPv4 Unicast (was not preserved
            Enhanced Refresh Capability: advertised
            Multisession Capability:
            Stateful switchover support enabled: NO for session 1
        Message statistics:
            InQ depth is 0
            OutQ depth is 0

                                Sent       Rcvd
            Opens:                  1          1
            Notifications:          0          0
            Updates:                2          3
            Keepalives:         30185      27427
            Route Refresh:          0          0
            Total:              30188      27431
        Do log neighbor state changes (via global configuration)
        Default minimum time between advertisement runs is 0 seconds

        Address tracking is enabled, the RIB does have a route to 3.3.3.3
        Route to peer address reachability Up: 1; Down: 0
            Last notification 2w5d
        Connections established 1; dropped 0
        Last reset never
        Interface associated: (none) (peering address NOT in same link)
        Transport(tcp) path-mtu-discovery is enabled
        Graceful-Restart is disabled
        SSO is disabled
        Connection state is ESTAB, I/O status: 1, unread input bytes: 0
        Connection is ECN Disabled, Mininum incoming TTL 0, Outgoing TTL 255
        Local host: 1.1.1.1, Local port: 43893
        Foreign host: 3.3.3.3, Foreign port: 179
        Connection tableid (VRF): 2
        Maximum output segment queue size: 50

        Enqueued packets for retransmit: 0, input: 0  mis-ordered: 0 (0 bytes)

        Event Timers (current time is 0x621EDF06):
        Timer          Starts    Wakeups            Next
        Retrans         30188          0             0x0
        TimeWait            0          0             0x0
        AckHold         27429      26958             0x0
        SendWnd             0          0             0x0
        KeepAlive           0          0             0x0
        GiveUp              0          0             0x0
        PmtuAger      1636291    1636290      0x621EE25B
        DeadWait            0          0             0x0
        Linger              0          0             0x0
        ProcessQ            0          0             0x0

        iss: 1210418011  snduna: 1210991663  sndnxt: 1210991663
        irs: 1252136999  rcvnxt: 1252658304

        sndwnd:  29200  scale:      0  maxrcvwnd:  16384
        rcvwnd:  15909  scale:      0  delrcvwnd:    475

        SRTT: 1000 ms, RTTO: 1003 ms, RTV: 3 ms, KRTT: 0 ms
        minRTT: 1 ms, maxRTT: 1000 ms, ACK hold: 200 ms
        uptime: 1645726624 ms, Sent idletime: 2482 ms, Receive idletime: 2682 ms
        Status Flags: active open
        Option Flags: VRF id set, nagle, path mtu capable
        IP Precedence value : 6

        Datagrams (max data segment is 1460 bytes):
        Rcvd: 57674 (out of order: 0), with data: 27429, total data bytes: 521304
        Sent: 57561 (retransmit: 0, fastretransmit: 0, partialack: 0, Second Congestion: 0), with data: 30187, total data bytes: 573651

        Packets received in fast path: 0, fast processed: 0, slow path: 0
        fast lock acquisition failures: 0, slow path: 0
        TCP Semaphore      0x7F23C7494450  FREE


        For address family: VPNv6 Unicast
        BGP neighbor is 2001:2:2:2::2,  vrf VRF1,  remote AS 65000, internal link
        BGP version 4, remote router ID 2.2.2.2
        BGP state = Established, up for 2w5d
        Last read 00:00:05, last write 00:00:26, hold time is 180, keepalive interval is 60 seconds
        Neighbor sessions:
            1 active, is not multisession capable (disabled)
        Neighbor capabilities:
            Route refresh: advertised and received(new)
            Four-octets ASN Capability: advertised and received
            Address family IPv6 Unicast: advertised and received
            Enhanced Refresh Capability: advertised
            Multisession Capability:
            Stateful switchover support enabled: NO for session 1
        Message statistics:
            InQ depth is 0
            OutQ depth is 0

                                Sent       Rcvd
            Opens:                  1          1
            Notifications:          0          0
            Updates:                2          2
            Keepalives:         30184      27417
            Route Refresh:          0          0
            Total:              30187      27420
        Do log neighbor state changes (via global configuration)
        Default minimum time between advertisement runs is 0 seconds

        Address tracking is enabled, the RIB does have a route to 2001:2:2:2::2
        Route to peer address reachability Up: 1; Down: 0
            Last notification 2w5d
        Connections established 1; dropped 0
        Last reset never
        Interface associated: (none) (peering address NOT in same link)
        Transport(tcp) path-mtu-discovery is enabled
        Graceful-Restart is disabled
        SSO is disabled
        Connection state is ESTAB, I/O status: 1, unread input bytes: 0
        Connection is ECN Disabled, Mininum incoming TTL 0, Outgoing TTL 255
        Local host: 2001:1:1:1::1, Local port: 32057
        Foreign host: 2001:2:2:2::2, Foreign port: 179
        Connection tableid (VRF): 503316482
        Maximum output segment queue size: 50

        Enqueued packets for retransmit: 0, input: 0  mis-ordered: 0 (0 bytes)

        Event Timers (current time is 0x621EDF09):
        Timer          Starts    Wakeups            Next
        Retrans         30190          4             0x0
        TimeWait            0          0             0x0
        AckHold         27420      26869             0x0
        SendWnd             0          0             0x0
        KeepAlive           0          0             0x0
        GiveUp              0          0             0x0
        PmtuAger            1          1             0x0
        DeadWait            0          0             0x0
        Linger              0          0             0x0
        ProcessQ            0          0             0x0

        iss: 3279254845  snduna: 3279828513  sndnxt: 3279828513
        irs: 2772915965  rcvnxt: 2773437057

        sndwnd:  32217  scale:      0  maxrcvwnd:  16384
        rcvwnd:  15225  scale:      0  delrcvwnd:   1159

        SRTT: 1000 ms, RTTO: 1003 ms, RTV: 3 ms, KRTT: 0 ms
        minRTT: 1 ms, maxRTT: 1000 ms, ACK hold: 200 ms
        uptime: 1645068087 ms, Sent idletime: 5770 ms, Receive idletime: 5970 ms
        Status Flags: active open
        Option Flags: VRF id set, nagle, path mtu capable
        IP Precedence value : 6

        Datagrams (max data segment is 1220 bytes):
        Rcvd: 57637 (out of order: 0), with data: 27419, total data bytes: 521091
        Sent: 57604 (retransmit: 4, fastretransmit: 0, partialack: 0, Second Congestion: 0), with data: 57604, total data bytes: 2877835

        Packets received in fast path: 0, fast processed: 0, slow path: 0
        fast lock acquisition failures: 0, slow path: 0
        TCP Semaphore      0x7F23C7640398  FREE

        BGP neighbor is 2001:3:3:3::3,  vrf VRF1,  remote AS 65000, internal link
        BGP version 4, remote router ID 3.3.3.3
        BGP state = Established, up for 2w5d
        Last read 00:00:39, last write 00:00:26, hold time is 180, keepalive interval is 60 seconds
        Neighbor sessions:
            1 active, is not multisession capable (disabled)
        Neighbor capabilities:
            Route refresh: advertised and received(new)
            Four-octets ASN Capability: advertised and received
            Address family IPv6 Unicast: advertised and received
            Graceful Restart Capability: received
            Remote Restart timer is 120 seconds
            Address families advertised by peer:
                IPv6 Unicast (was not preserved
            Enhanced Refresh Capability: advertised
            Multisession Capability:
            Stateful switchover support enabled: NO for session 1
        Message statistics:
            InQ depth is 0
            OutQ depth is 0

                                Sent       Rcvd
            Opens:                  1          1
            Notifications:          0          0
            Updates:                2          3
            Keepalives:         30166      27426
            Route Refresh:          0          0
            Total:              30169      27430
        Do log neighbor state changes (via global configuration)
        Default minimum time between advertisement runs is 0 seconds

        Address tracking is enabled, the RIB does have a route to 2001:3:3:3::3
        Route to peer address reachability Up: 1; Down: 0
            Last notification 2w5d
        Connections established 1; dropped 0
        Last reset never
        Interface associated: (none) (peering address NOT in same link)
        Transport(tcp) path-mtu-discovery is enabled
        Graceful-Restart is disabled
        SSO is disabled
        Connection state is ESTAB, I/O status: 1, unread input bytes: 0
        Connection is ECN Disabled, Mininum incoming TTL 0, Outgoing TTL 255
        Local host: 2001:1:1:1::1, Local port: 179
        Foreign host: 2001:3:3:3::3, Foreign port: 20838
        Connection tableid (VRF): 503316482
        Maximum output segment queue size: 50

        Enqueued packets for retransmit: 0, input: 0  mis-ordered: 0 (0 bytes)

        Event Timers (current time is 0x621EDF0B):
        Timer          Starts    Wakeups            Next
        Retrans         30168          0             0x0
        TimeWait            0          0             0x0
        AckHold         27429      26946             0x0
        SendWnd             0          0             0x0
        KeepAlive           0          0             0x0
        GiveUp              0          0             0x0
        PmtuAger            0          0             0x0
        DeadWait            0          0             0x0
        Linger              0          0             0x0
        ProcessQ            0          0             0x0

        iss: 2912962685  snduna: 2913536011  sndnxt: 2913536011
        irs: 3025088327  rcvnxt: 3025609679

        sndwnd:  28800  scale:      0  maxrcvwnd:  16384
        rcvwnd:  16327  scale:      0  delrcvwnd:     57

        SRTT: 1000 ms, RTTO: 1003 ms, RTV: 3 ms, KRTT: 0 ms
        minRTT: 1 ms, maxRTT: 1000 ms, ACK hold: 200 ms
        uptime: 1645724603 ms, Sent idletime: 26956 ms, Receive idletime: 26955 ms
        Status Flags: passive open, gen tcbs
        Option Flags: VRF id set, nagle, path mtu capable
        IP Precedence value : 6

        Datagrams (max data segment is 1440 bytes):
        Rcvd: 57671 (out of order: 0), with data: 27428, total data bytes: 521351
        Sent: 57550 (retransmit: 0, fastretransmit: 0, partialack: 0, Second Congestion: 0), with data: 57550, total data bytes: 2875333

        Packets received in fast path: 0, fast processed: 0, slow path: 0
        fast lock acquisition failures: 0, slow path: 0
        TCP Semaphore      0x7F23C74942B0  FREE


        For address family: IPv4 Multicast

        For address family: L2VPN E-VPN

        For address family: VPNv4 Multicast

        For address family: MVPNv4 Unicast

        For address family: MVPNv6 Unicast

        For address family: VPNv6 Multicast

        For address family: VPNv4 Flowspec

        For address family: VPNv6 Flowspec
    '''

    show_neighbor_policy_1 = '''\
        show bgp all neighbors 2.2.2.2 policy
        Neighbor: 2.2.2.2, Address-Family: IPv4 Unicast
        Neighbor: 2.2.2.2, Address-Family: VPNv4 Unicast (VRF1)
    '''

    show_neighbor_policy_2 = '''\
        show bgp all neighbors 2001:2:2:2::2 policy
        Neighbor: 2001:2:2:2::2, Address-Family: IPv6 Unicast
        Neighbor: 2001:2:2:2::2, Address-Family: VPNv6 Unicast (VRF1)
    '''

    show_neighbor_policy_3 = '''\
        show bgp all neighbors 2001:3:3:3::3 policy
        Neighbor: 2001:3:3:3::3, Address-Family: IPv6 Unicast
        Neighbor: 2001:3:3:3::3, Address-Family: VPNv6 Unicast (VRF1)
    '''

    show_neighbor_policy_4 = '''\
        show bgp all neighbors 3.3.3.3 policy
        Neighbor: 3.3.3.3, Address-Family: IPv4 Unicast
        Neighbor: 3.3.3.3, Address-Family: VPNv4 Unicast (VRF1)
    '''

    show_bgp_all = '''\
        show bgp all
        For address family: IPv4 Unicast

        BGP table version is 4, local router ID is 1.1.1.1
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
                    r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter,
                    x best-external, a additional-path, c RIB-compressed,
                    t secondary path, L long-lived-stale,
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

            Network          Next Hop            Metric LocPrf Weight Path
        *>   1.1.1.1/32       0.0.0.0                  0         32768 i
        r>i  2.2.2.2/32       2.2.2.2                  0    100      0 i
        r>i  3.3.3.3/32       3.3.3.3                       100      0 i

        For address family: IPv6 Unicast

        BGP table version is 5, local router ID is 1.1.1.1
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
                    r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter,
                    x best-external, a additional-path, c RIB-compressed,
                    t secondary path, L long-lived-stale,
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

            Network          Next Hop            Metric LocPrf Weight Path
        *>   2001:1:1:1::1/128
                            ::                       0         32768 i
        r>i  2001:2:2:2::2/128
                            2001:2:2:2::2            0    100      0 i
        r>i  2001:3:3:3::3/128
                            2001:3:3:3::3                 100      0 i

        For address family: VPNv4 Unicast

        BGP table version is 4, local router ID is 1.1.1.1
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
                    r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter,
                    x best-external, a additional-path, c RIB-compressed,
                    t secondary path, L long-lived-stale,
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

            Network          Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 65000:1 (default for vrf VRF1)
        *>   1.1.1.1/32       0.0.0.0                  0         32768 i
        r>i  2.2.2.2/32       2.2.2.2                  0    100      0 i
        r>i  3.3.3.3/32       3.3.3.3                       100      0 i

        For address family: VPNv6 Unicast

        BGP table version is 5, local router ID is 1.1.1.1
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
                    r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter,
                    x best-external, a additional-path, c RIB-compressed,
                    t secondary path, L long-lived-stale,
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

            Network          Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 65000:1 (default for vrf VRF1)
        *>   2001:1:1:1::1/128
                            ::                       0         32768 i
        r>i  2001:2:2:2::2/128
                            2001:2:2:2::2            0    100      0 i
        r>i  2001:3:3:3::3/128
                            2001:3:3:3::3                 100      0 i

        For address family: IPv4 Multicast


        For address family: L2VPN E-VPN


        For address family: VPNv4 Multicast


        For address family: MVPNv4 Unicast


        For address family: MVPNv6 Unicast


        For address family: VPNv6 Multicast


        For address family: VPNv4 Flowspec


        For address family: VPNv6 Flowspec
    '''

    show_bgp_all_detail = '''\
        show bgp all detail
        For address family: IPv4 Unicast

        BGP routing table entry for 1.1.1.1/32, version 2
        Paths: (1 available, best #1, table default)
        Advertised to update-groups:
            1
        Refresh Epoch 1
        Local
            0.0.0.0 from 0.0.0.0 (1.1.1.1)
            Origin IGP, metric 0, localpref 100, weight 32768, valid, sourced, local, best
            rx pathid: 0, tx pathid: 0x0
        BGP routing table entry for 2.2.2.2/32, version 4
        Paths: (1 available, best #1, table default, RIB-failure(17))
        Flag: 0x100
        Not advertised to any peer
        Refresh Epoch 1
        Local
            2.2.2.2 (metric 10752) from 2.2.2.2 (2.2.2.2)
            Origin IGP, metric 0, localpref 100, valid, internal, best
            rx pathid: 0, tx pathid: 0x0
        BGP routing table entry for 3.3.3.3/32, version 3
        Paths: (1 available, best #1, table default, RIB-failure(17))
        Not advertised to any peer
        Refresh Epoch 1
        Local
            3.3.3.3 (metric 2570240) from 3.3.3.3 (3.3.3.3)
            Origin IGP, localpref 100, valid, internal, best
            rx pathid: 0, tx pathid: 0x0

        For address family: IPv6 Unicast

        BGP routing table entry for 2001:1:1:1::1/128, version 3
        Paths: (1 available, best #1, table default)
        Advertised to update-groups:
            1
        Refresh Epoch 1
        Local
            :: from 0.0.0.0 (1.1.1.1)
            Origin IGP, metric 0, localpref 100, weight 32768, valid, sourced, local, best
            rx pathid: 0, tx pathid: 0x0
        BGP routing table entry for 2001:2:2:2::2/128, version 5
        Paths: (1 available, best #1, table default, RIB-failure(145))
        Flag: 0x100
        Not advertised to any peer
        Refresh Epoch 1
        Local
            2001:2:2:2::2 (metric 10752) from 2001:2:2:2::2 (2.2.2.2)
            Origin IGP, metric 0, localpref 100, valid, internal, best
            rx pathid: 0, tx pathid: 0x0
        BGP routing table entry for 2001:3:3:3::3/128, version 4
        Paths: (1 available, best #1, table default, RIB-failure(145))
        Not advertised to any peer
        Refresh Epoch 1
        Local
            2001:3:3:3::3 (metric 2570240) from 2001:3:3:3::3 (3.3.3.3)
            Origin IGP, localpref 100, valid, internal, best
            rx pathid: 0, tx pathid: 0x0

        For address family: VPNv4 Unicast


        Route Distinguisher: 65000:1 (default for vrf VRF1)
        BGP routing table entry for 65000:1:1.1.1.1/32, version 2
        Paths: (1 available, best #1, table VRF1)
        Advertised to update-groups:
            1
        Refresh Epoch 1
        Local
            0.0.0.0 (via vrf VRF1) from 0.0.0.0 (1.1.1.1)
            Origin IGP, metric 0, localpref 100, weight 32768, valid, sourced, local, best
            Extended Community: Cost:pre-bestpath:128:1280 0x8800:32768:0
                0x8801:100:32 0x8802:65280:256 0x8803:65281:1514 0x8806:0:16843009
            rx pathid: 0, tx pathid: 0x0
        BGP routing table entry for 65000:1:2.2.2.2/32, version 4
        Paths: (1 available, best #1, table VRF1, RIB-failure(17))
        Flag: 0x100
        Not advertised to any peer
        Refresh Epoch 1
        Local
            2.2.2.2 (metric 10752) (via vrf VRF1) from 2.2.2.2 (2.2.2.2)
            Origin IGP, metric 0, localpref 100, valid, internal, best
            rx pathid: 0, tx pathid: 0x0
        BGP routing table entry for 65000:1:3.3.3.3/32, version 3
        Paths: (1 available, best #1, table VRF1, RIB-failure(17))
        Not advertised to any peer
        Refresh Epoch 1
        Local
            3.3.3.3 (metric 2570240) (via vrf VRF1) from 3.3.3.3 (3.3.3.3)
            Origin IGP, localpref 100, valid, internal, best
            rx pathid: 0, tx pathid: 0x0

        For address family: VPNv6 Unicast


        Route Distinguisher: 65000:1 (default for vrf VRF1)
        BGP routing table entry for [65000:1]2001:1:1:1::1/128, version 3
        Paths: (1 available, best #1, table VRF1)
        Advertised to update-groups:
            1
        Refresh Epoch 1
        Local
            :: (via vrf VRF1) from 0.0.0.0 (1.1.1.1)
            Origin IGP, metric 0, localpref 100, weight 32768, valid, sourced, local, best
            Extended Community: Cost:pre-bestpath:128:1280 0x8800:32768:0
                0x8801:100:32 0x8802:65280:256 0x8803:65281:1514 0x8806:0:16843009
                0x8807:53266:318767104
            rx pathid: 0, tx pathid: 0x0
        BGP routing table entry for [65000:1]2001:2:2:2::2/128, version 5
        Paths: (1 available, best #1, table VRF1, RIB-failure(145))
        Flag: 0x100
        Not advertised to any peer
        Refresh Epoch 1
        Local
            2001:2:2:2::2 (metric 10752) (via vrf VRF1) from 2001:2:2:2::2 (2.2.2.2)
            Origin IGP, metric 0, localpref 100, valid, internal, best
            rx pathid: 0, tx pathid: 0x0
        BGP routing table entry for [65000:1]2001:3:3:3::3/128, version 4
        Paths: (1 available, best #1, table VRF1, RIB-failure(145))
        Not advertised to any peer
        Refresh Epoch 1
        Local
            2001:3:3:3::3 (metric 2570240) (via vrf VRF1) from 2001:3:3:3::3 (3.3.3.3)
            Origin IGP, localpref 100, valid, internal, best
            rx pathid: 0, tx pathid: 0x0

        For address family: IPv4 Multicast


        For address family: L2VPN E-VPN


        For address family: VPNv4 Multicast


        For address family: MVPNv4 Unicast


        For address family: MVPNv6 Unicast


        For address family: VPNv6 Multicast


        For address family: VPNv4 Flowspec


        For address family: VPNv6 Flowspec
    '''

    nbr_routes_1 = '''\
        show bgp all neighbors 2.2.2.2 routes
        For address family: IPv4 Unicast
        BGP table version is 4, local router ID is 1.1.1.1
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
                    r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
                    x best-external, a additional-path, c RIB-compressed, 
                    t secondary path, L long-lived-stale,
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

            Network          Next Hop            Metric LocPrf Weight Path
        r>i  2.2.2.2/32       2.2.2.2                  0    100      0 i

        Total number of prefixes 1 

        For address family: VPNv4 Unicast
        BGP table version is 4, local router ID is 1.1.1.1
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
                    r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
                    x best-external, a additional-path, c RIB-compressed, 
                    t secondary path, L long-lived-stale,
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

            Network          Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 65000:1 (default for vrf VRF1)
        r>i  2.2.2.2/32       2.2.2.2                  0    100      0 i

        Total number of prefixes 1 
    '''

    nbr_routes_2 = '''\
        show bgp all neighbors 2001:2:2:2::2 routes
        For address family: IPv6 Unicast
        BGP table version is 5, local router ID is 1.1.1.1
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
                    r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
                    x best-external, a additional-path, c RIB-compressed, 
                    t secondary path, L long-lived-stale,
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

            Network          Next Hop            Metric LocPrf Weight Path
        r>i  2001:2:2:2::2/128
                            2001:2:2:2::2            0    100      0 i

        Total number of prefixes 1 

        For address family: VPNv6 Unicast
        BGP table version is 5, local router ID is 1.1.1.1
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
                    r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
                    x best-external, a additional-path, c RIB-compressed, 
                    t secondary path, L long-lived-stale,
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

            Network          Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 65000:1 (default for vrf VRF1)
        r>i  2001:2:2:2::2/128
                            2001:2:2:2::2            0    100      0 i

        Total number of prefixes 1 
    '''

    nbr_routes_3 = '''\
        show bgp all neighbors 2001:3:3:3::3 routes
        For address family: IPv6 Unicast
        BGP table version is 5, local router ID is 1.1.1.1
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
                    r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
                    x best-external, a additional-path, c RIB-compressed, 
                    t secondary path, L long-lived-stale,
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

            Network          Next Hop            Metric LocPrf Weight Path
        r>i  2001:3:3:3::3/128
                            2001:3:3:3::3                 100      0 i

        Total number of prefixes 1 

        For address family: VPNv6 Unicast
        BGP table version is 5, local router ID is 1.1.1.1
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
                    r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
                    x best-external, a additional-path, c RIB-compressed, 
                    t secondary path, L long-lived-stale,
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

            Network          Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 65000:1 (default for vrf VRF1)
        r>i  2001:3:3:3::3/128
                            2001:3:3:3::3                 100      0 i

        Total number of prefixes 1 
    '''

    nbr_routes_4 = '''\
        show bgp all neighbors 3.3.3.3 routes
        For address family: IPv4 Unicast
        BGP table version is 4, local router ID is 1.1.1.1
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
                    r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
                    x best-external, a additional-path, c RIB-compressed, 
                    t secondary path, L long-lived-stale,
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

            Network          Next Hop            Metric LocPrf Weight Path
        r>i  3.3.3.3/32       3.3.3.3                       100      0 i

        Total number of prefixes 1 

        For address family: VPNv4 Unicast
        BGP table version is 4, local router ID is 1.1.1.1
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
                    r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
                    x best-external, a additional-path, c RIB-compressed, 
                    t secondary path, L long-lived-stale,
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

            Network          Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 65000:1 (default for vrf VRF1)
        r>i  3.3.3.3/32       3.3.3.3                       100      0 i

        Total number of prefixes 1 
    '''

    nbr_adv_routes_1 = '''\
        show bgp all neighbors 2.2.2.2 advertised-routes
        For address family: IPv4 Unicast
        BGP table version is 4, local router ID is 1.1.1.1
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
                    r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
                    x best-external, a additional-path, c RIB-compressed, 
                    t secondary path, L long-lived-stale,
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

            Network          Next Hop            Metric LocPrf Weight Path
        *>   1.1.1.1/32       0.0.0.0                  0         32768 i

        Total number of prefixes 1 

        For address family: VPNv4 Unicast
        BGP table version is 4, local router ID is 1.1.1.1
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
                    r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
                    x best-external, a additional-path, c RIB-compressed, 
                    t secondary path, L long-lived-stale,
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

            Network          Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 65000:1 (default for vrf VRF1)
        *>   1.1.1.1/32       0.0.0.0                  0         32768 i

        Total number of prefixes 1 
    '''
    
    nbr_adv_routes_2 = '''\
        show bgp all neighbors 2001:2:2:2::2 advertised-routes
        For address family: IPv6 Unicast
        BGP table version is 5, local router ID is 1.1.1.1
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
                    r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
                    x best-external, a additional-path, c RIB-compressed, 
                    t secondary path, L long-lived-stale,
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

            Network          Next Hop            Metric LocPrf Weight Path
        *>   2001:1:1:1::1/128
                            ::                       0         32768 i

        Total number of prefixes 1 

        For address family: VPNv6 Unicast
        BGP table version is 5, local router ID is 1.1.1.1
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
                    r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
                    x best-external, a additional-path, c RIB-compressed, 
                    t secondary path, L long-lived-stale,
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

            Network          Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 65000:1 (default for vrf VRF1)
        *>   2001:1:1:1::1/128
                            ::                       0         32768 i

        Total number of prefixes 1 
    '''

    nbr_adv_routes_3 = '''\
        show bgp all neighbors 2001:3:3:3::3 advertised-routes
        For address family: IPv6 Unicast
        BGP table version is 5, local router ID is 1.1.1.1
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
                    r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
                    x best-external, a additional-path, c RIB-compressed, 
                    t secondary path, L long-lived-stale,
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

            Network          Next Hop            Metric LocPrf Weight Path
        *>   2001:1:1:1::1/128
                            ::                       0         32768 i

        Total number of prefixes 1 

        For address family: VPNv6 Unicast
        BGP table version is 5, local router ID is 1.1.1.1
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
                    r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
                    x best-external, a additional-path, c RIB-compressed, 
                    t secondary path, L long-lived-stale,
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

            Network          Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 65000:1 (default for vrf VRF1)
        *>   2001:1:1:1::1/128
                            ::                       0         32768 i

        Total number of prefixes 1 
    '''

    nbr_adv_routes_4 = '''\
        show bgp all neighbors 3.3.3.3 advertised-routes
        For address family: IPv4 Unicast
        BGP table version is 4, local router ID is 1.1.1.1
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
                    r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
                    x best-external, a additional-path, c RIB-compressed, 
                    t secondary path, L long-lived-stale,
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

            Network          Next Hop            Metric LocPrf Weight Path
        *>   1.1.1.1/32       0.0.0.0                  0         32768 i

        Total number of prefixes 1 

        For address family: VPNv4 Unicast
        BGP table version is 4, local router ID is 1.1.1.1
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
                    r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
                    x best-external, a additional-path, c RIB-compressed, 
                    t secondary path, L long-lived-stale,
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

            Network          Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 65000:1 (default for vrf VRF1)
        *>   1.1.1.1/32       0.0.0.0                  0         32768 i

        Total number of prefixes 1 
    '''

    custom_output_1 = '''\
        show bgp vpnv4 unicast all neighbors 2.2.2.2
        BGP neighbor is 2.2.2.2,  vrf VRF1,  remote AS 65000, internal link
        BGP version 4, remote router ID 2.2.2.2
        BGP state = Established, up for 2w5d
        Last read 00:00:44, last write 00:00:42, hold time is 180, keepalive interval is 60 seconds
        Neighbor sessions:
            1 active, is not multisession capable (disabled)
        Neighbor capabilities:
            Route refresh: advertised and received(new)
            Four-octets ASN Capability: advertised and received
            Address family IPv4 Unicast: advertised and received
            Enhanced Refresh Capability: advertised
            Multisession Capability:
            Stateful switchover support enabled: NO for session 1
        Message statistics:
            InQ depth is 0
            OutQ depth is 0

                                Sent       Rcvd
            Opens:                  1          1
            Notifications:          0          0
            Updates:                2          2
            Keepalives:         30228      27466
            Route Refresh:          0          0
            Total:              30231      27469
        Do log neighbor state changes (via global configuration)
        Default minimum time between advertisement runs is 0 seconds

        For address family: VPNv4 Unicast
        Translates address family IPv4 Unicast for VRF VRF1
        Session: 2.2.2.2
        BGP table version 4, neighbor version 4/0
        Output queue size : 0
        Index 1, Advertise bit 0
        1 update-group member
        Slow-peer detection is disabled
        Slow-peer split-update-group dynamic is disabled
                                        Sent       Rcvd
        Prefix activity:               ----       ----
            Prefixes Current:               1          1 (Consumes 136 bytes)
            Prefixes Total:                 2          1
            Implicit Withdraw:              1          0
            Explicit Withdraw:              0          0
            Used as bestpath:             n/a          1
            Used as multipath:            n/a          0
            Used as secondary:            n/a          0

                                        Outbound    Inbound
        Local Policy Denied Prefixes:    --------    -------
            Bestpath from this peer:              2        n/a
            Bestpath from iBGP peer:              1        n/a
            Total:                                3          0
        Number of NLRIs in the update sent: max 1, min 0
        Last detected as dynamic slow peer: never
        Dynamic slow peer recovered: never
        Refresh Epoch: 1
        Last Sent Refresh Start-of-rib: never
        Last Sent Refresh End-of-rib: never
        Last Received Refresh Start-of-rib: never
        Last Received Refresh End-of-rib: never
                                            Sent       Rcvd
                Refresh activity:              ----       ----
                Refresh Start-of-RIB          0          0
                Refresh End-of-RIB            0          0

        Address tracking is enabled, the RIB does have a route to 2.2.2.2
        Route to peer address reachability Up: 2; Down: 0
            Last notification 2w5d
        Connections established 1; dropped 0
        Last reset never
        Interface associated: (none) (peering address NOT in same link)
        Transport(tcp) path-mtu-discovery is enabled
        Graceful-Restart is disabled
        SSO is disabled
        Connection state is ESTAB, I/O status: 1, unread input bytes: 0
        Connection is ECN Disabled, Mininum incoming TTL 0, Outgoing TTL 255
        Local host: 1.1.1.1, Local port: 179
        Foreign host: 2.2.2.2, Foreign port: 50426
        Connection tableid (VRF): 2
        Maximum output segment queue size: 50

        Enqueued packets for retransmit: 0, input: 0  mis-ordered: 0 (0 bytes)

        Event Timers (current time is 0x624C3478):
        Timer          Starts    Wakeups            Next
        Retrans         30234          4             0x0
        TimeWait            0          0             0x0
        AckHold         27469      26904             0x0
        SendWnd             0          0             0x0
        KeepAlive           0          0             0x0
        GiveUp              0          0             0x0
        PmtuAger            0          0             0x0
        DeadWait            0          0             0x0
        Linger              0          0             0x0
        ProcessQ            0          0             0x0

        iss: 3028094276  snduna: 3028668745  sndnxt: 3028668745
        irs:  568735500  rcvnxt:  569257487

        sndwnd:  32711  scale:      0  maxrcvwnd:  16384
        rcvwnd:  16061  scale:      0  delrcvwnd:    323

        SRTT: 1000 ms, RTTO: 1003 ms, RTV: 3 ms, KRTT: 0 ms
        minRTT: 1 ms, maxRTT: 1000 ms, ACK hold: 200 ms
        uptime: 1648039160 ms, Sent idletime: 43001 ms, Receive idletime: 42793 ms
        Status Flags: passive open, gen tcbs
        Option Flags: VRF id set, nagle, path mtu capable
        IP Precedence value : 6

        Datagrams (max data segment is 1240 bytes):
        Rcvd: 57771 (out of order: 0), with data: 27469, total data bytes: 521986
        Sent: 57713 (retransmit: 4, fastretransmit: 0, partialack: 0, Second Congestion: 0), with data: 30230, total data bytes: 574468

        Packets received in fast path: 0, fast processed: 0, slow path: 0
        fast lock acquisition failures: 0, slow path: 0
        TCP Semaphore      0x7F23C7640468  FREE
    '''

    custom_output_2 = '''\
        show bgp vpnv4 unicast all
        BGP table version is 4, local router ID is 1.1.1.1
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
                    r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter,
                    x best-external, a additional-path, c RIB-compressed,
                    t secondary path, L long-lived-stale,
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

            Network          Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 65000:1 (default for vrf VRF1)
        *>   1.1.1.1/32       0.0.0.0                  0         32768 i
        r>i  2.2.2.2/32       2.2.2.2                  0    100      0 i
        r>i  3.3.3.3/32       3.3.3.3                       100      0 i
    '''

    custom_output_3 = '''\
        show bgp vpnv4 unicast all neighbors 2.2.2.2 advertised-routes
        BGP table version is 4, local router ID is 1.1.1.1
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
                    r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter,
                    x best-external, a additional-path, c RIB-compressed,
                    t secondary path, L long-lived-stale,
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

            Network          Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 65000:1 (default for vrf VRF1)
        *>   1.1.1.1/32       0.0.0.0                  0         32768 i

        Total number of prefixes 1
    '''

    custom_output_4 = '''\
        show bgp all neighbors | i BGP neighbor
        BGP neighbor is 2.2.2.2,  remote AS 65000, internal link
        BGP neighbor is 3.3.3.3,  remote AS 65000, internal link
        BGP neighbor is 2001:2:2:2::2,  remote AS 65000, internal link
        BGP neighbor is 2001:3:3:3::3,  remote AS 65000, internal link
        BGP neighbor is 2.2.2.2,  vrf VRF1,  remote AS 65000, internal link
        BGP neighbor is 3.3.3.3,  vrf VRF1,  remote AS 65000, internal link
        BGP neighbor is 2001:2:2:2::2,  vrf VRF1,  remote AS 65000, internal link
        BGP neighbor is 2001:3:3:3::3,  vrf VRF1,  remote AS 65000, internal link
    '''

    custom_output_5 = '''\
        show bgp vpnv4 unicast all neighbors 2.2.2.2 routes
        BGP table version is 4, local router ID is 1.1.1.1
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
                    r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter,
                    x best-external, a additional-path, c RIB-compressed,
                    t secondary path, L long-lived-stale,
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

            Network          Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 65000:1 (default for vrf VRF1)
        r>i  2.2.2.2/32       2.2.2.2                  0    100      0 i

        Total number of prefixes 1
    '''

    bgp_info = {
        'instance': {
            'default': {
                'bgp_id': 65000,
                'vrf': {
                    'VRF1': {
                        'cluster_id': '1.1.1.1',
                        'neighbor': {
                            '2.2.2.2': {
                                'bgp_negotiated_capabilities': {
                                    'enhanced_refresh': 'advertised',
                                    'four_octets_asn': 'advertised and received',
                                    'route_refresh': 'advertised and received(new)',
                                    'stateful_switchover': 'NO for session 1',
                                },
                                'bgp_negotiated_keepalive_timers': {
                                    'hold_time': 180,
                                    'keepalive_interval': 60,
                                },
                                'bgp_neighbor_counters': {
                                    'messages': {
                                        'received': {
                                            'keepalives': 27417,
                                            'notifications': 0,
                                            'opens': 1,
                                            'updates': 2,
                                        },
                                        'sent': {
                                            'keepalives': 30174,
                                            'notifications': 0,
                                            'opens': 1,
                                            'updates': 2,
                                        },
                                    },
                                },
                                'bgp_session_transport': {
                                    'connection': {
                                        'last_reset': 'never',
                                        'state': 'Established',
                                    },
                                    'transport': {
                                        'foreign_host': '2.2.2.2',
                                        'foreign_port': '50426',
                                        'local_host': '1.1.1.1',
                                        'local_port': '179',
                                        'mss': 1240,
                                    },
                                },
                                'bgp_version': 4,
                                'remote_as': 65000,
                                'session_state': 'Established',
                                'shutdown': False,
                            },
                            '2001:2:2:2::2': {
                                'bgp_negotiated_capabilities': {
                                    'enhanced_refresh': 'advertised',
                                    'four_octets_asn': 'advertised and received',
                                    'route_refresh': 'advertised and received(new)',
                                    'stateful_switchover': 'NO for session 1',
                                },
                                'bgp_negotiated_keepalive_timers': {
                                    'hold_time': 180,
                                    'keepalive_interval': 60,
                                },
                                'bgp_neighbor_counters': {
                                    'messages': {
                                        'received': {
                                            'keepalives': 27417,
                                            'notifications': 0,
                                            'opens': 1,
                                            'updates': 2,
                                        },
                                        'sent': {
                                            'keepalives': 30184,
                                            'notifications': 0,
                                            'opens': 1,
                                            'updates': 2,
                                        },
                                    },
                                },
                                'bgp_session_transport': {
                                    'connection': {
                                        'last_reset': 'never',
                                        'state': 'Established',
                                    },
                                    'transport': {
                                        'foreign_host': '2001:2:2:2::2',
                                        'foreign_port': '179',
                                        'local_host': '2001:1:1:1::1',
                                        'local_port': '32057',
                                        'mss': 1220,
                                    },
                                },
                                'bgp_version': 4,
                                'remote_as': 65000,
                                'session_state': 'Established',
                                'shutdown': False,
                            },
                            '2001:3:3:3::3': {
                                'bgp_negotiated_capabilities': {
                                    'enhanced_refresh': 'advertised',
                                    'four_octets_asn': 'advertised and received',
                                    'graceful_restart': 'received',
                                    'route_refresh': 'advertised and received(new)',
                                    'stateful_switchover': 'NO for session 1',
                                },
                                'bgp_negotiated_keepalive_timers': {
                                    'hold_time': 180,
                                    'keepalive_interval': 60,
                                },
                                'bgp_neighbor_counters': {
                                    'messages': {
                                        'received': {
                                            'keepalives': 27426,
                                            'notifications': 0,
                                            'opens': 1,
                                            'updates': 3,
                                        },
                                        'sent': {
                                            'keepalives': 30166,
                                            'notifications': 0,
                                            'opens': 1,
                                            'updates': 2,
                                        },
                                    },
                                },
                                'bgp_session_transport': {
                                    'connection': {
                                        'last_reset': 'never',
                                        'state': 'Established',
                                    },
                                    'transport': {
                                        'foreign_host': '2001:3:3:3::3',
                                        'foreign_port': '20838',
                                        'local_host': '2001:1:1:1::1',
                                        'local_port': '179',
                                        'mss': 1440,
                                    },
                                },
                                'bgp_version': 4,
                                'remote_as': 65000,
                                'session_state': 'Established',
                                'shutdown': False,
                            },
                            '3.3.3.3': {
                                'bgp_negotiated_capabilities': {
                                    'enhanced_refresh': 'advertised',
                                    'four_octets_asn': 'advertised and received',
                                    'graceful_restart': 'received',
                                    'route_refresh': 'advertised and received(new)',
                                    'stateful_switchover': 'NO for session 1',
                                },
                                'bgp_negotiated_keepalive_timers': {
                                    'hold_time': 180,
                                    'keepalive_interval': 60,
                                },
                                'bgp_neighbor_counters': {
                                    'messages': {
                                        'received': {
                                            'keepalives': 27427,
                                            'notifications': 0,
                                            'opens': 1,
                                            'updates': 3,
                                        },
                                        'sent': {
                                            'keepalives': 30185,
                                            'notifications': 0,
                                            'opens': 1,
                                            'updates': 2,
                                        },
                                    },
                                },
                                'bgp_session_transport': {
                                    'connection': {
                                        'last_reset': 'never',
                                        'state': 'Established',
                                    },
                                    'transport': {
                                        'foreign_host': '3.3.3.3',
                                        'foreign_port': '179',
                                        'local_host': '1.1.1.1',
                                        'local_port': '43893',
                                        'mss': 1460,
                                    },
                                },
                                'bgp_version': 4,
                                'remote_as': 65000,
                                'session_state': 'Established',
                                'shutdown': False,
                            },
                        },
                    },
                    'default': {
                        'cluster_id': '1.1.1.1',
                        'neighbor': {
                            '2.2.2.2': {
                                'address_family': {
                                    'ipv4 unicast': {
                                        'bgp_table_version': 4,
                                        'path': {
                                            'memory_usage': 408,
                                            'total_entries': 3,
                                        },
                                        'prefixes': {
                                            'memory_usage': 744,
                                            'total_entries': 3,
                                        },
                                        'routing_table_version': 4,
                                        'total_memory': 2492,
                                    },
                                    'vpnv4 unicast': {
                                        'bgp_table_version': 4,
                                        'path': {
                                            'memory_usage': 408,
                                            'total_entries': 3,
                                        },
                                        'prefixes': {
                                            'memory_usage': 768,
                                            'total_entries': 3,
                                        },
                                        'routing_table_version': 4,
                                        'total_memory': 2564,
                                    },
                                },
                                'bgp_negotiated_capabilities': {
                                    'enhanced_refresh': 'advertised',
                                    'four_octets_asn': 'advertised and received',
                                    'route_refresh': 'advertised and received(new)',
                                    'stateful_switchover': 'NO for session 1',
                                },
                                'bgp_negotiated_keepalive_timers': {
                                    'hold_time': 180,
                                    'keepalive_interval': 60,
                                },
                                'bgp_neighbor_counters': {
                                    'messages': {
                                        'received': {
                                            'keepalives': 27417,
                                            'notifications': 0,
                                            'opens': 1,
                                            'updates': 2,
                                        },
                                        'sent': {
                                            'keepalives': 30186,
                                            'notifications': 0,
                                            'opens': 1,
                                            'updates': 2,
                                        },
                                    },
                                },
                                'bgp_session_transport': {
                                    'connection': {
                                        'last_reset': 'never',
                                        'state': 'Established',
                                    },
                                    'transport': {
                                        'foreign_host': '2.2.2.2',
                                        'foreign_port': '25026',
                                        'local_host': '1.1.1.1',
                                        'local_port': '179',
                                        'mss': 1240,
                                    },
                                },
                                'bgp_version': 4,
                                'remote_as': 65000,
                                'session_state': 'Established',
                                'shutdown': False,
                            },
                            '2001:2:2:2::2': {
                                'address_family': {
                                    'ipv6 unicast': {
                                        'bgp_table_version': 5,
                                        'path': {
                                            'memory_usage': 456,
                                            'total_entries': 3,
                                        },
                                        'prefixes': {
                                            'memory_usage': 816,
                                            'total_entries': 3,
                                        },
                                        'routing_table_version': 5,
                                        'total_memory': 2612,
                                    },
                                    'vpnv6 unicast': {
                                        'bgp_table_version': 5,
                                        'path': {
                                            'memory_usage': 468,
                                            'total_entries': 3,
                                        },
                                        'prefixes': {
                                            'memory_usage': 840,
                                            'total_entries': 3,
                                        },
                                        'routing_table_version': 5,
                                        'total_memory': 2696,
                                    },
                                },
                                'bgp_negotiated_capabilities': {
                                    'enhanced_refresh': 'advertised',
                                    'four_octets_asn': 'advertised and received',
                                    'route_refresh': 'advertised and received(new)',
                                    'stateful_switchover': 'NO for session 1',
                                },
                                'bgp_negotiated_keepalive_timers': {
                                    'hold_time': 180,
                                    'keepalive_interval': 60,
                                },
                                'bgp_neighbor_counters': {
                                    'messages': {
                                        'received': {
                                            'keepalives': 27417,
                                            'notifications': 0,
                                            'opens': 1,
                                            'updates': 2,
                                        },
                                        'sent': {
                                            'keepalives': 30188,
                                            'notifications': 0,
                                            'opens': 1,
                                            'updates': 2,
                                        },
                                    },
                                },
                                'bgp_session_transport': {
                                    'connection': {
                                        'last_reset': 'never',
                                        'state': 'Established',
                                    },
                                    'transport': {
                                        'foreign_host': '2001:2:2:2::2',
                                        'foreign_port': '52223',
                                        'local_host': '2001:1:1:1::1',
                                        'local_port': '179',
                                        'mss': 1220,
                                    },
                                },
                                'bgp_version': 4,
                                'remote_as': 65000,
                                'session_state': 'Established',
                                'shutdown': False,
                            },
                            '2001:3:3:3::3': {
                                'address_family': {
                                    'ipv6 unicast': {
                                        'bgp_table_version': 5,
                                        'path': {
                                            'memory_usage': 456,
                                            'total_entries': 3,
                                        },
                                        'prefixes': {
                                            'memory_usage': 816,
                                            'total_entries': 3,
                                        },
                                        'routing_table_version': 5,
                                        'total_memory': 2612,
                                    },
                                    'vpnv6 unicast': {
                                        'bgp_table_version': 5,
                                        'path': {
                                            'memory_usage': 468,
                                            'total_entries': 3,
                                        },
                                        'prefixes': {
                                            'memory_usage': 840,
                                            'total_entries': 3,
                                        },
                                        'routing_table_version': 5,
                                        'total_memory': 2696,
                                    },
                                },
                                'bgp_negotiated_capabilities': {
                                    'enhanced_refresh': 'advertised',
                                    'four_octets_asn': 'advertised and received',
                                    'graceful_restart': 'received',
                                    'route_refresh': 'advertised and received(new)',
                                    'stateful_switchover': 'NO for session 1',
                                },
                                'bgp_negotiated_keepalive_timers': {
                                    'hold_time': 180,
                                    'keepalive_interval': 60,
                                },
                                'bgp_neighbor_counters': {
                                    'messages': {
                                        'received': {
                                            'keepalives': 27427,
                                            'notifications': 0,
                                            'opens': 1,
                                            'updates': 2,
                                        },
                                        'sent': {
                                            'keepalives': 30178,
                                            'notifications': 0,
                                            'opens': 1,
                                            'updates': 2,
                                        },
                                    },
                                },
                                'bgp_session_transport': {
                                    'connection': {
                                        'last_reset': 'never',
                                        'state': 'Established',
                                    },
                                    'transport': {
                                        'foreign_host': '2001:3:3:3::3',
                                        'foreign_port': '47133',
                                        'local_host': '2001:1:1:1::1',
                                        'local_port': '179',
                                        'mss': 1440,
                                    },
                                },
                                'bgp_version': 4,
                                'remote_as': 65000,
                                'session_state': 'Established',
                                'shutdown': False,
                            },
                            '3.3.3.3': {
                                'address_family': {
                                    'ipv4 unicast': {
                                        'bgp_table_version': 4,
                                        'path': {
                                            'memory_usage': 408,
                                            'total_entries': 3,
                                        },
                                        'prefixes': {
                                            'memory_usage': 744,
                                            'total_entries': 3,
                                        },
                                        'routing_table_version': 4,
                                        'total_memory': 2492,
                                    },
                                    'vpnv4 unicast': {
                                        'bgp_table_version': 4,
                                        'path': {
                                            'memory_usage': 408,
                                            'total_entries': 3,
                                        },
                                        'prefixes': {
                                            'memory_usage': 768,
                                            'total_entries': 3,
                                        },
                                        'routing_table_version': 4,
                                        'total_memory': 2564,
                                    },
                                },
                                'bgp_negotiated_capabilities': {
                                    'enhanced_refresh': 'advertised',
                                    'four_octets_asn': 'advertised and received',
                                    'graceful_restart': 'received',
                                    'route_refresh': 'advertised and received(new)',
                                    'stateful_switchover': 'NO for session 1',
                                },
                                'bgp_negotiated_keepalive_timers': {
                                    'hold_time': 180,
                                    'keepalive_interval': 60,
                                },
                                'bgp_neighbor_counters': {
                                    'messages': {
                                        'received': {
                                            'keepalives': 27427,
                                            'notifications': 0,
                                            'opens': 1,
                                            'updates': 2,
                                        },
                                        'sent': {
                                            'keepalives': 30162,
                                            'notifications': 0,
                                            'opens': 1,
                                            'updates': 2,
                                        },
                                    },
                                },
                                'bgp_session_transport': {
                                    'connection': {
                                        'last_reset': 'never',
                                        'state': 'Established',
                                    },
                                    'transport': {
                                        'foreign_host': '3.3.3.3',
                                        'foreign_port': '179',
                                        'local_host': '1.1.1.1',
                                        'local_port': '11084',
                                        'mss': 1460,
                                    },
                                },
                                'bgp_version': 4,
                                'remote_as': 65000,
                                'session_state': 'Established',
                                'shutdown': False,
                            },
                        },
                    },
                },
            },
        },
    }

    bgp_table = {
        'instance': {
            'default': {
                'vrf': {
                    'VRF1': {
                        'address_family': {
                            'vpnv4 unicast RD 65000:1': {
                                'bgp_table_version': 4,
                                'default_vrf': 'VRF1',
                                'prefixes': {
                                    '1.1.1.1/32': {
                                        'index': {
                                            1: {
                                                'gateway': '0.0.0.0',
                                                'localpref': 100,
                                                'metric': 0,
                                                'next_hop': '0.0.0.0',
                                                'origin_codes': 'i',
                                                'originator': '1.1.1.1',
                                                'status_codes': '*>',
                                                'update_group': 1,
                                                'weight': '32768',
                                            },
                                        },
                                        'paths': '1 available, best #1, table VRF1',
                                        'table_version': '2',
                                    },
                                    '2.2.2.2/32': {
                                        'index': {
                                            1: {
                                                'gateway': '2.2.2.2',
                                                'localpref': 100,
                                                'metric': 0,
                                                'next_hop': '2.2.2.2',
                                                'next_hop_igp_metric': '10752',
                                                'origin_codes': 'i',
                                                'originator': '2.2.2.2',
                                                'status_codes': '*>',
                                            },
                                        },
                                        'paths': '1 available, best #1, table VRF1, RIB-failure(17)',
                                        'table_version': '4',
                                    },
                                    '3.3.3.3/32': {
                                        'index': {
                                            1: {
                                                'gateway': '3.3.3.3',
                                                'localpref': 100,
                                                'next_hop': '3.3.3.3',
                                                'next_hop_igp_metric': '2570240',
                                                'origin_codes': 'i',
                                                'originator': '3.3.3.3',
                                                'status_codes': '*>',
                                            },
                                        },
                                        'paths': '1 available, best #1, table VRF1, RIB-failure(17)',
                                        'table_version': '3',
                                    },
                                },
                                'route_distinguisher': '65000:1',
                                'route_identifier': '1.1.1.1',
                            },
                            'vpnv6 unicast RD 65000:1': {
                                'bgp_table_version': 5,
                                'default_vrf': 'VRF1',
                                'prefixes': {
                                    '2001:1:1:1::1/128': {
                                        'index': {
                                            1: {
                                                'gateway': '0.0.0.0',
                                                'localpref': 100,
                                                'metric': 0,
                                                'next_hop': '::',
                                                'origin_codes': 'i',
                                                'originator': '1.1.1.1',
                                                'status_codes': '*>',
                                                'update_group': 1,
                                                'weight': '32768',
                                            },
                                        },
                                        'paths': '1 available, best #1, table VRF1',
                                        'table_version': '3',
                                    },
                                    '2001:2:2:2::2/128': {
                                        'index': {
                                            1: {
                                                'gateway': '2001:2:2:2::2',
                                                'localpref': 100,
                                                'metric': 0,
                                                'next_hop': '2001:2:2:2::2',
                                                'next_hop_igp_metric': '10752',
                                                'origin_codes': 'i',
                                                'originator': '2.2.2.2',
                                                'status_codes': '*>',
                                            },
                                        },
                                        'paths': '1 available, best #1, table VRF1, RIB-failure(145)',
                                        'table_version': '5',
                                    },
                                    '2001:3:3:3::3/128': {
                                        'index': {
                                            1: {
                                                'gateway': '2001:3:3:3::3',
                                                'localpref': 100,
                                                'next_hop': '2001:3:3:3::3',
                                                'next_hop_igp_metric': '2570240',
                                                'origin_codes': 'i',
                                                'originator': '3.3.3.3',
                                                'status_codes': '*>',
                                            },
                                        },
                                        'paths': '1 available, best #1, table VRF1, RIB-failure(145)',
                                        'table_version': '4',
                                    },
                                },
                                'route_distinguisher': '65000:1',
                                'route_identifier': '1.1.1.1',
                            },
                        },
                    },
                    'default': {
                        'address_family': {
                            'ipv4 unicast': {
                                'prefixes': {
                                    '1.1.1.1/32': {
                                        'index': {
                                            1: {
                                                'gateway': '0.0.0.0',
                                                'localpref': 100,
                                                'metric': 0,
                                                'next_hop': '0.0.0.0',
                                                'origin_codes': 'i',
                                                'originator': '1.1.1.1',
                                                'status_codes': '*>',
                                                'update_group': 1,
                                                'weight': '32768',
                                            },
                                        },
                                        'paths': '1 available, best #1, table default',
                                        'table_version': '2',
                                    },
                                    '2.2.2.2/32': {
                                        'index': {
                                            1: {
                                                'gateway': '2.2.2.2',
                                                'localpref': 100,
                                                'metric': 0,
                                                'next_hop': '2.2.2.2',
                                                'next_hop_igp_metric': '10752',
                                                'origin_codes': 'i',
                                                'originator': '2.2.2.2',
                                                'status_codes': '*>',
                                            },
                                        },
                                        'paths': '1 available, best #1, table default, RIB-failure(17)',
                                        'table_version': '4',
                                    },
                                    '3.3.3.3/32': {
                                        'index': {
                                            1: {
                                                'gateway': '3.3.3.3',
                                                'localpref': 100,
                                                'next_hop': '3.3.3.3',
                                                'next_hop_igp_metric': '2570240',
                                                'origin_codes': 'i',
                                                'originator': '3.3.3.3',
                                                'status_codes': '*>',
                                            },
                                        },
                                        'paths': '1 available, best #1, table default, RIB-failure(17)',
                                        'table_version': '3',
                                    },
                                },
                            },
                            'ipv6 unicast': {
                                'prefixes': {
                                    '2001:1:1:1::1/128': {
                                        'index': {
                                            1: {
                                                'gateway': '0.0.0.0',
                                                'localpref': 100,
                                                'metric': 0,
                                                'next_hop': '::',
                                                'origin_codes': 'i',
                                                'originator': '1.1.1.1',
                                                'status_codes': '*>',
                                                'update_group': 1,
                                                'weight': '32768',
                                            },
                                        },
                                        'paths': '1 available, best #1, table default',
                                        'table_version': '3',
                                    },
                                    '2001:2:2:2::2/128': {
                                        'index': {
                                            1: {
                                                'gateway': '2001:2:2:2::2',
                                                'localpref': 100,
                                                'metric': 0,
                                                'next_hop': '2001:2:2:2::2',
                                                'next_hop_igp_metric': '10752',
                                                'origin_codes': 'i',
                                                'originator': '2.2.2.2',
                                                'status_codes': '*>',
                                            },
                                        },
                                        'paths': '1 available, best #1, table default, RIB-failure(145)',
                                        'table_version': '5',
                                    },
                                    '2001:3:3:3::3/128': {
                                        'index': {
                                            1: {
                                                'gateway': '2001:3:3:3::3',
                                                'localpref': 100,
                                                'next_hop': '2001:3:3:3::3',
                                                'next_hop_igp_metric': '2570240',
                                                'origin_codes': 'i',
                                                'originator': '3.3.3.3',
                                                'status_codes': '*>',
                                            },
                                        },
                                        'paths': '1 available, best #1, table default, RIB-failure(145)',
                                        'table_version': '4',
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    bgp_routes_per_peer = {
        'instance': {
            'default': {
                'vrf': {
                    'VRF1': {
                        'neighbor': {
                            '2.2.2.2': {
                                'address_family': {
                                    'ipv4 unicast': {
                                        'advertised': {
                                            '1.1.1.1/32': {
                                                'index': {
                                                    1: {
                                                        'localprf': 0,
                                                        'next_hop': '0.0.0.0',
                                                        'origin_codes': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 32768,
                                                    },
                                                },
                                            },
                                        },
                                        'routes': {
                                            '2.2.2.2/32': {
                                                'index': {
                                                    1: {
                                                        'localprf': 100,
                                                        'metric': 0,
                                                        'next_hop': '2.2.2.2',
                                                        'origin_codes': 'i',
                                                        'status_codes': 'r>',
                                                        'weight': 0,
                                                    },
                                                },
                                            },
                                        },
                                    },
                                    'vpnv4 unicast': {
                                        'advertised': {
                                        },
                                        'routes': {
                                        },
                                    },
                                    'vpnv4 unicast RD 65000:1': {
                                        'advertised': {
                                            '1.1.1.1/32': {
                                                'index': {
                                                    1: {
                                                        'localprf': 0,
                                                        'next_hop': '0.0.0.0',
                                                        'origin_codes': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 32768,
                                                    },
                                                },
                                            },
                                        },
                                        'default_vrf': 'VRF1',
                                        'route_distinguisher': '65000:1',
                                        'routes': {
                                            '2.2.2.2/32': {
                                                'index': {
                                                    1: {
                                                        'localprf': 100,
                                                        'metric': 0,
                                                        'next_hop': '2.2.2.2',
                                                        'origin_codes': 'i',
                                                        'status_codes': 'r>',
                                                        'weight': 0,
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                'remote_as': 65000,
                            },
                            '2001:2:2:2::2': {
                                'address_family': {
                                    'ipv4 unicast': {
                                        'advertised': {
                                            '1.1.1.1/32': {
                                                'index': {
                                                    1: {
                                                        'localprf': 0,
                                                        'next_hop': '0.0.0.0',
                                                        'origin_codes': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 32768,
                                                    },
                                                },
                                            },
                                        },
                                    },
                                    'ipv6 unicast': {
                                        'routes': {
                                            '2001:2:2:2::2/128': {
                                                'index': {
                                                    1: {
                                                        'localprf': 100,
                                                        'metric': 0,
                                                        'next_hop': '2001:2:2:2::2',
                                                        'origin_codes': 'i',
                                                        'status_codes': 'r>',
                                                        'weight': 0,
                                                    },
                                                },
                                            },
                                        },
                                    },
                                    'vpnv4 unicast': {
                                        'advertised': {
                                        },
                                    },
                                    'vpnv4 unicast RD 65000:1': {
                                        'advertised': {
                                            '1.1.1.1/32': {
                                                'index': {
                                                    1: {
                                                        'localprf': 0,
                                                        'next_hop': '0.0.0.0',
                                                        'origin_codes': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 32768,
                                                    },
                                                },
                                            },
                                        },
                                        'default_vrf': 'VRF1',
                                        'route_distinguisher': '65000:1',
                                    },
                                    'vpnv6 unicast': {
                                        'routes': {
                                        },
                                    },
                                    'vpnv6 unicast RD 65000:1': {
                                        'routes': {
                                            '2001:2:2:2::2/128': {
                                                'index': {
                                                    1: {
                                                        'localprf': 100,
                                                        'metric': 0,
                                                        'next_hop': '2001:2:2:2::2',
                                                        'origin_codes': 'i',
                                                        'status_codes': 'r>',
                                                        'weight': 0,
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                'remote_as': 65000,
                            },
                            '2001:3:3:3::3': {
                                'address_family': {
                                    'ipv4 unicast': {
                                        'advertised': {
                                            '1.1.1.1/32': {
                                                'index': {
                                                    1: {
                                                        'localprf': 0,
                                                        'next_hop': '0.0.0.0',
                                                        'origin_codes': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 32768,
                                                    },
                                                },
                                            },
                                        },
                                    },
                                    'ipv6 unicast': {
                                        'routes': {
                                            '2001:3:3:3::3/128': {
                                                'index': {
                                                    1: {
                                                        'localprf': 100,
                                                        'next_hop': '2001:3:3:3::3',
                                                        'origin_codes': 'i',
                                                        'status_codes': 'r>',
                                                        'weight': 0,
                                                    },
                                                },
                                            },
                                        },
                                    },
                                    'vpnv4 unicast': {
                                        'advertised': {
                                        },
                                    },
                                    'vpnv4 unicast RD 65000:1': {
                                        'advertised': {
                                            '1.1.1.1/32': {
                                                'index': {
                                                    1: {
                                                        'localprf': 0,
                                                        'next_hop': '0.0.0.0',
                                                        'origin_codes': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 32768,
                                                    },
                                                },
                                            },
                                        },
                                        'default_vrf': 'VRF1',
                                        'route_distinguisher': '65000:1',
                                    },
                                    'vpnv6 unicast': {
                                        'routes': {
                                        },
                                    },
                                    'vpnv6 unicast RD 65000:1': {
                                        'routes': {
                                            '2001:3:3:3::3/128': {
                                                'index': {
                                                    1: {
                                                        'localprf': 100,
                                                        'next_hop': '2001:3:3:3::3',
                                                        'origin_codes': 'i',
                                                        'status_codes': 'r>',
                                                        'weight': 0,
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                'remote_as': 65000,
                            },
                            '3.3.3.3': {
                                'address_family': {
                                    'ipv4 unicast': {
                                        'advertised': {
                                            '1.1.1.1/32': {
                                                'index': {
                                                    1: {
                                                        'localprf': 0,
                                                        'next_hop': '0.0.0.0',
                                                        'origin_codes': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 32768,
                                                    },
                                                },
                                            },
                                        },
                                        'routes': {
                                            '3.3.3.3/32': {
                                                'index': {
                                                    1: {
                                                        'localprf': 100,
                                                        'next_hop': '3.3.3.3',
                                                        'origin_codes': 'i',
                                                        'status_codes': 'r>',
                                                        'weight': 0,
                                                    },
                                                },
                                            },
                                        },
                                    },
                                    'vpnv4 unicast': {
                                        'advertised': {
                                        },
                                        'routes': {
                                        },
                                    },
                                    'vpnv4 unicast RD 65000:1': {
                                        'advertised': {
                                            '1.1.1.1/32': {
                                                'index': {
                                                    1: {
                                                        'localprf': 0,
                                                        'next_hop': '0.0.0.0',
                                                        'origin_codes': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 32768,
                                                    },
                                                },
                                            },
                                        },
                                        'default_vrf': 'VRF1',
                                        'route_distinguisher': '65000:1',
                                        'routes': {
                                            '3.3.3.3/32': {
                                                'index': {
                                                    1: {
                                                        'localprf': 100,
                                                        'next_hop': '3.3.3.3',
                                                        'origin_codes': 'i',
                                                        'status_codes': 'r>',
                                                        'weight': 0,
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                'remote_as': 65000,
                            },
                        },
                    },
                    'default': {
                        'neighbor': {
                            '2.2.2.2': {
                                'address_family': {
                                    'ipv4 unicast': {
                                        'input_queue': 0,
                                        'msg_rcvd': 27420,
                                        'msg_sent': 30189,
                                        'output_queue': 0,
                                        'state_pfxrcd': '1',
                                        'tbl_ver': 4,
                                        'up_down': '2w5d',
                                    },
                                    'vpnv4 unicast': {
                                        'input_queue': 0,
                                        'msg_rcvd': 27420,
                                        'msg_sent': 30177,
                                        'output_queue': 0,
                                        'state_pfxrcd': '1',
                                        'tbl_ver': 4,
                                        'up_down': '2w5d',
                                    },
                                },
                                'remote_as': 65000,
                            },
                            '2001:2:2:2::2': {
                                'address_family': {
                                    'ipv6 unicast': {
                                        'input_queue': 0,
                                        'msg_rcvd': 27420,
                                        'msg_sent': 30190,
                                        'output_queue': 0,
                                        'state_pfxrcd': '1',
                                        'tbl_ver': 5,
                                        'up_down': '2w5d',
                                    },
                                    'vpnv6 unicast': {
                                        'input_queue': 0,
                                        'msg_rcvd': 27420,
                                        'msg_sent': 30187,
                                        'output_queue': 0,
                                        'state_pfxrcd': '1',
                                        'tbl_ver': 5,
                                        'up_down': '2w5d',
                                    },
                                },
                                'remote_as': 65000,
                            },
                            '2001:3:3:3::3': {
                                'address_family': {
                                    'ipv6 unicast': {
                                        'input_queue': 0,
                                        'msg_rcvd': 27430,
                                        'msg_sent': 30181,
                                        'output_queue': 0,
                                        'state_pfxrcd': '1',
                                        'tbl_ver': 5,
                                        'up_down': '2w5d',
                                    },
                                    'vpnv6 unicast': {
                                        'input_queue': 0,
                                        'msg_rcvd': 27430,
                                        'msg_sent': 30169,
                                        'output_queue': 0,
                                        'state_pfxrcd': '1',
                                        'tbl_ver': 5,
                                        'up_down': '2w5d',
                                    },
                                },
                                'remote_as': 65000,
                            },
                            '3.3.3.3': {
                                'address_family': {
                                    'ipv4 unicast': {
                                        'input_queue': 0,
                                        'msg_rcvd': 27430,
                                        'msg_sent': 30165,
                                        'output_queue': 0,
                                        'state_pfxrcd': '1',
                                        'tbl_ver': 4,
                                        'up_down': '2w5d',
                                    },
                                    'vpnv4 unicast': {
                                        'input_queue': 0,
                                        'msg_rcvd': 27431,
                                        'msg_sent': 30188,
                                        'output_queue': 0,
                                        'state_pfxrcd': '1',
                                        'tbl_ver': 4,
                                        'up_down': '2w5d',
                                    },
                                },
                                'remote_as': 65000,
                            },
                        },
                    },
                },
            },
        },
    }

    bgp_info_custom = {
        'instance': {
            'default': {
                'bgp_id': 65000,
                'vrf': {
                    'default': {
                        'cluster_id': '1.1.1.1',
                        'neighbor': {
                            '2.2.2.2': {
                                'address_family': {
                                    'ipv4 unicast': {
                                        'bgp_table_version': 4,
                                        'path': {
                                            'memory_usage': 408,
                                            'total_entries': 3,
                                        },
                                        'prefixes': {
                                            'memory_usage': 744,
                                            'total_entries': 3,
                                        },
                                        'routing_table_version': 4,
                                        'total_memory': 2492,
                                    },
                                    'vpnv4 unicast': {
                                        'bgp_table_version': 4,
                                        'path': {
                                            'memory_usage': 408,
                                            'total_entries': 3,
                                        },
                                        'prefixes': {
                                            'memory_usage': 768,
                                            'total_entries': 3,
                                        },
                                        'routing_table_version': 4,
                                        'total_memory': 2564,
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    bgp_routes_per_peer_custom = {
        'instance': {
            'default': {
                'vrf': {
                    'default': {
                        'neighbor': {
                            '2.2.2.2': {
                                'address_family': {
                                    'vpnv4 unicast': {
                                        'input_queue': 0,
                                        'msg_rcvd': 27420,
                                        'msg_sent': 30177,
                                        'output_queue': 0,
                                        'state_pfxrcd': '1',
                                        'tbl_ver': 4,
                                        'up_down': '2w5d',
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }
