''' 
Lisp Genie Ops Object Outputs for IOS
'''


class LispOutput(object):

    ############################################################################
    #                           LISP INFO OUTPUTS
    ############################################################################

    # --------------------------------------------------------------------------
    # 'show lisp all service <service> summary'
    # --------------------------------------------------------------------------

    # 'show lisp all service ipv4 summary'
    ShowLispServiceIpv4Summary = '''\
        202-XTR#show lisp all service ipv4 summary 

        =====================================================
        Output for router lisp 0
        =====================================================
        Router-lisp ID:   0
        Instance count:   2
        Key: DB - Local EID Database entry count (@ - RLOC check pending
                                                  * - RLOC consistency problem),
             DB no route - Local EID DB entries with no matching RIB route,
             Cache - Remote EID mapping cache size, IID - Instance ID,
             Role - Configured Role

                              Interface    DB  DB no  Cache Incom Cache 
        EID VRF name             (.IID)  size  route   size plete  Idle Role
        red                   LISP0.101     1      0      2  0.0%  0.0% ITR-ETR

        Number of eid-tables:                                 2
        Total number of database entries:                     2 (inactive 0)
        EID-tables with inconsistent locators:                0
        Total number of map-cache entries:                    3
        EID-tables with incomplete map-cache entries:         0
        EID-tables pending map-cache update to FIB:           0
        '''

    # 'show lisp all service ipv6 summary'
    ShowLispServiceIpv6Summary = '''\
        202-XTR#show lisp all service ipv6 summary 
        =====================================================
        Output for router lisp 0
        =====================================================
        Router-lisp ID:   0
        Instance count:   2
        Key: DB - Local EID Database entry count (@ - RLOC check pending
                                                  * - RLOC consistency problem),
             DB no route - Local EID DB entries with no matching RIB route,
             Cache - Remote EID mapping cache size, IID - Instance ID,
             Role - Configured Role

                              Interface    DB  DB no  Cache Incom Cache 
        EID VRF name             (.IID)  size  route   size plete  Idle Role
        red                   LISP0.101     1      0      2  0.0%  0.0% ITR-ETR

        Number of eid-tables:                                 1
        Total number of database entries:                     1 (inactive 0)
        EID-tables with inconsistent locators:                0
        Total number of map-cache entries:                    2
        EID-tables with incomplete map-cache entries:         0
        EID-tables pending map-cache update to FIB:           0
        '''

    # 'show lisp all service ethernet summary'
    ShowLispServiceEthernetSummary = '''
        202-XTR#show lisp all service ethernet summary
        =================================================
        Output for router lisp 0
        =================================================
        Router-lisp ID:   0
        Instance count:   69
        Key: DB - Local EID Database entry count (@ - RLOC check pending
                                                  * - RLOC consistency problem),
             DB no route - Local EID DB entries with no matching RIB route,
             Cache - Remote EID mapping cache size, IID - Instance ID,
             Role - Configured Role

                              Interface    DB  DB no  Cache Incom Cache
        EID VRF name             (.IID)  size  route   size plete  Idle Role
                              LISP0.101     2      0      4  0.0%  100% NONE

        Number of eid-tables:                                 2
        Total number of database entries:                     4 (inactive 0)
        Maximum database entries:                          5120
        EID-tables with inconsistent locators:                0
        Total number of map-cache entries:                    4
        Maximum map-cache entries:                         5120
        EID-tables with incomplete map-cache entries:         0
        EID-tables pending map-cache update to FIB:           0
        '''

    # --------------------------------------------------------------------------
    # 'show lisp all service <service>'
    # --------------------------------------------------------------------------

    # 'show lisp all service ipv4'
    ShowLispServiceIpv4 = '''\
        202-XTR#show lisp all service ipv4
        =================================================
        Output for router lisp 0
        =================================================
          Router-lisp ID:                      0
          Locator table:                       default
          Ingress Tunnel Router (ITR):         enabled
          Egress Tunnel Router (ETR):          enabled
          Proxy-ITR Router (PITR):             enabled RLOCs: 10.10.10.10
          Proxy-ETR Router (PETR):             disabled
          NAT-traversal Router (NAT-RTR):      disabled
          Mobility First-Hop Router:           disabled
          Map Server (MS):                     disabled
          Map Resolver (MR):                   disabled
          Delegated Database Tree (DDT):       disabled
          ITR Map-Resolver(s):                 10.64.4.4, 10.166.13.13
          ETR Map-Server(s):                   10.64.4.4, 10.166.13.13
          xTR-ID:                              0x730E0861-0x12996F6D-0xEFEA2114-0xE1C951F7
          site-ID:                             unspecified
          ITR local RLOC (last resort):        *** NOT FOUND ***
          ITR Solicit Map Request (SMR):       accept and process
            Max SMRs per map-cache entry:      8 more specifics
            Multiple SMR suppression time:     20 secs
          ETR accept mapping data:             disabled, verify disabled
          ETR map-cache TTL:                   1d00h
          Locator Status Algorithms:
            RLOC-probe algorithm:              disabled
            RLOC-probe on route change:        N/A (periodic probing disabled)
            RLOC-probe on member change:       disabled
            LSB reports:                       process
            IPv4 RLOC minimum mask length:     /0
            IPv6 RLOC minimum mask length:     /0
          Map-cache:                           
            Map-cache limit:                   1000
            Map-cache activity check period:   60 secs
            Persistent map-cache:              disabled
          Database:                            
            Dynamic database mapping limit:    1000
        '''

    # 'show lisp all service ipv6'
    ShowLispServiceIpv6 = '''\
        202-XTR#show lisp all service ipv6
        =================================================
        Output for router lisp 0
        =================================================
          Router-lisp ID:                      0
          Locator table:                       default
          Ingress Tunnel Router (ITR):         enabled
          Egress Tunnel Router (ETR):          enabled
          Proxy-ITR Router (PITR):             disabled
          Proxy-ETR Router (PETR):             disabled
          NAT-traversal Router (NAT-RTR):      disabled
          Mobility First-Hop Router:           disabled
          Map Server (MS):                     disabled
          Map Resolver (MR):                   disabled
          Delegated Database Tree (DDT):       disabled
          ITR Map-Resolver(s):                 10.64.4.4, 10.166.13.13
          ETR Map-Server(s):                   10.64.4.4, 10.166.13.13
          xTR-ID:                              0x730E0861-0x12996F6D-0xEFEA2114-0xE1C951F7
          site-ID:                             unspecified
          ITR local RLOC (last resort):        *** NOT FOUND ***
          ITR Solicit Map Request (SMR):       accept and process
            Max SMRs per map-cache entry:      8 more specifics
            Multiple SMR suppression time:     20 secs
          ETR accept mapping data:             disabled, verify disabled
          ETR map-cache TTL:                   1d00h
          Locator Status Algorithms:
            RLOC-probe algorithm:              disabled
            RLOC-probe on route change:        N/A (periodic probing disabled)
            RLOC-probe on member change:       disabled
            LSB reports:                       process
            IPv4 RLOC minimum mask length:     /0
            IPv6 RLOC minimum mask length:     /0
          Map-cache:                           
            Map-cache limit:                   1000
            Map-cache activity check period:   60 secs
            Persistent map-cache:              disabled
          Database:                            
            Dynamic database mapping limit:    1000
        '''

    # 'show lisp all service ethernet'
    ShowLispServiceEthernet = '''\
        OTT-LISP-C3K-3-xTR1#show lisp all service ethernet

        =================================================
        Output for router lisp 0
        =================================================
          Router-lisp ID:                      0
          Locator table:                       default
          Ingress Tunnel Router (ITR):         enabled
          Egress Tunnel Router (ETR):          enabled
          Proxy-ITR Router (PITR):             disabled
          Proxy-ETR Router (PETR):             disabled
          NAT-traversal Router (NAT-RTR):      disabled
          Mobility First-Hop Router:           disabled
          Map Server (MS):                     disabled
          Map Resolver (MR):                   disabled
          Mr-use-petr:                         disabled
          Delegated Database Tree (DDT):       disabled
          ITR Map-Resolver(s):                 10.94.44.44
                                               10.84.66.66
          ETR Map-Server(s):                   10.94.44.44
                                               10.84.66.66
          xTR-ID:                              0x730E0861-0x12996F6D-0xEFEA2114-0xE1C951F7
          site-ID:                             unspecified
          ITR local RLOC (last resort):        *** NOT FOUND ***
          ITR Solicit Map Request (SMR):       accept and process
            Max SMRs per map-cache entry:      8 more specifics
            Multiple SMR suppression time:     20 secs
          ETR accept mapping data:             disabled, verify disabled
          ETR map-cache TTL:                   1d00h
          Locator Status Algorithms:
            RLOC-probe algorithm:              disabled
            RLOC-probe on route change:        N/A (periodic probing disabled)
            RLOC-probe on member change:       disabled
            LSB reports:                       process
            IPv4 RLOC minimum mask length:     /0
            IPv6 RLOC minimum mask length:     /0
          Map-cache:
            Map-cache limit:                   5120
            Map-cache activity check period:   60 secs
            Persistent map-cache:              disabled
          Source locator configuration:
            Vlan100: 10.229.11.1 (Loopback0)
            Vlan101: 10.229.11.1 (Loopback0)
          Database:
            Dynamic database mapping limit:    5120
        '''

    # --------------------------------------------------------------------------
    # 'show lisp all instance-id <instance_id> <service>'
    # --------------------------------------------------------------------------

    # 'show lisp all instance-id 101 service ipv4'
    ShowLispInstance101ServiceIpv4 = '''
        202-XTR#show lisp all instance-id 101 ipv4

        =================================================
        Output for router lisp 0
        =================================================
          Instance ID:                         101
          Router-lisp ID:                      0
          Locator table:                       default
          EID table:                           vrf red
          Ingress Tunnel Router (ITR):         enabled
          Egress Tunnel Router (ETR):          enabled
          Proxy-ITR Router (PITR):             enabled RLOCs: 10.10.10.10
          Proxy-ETR Router (PETR):             disabled
          NAT-traversal Router (NAT-RTR):      disabled
          Mobility First-Hop Router:           disabled
          Map Server (MS):                     disabled
          Map Resolver (MR):                   disabled
          Delegated Database Tree (DDT):       disabled
          Site Registration Limit:             0
          Map-Request source:                  derived from EID destination
          ITR Map-Resolver(s):                 10.64.4.4, 10.166.13.13
          ETR Map-Server(s):                   10.64.4.4 (17:49:58), 10.166.13.13 (00:00:35)
          xTR-ID:                              0x730E0861-0x12996F6D-0xEFEA2114-0xE1C951F7
          site-ID:                             unspecified
          ITR local RLOC (last resort):        10.16.2.2
          ITR use proxy ETR RLOC(s):           10.10.10.10
          ITR Solicit Map Request (SMR):       accept and process
            Max SMRs per map-cache entry:      8 more specifics
            Multiple SMR suppression time:     20 secs
          ETR accept mapping data:             disabled, verify disabled
          ETR map-cache TTL:                   1d00h
          Locator Status Algorithms:
            RLOC-probe algorithm:              disabled
            RLOC-probe on route change:        N/A (periodic probing disabled)
            RLOC-probe on member change:       disabled
            LSB reports:                       process
            IPv4 RLOC minimum mask length:     /0
            IPv6 RLOC minimum mask length:     /0
          Map-cache:                           
            Static mappings configured:        0
            Map-cache size/limit:              2/1000
            Imported route count/limit:        0/1000
            Map-cache activity check period:   60 secs
            Map-cache FIB updates:             established
            Persistent map-cache:              disabled
          Database:                            
            Total database mapping size:       1
            static database size/limit:        1/65535
            dynamic database size/limit:       0/65535
            route-import database size/limit:  0/1000
            Inactive (deconfig/away) size:     0
          Encapsulation type:                  lisp
        '''

    # 'show lisp all instance-id 101 service ipv6'
    ShowLispInstance101ServiceIpv6 = '''\
        202-XTR#show lisp all instance-id 101 ipv6

        =================================================
        Output for router lisp 0
        =================================================
          Instance ID:                         101
          Router-lisp ID:                      0
          Locator table:                       default
          EID table:                           vrf red
          Ingress Tunnel Router (ITR):         enabled
          Egress Tunnel Router (ETR):          enabled
          Proxy-ITR Router (PITR):             disabled
          Proxy-ETR Router (PETR):             disabled
          NAT-traversal Router (NAT-RTR):      disabled
          Mobility First-Hop Router:           disabled
          Map Server (MS):                     disabled
          Map Resolver (MR):                   disabled
          Delegated Database Tree (DDT):       disabled
          Site Registration Limit:             0
          Map-Request source:                  derived from EID destination
          ITR Map-Resolver(s):                 10.100.5.5, 10.66.12.12
          ETR Map-Server(s):                   10.100.5.5 (17:49:58), 10.66.12.12 (00:00:35)
          xTR-ID:                              0x730E0861-0x12996F6D-0xEFEA2114-0xE1C951F7
          site-ID:                             unspecified
          ITR local RLOC (last resort):        10.16.2.2
          ITR use proxy ETR RLOC(s):           10.10.10.10
          ITR Solicit Map Request (SMR):       accept and process
            Max SMRs per map-cache entry:      8 more specifics
            Multiple SMR suppression time:     20 secs
          ETR accept mapping data:             disabled, verify disabled
          ETR map-cache TTL:                   1d00h
          Locator Status Algorithms:
            RLOC-probe algorithm:              disabled
            RLOC-probe on route change:        N/A (periodic probing disabled)
            RLOC-probe on member change:       disabled
            LSB reports:                       process
            IPv4 RLOC minimum mask length:     /0
            IPv6 RLOC minimum mask length:     /0
          Map-cache:                           
            Static mappings configured:        0
            Map-cache size/limit:              2/1000
            Imported route count/limit:        0/1000
            Map-cache activity check period:   60 secs
            Map-cache FIB updates:             established
            Persistent map-cache:              disabled
          Database:                            
            Total database mapping size:       1
            static database size/limit:        1/65535
            dynamic database size/limit:       0/65535
            route-import database size/limit:  0/1000
            Inactive (deconfig/away) size:     0
          Encapsulation type:                  lisp
        '''

    # 'show lisp all instance-id 101 service ethernet'
    ShowLispInstance101ServiceEthernet = '''\
        '''

    # --------------------------------------------------------------------------
    # 'show lisp all instance-id <instance_id> <service> server detail internal'
    # --------------------------------------------------------------------------

    # 'show lisp all instance-id 101 service ipv4 server detail internal'
    ShowLispInstance101Ipv4ServerDetailInternal = '''\
        204-MSMR#show lisp all instance-id 101 ipv4 server detail internal
        =====================================================
        Output for router lisp 0
        =====================================================
        LISP Site Registration Information

        Site name: provider
        Allowed configured locators: any
        Allowed EID-prefixes:

        Site name: xtr1_1
        Allowed configured locators: any
        Allowed EID-prefixes:

          EID-prefix: 192.168.0.0/24 instance-id 101
            First registered:     1w4d
            Last registered:      02:41:22
            Routing table tag:    0
            Origin:               Configuration, accepting more specifics
            Merge active:         No
            Proxy reply:          No
            TTL:                  00:00:00
            State:                unknown
            Registration errors:
              Authentication failures:   0
              Allowed locators mismatch: 0
            No registrations.

          EID-prefix: 192.168.0.1/32 instance-id 101
            First registered:     01:12:41
            Last registered:      01:12:41
            Routing table tag:    0
            Origin:               Dynamic, more specific of 192.168.0.0/24
            Merge active:         No
            Proxy reply:          Yes
            TTL:                  1d00h
            State:                complete
            Registration errors:
              Authentication failures:   0
              Allowed locators mismatch: 0
            ETR 10.16.2.2, last registered 01:12:41, proxy-reply, map-notify
                         TTL 1d00h, no merge, hash-function sha1, nonce 0x70D18EF4-0x3A605D67
                         state complete, no security-capability
                         xTR-ID 0x21EDD25F-0x7598784C-0x769C8E4E-0xC04926EC
                         site-ID unspecified
                         sourced by reliable transport
              Locator  Local  State      Pri/Wgt  Scope
              10.16.2.2  yes    up          50/50   IPv4 none

        Site name: xtr1_2
        Allowed configured locators: any
        Allowed EID-prefixes:

        Site name: xtr2
        Allowed configured locators: any
        Allowed EID-prefixes:

          EID-prefix: 192.168.9.0/24 instance-id 101
            First registered:     01:55:47
            Last registered:      01:55:47
            Routing table tag:    0
            Origin:               Configuration
            Merge active:         No
            Proxy reply:          Yes
            TTL:                  1d00h
            State:                complete
            Registration errors:
              Authentication failures:   0
              Allowed locators mismatch: 0
            ETR 10.1.8.8, last registered 01:55:47, proxy-reply, map-notify
                         TTL 1d00h, no merge, hash-function sha1, nonce 0xB06AE31D-0x6ADB0BA5
                         state complete, no security-capability
                         xTR-ID 0x77200484-0xD134DC48-0x0FBAD9DC-0x4A46CA5D
                         site-ID unspecified
                         sourced by reliable transport
              Locator  Local  State      Pri/Wgt  Scope
              10.1.8.8  yes    up          50/50   IPv4 none
        '''

    # 'show lisp all instance-id 101 service ipv6 server detail internal'
    ShowLispInstance101Ipv6ServerDetailInternal = '''\
        '''

    # 'show lisp all instance-id 101 service ethernet server detail internal'
    ShowLispInstance101EthernetServerDetailInternal = '''\
        '''

    # --------------------------------------------------------------------------
    # 'show lisp all extranet <extranet> instance-id <instance_id>'
    # --------------------------------------------------------------------------

    # 'show lisp all extranet ext1 instance-id 101'
    ShowLispExtranet101 = '''\
        204-MSMR#show lisp all extranet ext1 instance-id 101
        Output for router lisp 0

        -----------------------------------------------------
        LISP Extranet table
        Home Instance ID: 101
        Total entries: 6
        Provider/Subscriber  Inst ID    EID prefix
        Provider             103        10.121.88.0/24
        Provider             103        10.220.100.0/24
        Provider             103        192.168.195.0/24
        Subscriber           102        172.16.1.0/24
        Subscriber           101        192.168.0.0/24
        Subscriber           101        192.168.9.0/24
        '''

    # --------------------------------------------------------------------------
    # 'show lisp all instance-id <instance_id> <service> statistics'
    # --------------------------------------------------------------------------

    # 'show lisp all instance-id 101 ipv4 statistics'
    ShowLispInstance101Ipv4Stats = '''
        202-XTR#show lisp all instance-id 101 ipv4 statistics 
        =====================================================
        Output for router lisp 0
        =====================================================
        LISP EID Statistics for instance ID 101 - last cleared: never
        Control Packets:
          Map-Requests in/out:                      0/4
            Encapsulated Map-Requests in/out:       0/3
            RLOC-probe Map-Requests in/out:         0/1
            SMR-based Map-Requests in/out:          0/0
            Map-Requests expired on-queue/no-reply:  0/0
            Map-Resolver Map-Requests forwarded:    0
            Map-Server Map-Requests forwarded:      0
          Map-Reply records in/out:                 2/1
            Authoritative records in/out:           1/1
            Non-authoritative records in/out:       1/0
            Negative records in/out:                0/0
            RLOC-probe records in/out:              1/1
            Map-Server Proxy-Reply records out:     0
          WLC Map-Subscribe records in/out:         0/1
            Map-Subscribe failures in/out:          0/0
          WLC Map-Unsubscribe records in/out:       0/0
            Map-Unsubscribe failures in/out:        0/0
          Map-Register records in/out:              0/2857
            Map-Server AF disabled:                 0
            Authentication failures:                0
          WLC Map-Register records in/out:          0/0
            WLC AP Map-Register in/out:             0/0
            WLC Client Map-Register in/out:         0/0
            WLC Map-Register failures in/out:       0/0
          Map-Notify records in/out:                4/0
            Authentication failures:                0
          WLC Map-Notify records in/out:            0/0
            WLC AP Map-Notify in/out:               0/0
            WLC Client Map-Notify in/out:           0/0
            WLC Map-Notify failures in/out:         0/0
          Dropped control packets in input queue:   0
          Deferred packet transmission:             0/0
            DDT referral deferred/dropped:          0/0
            DDT request deferred/dropped:           0/0
            Map-Reply deferred/dropped:             0/0
            MR negative Map-Reply deferred/dropped: 0/0
            MR Map-Request fwd deferred/dropped:    0/0
            MS Map-Request fwd deferred/dropped:    0/0
            MS proxy Map-Reply deferred/dropped:    0/0
            xTR mcast Map-Notify deferred/dropped:  0/0
            MS Info-Reply deferred/dropped:         0/0
            RTR Map-Register fwd deferred/dropped:  0/0
            RTR Map-Notify fwd deferred/dropped:    0/0
            ETR Info-Request deferred/dropped:      0/0
        Errors:
          Map-Request invalid source rloc drops:    0
          Map-Register invalid source rloc drops:   0
          DDT ITR Map-Requests dropped:             0 (nonce-collision: 0, bad-xTR-nonce: 0)
        Cache Related:
          Cache entries created/deleted:            3/1
          NSF CEF replay entry count                0
          Number of EID-prefixes in map-cache:      2
          Number of negative entries in map-cache:  1
          Total number of RLOCs in map-cache:       1
          Average RLOCs per EID-prefix:             1
        Forwarding:
          Number of data signals processed:         1 (+ dropped 0)
          Number of reachability reports:           0 (+ dropped 0)
        ITR Map-Resolvers:
          Map-Resolver         LastReply  Metric ReqsSent Positive Negative No-Reply
          10.64.4.4              03:13:58        4        1        1        0        0
          10.166.13.13          03:13:58       26        2        0        0        1
        LISP RLOC Statistics - last cleared: never
        Control Packets:
            RTR Map-Requests forwarded:             0
            RTR Map-Notifies forwarded:             0
          DDT-Map-Requests in/out:                  0/0
          DDT-Map-Referrals in/out:                 0/0
        Errors:
          Map-Request format errors:                0
          Map-Reply format errors:                  0
          Map-Referral format errors:               0
          Mapping record TTL alerts:                0
          DDT Requests failed:                      0
        LISP Miscellaneous Statistics - last cleared: never
        Errors:
          Invalid IP version drops:                 0
          Invalid IP header drops:                  0
          Invalid IP proto field drops:             0
          Invalid packet size dropss:               0
          Invalid LISP control port drops:          0
          Invalid LISP checksum drops:              0
          Unsupported LISP packet type drops:       0
          Unknown packet drops:                     0
        '''

    # 'show lisp all instance-id 101 ipv6 statistics'
    ShowLispInstance101Ipv6Stats = '''
        202-XTR#show lisp all instance-id 101 ipv6 statistics 
        =====================================================
        Output for router lisp 0
        =====================================================
        LISP EID Statistics for instance ID 101 - last cleared: never
        Control Packets:
          Map-Requests in/out:                      0/6
            Encapsulated Map-Requests in/out:       0/5
            RLOC-probe Map-Requests in/out:         0/1
            SMR-based Map-Requests in/out:          0/0
            Map-Requests expired on-queue/no-reply  0/1
            Map-Resolver Map-Requests forwarded:    0
            Map-Server Map-Requests forwarded:      0
          Map-Reply records in/out:                 2/1
            Authoritative records in/out:           1/1
            Non-authoritative records in/out:       1/0
            Negative records in/out:                0/0
            RLOC-probe records in/out:              1/1
            Map-Server Proxy-Reply records out:     0
          WLC Map-Subscribe records in/out:         0/2
            Map-Subscribe failures in/out:          0/0
          WLC Map-Unsubscribe records in/out:       0/0
            Map-Unsubscribe failures in/out:        0/0
          Map-Register records in/out:              0/52
            Map-Server AF disabled:                 0
            Authentication failures:                0
          WLC Map-Register records in/out:          0/0
            WLC AP Map-Register in/out:             0/0
            WLC Client Map-Register in/out:         0/0
            WLC Map-Register failures in/out:       0/0
          Map-Notify records in/out:                2/0
            Authentication failures:                0
          WLC Map-Notify records in/out:            0/0
            WLC AP Map-Notify in/out:               0/0
            WLC Client Map-Notify in/out:           0/0
            WLC Map-Notify failures in/out:         0/0
          Dropped control packets in input queue:   0
          Deferred packet transmission:             0/0
            DDT referral deferred/dropped:          0/0
            DDT request deferred/dropped:           0/0
            Map-Reply deferred/dropped:             0/0
            MR negative Map-Reply deferred/dropped: 0/0
            MR Map-Request fwd deferred/dropped:    0/0
            MS Map-Request fwd deferred/dropped:    0/0
            MS proxy Map-Reply deferred/dropped:    0/0
            xTR mcast Map-Notify deferred/dropped:  0/0
            MS Info-Reply deferred/dropped:         0/0
            RTR Map-Register fwd deferred/dropped:  0/0
            RTR Map-Notify fwd deferred/dropped:    0/0
            ETR Info-Request deferred/dropped:      0/0
        Errors:
          Map-Request invalid source rloc drops:    0
          Map-Register invalid source rloc drops:   0
          DDT ITR Map-Requests dropped:             0 (nonce-collision: 0, bad-xTR-nonce: 0)
        Cache Related:
          Cache entries created/deleted:            4/2
          NSF CEF replay entry count                0
          Number of EID-prefixes in map-cache:      2
          Number of negative entries in map-cache:  1
          Total number of RLOCs in map-cache:       1
          Average RLOCs per EID-prefix:             1
        Forwarding:
          Number of data signals processed:         2 (+ dropped 0)
          Number of reachability reports:           0 (+ dropped 0)
        ITR Map-Resolvers:
          Map-Resolver         LastReply  Metric ReqsSent Positive Negative No-Reply
          10.64.4.4              00:15:36       19        2        1        0        1
          10.166.13.13          00:17:11       31        3        0        0        2
        LISP RLOC Statistics - last cleared: never
        Control Packets:
            RTR Map-Requests forwarded:             0
            RTR Map-Notifies forwarded:             0
          DDT-Map-Requests in/out:                  0/0
          DDT-Map-Referrals in/out:                 0/0
        Errors:
          Map-Request format errors:                0
          Map-Reply format errors:                  0
          Map-Referral format errors:               0
          Mapping record TTL alerts:                0
          DDT Requests failed:                      0
        LISP Miscellaneous Statistics - last cleared: never
        Errors:
          Invalid IP version drops:                 0
          Invalid IP header drops:                  0
          Invalid IP proto field drops:             0
          Invalid packet size dropss:               0
          Invalid LISP control port drops:          0
          Invalid LISP checksum drops:              0
          Unsupported LISP packet type drops:       0
          Unknown packet drops:                     0
        '''

    # 'show lisp all instance-id 101 ethernet statistics'
    ShowLispInstance101EthernetStats = '''\
        '''

    # --------------------------------------------------------------------------
    # 'show lisp all instance-id <instance_id> <service> server summary'
    # --------------------------------------------------------------------------

    ShowLispInstance101Ipv4ServerSummary = '''
        204-MSMR#show lisp all instance-id 101 ipv4 server summary 
        =====================================================
        Output for router lisp 0
        =====================================================
                             -----------  IPv4 ----------- 
         Site name            Configured Registered Incons
        xtr1_1                        1          1      0
        xtr2                          1          1      0

        Number of configured sites:                     2
        Number of registered sites:                     2
        Sites with inconsistent registrations:          0
        IPv4
          Number of configured EID prefixes:            2
          Number of registered EID prefixes:            2
        '''

    ShowLispInstance101Ipv6ServerSummary = '''\
        204-MSMR#show lisp all instance-id 101 ipv6 server summary 
        =====================================================
        Output for router lisp 0
        =====================================================
                             -----------  IPv6 ----------- 
         Site name            Configured Registered Incons
        xtr1_1                        1          1      0
        xtr2                          1          1      0

        Number of configured sites:                     2
        Number of registered sites:                     2
        Sites with inconsistent registrations:          0
        IPv6
          Number of configured EID prefixes:            2
          Number of registered EID prefixes:            2
        '''

    ShowLispInstance101EthernetServerSummary = '''\
        '''

    # --------------------------------------------------------------------------
    # 'show lisp all instance-id <instance-d> <service> map-cache'
    # --------------------------------------------------------------------------

    # 'show lisp all instance-id 101 ipv4 map-cache'
    ShowLispInstance101Ipv4MapCache= '''\
        202-XTR#show lisp all instance-id 101 ipv4 map-cache 
        =====================================================
        Output for router lisp 0
        =====================================================
        LISP IPv4 Mapping Cache for EID-table vrf red (IID 101), 2 entries

        0.0.0.0/0, uptime: 15:23:50, expires: never, via static-send-map-request
          Negative cache entry, action: send-map-request
        192.168.9.0/24, uptime: 00:04:02, expires: 23:55:57, via map-reply, complete
          Locator  Uptime    State      Pri/Wgt     Encap-IID
          10.1.8.8  00:04:02  up          50/50        -
        '''

    # 'show lisp all instance-id 101 ipv6 map-cache'
    ShowLispInstance101Ipv6MapCache = '''\
        202-XTR#show lisp all instance-id 101 ipv6 map-cache 

        =====================================================
        Output for router lisp 0
        =====================================================
        LISP IPv6 Mapping Cache for EID-table vrf red (IID 101), 2 entries

        ::/0, uptime: 00:11:28, expires: never, via static-send-map-request
          Negative cache entry, action: send-map-request
        2001:192:168:9::/64, uptime: 00:06:51, expires: 23:53:08, via map-reply, complete
          Locator  Uptime    State      Pri/Wgt     Encap-IID
          10.1.8.8  00:06:51  up          50/50        -
        172.16.10.0/24, uptime: 00:00:00, expires: 23:59:59, via map-reply, complete
          Locator                     Uptime    State      Pri/Wgt
          172.16.156.134             00:00:00  up           1/50
          192.168.65.94                00:00:00  up           1/50
          2001:DB8:BBED:2829::80DF:9C86  00:00:00  up           2/100
        '''

    # 'show lisp all instance-id 101 ethernet map-cache'
    ShowLispInstance101EthernetMapCache = '''\
        '''

    # --------------------------------------------------------------------------
    # 'show lisp all instance-id <instance_id> <service> dabatase'
    # --------------------------------------------------------------------------

    # 'show lisp all instance-id 101 ipv4 database'
    ShowLispInstance101Ipv4Database = '''\
        202-XTR#show lisp all instance-id 101 ipv4 database  
        =====================================================
        Output for router lisp 0
        =====================================================
        LISP ETR IPv4 Mapping Database for EID-table vrf red (IID 101), LSBs: 0x1
        Entries total 1, no-route 0, inactive 0

        192.168.0.0/24, locator-set RLOC
          Locator  Pri/Wgt  Source     State
          10.16.2.2   50/50   cfg-intf   site-self, reachable
        '''

    # 'show lisp all instance-id 101 ipv6 database'
    ShowLispInstance101Ipv6Database = '''\
        202-XTR#show lisp all instance-id 101 ipv6 database 
        =====================================================
        Output for router lisp 0
        =====================================================
        LISP ETR IPv6 Mapping Database for EID-table vrf red (IID 101), LSBs: 0x1
        Entries total 1, no-route 0, inactive 0

        2001:192:168::/64, locator-set RLOC
          Locator  Pri/Wgt  Source     State
          10.16.2.2   50/50   cfg-intf   site-self, reachable
        '''

    # 'show lisp all instance-id 101 ethernet database'
    ShowLispInstance101EthernetDatabase = '''
        202-XTR#show lisp all instance-id 101 ethernet database

        =================================================
        Output for router lisp 0
        =================================================
        LISP ETR MAC Mapping Database for EID-table Vlan 101 (IID 101), LSBs: 0x1
        Entries total 2, no-route 0, inactive 0

        0050.56b0.6a0e/48, dynamic-eid Auto-L2-group-1, inherited from default locator-set RLOC
          Locator     Pri/Wgt  Source     State
          10.229.11.1    1/100  cfg-intf   site-self, reachable
        cafe.cafe.cafe/48, dynamic-eid Auto-L2-group-1, inherited from default locator-set RLOC
          Locator     Pri/Wgt  Source     State
          10.229.11.1    1/100  cfg-intf   site-self, reachable
        '''

    ############################################################################
    #                           LISP INFO STRUCTURE
    ############################################################################

    LispInfo = {
        'lisp_router_instances': 
            {0: 
                {'lisp_router_id': 
                    {'site_id': 'unspecified',
                    'xtr_id': '0x730E0861-0x12996F6D-0xEFEA2114-0xE1C951F7'},
                'lisp_router_instance_id': 0,
                'locator_sets': 
                    {'RLOC': 
                        {'locator_set_name': 'RLOC'}},
                'service': 
                    {'ethernet':
                        {'etr':
                            {'local_eids':
                                {'101':
                                    {'dynamic_eids':
                                        {'0050.56b0.6a0e/48':
                                            {'eid_address':
                                                {'address_type': 'ethernet',
                                                'vrf': '101'},
                                            'id': '0050.56b0.6a0e/48',
                                            'loopback_address': '10.229.11.1',
                                            'priority': 1,
                                            'rlocs': 'RLOC',
                                            'weight': 100},
                                        'cafe.cafe.cafe/48':
                                            {'eid_address':
                                                {'address_type': 'ethernet',
                                                'vrf': '101'},
                                            'id': 'cafe.cafe.cafe/48',
                                            'loopback_address': '10.229.11.1',
                                            'priority': 1,
                                            'rlocs': 'RLOC',
                                            'weight': 100}},
                        'vni': '101'}}},
                        'service': 'ethernet',
                        'virtual_network_ids':
                            {'101':
                                {'lisp_role':
                                    {'none':
                                        {'lisp_role_type': 'none'}}}}},
                    'ipv4':
                        {'etr': 
                            {'enabled': True,
                            'encapsulation': 'lisp',
                            'local_eids': 
                                {'101': 
                                    {'eids': 
                                        {'192.168.0.0/24': 
                                            {'eid_address': 
                                                {'address_type': 'ipv4',
                                                'vrf': 'red'},
                                            'id': '192.168.0.0/24',
                                            'loopback_address': '10.16.2.2',
                                            'priority': 50,
                                            'rlocs': 'RLOC',
                                            'weight': 50}},
                                    'use_petrs': 
                                        {'10.10.10.10': 
                                            {'use_petr': '10.10.10.10',
                                            },
                                        },
                                    'vni': '101'}},
                            'mapping_servers': 
                                {'10.166.13.13': 
                                    {'ms_address': '10.166.13.13'},
                                '10.64.4.4': 
                                    {'ms_address': '10.64.4.4'}}},
                        'itr': 
                            {'enabled': True,
                            'map_cache': 
                                {'101': 
                                    {'mappings': 
                                        {'0.0.0.0/0': 
                                            {'creation_time': '15:23:50',
                                            'eid': 
                                                {'address_type': 'ipv4-afi',
                                                'ipv4': 
                                                    {'ipv4': '0.0.0.0/0'},
                                                'vrf': 'red'},
                                            'id': '0.0.0.0/0',
                                            'negative_mapping': 
                                                {'map_reply_action': 'send-map-request'},
                                            'time_to_live': 'never'},
                                        '192.168.9.0/24': 
                                            {'creation_time': '00:04:02',
                                            'eid': 
                                                {'address_type': 'ipv4-afi',
                                                'ipv4': 
                                                    {'ipv4': '192.168.9.0/24'},
                                                'vrf': 'red'},
                                            'id': '192.168.9.0/24',
                                            'positive_mapping': 
                                                {'rlocs': 
                                                    {1: 
                                                        {'id': '1',
                                                        'locator_address': 
                                                            {'address_type': 'ipv4-afi',
                                                            'ipv4': 
                                                                {'ipv4': '10.1.8.8'},
                                                            'virtual_network_id': '101'},
                                                        'priority': 50,
                                                        'weight': 50}}},
                                            'time_to_live': '23:55:57'}},
                                    'vni': '101'}},
                            'map_resolvers': 
                                {'10.166.13.13': 
                                    {'map_resolver': '10.166.13.13'},
                                '10.64.4.4': 
                                    {'map_resolver': '10.64.4.4'}},
                            'proxy_itrs': 
                                {'10.10.10.10': 
                                    {'proxy_etr_address': '10.10.10.10'}}},
                        'map_server': 
                            {'enabled': False,
                            'sites': 
                                {'provider': 
                                    {'site_id': 'provider'},
                                'xtr1_1': 
                                    {'site_id': 'xtr1_1'},
                                'xtr1_2': 
                                    {'site_id': 'xtr1_2'},
                                'xtr2': 
                                    {'site_id': 'xtr2'}},
                            'summary': 
                                {'af_datum': 
                                    {'ipv4-afi': 
                                        {'address_type': 'ipv4-afi',
                                        'number_configured_eids': 2,
                                        'number_registered_eids': 2}},
                                'number_configured_sites': 2,
                                'number_registered_sites': 2},
                            'virtual_network_ids': 
                                {'101': 
                                    {'counters': 
                                        {'map_notify_records_out': '0',
                                        'map_registers_in': '0',
                                        'map_registers_in_auth_failed': '0',
                                        'map_requests_forwarded_out': '0',
                                        'proxy_reply_records_out': '0'},
                                    'extranets': 
                                        {'ext1': 
                                            {'extranet': 'ext1',
                                            'home_instance_id': 101,
                                            'subscriber': 
                                                {'192.168.0.0/24': 
                                                    {'bidirectional': True,
                                                    'eid_record': '192.168.0.0/24'},
                                                '192.168.9.0/24': 
                                                    {'bidirectional': True,
                                                    'eid_record': '192.168.9.0/24'}}}},
                                    'mappings': 
                                        {'192.168.0.0/24': 
                                            {'eid_address': 
                                                {'address_type': 'ipv4-afi',
                                                'ipv4': 
                                                    {'ipv4': '192.168.0.0/24'},
                                                'virtual_network_id': '101'},
                                            'eid_id': '192.168.0.0/24',
                                            'more_specifics_accepted': True,
                                            'site_id': 'xtr1_1'},
                                        '192.168.0.1/32': 
                                            {'eid_address': 
                                                {'address_type': 'ipv4-afi',
                                                'ipv4': 
                                                    {'ipv4': '192.168.0.1/32'},
                                                'virtual_network_id': '101'},
                                            'eid_id': '192.168.0.1/32',
                                            'mapping_records': 
                                                {'0x21EDD25F-0x7598784C-0x769C8E4E-0xC04926EC': 
                                                    {'creation_time': '01:12:41',
                                                    'eid': 
                                                        {'address_type': 'ipv4-afi',
                                                        'ipv4': 
                                                            {'ipv4': '192.168.0.1/32'},
                                                        'virtual_network_id': '101'},
                                                    'site_id': 'unspecified',
                                                    'time_to_live': 86400,
                                                    'xtr_id': '0x21EDD25F-0x7598784C-0x769C8E4E-0xC04926EC'}},
                                            'site_id': 'xtr1_1'},
                                        '192.168.9.0/24': 
                                            {'eid_address': 
                                                {'address_type': 'ipv4-afi',
                                                'ipv4': 
                                                    {'ipv4': '192.168.9.0/24'},
                                                'virtual_network_id': '101'},
                                            'eid_id': '192.168.9.0/24',
                                            'mapping_records': 
                                                {'0x77200484-0xD134DC48-0x0FBAD9DC-0x4A46CA5D': 
                                                    {'creation_time': '01:55:47',
                                                    'eid': 
                                                        {'address_type': 'ipv4-afi',
                                                        'ipv4': 
                                                            {'ipv4': '192.168.9.0/24'},
                                                        'virtual_network_id': '101'},
                                                        'site_id': 'unspecified',
                                                        'time_to_live': 86400,
                                                        'xtr_id': '0x77200484-0xD134DC48-0x0FBAD9DC-0x4A46CA5D'}},
                                            'site_id': 'xtr2'}},
                                    'vni': '101'},
                                '102': 
                                    {'extranets': 
                                        {'ext1': 
                                            {'extranet': 'ext1',
                                            'home_instance_id': 101,
                                            'subscriber': 
                                                {'172.16.1.0/24': 
                                                    {'bidirectional': True,
                                                    'eid_record': '172.16.1.0/24'}}}},
                                    'vni': '102'},
                                '103': 
                                    {'extranets': 
                                        {'ext1': 
                                            {'extranet': 'ext1',
                                            'home_instance_id': 101,
                                            'provider': 
                                                {'10.220.100.0/24': 
                                                    {'bidirectional': True,
                                                    'eid_record': '10.220.100.0/24'},
                                                '192.168.195.0/24': 
                                                    {'bidirectional': True,
                                                    'eid_record': '192.168.195.0/24'},
                                                '10.121.88.0/24': 
                                                    {'bidirectional': True,
                                                    'eid_record': '10.121.88.0/24'}}}},
                                    'vni': '103'}}},
                        'service': 'ipv4',
                        'virtual_network_ids': 
                            {'101': 
                                {'lisp_role': 
                                    {'itr-etr': 
                                        {'lisp_role_type': 'itr-etr'}}}}},
                    'ipv6': 
                        {'etr': 
                            {'enabled': True,
                            'encapsulation': 'lisp',
                            'local_eids': 
                                {'101': 
                                    {'eids': 
                                        {'2001:192:168::/64': 
                                            {'eid_address': 
                                                {'address_type': 'ipv6',
                                                'vrf': 'red'},
                                            'id': '2001:192:168::/64',
                                            'loopback_address': '10.16.2.2',
                                            'priority': 50,
                                            'rlocs': 'RLOC',
                                            'weight': 50}},
                                    'use_petrs': 
                                        {'10.10.10.10': 
                                            {'use_petr': '10.10.10.10',
                                            },
                                        },
                                    'vni': '101'}},
                            'mapping_servers': 
                                {'10.66.12.12': 
                                    {'ms_address': '10.66.12.12'},
                                '10.100.5.5': 
                                    {'ms_address': '10.100.5.5'}}},
                        'itr': 
                            {'enabled': True,
                            'map_cache': 
                                {'101': 
                                    {'mappings': 
                                        {'172.16.10.0/24': 
                                            {'creation_time': '00:00:00',
                                            'eid': 
                                                {'address_type': 'ipv4-afi',
                                                'ipv4': 
                                                    {'ipv4': '172.16.10.0/24'},
                                                    'vrf': 'red'},
                                            'id': '172.16.10.0/24',
                                            'positive_mapping': 
                                                {'rlocs': 
                                                    {1: 
                                                        {'id': '1',
                                                        'locator_address': 
                                                            {'address_type': 'ipv4-afi',
                                                            'ipv4': 
                                                                {'ipv4': '172.16.156.134'},
                                                            'virtual_network_id': '101'},
                                                        'priority': 1,
                                                        'weight': 50},
                                                    2: 
                                                        {'id': '2',
                                                        'locator_address': 
                                                            {'address_type': 'ipv4-afi',
                                                            'ipv4': 
                                                                {'ipv4': '192.168.65.94'},
                                                            'virtual_network_id': '101'},
                                                        'priority': 1,
                                                        'weight': 50},
                                                    3: 
                                                        {'id': '3',
                                                        'locator_address': 
                                                            {'address_type': 'ipv6-afi',
                                                            'ipv6': 
                                                                {'ipv6': '2001:DB8:BBED:2829::80DF:9C86'},
                                                            'virtual_network_id': '101'},
                                                        'priority': 2,
                                                        'weight': 100}}},
                                            'time_to_live': '23:59:59'},
                                        '2001:192:168:9::/64': 
                                            {'creation_time': '00:06:51',
                                            'eid': 
                                                {'address_type': 'ipv6-afi',
                                                'vrf': 'red'},
                                            'id': '2001:192:168:9::/64',
                                            'positive_mapping': 
                                                {'rlocs': 
                                                    {1: 
                                                        {'id': '1',
                                                        'locator_address': 
                                                            {'address_type': 'ipv4-afi',
                                                            'ipv4': 
                                                                {'ipv4': '10.1.8.8'},
                                                            'virtual_network_id': '101'},
                                                        'priority': 50,
                                                        'weight': 50}}},
                                            'time_to_live': '23:53:08'},
                                        '::/0': 
                                            {'creation_time': '00:11:28',
                                            'eid': 
                                                {'address_type': 'ipv6-afi',
                                                'vrf': 'red'},
                                            'id': '::/0',
                                            'negative_mapping': 
                                                {'map_reply_action': 'send-map-request'},
                                            'time_to_live': 'never'}},
                                    'vni': '101'}},
                            'map_resolvers': 
                                {'10.66.12.12': 
                                    {'map_resolver': '10.66.12.12'},
                                '10.100.5.5': 
                                    {'map_resolver': '10.100.5.5'}}},
                        'map_server': 
                            {'enabled': False,
                            'summary': 
                                {'af_datum': 
                                    {'ipv6-afi': 
                                        {'address_type': 'ipv6-afi',
                                        'number_configured_eids': 2,
                                        'number_registered_eids': 2}},
                                'number_configured_sites': 2,
                                'number_registered_sites': 2},
                            'virtual_network_ids': 
                                {'101': 
                                    {'counters': 
                                        {'map_notify_records_out': '0',
                                        'map_registers_in': '0',
                                        'map_registers_in_auth_failed': '0',
                                        'map_requests_forwarded_out': '0',
                                        'proxy_reply_records_out': '0',
                                        },
                                    },
                                },
                            },
                        'service': 'ipv6',
                        'virtual_network_ids': 
                            {'101': 
                                {'lisp_role': 
                                    {'itr-etr': 
                                        {'lisp_role_type': 'itr-etr'}}}}}}}}}

