""" 
Isis Genie Ops Object Outputs for IOSXR.
"""

class IsisOutput(object):

    showIsis = """\
        #show isis

        IS-IS Router: test
        System Id: 4444.4444.4444
        Instance Id: 0
        IS Levels: level-1
        Manual area address(es):
            49.0002
        Routing for area address(es):
            49.0002
        Non-stop forwarding: Disabled
        Most recent startup mode: Cold Restart
        TE connection status: Down
        Topologies supported by IS-IS:
            IPv4 Unicast
            Level-1
                Metric style (generate/accept): Wide/Wide
                Metric: 10
                ISPF status: Disabled
            No protocols redistributed
            Distance: 115
            Advertise Passive Interface Prefixes Only: No
            IPv6 Unicast
            Level-1
                Metric: 10
                ISPF status: Disabled
            No protocols redistributed
            Distance: 115
            Advertise Passive Interface Prefixes Only: No
        SRLB not allocated
        SRGB not allocated
        Interfaces supported by IS-IS:
            Loopback0 is running actively (active in configuration)
            GigabitEthernet0/0/0/0 is running actively (active in configuration)
            GigabitEthernet0/0/0/1 is running actively (active in configuration)
    """

    showIsisHostname = '''\
        #show isis hostname

        IS-IS test hostnames
        Level  System ID      Dynamic Hostname
        1   * 4444.4444.4444 R4
        1     6666.6666.6666 R6
        1     7777.7777.7777 R7
        1     3333.3333.3333 R3
        1     5555.5555.5555 R5
    '''

    showIsisAdjacency = '''\
        show isis adjacency
        Wed Nov 27 18:13:32.411 UTC

        IS-IS test Level-1 adjacencies:
        System Id      Interface        SNPA           State Hold Changed  NSF IPv4 IPv6
                                                                            BFD  BFD
        R3             Gi0/0/0/0        fa16.3e19.b468 Up    28   1w1d     Yes None None
        R5             Gi0/0/0/1        fa16.3eed.3775 Up    8    1w1d     Yes None None

        Total adjacency count: 2
    '''

    showIsisLspLog = """\
        show isis lsp-log

        IS-IS test Level 1 LSP log
        When          Count  Interface          Triggers
        --- Tue Nov 19 2019 ---
        01:34:54.037      1                     CONFIG
        01:34:54.618      6  Gi0/0/0/0          CONFIG NEWADJ IPUP
        01:34:55.019      2  Lo0                IPUP
        01:34:57.597      2  Gi0/0/0/0          DIS
        01:35:10.145      1                     LSPDBOL

        IS-IS test Level 1 Pseudo-node 3 LSP log
        When          Count  Interface          Triggers
        --- Tue Nov 19 2019 ---
        01:34:57.597      1  Gi0/0/0/0          DIS
    """

    showIsisSpfLog = """\
        show isis spf-log

        IS-IS test Level 1 IPv4 Unicast Route Calculation Log
                            Time Total Trig.
        Timestamp    Type   (ms) Nodes Count First Trigger LSP    Triggers
        ------------ ----- ----- ----- ----- -------------------- -----------------------
        --- Mon Nov 25 2019 ---
        13:56:31.093  FSPF     0    11     1                      PERIODIC
        14:11:31.147  FSPF     0    11     1                      PERIODIC
        14:26:31.199  FSPF     0    11     1                      PERIODIC
        14:41:31.251  FSPF     0    11     1                      PERIODIC
        14:56:31.303  FSPF     0    11     1                      PERIODIC
        15:11:31.358  FSPF     0    11     1                      PERIODIC
        15:26:31.411  FSPF     0    11     1                      PERIODIC
        15:41:31.462  FSPF     0    11     1                      PERIODIC
        15:56:31.516  FSPF     0    11     1                      PERIODIC
        16:11:31.568  FSPF     0    11     1                      PERIODIC
        16:26:31.624  FSPF     0    11     1                      PERIODIC
        16:41:31.675  FSPF     0    11     1                      PERIODIC
        16:56:31.726  FSPF     0    11     1                      PERIODIC
        17:11:31.806  FSPF     0    11     1                      PERIODIC
        17:26:31.858  FSPF     0    11     1                      PERIODIC
        17:41:31.913  FSPF     0    11     1                      PERIODIC
        17:56:31.969  FSPF     0    11     1                      PERIODIC
        18:11:32.026  FSPF     0    11     1                      PERIODIC
        18:26:32.077  FSPF     0    11     1                      PERIODIC
        18:41:32.130  FSPF     0    11     1                      PERIODIC
        18:56:32.184  FSPF     0    11     1                      PERIODIC
        19:11:32.236  FSPF     0    11     1                      PERIODIC
        19:26:32.289  FSPF     0    11     1                      PERIODIC
        19:41:32.344  FSPF     0    11     1                      PERIODIC
        19:56:32.398  FSPF     0    11     1                      PERIODIC
        20:11:32.453  FSPF     0    11     1                      PERIODIC
        20:26:32.509  FSPF     0    11     1                      PERIODIC
        20:41:32.565  FSPF     0    11     1                      PERIODIC
        20:56:32.620  FSPF     0    11     1                      PERIODIC
        21:11:32.677  FSPF     0    11     1                      PERIODIC
        21:26:32.731  FSPF     0    11     1                      PERIODIC
        21:41:32.785  FSPF     0    11     1                      PERIODIC
        21:56:32.837  FSPF     0    11     1                      PERIODIC
        22:11:32.890  FSPF     0    11     1                      PERIODIC
        22:26:32.947  FSPF     0    11     1                      PERIODIC
        22:41:33.001  FSPF     0    11     1                      PERIODIC
        22:56:33.057  FSPF     0    11     1                      PERIODIC
        23:11:33.113  FSPF     0    11     1                      PERIODIC
        23:26:33.164  FSPF     0    11     1                      PERIODIC
        23:41:33.218  FSPF     0    11     1                      PERIODIC
        23:56:33.270  FSPF     0    11     1                      PERIODIC
        --- Tue Nov 26 2019 ---
        00:11:33.324  FSPF     0    11     1                      PERIODIC
        00:26:33.381  FSPF     0    11     1                      PERIODIC
        00:41:33.436  FSPF     0    11     1                      PERIODIC
        00:56:33.492  FSPF     0    11     1                      PERIODIC
        01:11:33.545  FSPF     0    11     1                      PERIODIC
        01:26:33.602  FSPF     0    11     1                      PERIODIC
        01:41:33.658  FSPF     0    11     1                      PERIODIC
        01:56:33.712  FSPF     0    11     1                      PERIODIC
        02:11:33.767  FSPF     0    11     1                      PERIODIC
        02:26:33.821  FSPF     0    11     1                      PERIODIC
        02:41:33.874  FSPF     0    11     1                      PERIODIC
        02:56:33.927  FSPF     0    11     1                      PERIODIC
        03:11:33.986  FSPF     0    11     1                      PERIODIC
        03:26:34.042  FSPF     0    11     1                      PERIODIC
        03:41:34.095  FSPF     0    11     1                      PERIODIC
        03:56:34.151  FSPF     0    11     1                      PERIODIC
        04:11:34.204  FSPF     0    11     1                      PERIODIC
        04:26:34.255  FSPF     0    11     1                      PERIODIC
        04:41:34.309  FSPF     0    11     1                      PERIODIC
        04:56:34.362  FSPF     0    11     1                      PERIODIC
        05:11:34.420  FSPF     0    11     1                      PERIODIC
        05:26:34.472  FSPF     0    11     1                      PERIODIC
        05:41:34.527  FSPF     0    11     1                      PERIODIC
        05:56:34.582  FSPF     0    11     1                      PERIODIC
        06:11:34.639  FSPF     0    11     1                      PERIODIC
        06:26:34.693  FSPF     0    11     1                      PERIODIC
        06:41:34.746  FSPF     0    11     1                      PERIODIC
        06:56:34.797  FSPF     0    11     1                      PERIODIC
        07:11:34.853  FSPF     0    11     1                      PERIODIC
        07:26:34.908  FSPF     0    11     1                      PERIODIC
        07:41:34.961  FSPF     0    11     1                      PERIODIC
        07:56:35.018  FSPF     0    11     1                      PERIODIC
        08:11:35.072  FSPF     0    11     1                      PERIODIC
        08:26:35.126  FSPF     0    11     1                      PERIODIC
        08:41:35.177  FSPF     0    11     1                      PERIODIC
        08:56:35.229  FSPF     0    11     1                      PERIODIC
        09:11:35.283  FSPF     0    11     1                      PERIODIC
        09:26:35.337  FSPF     0    11     1                      PERIODIC
        09:41:35.391  FSPF     0    11     1                      PERIODIC
        09:56:35.443  FSPF     0    11     1                      PERIODIC
        10:11:35.494  FSPF     0    11     1                      PERIODIC
        10:26:35.546  FSPF     0    11     1                      PERIODIC
        10:41:35.602  FSPF     0    11     1                      PERIODIC
        10:56:35.657  FSPF     0    11     1                      PERIODIC
        11:11:35.710  FSPF     0    11     1                      PERIODIC
        11:26:35.762  FSPF     0    11     1                      PERIODIC
        11:41:35.817  FSPF     0    11     1                      PERIODIC
        11:56:35.869  FSPF     0    11     1                      PERIODIC
        12:11:35.920  FSPF     0    11     1                      PERIODIC
        12:26:35.974  FSPF     0    11     1                      PERIODIC
        12:41:36.031  FSPF     0    11     1                      PERIODIC
        12:56:36.084  FSPF     0    11     1                      PERIODIC
        13:11:36.139  FSPF     0    11     1                      PERIODIC
        13:26:36.197  FSPF     0    11     1                      PERIODIC
        13:41:36.250  FSPF     0    11     1                      PERIODIC
        13:56:36.302  FSPF     0    11     1                      PERIODIC
        14:11:36.355  FSPF     0    11     1                      PERIODIC
        14:26:36.408  FSPF     0    11     1                      PERIODIC
        14:41:36.460  FSPF     0    11     1                      PERIODIC
        14:56:36.517  FSPF     0    11     1                      PERIODIC
        15:11:36.568  FSPF     0    11     1                      PERIODIC
        15:26:36.627  FSPF     0    11     1                      PERIODIC
        15:41:36.679  FSPF     0    11     1                      PERIODIC
        15:56:36.731  FSPF     0    11     1                      PERIODIC
        16:11:36.785  FSPF     0    11     1                      PERIODIC
        16:26:36.839  FSPF     0    11     1                      PERIODIC
        16:41:36.895  FSPF     0    11     1                      PERIODIC
        16:56:36.950  FSPF     0    11     1                      PERIODIC
        17:11:37.001  FSPF     0    11     1                      PERIODIC
        17:26:37.052  FSPF     0    11     1                      PERIODIC
        17:41:37.105  FSPF     0    11     1                      PERIODIC
        17:56:37.159  FSPF     0    11     1                      PERIODIC
        18:11:37.211  FSPF     0    11     1                      PERIODIC
        18:26:37.262  FSPF     0    11     1                      PERIODIC
        18:41:37.317  FSPF     0    11     1                      PERIODIC
        18:56:37.369  FSPF     0    11     1                      PERIODIC
        19:11:37.421  FSPF     0    11     1                      PERIODIC
        19:26:37.474  FSPF     0    11     1                      PERIODIC
        19:41:37.529  FSPF     0    11     1                      PERIODIC
        19:56:37.584  FSPF     0    11     1                      PERIODIC
        20:11:37.641  FSPF     0    11     1                      PERIODIC
        20:26:37.695  FSPF     0    11     1                      PERIODIC
        20:41:37.751  FSPF     0    11     1                      PERIODIC
        20:56:37.803  FSPF     0    11     1                      PERIODIC
        21:11:37.855  FSPF     0    11     1                      PERIODIC
        21:26:37.908  FSPF     0    11     1                      PERIODIC
        21:41:37.960  FSPF     0    11     1                      PERIODIC
        21:56:38.013  FSPF     0    11     1                      PERIODIC
        22:11:38.063  FSPF     0    11     1                      PERIODIC
        22:26:38.120  FSPF     0    11     1                      PERIODIC
        22:41:38.172  FSPF     0    11     1                      PERIODIC
        22:56:38.228  FSPF     0    11     1                      PERIODIC
        23:11:38.283  FSPF     0    11     1                      PERIODIC
        23:26:38.339  FSPF     0    11     1                      PERIODIC
        23:41:38.394  FSPF     0    11     1                      PERIODIC
        23:56:38.447  FSPF     0    11     1                      PERIODIC
        --- Wed Nov 27 2019 ---
        00:11:38.506  FSPF     0    11     1                      PERIODIC
        00:26:38.557  FSPF     0    11     1                      PERIODIC
        00:41:38.610  FSPF     0    11     1                      PERIODIC
        00:56:38.662  FSPF     0    11     1                      PERIODIC
        01:11:38.717  FSPF     0    11     1                      PERIODIC
        01:26:38.769  FSPF     0    11     1                      PERIODIC
        01:41:38.822  FSPF     0    11     1                      PERIODIC
        01:56:38.877  FSPF     0    11     1                      PERIODIC
        02:11:38.931  FSPF     0    11     1                      PERIODIC
        02:26:38.989  FSPF     0    11     1                      PERIODIC
        02:41:39.041  FSPF     0    11     1                      PERIODIC
        02:56:39.093  FSPF     0    11     1                      PERIODIC
        03:11:39.148  FSPF     0    11     1                      PERIODIC
        03:26:39.202  FSPF     0    11     1                      PERIODIC
        03:41:39.260  FSPF     0    11     1                      PERIODIC
        03:56:39.315  FSPF     0    11     1                      PERIODIC
        04:11:39.368  FSPF     0    11     1                      PERIODIC
        04:26:39.424  FSPF     0    11     1                      PERIODIC
        04:41:39.476  FSPF     0    11     1                      PERIODIC
        04:56:39.528  FSPF     0    11     1                      PERIODIC
        05:11:39.586  FSPF     0    11     1                      PERIODIC
        05:26:39.639  FSPF     0    11     1                      PERIODIC
        05:41:39.692  FSPF     0    11     1                      PERIODIC
        05:56:39.767  FSPF     0    11     1                      PERIODIC
        06:11:39.822  FSPF     0    11     1                      PERIODIC
        06:26:39.875  FSPF     0    11     1                      PERIODIC
        06:41:39.946  FSPF     0    11     1                      PERIODIC
        06:56:40.000  FSPF     0    11     1                      PERIODIC
        07:11:40.052  FSPF     0    11     1                      PERIODIC
        07:26:40.107  FSPF     0    11     1                      PERIODIC
        07:41:40.164  FSPF     0    11     1                      PERIODIC
        07:56:40.216  FSPF     0    11     1                      PERIODIC
        08:11:40.269  FSPF     0    11     1                      PERIODIC
        08:26:40.323  FSPF     0    11     1                      PERIODIC
        08:41:40.379  FSPF     0    11     1                      PERIODIC
        08:56:40.434  FSPF     0    11     1                      PERIODIC
        09:11:40.487  FSPF     0    11     1                      PERIODIC
        09:26:40.541  FSPF     0    11     1                      PERIODIC
        09:41:40.593  FSPF     0    11     1                      PERIODIC
        09:56:40.644  FSPF     0    11     1                      PERIODIC
        10:11:40.700  FSPF     0    11     1                      PERIODIC
        10:26:40.758  FSPF     0    11     1                      PERIODIC
        10:41:40.814  FSPF     0    11     1                      PERIODIC
        10:56:40.868  FSPF     0    11     1                      PERIODIC
        11:11:40.922  FSPF     0    11     1                      PERIODIC
        11:26:40.976  FSPF     0    11     1                      PERIODIC
        11:41:41.028  FSPF     0    11     1                      PERIODIC
        11:56:41.080  FSPF     0    11     1                      PERIODIC
        12:11:41.135  FSPF     0    11     1                      PERIODIC
        12:26:41.187  FSPF     0    11     1                      PERIODIC
        12:41:41.238  FSPF     0    11     1                      PERIODIC
        12:56:41.290  FSPF     0    11     1                      PERIODIC
        13:11:41.342  FSPF     0    11     1                      PERIODIC
        13:26:41.394  FSPF     0    11     1                      PERIODIC
        13:41:41.447  FSPF     0    11     1                      PERIODIC
        13:56:41.505  FSPF     0    11     1                      PERIODIC
        14:11:41.558  FSPF     0    11     1                      PERIODIC
        14:26:41.610  FSPF     0    11     1                      PERIODIC
        14:41:41.662  FSPF     0    11     1                      PERIODIC
        14:56:41.718  FSPF     0    11     1                      PERIODIC
        15:11:41.774  FSPF     0    11     1                      PERIODIC
        15:26:41.826  FSPF     0    11     1                      PERIODIC
        15:41:41.881  FSPF     0    11     1                      PERIODIC
        15:56:41.932  FSPF     0    11     1                      PERIODIC
        16:11:41.990  FSPF     0    11     1                      PERIODIC
        16:26:42.042  FSPF     0    11     1                      PERIODIC
        16:41:42.098  FSPF     0    11     1                      PERIODIC
        16:56:42.151  FSPF     0    11     1                      PERIODIC
        17:11:42.211  FSPF     0    11     1                      PERIODIC
        17:26:42.267  FSPF     0    11     1                      PERIODIC
        17:41:42.323  FSPF     0    11     1                      PERIODIC
        17:56:42.375  FSPF     0    11     1                      PERIODIC
        18:11:42.427  FSPF     0    11     1                      PERIODIC
    """

    showIsisInterface = '''\
        show isis interface

        IS-IS test Interfaces
        Loopback0                   Enabled
        Adjacency Formation:      Enabled
        Prefix Advertisement:     Enabled
        IPv4 BFD:                 Disabled
        IPv6 BFD:                 Disabled
        BFD Min Interval:         150
        BFD Multiplier:           3
        Bandwidth:                0

        Circuit Type:             level-1 (Interface circuit type is level-1-2)
        Media Type:               Loop
        Circuit Number:           0

        Level-1
            Adjacency Count:        0
            LSP Pacing Interval:    33 ms
            PSNP Entry Queue Size:  0
            Hello Interval:         10 s
            Hello Multiplier:       3

        CLNS I/O
            Protocol State:         Up
            MTU:                    1500

        IPv4 Unicast Topology:    Enabled
            Adjacency Formation:    Running
            Prefix Advertisement:   Running
            Metric (L1/L2):         10/10
            Weight (L1/L2):         0/0
            MPLS Max Label Stack:   1/3/10 (PRI/BKP/SRTE)
            MPLS LDP Sync (L1/L2):  Disabled/Disabled
            FRR (L1/L2):            L1 Not Enabled     L2 Not Enabled
            FRR Type:             None               None
        IPv6 Unicast Topology:    Enabled
            Adjacency Formation:    Running
            Prefix Advertisement:   Running
            Metric (L1/L2):         10/10
            Weight (L1/L2):         0/0
            MPLS Max Label Stack:   1/3/10 (PRI/BKP/SRTE)
            MPLS LDP Sync (L1/L2):  Disabled/Disabled
            FRR (L1/L2):            L1 Not Enabled     L2 Not Enabled
            FRR Type:             None               None

        IPv4 Address Family:      Enabled
            Protocol State:         Up
            Forwarding Address(es): 0.0.0.0
            Global Prefix(es):      4.4.4.4/32
        IPv6 Address Family:      Enabled
            Protocol State:         Up
            Forwarding Address(es): ::
            Global Prefix(es):      2001:db8:4:4:4::4/128

        LSP transmit timer expires in 0 ms
        LSP transmission is idle
        Can send up to 10 back-to-back LSPs in the next 0 ms

        GigabitEthernet0/0/0/0      Enabled
        Adjacency Formation:      Enabled
        Prefix Advertisement:     Enabled
        IPv4 BFD:                 Disabled
        IPv6 BFD:                 Disabled
        BFD Min Interval:         150
        BFD Multiplier:           3
        Bandwidth:                1000000

        Circuit Type:             level-1 (Interface circuit type is level-1-2)
        Media Type:               LAN
        Circuit Number:           3

        Level-1
            Adjacency Count:        1
            LAN ID:                 R4.03
            Priority (Local/DIS):   64/64
            Next LAN IIH in:        262 ms
            LSP Pacing Interval:    33 ms
            PSNP Entry Queue Size:  0
            Hello Interval:         10 s
            Hello Multiplier:       3

        CLNS I/O
            Protocol State:         Up
            MTU:                    1497
            SNPA:                   fa16.3ed2.6534
            Layer-2 MCast Groups Membership:
            All Level-1 ISs:      Yes

        IPv4 Unicast Topology:    Enabled
            Adjacency Formation:    Running
            Prefix Advertisement:   Running
            Metric (L1/L2):         10/10
            Weight (L1/L2):         0/0
            MPLS Max Label Stack:   1/3/10 (PRI/BKP/SRTE)
            MPLS LDP Sync (L1/L2):  Disabled/Disabled
            FRR (L1/L2):            L1 Not Enabled     L2 Not Enabled
            FRR Type:             None               None
        IPv6 Unicast Topology:    Enabled
            Adjacency Formation:    Running
            Prefix Advertisement:   Running
            Metric (L1/L2):         10/10
            Weight (L1/L2):         0/0
            MPLS Max Label Stack:   1/3/10 (PRI/BKP/SRTE)
            MPLS LDP Sync (L1/L2):  Disabled/Disabled
            FRR (L1/L2):            L1 Not Enabled     L2 Not Enabled
            FRR Type:             None               None

        IPv4 Address Family:      Enabled
            Protocol State:         Up
            Forwarding Address(es): 10.3.4.4
            Global Prefix(es):      10.3.4.0/24
        IPv6 Address Family:      Enabled
            Protocol State:         Up
            Forwarding Address(es): fe80::f816:3eff:fed2:6534
            Global Prefix(es):      2001:db8:10:3::/64

        LSP transmit timer expires in 0 ms
        LSP transmission is idle
        Can send up to 9 back-to-back LSPs in the next 0 ms

        GigabitEthernet0/0/0/1      Enabled
        Adjacency Formation:      Enabled
        Prefix Advertisement:     Enabled
        IPv4 BFD:                 Disabled
        IPv6 BFD:                 Disabled
        BFD Min Interval:         150
        BFD Multiplier:           3
        Bandwidth:                1000000

        Circuit Type:             level-1 (Interface circuit type is level-1-2)
        Media Type:               LAN
        Circuit Number:           1

        Level-1
            Adjacency Count:        1
            LAN ID:                 R5.02
            Priority (Local/DIS):   64/64
            Next LAN IIH in:        3 s
            LSP Pacing Interval:    33 ms
            PSNP Entry Queue Size:  0
            Hello Interval:         10 s
            Hello Multiplier:       3

        CLNS I/O
            Protocol State:         Up
            MTU:                    1497
            SNPA:                   fa16.3eec.fc83
            Layer-2 MCast Groups Membership:
            All Level-1 ISs:      Yes

        IPv4 Unicast Topology:    Enabled
            Adjacency Formation:    Running
            Prefix Advertisement:   Running
            Metric (L1/L2):         10/10
            Weight (L1/L2):         0/0
            MPLS Max Label Stack:   1/3/10 (PRI/BKP/SRTE)
            MPLS LDP Sync (L1/L2):  Disabled/Disabled
            FRR (L1/L2):            L1 Not Enabled     L2 Not Enabled
            FRR Type:             None               None
        IPv6 Unicast Topology:    Enabled
            Adjacency Formation:    Running
            Prefix Advertisement:   Running
            Metric (L1/L2):         10/10
            Weight (L1/L2):         0/0
            MPLS Max Label Stack:   1/3/10 (PRI/BKP/SRTE)
            MPLS LDP Sync (L1/L2):  Disabled/Disabled
            FRR (L1/L2):            L1 Not Enabled     L2 Not Enabled
            FRR Type:             None               None

        IPv4 Address Family:      Enabled
            Protocol State:         Up
            Forwarding Address(es): 10.4.5.4
            Global Prefix(es):      10.4.5.0/24
        IPv6 Address Family:      Enabled
            Protocol State:         Up
            Forwarding Address(es): fe80::f816:3eff:feec:fc83
            Global Prefix(es):      2001:db8:10:4::/64

        LSP transmit timer expires in 0 ms
        LSP transmission is idle
        Can send up to 9 back-to-back LSPs in the next 0 ms
    '''

    showIsisStatistics = '''\
        show isis statistics

        IS-IS test statistics:
            Fast PSNP cache (hits/tries): 4464/14245
            Fast CSNP cache (hits/tries): 74900/85843
            Fast CSNP cache updates: 21885
            LSP checksum errors received: 0
            LSP Dropped: 0
            SNP Dropped: 0
            UPD Max Queue size: 3
            UPD Queue size: 0
            Average transmit times and rate:
            Hello:          0 s,      42694 ns,         26/s
            CSNP:           0 s,      34560 ns,          6/s
            PSNP:           0 s,       4092 ns,          0/s
            LSP:            0 s,      29341 ns,          0/s
            Average process times and rate:
            Hello:          0 s,      26279 ns,         25/s
            CSNP:           0 s,      17444 ns,          6/s
            PSNP:           0 s,          0 ns,          0/s
            LSP:            0 s,      32157 ns,          1/s
            Level-1:
            LSPs sourced (new/refresh): 7/1900
            IPv4 Unicast
                Total SPF calculations     : 840
                Full SPF calculations      : 840
                ISPF calculations          : 0
                Next Hop Calculations      : 0
                Partial Route Calculations : 0
                Periodic SPF calculations  : 834
            IPv6 Unicast
                Total SPF calculations     : 839
                Full SPF calculations      : 839
                ISPF calculations          : 0
                Next Hop Calculations      : 0
                Partial Route Calculations : 0
                Periodic SPF calculations  : 834
        Interface Loopback0:
            Level-1 LSPs (sent/rcvd)  : 0/0
            Level-1 CSNPs (sent/rcvd) : 0/0
            Level-1 PSNPs (sent/rcvd) : 0/0
            Level-1 LSP Flooding Duplicates     : 9781
            Level-1 LSPs Arrival Time Throttled : 0
        Interface GigabitEthernet0/0/0/0:
            Level-1 Hellos (sent/rcvd): 257510/85901
            Level-1 DR Elections      : 1
            Level-1 LSPs (sent/rcvd)  : 5316/7920
            Level-1 CSNPs (sent/rcvd) : 85843/0
            Level-1 PSNPs (sent/rcvd) : 0/0
            Level-1 LSP Flooding Duplicates     : 0
            Level-1 LSPs Arrival Time Throttled : 0
        Interface GigabitEthernet0/0/0/1:
            Level-1 Hellos (sent/rcvd): 85893/256730
            Level-1 DR Elections      : 1
            Level-1 LSPs (sent/rcvd)  : 7264/6325
            Level-1 CSNPs (sent/rcvd) : 0/85595
            Level-1 PSNPs (sent/rcvd) : 0/0
            Level-1 LSP Flooding Duplicates     : 0
            Level-1 LSPs Arrival Time Throttled : 0
    '''

    showIsisDatabaseDetail = """\
        show isis database detail
        Wed Nov 27 18:23:00.945 UTC

        IS-IS test (Level-1) Link State Database
        LSPID                 LSP Seq Num  LSP Checksum  LSP Holdtime/Rcvd  ATT/P/OL
        R3.00-00              0x000003bd   0xfe94        402  /1200         1/0/0
        Area Address:   49.0002
        Metric: 10         IS-Extended R3.01
        Metric: 10         IS-Extended R4.03
        Metric: 10         IS-Extended R3.05
        NLPID:          0xcc
        NLPID:          0x8e
        IP Address:     3.3.3.3
        Metric: 10         IP-Extended 3.3.3.0/24
        Metric: 10         IP-Extended 10.2.3.0/24
        Metric: 10         IP-Extended 10.3.4.0/24
        Metric: 10         IP-Extended 10.3.5.0/24
        Metric: 10         IP-Extended 10.3.6.0/24
        Hostname:       R3
        Metric: 10         MT (IPv6 Unicast) IS-Extended R3.01
        Metric: 10         MT (IPv6 Unicast) IS-Extended R4.03
        Metric: 10         MT (IPv6 Unicast) IS-Extended R3.05
        IPv6 Address:   2001:db8:3:3:3::3
        Metric: 10         MT (IPv6 Unicast) IPv6 2001:db8:3:3:3::3/128
        Metric: 10         MT (IPv6 Unicast) IPv6 2001:db8:10:2::/64
        Metric: 10         MT (IPv6 Unicast) IPv6 2001:db8:10:3::/64
        MT:             Standard (IPv4 Unicast)
        MT:             IPv6 Unicast                                 1/0/0
        R3.01-00              0x000003bf   0x1591        1195 /1200         0/0/0
        Metric: 0          IS-Extended R3.00
        Metric: 0          IS-Extended R5.00
        R3.05-00              0x000003b8   0x073c        1005 /1200         0/0/0
        Metric: 0          IS-Extended R3.00
        Metric: 0          IS-Extended R6.00
        R4.00-00            * 0x000003be   0x73d0        1087 /*            0/0/0
        Area Address:   49.0002
        Metric: 10         IS-Extended R4.03
        Metric: 10         IS-Extended R5.02
        NLPID:          0xcc
        NLPID:          0x8e
        IP Address:     4.4.4.4
        Metric: 10         IP-Extended 4.4.4.4/32
        Metric: 10         IP-Extended 10.3.4.0/24
        Metric: 10         IP-Extended 10.4.5.0/24
        Hostname:       R4
        Metric: 10         MT (IPv6 Unicast) IS-Extended R4.03
        Metric: 10         MT (IPv6 Unicast) IS-Extended R5.02
        IPv6 Address:   2001:db8:4:4:4::4
        Metric: 10         MT (IPv6 Unicast) IPv6 2001:db8:4:4:4::4/128
        Metric: 10         MT (IPv6 Unicast) IPv6 2001:db8:10:3::/64
        Metric: 10         MT (IPv6 Unicast) IPv6 2001:db8:10:4::/64
        MT:             Standard (IPv4 Unicast)
        MT:             IPv6 Unicast                                 0/0/0
        R4.03-00              0x000003b6   0x7d32        1011 /*            0/0/0
        Metric: 0          IS-Extended R4.00
        Metric: 0          IS-Extended R3.00
        R5.00-00              0x000003b8   0x0912        490  /1200         1/0/0
        Area Address:   49.0002
        NLPID:          0xcc
        NLPID:          0x8e
        MT:             Standard (IPv4 Unicast)
        MT:             IPv6 Unicast                                 1/0/0
        Hostname:       R5
        Metric: 10         IS-Extended R5.03
        Metric: 10         IS-Extended R3.01
        Metric: 10         IS-Extended R5.02
        Metric: 10         MT (IPv6 Unicast) IS-Extended R5.03
        Metric: 10         MT (IPv6 Unicast) IS-Extended R3.01
        Metric: 10         MT (IPv6 Unicast) IS-Extended R5.02
        IP Address:     5.5.5.5
        Metric: 10         IP-Extended 5.5.5.5/32
        Metric: 10         IP-Extended 10.3.5.0/24
        Metric: 10         IP-Extended 10.4.5.0/24
        Metric: 10         IP-Extended 10.5.7.0/24
        IPv6 Address:   2001:db8:5:5:5::5
        Metric: 10         MT (IPv6 Unicast) IPv6 2001:db8:5:5:5::5/128
        Metric: 10         MT (IPv6 Unicast) IPv6 2001:db8:10:3::/64
        Metric: 10         MT (IPv6 Unicast) IPv6 2001:db8:10:4::/64
        Metric: 10         MT (IPv6 Unicast) IPv6 2001:db8:10:5::/64
        R5.02-00              0x000003b9   0xce21        613  /1199         0/0/0
        Metric: 0          IS-Extended R5.00
        Metric: 0          IS-Extended R4.00
        R5.03-00              0x000003ba   0xc5f4        839  /1199         0/0/0
        Metric: 0          IS-Extended R5.00
        Metric: 0          IS-Extended R7.00
        R6.00-00              0x0000054b   0x73c5        1055 /1200         0/0/0
        Area Address:   49.0002
        NLPID:          0xcc
        NLPID:          0x8e
        Router ID:      6.6.6.6
        IP Address:     6.6.6.6
        MT:             IPv6 Unicast                                 0/0/0
        MT:             Standard (IPv4 Unicast)
        Hostname:       R6
        Metric: 40         MT (IPv6 Unicast) IS-Extended R3.05
        Metric: 40         MT (IPv6 Unicast) IS-Extended R7.02
        Metric: 40         IS-Extended R3.05
        Metric: 40         IS-Extended R7.02
        Metric: 1          IP-Extended 6.6.6.0/24
        Metric: 40         IP-Extended 10.6.7.0/24
        Metric: 40         IP-Extended 10.3.6.0/24
        Metric: 1          MT (IPv6 Unicast) IPv6 2001:db8:6:6:6::6/128
        Metric: 40         MT (IPv6 Unicast) IPv6 2001:db8:10:6::/64
        Metric: 40         MT (IPv6 Unicast) IPv6 2001:db8:10:3::/64
        R7.00-00              0x0000054f   0x0ef9        894  /1198         1/0/0
        Area Address:   49.0002
        NLPID:          0xcc
        NLPID:          0x8e
        Router ID:      7.7.7.7
        IP Address:     7.7.7.7
        MT:             IPv6 Unicast                                 0/0/0
        MT:             Standard (IPv4 Unicast)
        Hostname:       R7
        Metric: 40         MT (IPv6 Unicast) IS-Extended R7.02
        Metric: 40         MT (IPv6 Unicast) IS-Extended R5.03
        Metric: 40         IS-Extended R7.02
        Metric: 40         IS-Extended R5.03
        Metric: 40         IP-Extended-Interarea 10.7.8.0/24
        Metric: 1          IP-Extended 7.7.7.7/32
        Metric: 40         IP-Extended 10.7.9.0/24
        Metric: 40         IP-Extended 10.6.7.0/24
        Metric: 40         IP-Extended 10.5.7.0/24
        Metric: 40         MT (IPv6 Unicast) IPv6-Interarea 2001:db8:10:7::/64
        Metric: 1          MT (IPv6 Unicast) IPv6 2001:db8:7:7:7::7/128
        Metric: 40         MT (IPv6 Unicast) IPv6 2001:db8:10:77::/64
        Metric: 40         MT (IPv6 Unicast) IPv6 2001:db8:10:6::/64
        Metric: 40         MT (IPv6 Unicast) IPv6 2001:db8:10:5::/64
        R7.02-00              0x0000054b   0xf08d        1108 /1200         0/0/0
        Metric: 0          IS-Extended R6.00
        Metric: 0          IS-Extended R7.00

        Total Level-1 LSP count: 11     Local Level-1 LSP count: 1
    """

    isisOpsOutput = {
        'instance': {
            'test': {
                'process_id': 'test',
                'vrf': {
                    'default': {
                        'area_address': ['49.0002'],
                        'enable': True,
                        'hostname_db': {
                            'hostname': {
                                '3333.3333.3333': {
                                    'hostname': 'R3',
                                },
                                '4444.4444.4444': {
                                    'hostname': 'R4',
                                },
                                '5555.5555.5555': {
                                    'hostname': 'R5',
                                },
                                '6666.6666.6666': {
                                    'hostname': 'R6',
                                },
                                '7777.7777.7777': {
                                    'hostname': 'R7',
                                },
                            },
                        },
                        'interfaces': {
                            'GigabitEthernet0/0/0/0': {
                                'adjacencies': {
                                    'R3': {
                                        'neighbor_snpa': {
                                            'fa16.3e19.b468': {
                                                'level': {
                                                    'level-1': {
                                                        'hold_timer': 28,
                                                        'lastuptime': '1w1d',
                                                        'state': 'Up',
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                'hello_interval': {
                                    'level_1': {
                                        'interval': 10,
                                    },
                                },
                                'hello_multiplier': {
                                    'level_1': {
                                        'multiplier': 3,
                                    },
                                },
                                'interface_type': 'broadcast',
                                'level_type': 'level-1-only',
                                'lsp_pacing_interval': 33,
                                'name': 'GigabitEthernet0/0/0/0',
                                'packet_counters': {
                                    'level': {
                                        'level-1': {
                                            'csnp': {
                                                'in': 0,
                                                'out': 85843,
                                            },
                                            'level': 'level-1',
                                            'lsp': {
                                                'in': 7920,
                                                'out': 5316,
                                            },
                                            'psnp': {
                                                'in': 0,
                                                'out': 0,
                                            },
                                        },
                                    },
                                },
                                'passive': False,
                                'priority': {
                                    'level_1': {
                                        'priority': 64,
                                    },
                                },
                                'topologies': {
                                    'ipv4 unicast': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 10,
                                            },
                                            'level_2': {
                                                'metric': 10,
                                            },
                                        },
                                        'name': 'ipv4 unicast',
                                    },
                                    'ipv6 unicast': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 10,
                                            },
                                            'level_2': {
                                                'metric': 10,
                                            },
                                        },
                                        'name': 'ipv6 unicast',
                                    },
                                },
                            },
                            'GigabitEthernet0/0/0/1': {
                                'adjacencies': {
                                    'R5': {
                                        'neighbor_snpa': {
                                            'fa16.3eed.3775': {
                                                'level': {
                                                    'level-1': {
                                                        'hold_timer': 8,
                                                        'lastuptime': '1w1d',
                                                        'state': 'Up',
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                'hello_interval': {
                                    'level_1': {
                                        'interval': 10,
                                    },
                                },
                                'hello_multiplier': {
                                    'level_1': {
                                        'multiplier': 3,
                                    },
                                },
                                'interface_type': 'broadcast',
                                'level_type': 'level-1-only',
                                'lsp_pacing_interval': 33,
                                'name': 'GigabitEthernet0/0/0/1',
                                'packet_counters': {
                                    'level': {
                                        'level-1': {
                                            'csnp': {
                                                'in': 85595,
                                                'out': 0,
                                            },
                                            'level': 'level-1',
                                            'lsp': {
                                                'in': 6325,
                                                'out': 7264,
                                            },
                                            'psnp': {
                                                'in': 0,
                                                'out': 0,
                                            },
                                        },
                                    },
                                },
                                'passive': False,
                                'priority': {
                                    'level_1': {
                                        'priority': 64,
                                    },
                                },
                                'topologies': {
                                    'ipv4 unicast': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 10,
                                            },
                                            'level_2': {
                                                'metric': 10,
                                            },
                                        },
                                        'name': 'ipv4 unicast',
                                    },
                                    'ipv6 unicast': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 10,
                                            },
                                            'level_2': {
                                                'metric': 10,
                                            },
                                        },
                                        'name': 'ipv6 unicast',
                                    },
                                },
                            },
                            'Loopback0': {
                                'hello_interval': {
                                    'level_1': {
                                        'interval': 10,
                                    },
                                },
                                'hello_multiplier': {
                                    'level_1': {
                                        'multiplier': 3,
                                    },
                                },
                                'interface_type': 'loopback',
                                'level_type': 'level-1-only',
                                'lsp_pacing_interval': 33,
                                'name': 'Loopback0',
                                'packet_counters': {
                                    'level': {
                                        'level-1': {
                                            'csnp': {
                                                'in': 0,
                                                'out': 0,
                                            },
                                            'level': 'level-1',
                                            'lsp': {
                                                'in': 0,
                                                'out': 0,
                                            },
                                            'psnp': {
                                                'in': 0,
                                                'out': 0,
                                            },
                                        },
                                    },
                                },
                                'passive': False,
                                'topologies': {
                                    'ipv4 unicast': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 10,
                                            },
                                            'level_2': {
                                                'metric': 10,
                                            },
                                        },
                                        'name': 'ipv4 unicast',
                                    },
                                    'ipv6 unicast': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 10,
                                            },
                                            'level_2': {
                                                'metric': 10,
                                            },
                                        },
                                        'name': 'ipv6 unicast',
                                    },
                                },
                            },
                        },
                        'lsp_log': {
                            1: {
                                'id': 1,
                                'level': 1,
                                'received_timestamp': 'Tue Nov 19 2019 01:34:54.037',
                            },
                            2: {
                                'id': 2,
                                'level': 1,
                                'received_timestamp': 'Tue Nov 19 2019 01:34:54.618',
                            },
                            3: {
                                'id': 3,
                                'level': 1,
                                'received_timestamp': 'Tue Nov 19 2019 01:34:55.019',
                            },
                            4: {
                                'id': 4,
                                'level': 1,
                                'received_timestamp': 'Tue Nov 19 2019 01:34:57.597',
                            },
                            5: {
                                'id': 5,
                                'level': 1,
                                'received_timestamp': 'Tue Nov 19 2019 01:35:10.145',
                            },
                            6: {
                                'id': 6,
                                'level': 1,
                                'received_timestamp': 'Tue Nov 19 2019 01:34:57.597',
                            },
                        },
                        'spf_log': {
                            1: {
                                'id': 1,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 13:56:31.093',
                            },
                            2: {
                                'id': 2,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 14:11:31.147',
                            },
                            3: {
                                'id': 3,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 14:26:31.199',
                            },
                            4: {
                                'id': 4,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 14:41:31.251',
                            },
                            5: {
                                'id': 5,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 14:56:31.303',
                            },
                            6: {
                                'id': 6,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 15:11:31.358',
                            },
                            7: {
                                'id': 7,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 15:26:31.411',
                            },
                            8: {
                                'id': 8,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 15:41:31.462',
                            },
                            9: {
                                'id': 9,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 15:56:31.516',
                            },
                            10: {
                                'id': 10,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 16:11:31.568',
                            },
                            11: {
                                'id': 11,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 16:26:31.624',
                            },
                            12: {
                                'id': 12,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 16:41:31.675',
                            },
                            13: {
                                'id': 13,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 16:56:31.726',
                            },
                            14: {
                                'id': 14,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 17:11:31.806',
                            },
                            15: {
                                'id': 15,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 17:26:31.858',
                            },
                            16: {
                                'id': 16,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 17:41:31.913',
                            },
                            17: {
                                'id': 17,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 17:56:31.969',
                            },
                            18: {
                                'id': 18,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 18:11:32.026',
                            },
                            19: {
                                'id': 19,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 18:26:32.077',
                            },
                            20: {
                                'id': 20,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 18:41:32.130',
                            },
                            21: {
                                'id': 21,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 18:56:32.184',
                            },
                            22: {
                                'id': 22,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 19:11:32.236',
                            },
                            23: {
                                'id': 23,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 19:26:32.289',
                            },
                            24: {
                                'id': 24,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 19:41:32.344',
                            },
                            25: {
                                'id': 25,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 19:56:32.398',
                            },
                            26: {
                                'id': 26,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 20:11:32.453',
                            },
                            27: {
                                'id': 27,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 20:26:32.509',
                            },
                            28: {
                                'id': 28,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 20:41:32.565',
                            },
                            29: {
                                'id': 29,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 20:56:32.620',
                            },
                            30: {
                                'id': 30,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 21:11:32.677',
                            },
                            31: {
                                'id': 31,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 21:26:32.731',
                            },
                            32: {
                                'id': 32,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 21:41:32.785',
                            },
                            33: {
                                'id': 33,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 21:56:32.837',
                            },
                            34: {
                                'id': 34,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 22:11:32.890',
                            },
                            35: {
                                'id': 35,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 22:26:32.947',
                            },
                            36: {
                                'id': 36,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 22:41:33.001',
                            },
                            37: {
                                'id': 37,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 22:56:33.057',
                            },
                            38: {
                                'id': 38,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 23:11:33.113',
                            },
                            39: {
                                'id': 39,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 23:26:33.164',
                            },
                            40: {
                                'id': 40,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 23:41:33.218',
                            },
                            41: {
                                'id': 41,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Mon Nov 25 2019 23:56:33.270',
                            },
                            42: {
                                'id': 42,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 00:11:33.324',
                            },
                            43: {
                                'id': 43,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 00:26:33.381',
                            },
                            44: {
                                'id': 44,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 00:41:33.436',
                            },
                            45: {
                                'id': 45,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 00:56:33.492',
                            },
                            46: {
                                'id': 46,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 01:11:33.545',
                            },
                            47: {
                                'id': 47,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 01:26:33.602',
                            },
                            48: {
                                'id': 48,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 01:41:33.658',
                            },
                            49: {
                                'id': 49,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 01:56:33.712',
                            },
                            50: {
                                'id': 50,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 02:11:33.767',
                            },
                            51: {
                                'id': 51,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 02:26:33.821',
                            },
                            52: {
                                'id': 52,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 02:41:33.874',
                            },
                            53: {
                                'id': 53,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 02:56:33.927',
                            },
                            54: {
                                'id': 54,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 03:11:33.986',
                            },
                            55: {
                                'id': 55,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 03:26:34.042',
                            },
                            56: {
                                'id': 56,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 03:41:34.095',
                            },
                            57: {
                                'id': 57,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 03:56:34.151',
                            },
                            58: {
                                'id': 58,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 04:11:34.204',
                            },
                            59: {
                                'id': 59,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 04:26:34.255',
                            },
                            60: {
                                'id': 60,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 04:41:34.309',
                            },
                            61: {
                                'id': 61,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 04:56:34.362',
                            },
                            62: {
                                'id': 62,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 05:11:34.420',
                            },
                            63: {
                                'id': 63,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 05:26:34.472',
                            },
                            64: {
                                'id': 64,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 05:41:34.527',
                            },
                            65: {
                                'id': 65,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 05:56:34.582',
                            },
                            66: {
                                'id': 66,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 06:11:34.639',
                            },
                            67: {
                                'id': 67,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 06:26:34.693',
                            },
                            68: {
                                'id': 68,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 06:41:34.746',
                            },
                            69: {
                                'id': 69,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 06:56:34.797',
                            },
                            70: {
                                'id': 70,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 07:11:34.853',
                            },
                            71: {
                                'id': 71,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 07:26:34.908',
                            },
                            72: {
                                'id': 72,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 07:41:34.961',
                            },
                            73: {
                                'id': 73,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 07:56:35.018',
                            },
                            74: {
                                'id': 74,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 08:11:35.072',
                            },
                            75: {
                                'id': 75,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 08:26:35.126',
                            },
                            76: {
                                'id': 76,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 08:41:35.177',
                            },
                            77: {
                                'id': 77,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 08:56:35.229',
                            },
                            78: {
                                'id': 78,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 09:11:35.283',
                            },
                            79: {
                                'id': 79,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 09:26:35.337',
                            },
                            80: {
                                'id': 80,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 09:41:35.391',
                            },
                            81: {
                                'id': 81,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 09:56:35.443',
                            },
                            82: {
                                'id': 82,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 10:11:35.494',
                            },
                            83: {
                                'id': 83,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 10:26:35.546',
                            },
                            84: {
                                'id': 84,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 10:41:35.602',
                            },
                            85: {
                                'id': 85,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 10:56:35.657',
                            },
                            86: {
                                'id': 86,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 11:11:35.710',
                            },
                            87: {
                                'id': 87,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 11:26:35.762',
                            },
                            88: {
                                'id': 88,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 11:41:35.817',
                            },
                            89: {
                                'id': 89,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 11:56:35.869',
                            },
                            90: {
                                'id': 90,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 12:11:35.920',
                            },
                            91: {
                                'id': 91,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 12:26:35.974',
                            },
                            92: {
                                'id': 92,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 12:41:36.031',
                            },
                            93: {
                                'id': 93,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 12:56:36.084',
                            },
                            94: {
                                'id': 94,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 13:11:36.139',
                            },
                            95: {
                                'id': 95,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 13:26:36.197',
                            },
                            96: {
                                'id': 96,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 13:41:36.250',
                            },
                            97: {
                                'id': 97,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 13:56:36.302',
                            },
                            98: {
                                'id': 98,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 14:11:36.355',
                            },
                            99: {
                                'id': 99,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 14:26:36.408',
                            },
                            100: {
                                'id': 100,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 14:41:36.460',
                            },
                            101: {
                                'id': 101,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 14:56:36.517',
                            },
                            102: {
                                'id': 102,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 15:11:36.568',
                            },
                            103: {
                                'id': 103,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 15:26:36.627',
                            },
                            104: {
                                'id': 104,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 15:41:36.679',
                            },
                            105: {
                                'id': 105,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 15:56:36.731',
                            },
                            106: {
                                'id': 106,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 16:11:36.785',
                            },
                            107: {
                                'id': 107,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 16:26:36.839',
                            },
                            108: {
                                'id': 108,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 16:41:36.895',
                            },
                            109: {
                                'id': 109,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 16:56:36.950',
                            },
                            110: {
                                'id': 110,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 17:11:37.001',
                            },
                            111: {
                                'id': 111,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 17:26:37.052',
                            },
                            112: {
                                'id': 112,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 17:41:37.105',
                            },
                            113: {
                                'id': 113,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 17:56:37.159',
                            },
                            114: {
                                'id': 114,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 18:11:37.211',
                            },
                            115: {
                                'id': 115,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 18:26:37.262',
                            },
                            116: {
                                'id': 116,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 18:41:37.317',
                            },
                            117: {
                                'id': 117,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 18:56:37.369',
                            },
                            118: {
                                'id': 118,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 19:11:37.421',
                            },
                            119: {
                                'id': 119,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 19:26:37.474',
                            },
                            120: {
                                'id': 120,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 19:41:37.529',
                            },
                            121: {
                                'id': 121,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 19:56:37.584',
                            },
                            122: {
                                'id': 122,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 20:11:37.641',
                            },
                            123: {
                                'id': 123,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 20:26:37.695',
                            },
                            124: {
                                'id': 124,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 20:41:37.751',
                            },
                            125: {
                                'id': 125,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 20:56:37.803',
                            },
                            126: {
                                'id': 126,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 21:11:37.855',
                            },
                            127: {
                                'id': 127,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 21:26:37.908',
                            },
                            128: {
                                'id': 128,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 21:41:37.960',
                            },
                            129: {
                                'id': 129,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 21:56:38.013',
                            },
                            130: {
                                'id': 130,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 22:11:38.063',
                            },
                            131: {
                                'id': 131,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 22:26:38.120',
                            },
                            132: {
                                'id': 132,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 22:41:38.172',
                            },
                            133: {
                                'id': 133,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 22:56:38.228',
                            },
                            134: {
                                'id': 134,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 23:11:38.283',
                            },
                            135: {
                                'id': 135,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 23:26:38.339',
                            },
                            136: {
                                'id': 136,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 23:41:38.394',
                            },
                            137: {
                                'id': 137,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Tue Nov 26 2019 23:56:38.447',
                            },
                            138: {
                                'id': 138,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 00:11:38.506',
                            },
                            139: {
                                'id': 139,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 00:26:38.557',
                            },
                            140: {
                                'id': 140,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 00:41:38.610',
                            },
                            141: {
                                'id': 141,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 00:56:38.662',
                            },
                            142: {
                                'id': 142,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 01:11:38.717',
                            },
                            143: {
                                'id': 143,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 01:26:38.769',
                            },
                            144: {
                                'id': 144,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 01:41:38.822',
                            },
                            145: {
                                'id': 145,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 01:56:38.877',
                            },
                            146: {
                                'id': 146,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 02:11:38.931',
                            },
                            147: {
                                'id': 147,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 02:26:38.989',
                            },
                            148: {
                                'id': 148,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 02:41:39.041',
                            },
                            149: {
                                'id': 149,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 02:56:39.093',
                            },
                            150: {
                                'id': 150,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 03:11:39.148',
                            },
                            151: {
                                'id': 151,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 03:26:39.202',
                            },
                            152: {
                                'id': 152,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 03:41:39.260',
                            },
                            153: {
                                'id': 153,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 03:56:39.315',
                            },
                            154: {
                                'id': 154,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 04:11:39.368',
                            },
                            155: {
                                'id': 155,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 04:26:39.424',
                            },
                            156: {
                                'id': 156,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 04:41:39.476',
                            },
                            157: {
                                'id': 157,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 04:56:39.528',
                            },
                            158: {
                                'id': 158,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 05:11:39.586',
                            },
                            159: {
                                'id': 159,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 05:26:39.639',
                            },
                            160: {
                                'id': 160,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 05:41:39.692',
                            },
                            161: {
                                'id': 161,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 05:56:39.767',
                            },
                            162: {
                                'id': 162,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 06:11:39.822',
                            },
                            163: {
                                'id': 163,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 06:26:39.875',
                            },
                            164: {
                                'id': 164,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 06:41:39.946',
                            },
                            165: {
                                'id': 165,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 06:56:40.000',
                            },
                            166: {
                                'id': 166,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 07:11:40.052',
                            },
                            167: {
                                'id': 167,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 07:26:40.107',
                            },
                            168: {
                                'id': 168,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 07:41:40.164',
                            },
                            169: {
                                'id': 169,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 07:56:40.216',
                            },
                            170: {
                                'id': 170,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 08:11:40.269',
                            },
                            171: {
                                'id': 171,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 08:26:40.323',
                            },
                            172: {
                                'id': 172,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 08:41:40.379',
                            },
                            173: {
                                'id': 173,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 08:56:40.434',
                            },
                            174: {
                                'id': 174,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 09:11:40.487',
                            },
                            175: {
                                'id': 175,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 09:26:40.541',
                            },
                            176: {
                                'id': 176,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 09:41:40.593',
                            },
                            177: {
                                'id': 177,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 09:56:40.644',
                            },
                            178: {
                                'id': 178,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 10:11:40.700',
                            },
                            179: {
                                'id': 179,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 10:26:40.758',
                            },
                            180: {
                                'id': 180,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 10:41:40.814',
                            },
                            181: {
                                'id': 181,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 10:56:40.868',
                            },
                            182: {
                                'id': 182,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 11:11:40.922',
                            },
                            183: {
                                'id': 183,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 11:26:40.976',
                            },
                            184: {
                                'id': 184,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 11:41:41.028',
                            },
                            185: {
                                'id': 185,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 11:56:41.080',
                            },
                            186: {
                                'id': 186,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 12:11:41.135',
                            },
                            187: {
                                'id': 187,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 12:26:41.187',
                            },
                            188: {
                                'id': 188,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 12:41:41.238',
                            },
                            189: {
                                'id': 189,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 12:56:41.290',
                            },
                            190: {
                                'id': 190,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 13:11:41.342',
                            },
                            191: {
                                'id': 191,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 13:26:41.394',
                            },
                            192: {
                                'id': 192,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 13:41:41.447',
                            },
                            193: {
                                'id': 193,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 13:56:41.505',
                            },
                            194: {
                                'id': 194,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 14:11:41.558',
                            },
                            195: {
                                'id': 195,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 14:26:41.610',
                            },
                            196: {
                                'id': 196,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 14:41:41.662',
                            },
                            197: {
                                'id': 197,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 14:56:41.718',
                            },
                            198: {
                                'id': 198,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 15:11:41.774',
                            },
                            199: {
                                'id': 199,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 15:26:41.826',
                            },
                            200: {
                                'id': 200,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 15:41:41.881',
                            },
                            201: {
                                'id': 201,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 15:56:41.932',
                            },
                            202: {
                                'id': 202,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 16:11:41.990',
                            },
                            203: {
                                'id': 203,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 16:26:42.042',
                            },
                            204: {
                                'id': 204,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 16:41:42.098',
                            },
                            205: {
                                'id': 205,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 16:56:42.151',
                            },
                            206: {
                                'id': 206,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 17:11:42.211',
                            },
                            207: {
                                'id': 207,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 17:26:42.267',
                            },
                            208: {
                                'id': 208,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 17:41:42.323',
                            },
                            209: {
                                'id': 209,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 17:56:42.375',
                            },
                            210: {
                                'id': 210,
                                'level': 1,
                                'spf_type': 'full',
                                'start_timestamp': 'Wed Nov 27 2019 18:11:42.427',
                            },
                        },
                        'system_id': '4444.4444.4444',
                        'topologies': {
                            'IPv4 Unicast': {
                                'preference': {
                                    'coarse': {
                                        'default': 115,
                                    },
                                },
                                'topology': 'IPv4 Unicast',
                            },
                            'IPv6 Unicast': {
                                'preference': {
                                    'coarse': {
                                        'default': 115,
                                    },
                                },
                                'topology': 'IPv6 Unicast',
                            },
                        },
                        'vrf': 'default',
                    },
                },
            },
        },
    }

    isisLsdbOpsOutput = {
        'instance': {
            'test': {
                'vrf': {
                    'default': {
                        'level_db': {
                            1: {
                                'R3.00-00': {
                                    'checksum': '0xfe94',
                                    'dynamic_hostname': 'R3',
                                    'extended_ipv4_reachability': {
                                        '10.2.3.0/24': {
                                            'ip_prefix': '10.2.3.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                        },
                                        '10.3.4.0/24': {
                                            'ip_prefix': '10.3.4.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                        },
                                        '10.3.5.0/24': {
                                            'ip_prefix': '10.3.5.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                        },
                                        '10.3.6.0/24': {
                                            'ip_prefix': '10.3.6.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                        },
                                        '3.3.3.0/24': {
                                            'ip_prefix': '3.3.3.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                        },
                                    },
                                    'extended_is_neighbor': {
                                        'R3.01': {
                                            'metric': 10,
                                            'neighbor_id': 'R3.01',
                                        },
                                        'R3.05': {
                                            'metric': 10,
                                            'neighbor_id': 'R3.05',
                                        },
                                        'R4.03': {
                                            'metric': 10,
                                            'neighbor_id': 'R4.03',
                                        },
                                    },
                                    'ipv4_addresses': ['3.3.3.3'],
                                    'ipv6_addresses': ['2001:db8:3:3:3::3'],
                                    'lsp_id': 'R3.00-00',
                                    'mt_entries': {
                                        'IPv6 Unicast': {
                                            'attributes': '1',
                                            'mt_id': 'IPv6 Unicast',
                                        },
                                        'Standard (IPv4 Unicast)': {
                                            'mt_id': 'Standard (IPv4 Unicast)',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:db8:10:2::/64': {
                                            'ip_prefix': '2001:db8:10:2::',
                                            'metric': 10,
                                            'prefix_len': '64',
                                        },
                                        '2001:db8:10:3::/64': {
                                            'ip_prefix': '2001:db8:10:3::',
                                            'metric': 10,
                                            'prefix_len': '64',
                                        },
                                        '2001:db8:3:3:3::3/128': {
                                            'ip_prefix': '2001:db8:3:3:3::3',
                                            'metric': 10,
                                            'prefix_len': '128',
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R3.01': {
                                            'metric': 10,
                                            'mt_id': 'MT (IPv6 Unicast)',
                                            'neighbor_id': 'R3.01',
                                        },
                                        'R3.05': {
                                            'metric': 10,
                                            'mt_id': 'MT (IPv6 Unicast)',
                                            'neighbor_id': 'R3.05',
                                        },
                                        'R4.03': {
                                            'metric': 10,
                                            'mt_id': 'MT (IPv6 Unicast)',
                                            'neighbor_id': 'R4.03',
                                        },
                                    },
                                    'remaining_lifetime': 402,
                                    'sequence': '0x000003bd',
                                },
                                'R3.01-00': {
                                    'checksum': '0x1591',
                                    'extended_is_neighbor': {
                                        'R3.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R3.00',
                                        },
                                        'R5.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R5.00',
                                        },
                                    },
                                    'lsp_id': 'R3.01-00',
                                    'remaining_lifetime': 1195,
                                    'sequence': '0x000003bf',
                                },
                                'R3.05-00': {
                                    'checksum': '0x073c',
                                    'extended_is_neighbor': {
                                        'R3.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R3.00',
                                        },
                                        'R6.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R6.00',
                                        },
                                    },
                                    'lsp_id': 'R3.05-00',
                                    'remaining_lifetime': 1005,
                                    'sequence': '0x000003b8',
                                },
                                'R4.00-00': {
                                    'checksum': '0x73d0',
                                    'dynamic_hostname': 'R4',
                                    'extended_ipv4_reachability': {
                                        '10.3.4.0/24': {
                                            'ip_prefix': '10.3.4.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                        },
                                        '10.4.5.0/24': {
                                            'ip_prefix': '10.4.5.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                        },
                                        '4.4.4.4/32': {
                                            'ip_prefix': '4.4.4.4',
                                            'metric': 10,
                                            'prefix_len': '32',
                                        },
                                    },
                                    'extended_is_neighbor': {
                                        'R4.03': {
                                            'metric': 10,
                                            'neighbor_id': 'R4.03',
                                        },
                                        'R5.02': {
                                            'metric': 10,
                                            'neighbor_id': 'R5.02',
                                        },
                                    },
                                    'ipv4_addresses': ['4.4.4.4'],
                                    'ipv6_addresses': ['2001:db8:4:4:4::4'],
                                    'lsp_id': 'R4.00-00',
                                    'mt_entries': {
                                        'IPv6 Unicast': {
                                            'mt_id': 'IPv6 Unicast',
                                        },
                                        'Standard (IPv4 Unicast)': {
                                            'mt_id': 'Standard (IPv4 Unicast)',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:db8:10:3::/64': {
                                            'ip_prefix': '2001:db8:10:3::',
                                            'metric': 10,
                                            'prefix_len': '64',
                                        },
                                        '2001:db8:10:4::/64': {
                                            'ip_prefix': '2001:db8:10:4::',
                                            'metric': 10,
                                            'prefix_len': '64',
                                        },
                                        '2001:db8:4:4:4::4/128': {
                                            'ip_prefix': '2001:db8:4:4:4::4',
                                            'metric': 10,
                                            'prefix_len': '128',
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R4.03': {
                                            'metric': 10,
                                            'mt_id': 'MT (IPv6 Unicast)',
                                            'neighbor_id': 'R4.03',
                                        },
                                        'R5.02': {
                                            'metric': 10,
                                            'mt_id': 'MT (IPv6 Unicast)',
                                            'neighbor_id': 'R5.02',
                                        },
                                    },
                                    'remaining_lifetime': 1087,
                                    'sequence': '0x000003be',
                                },
                                'R4.03-00': {
                                    'checksum': '0x7d32',
                                    'extended_is_neighbor': {
                                        'R3.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R3.00',
                                        },
                                        'R4.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R4.00',
                                        },
                                    },
                                    'lsp_id': 'R4.03-00',
                                    'remaining_lifetime': 1011,
                                    'sequence': '0x000003b6',
                                },
                                'R5.00-00': {
                                    'checksum': '0x0912',
                                    'dynamic_hostname': 'R5',
                                    'extended_ipv4_reachability': {
                                        '10.3.5.0/24': {
                                            'ip_prefix': '10.3.5.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                        },
                                        '10.4.5.0/24': {
                                            'ip_prefix': '10.4.5.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                        },
                                        '10.5.7.0/24': {
                                            'ip_prefix': '10.5.7.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                        },
                                        '5.5.5.5/32': {
                                            'ip_prefix': '5.5.5.5',
                                            'metric': 10,
                                            'prefix_len': '32',
                                        },
                                    },
                                    'extended_is_neighbor': {
                                        'R3.01': {
                                            'metric': 10,
                                            'neighbor_id': 'R3.01',
                                        },
                                        'R5.02': {
                                            'metric': 10,
                                            'neighbor_id': 'R5.02',
                                        },
                                        'R5.03': {
                                            'metric': 10,
                                            'neighbor_id': 'R5.03',
                                        },
                                    },
                                    'ipv4_addresses': ['5.5.5.5'],
                                    'ipv6_addresses': ['2001:db8:5:5:5::5'],
                                    'lsp_id': 'R5.00-00',
                                    'mt_entries': {
                                        'IPv6 Unicast': {
                                            'attributes': '1',
                                            'mt_id': 'IPv6 Unicast',
                                        },
                                        'Standard (IPv4 Unicast)': {
                                            'mt_id': 'Standard (IPv4 Unicast)',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:db8:10:3::/64': {
                                            'ip_prefix': '2001:db8:10:3::',
                                            'metric': 10,
                                            'prefix_len': '64',
                                        },
                                        '2001:db8:10:4::/64': {
                                            'ip_prefix': '2001:db8:10:4::',
                                            'metric': 10,
                                            'prefix_len': '64',
                                        },
                                        '2001:db8:10:5::/64': {
                                            'ip_prefix': '2001:db8:10:5::',
                                            'metric': 10,
                                            'prefix_len': '64',
                                        },
                                        '2001:db8:5:5:5::5/128': {
                                            'ip_prefix': '2001:db8:5:5:5::5',
                                            'metric': 10,
                                            'prefix_len': '128',
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R3.01': {
                                            'metric': 10,
                                            'mt_id': 'MT (IPv6 Unicast)',
                                            'neighbor_id': 'R3.01',
                                        },
                                        'R5.02': {
                                            'metric': 10,
                                            'mt_id': 'MT (IPv6 Unicast)',
                                            'neighbor_id': 'R5.02',
                                        },
                                        'R5.03': {
                                            'metric': 10,
                                            'mt_id': 'MT (IPv6 Unicast)',
                                            'neighbor_id': 'R5.03',
                                        },
                                    },
                                    'remaining_lifetime': 490,
                                    'sequence': '0x000003b8',
                                },
                                'R5.02-00': {
                                    'checksum': '0xce21',
                                    'extended_is_neighbor': {
                                        'R4.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R4.00',
                                        },
                                        'R5.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R5.00',
                                        },
                                    },
                                    'lsp_id': 'R5.02-00',
                                    'remaining_lifetime': 613,
                                    'sequence': '0x000003b9',
                                },
                                'R5.03-00': {
                                    'checksum': '0xc5f4',
                                    'extended_is_neighbor': {
                                        'R5.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R5.00',
                                        },
                                        'R7.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R7.00',
                                        },
                                    },
                                    'lsp_id': 'R5.03-00',
                                    'remaining_lifetime': 839,
                                    'sequence': '0x000003ba',
                                },
                                'R6.00-00': {
                                    'checksum': '0x73c5',
                                    'dynamic_hostname': 'R6',
                                    'extended_ipv4_reachability': {
                                        '10.3.6.0/24': {
                                            'ip_prefix': '10.3.6.0',
                                            'metric': 40,
                                            'prefix_len': '24',
                                        },
                                        '10.6.7.0/24': {
                                            'ip_prefix': '10.6.7.0',
                                            'metric': 40,
                                            'prefix_len': '24',
                                        },
                                        '6.6.6.0/24': {
                                            'ip_prefix': '6.6.6.0',
                                            'metric': 1,
                                            'prefix_len': '24',
                                        },
                                    },
                                    'extended_is_neighbor': {
                                        'R3.05': {
                                            'metric': 40,
                                            'neighbor_id': 'R3.05',
                                        },
                                        'R7.02': {
                                            'metric': 40,
                                            'neighbor_id': 'R7.02',
                                        },
                                    },
                                    'ipv4_addresses': ['6.6.6.6'],
                                    'lsp_id': 'R6.00-00',
                                    'mt_entries': {
                                        'IPv6 Unicast': {
                                            'mt_id': 'IPv6 Unicast',
                                        },
                                        'Standard (IPv4 Unicast)': {
                                            'mt_id': 'Standard (IPv4 Unicast)',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:db8:10:3::/64': {
                                            'ip_prefix': '2001:db8:10:3::',
                                            'metric': 40,
                                            'prefix_len': '64',
                                        },
                                        '2001:db8:10:6::/64': {
                                            'ip_prefix': '2001:db8:10:6::',
                                            'metric': 40,
                                            'prefix_len': '64',
                                        },
                                        '2001:db8:6:6:6::6/128': {
                                            'ip_prefix': '2001:db8:6:6:6::6',
                                            'metric': 1,
                                            'prefix_len': '128',
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R3.05': {
                                            'metric': 40,
                                            'mt_id': 'MT (IPv6 Unicast)',
                                            'neighbor_id': 'R3.05',
                                        },
                                        'R7.02': {
                                            'metric': 40,
                                            'mt_id': 'MT (IPv6 Unicast)',
                                            'neighbor_id': 'R7.02',
                                        },
                                    },
                                    'remaining_lifetime': 1055,
                                    'sequence': '0x0000054b',
                                },
                                'R7.00-00': {
                                    'checksum': '0x0ef9',
                                    'dynamic_hostname': 'R7',
                                    'extended_ipv4_reachability': {
                                        '10.5.7.0/24': {
                                            'ip_prefix': '10.5.7.0',
                                            'metric': 40,
                                            'prefix_len': '24',
                                        },
                                        '10.6.7.0/24': {
                                            'ip_prefix': '10.6.7.0',
                                            'metric': 40,
                                            'prefix_len': '24',
                                        },
                                        '10.7.9.0/24': {
                                            'ip_prefix': '10.7.9.0',
                                            'metric': 40,
                                            'prefix_len': '24',
                                        },
                                        '7.7.7.7/32': {
                                            'ip_prefix': '7.7.7.7',
                                            'metric': 1,
                                            'prefix_len': '32',
                                        },
                                    },
                                    'extended_is_neighbor': {
                                        'R5.03': {
                                            'metric': 40,
                                            'neighbor_id': 'R5.03',
                                        },
                                        'R7.02': {
                                            'metric': 40,
                                            'neighbor_id': 'R7.02',
                                        },
                                    },
                                    'ipv4_addresses': ['7.7.7.7'],
                                    'lsp_id': 'R7.00-00',
                                    'mt_entries': {
                                        'IPv6 Unicast': {
                                            'mt_id': 'IPv6 Unicast',
                                        },
                                        'Standard (IPv4 Unicast)': {
                                            'mt_id': 'Standard (IPv4 Unicast)',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:db8:10:5::/64': {
                                            'ip_prefix': '2001:db8:10:5::',
                                            'metric': 40,
                                            'prefix_len': '64',
                                        },
                                        '2001:db8:10:6::/64': {
                                            'ip_prefix': '2001:db8:10:6::',
                                            'metric': 40,
                                            'prefix_len': '64',
                                        },
                                        '2001:db8:10:77::/64': {
                                            'ip_prefix': '2001:db8:10:77::',
                                            'metric': 40,
                                            'prefix_len': '64',
                                        },
                                        '2001:db8:7:7:7::7/128': {
                                            'ip_prefix': '2001:db8:7:7:7::7',
                                            'metric': 1,
                                            'prefix_len': '128',
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R5.03': {
                                            'metric': 40,
                                            'mt_id': 'MT (IPv6 Unicast)',
                                            'neighbor_id': 'R5.03',
                                        },
                                        'R7.02': {
                                            'metric': 40,
                                            'mt_id': 'MT (IPv6 Unicast)',
                                            'neighbor_id': 'R7.02',
                                        },
                                    },
                                    'remaining_lifetime': 894,
                                    'sequence': '0x0000054f',
                                },
                                'R7.02-00': {
                                    'checksum': '0xf08d',
                                    'extended_is_neighbor': {
                                        'R6.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R6.00',
                                        },
                                        'R7.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R7.00',
                                        },
                                    },
                                    'lsp_id': 'R7.02-00',
                                    'remaining_lifetime': 1108,
                                    'sequence': '0x0000054b',
                                },
                            },
                        },
                    },
                },
            },
        },
    }
