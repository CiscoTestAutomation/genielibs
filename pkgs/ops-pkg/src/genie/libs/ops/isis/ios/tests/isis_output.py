""" 
Isis Genie Ops Object Outputs for IOS.
"""


class IsisOutput(object):
    showRunSectionIsis = {
        'instance': {
            'test': {
                'vrf': {'default': {}}},
            'test1': {
                'vrf': {'VRF1': {}}}
        }
    }

    showIsisHostname = """\
        show isis hostname
        Level  System ID      Dynamic Hostname  (test)
        2     2222.2222.2222 R2_xr
        2     3333.3333.3333 R3_nx
            * 1111.1111.1111 R1_xe
        Level  System ID      Dynamic Hostname  (test1)
        2     3333.3333.3333 R3_nx
            * 1111.1111.1111 R1_xe
    """

    showIsisLspLog = """\
        show isis lsp-log
        Tag test:

          Level 1 LSP log
          When       Count             Interface         Triggers
        3d04h           5                            CONFIG OTVINFOCHG
        3d04h           2     GigabitEthernet2.115   IFDOWN
        3d04h           2     GigabitEthernet3.115   NEWADJ DIS
        3d04h           3     GigabitEthernet2.115   NEWADJ DIS IPV6IA ADJMTIDCHG

          Level 2 LSP log
          When       Count             Interface         Triggers
        3d04h           5                            CONFIG OTVINFOCHG
        3d04h           2     GigabitEthernet2.115   IFDOWN
        3d04h           2     GigabitEthernet3.115   NEWADJ IPIA IPV6IA
        3d04h           2     GigabitEthernet3.115   NEWADJ DIS
        3d04h           5     GigabitEthernet2.115   NEWADJ IPIA IPV6IA ADJMTIDCHG
        3d04h           2     GigabitEthernet2.115   NEWADJ DIS
        3d04h           1                            IPEXT

        Tag test1:

          Level 1 LSP log
          When       Count             Interface         Triggers
        3d04h           5                            CONFIG OTVINFOCHG
        3d04h           2     GigabitEthernet2.415   IFDOWN
        3d04h           3     GigabitEthernet3.415   NEWADJ DIS ADJMTIDCHG

          Level 2 LSP log
          When       Count             Interface         Triggers
        3d04h           5                            CONFIG OTVINFOCHG
        3d04h           2     GigabitEthernet2.415   IFDOWN
        3d04h           2     GigabitEthernet3.415   NEWADJ IPIA IPV6IA ADJMTIDCHG
        3d04h           2     GigabitEthernet3.415   NEWADJ DIS
    """

    showIsisDatabaseDetail = """\
        show isis database detail

        Tag test:
        IS-IS Level-1 Link State Database:
        LSPID                 LSP Seq Num  LSP Checksum  LSP Holdtime/Rcvd      ATT/P/OL
        R1_xe.00-00         * 0x00000163   0x94AB                 820/*         0/0/0
          Area Address: 49.0001
          NLPID:        0xCC 0x8E
          Topology:     IPv4 (0x0)
                        IPv6 (0x2)
          Hostname: R1_xe
          Metric: 10         IS-Extended R1_xe.02
          Metric: 10         IS (MT-IPv6) R1_xe.02
          Metric: 10         IS-Extended R1_xe.01
          Metric: 10         IS (MT-IPv6) R1_xe.01
          IP Address:   10.13.115.1
          Metric: 10         IP 10.12.115.0/24
          Metric: 10         IP 10.13.115.0/24
          IPv6 Address: 2001:10:13:115::1
          Metric: 10         IPv6 (MT-IPv6) 2001:10:12:115::/64
          Metric: 10         IPv6 (MT-IPv6) 2001:10:13:115::/64
        R1_xe.01-00         * 0x0000015C   0xFC53                 760/*         0/0/0
          Metric: 0          IS-Extended R1_xe.00
          Metric: 0          IS-Extended R2_xr.00
        R1_xe.02-00         * 0x0000015D   0xF3F3                 472/*         0/0/0
          Metric: 0          IS-Extended R1_xe.00
          Metric: 0          IS-Extended R3_nx.00
        R2_xr.00-00           0x00000166   0x3C94                 979/1200      0/0/0
          Area Address: 49.0001
          Metric: 10         IS-Extended R1_xe.01
          Metric: 10         IS-Extended R2_xr.03
          NLPID:        0xCC 0x8E
          IP Address:   2.2.2.2
          Metric: 10         IP 2.2.2.2/32
          Metric: 10         IP 10.12.115.0/24
          Metric: 10         IP 10.23.115.0/24
          Hostname: R2_xr
          Metric: 10         IS (MT-IPv6) R1_xe.01
          Metric: 10         IS (MT-IPv6) R2_xr.03
          IPv6 Address: 2001:2:2:2::2
          Metric: 10         IPv6 (MT-IPv6) 2001:2:2:2::2/128
          Metric: 10         IPv6 (MT-IPv6) 2001:10:12:115::/64
          Metric: 10         IPv6 (MT-IPv6) 2001:10:23:115::/64
          Topology:     IPv4 (0x0)
                        IPv6 (0x2)
        R2_xr.03-00           0x0000015E   0x6938                 884/1200      0/0/0
          Metric: 0          IS-Extended R2_xr.00
          Metric: 0          IS-Extended R3_nx.00
        R3_nx.00-00           0x000001F6   0xB985                 978/1199      0/0/0
          Area Address: 49.0001
          NLPID:        0xCC 0x8E
          Router ID:    3.3.3.3
          IP Address:   3.3.3.3
          Topology:     IPv6 (0x2)
                        IPv4 (0x0)
          Hostname: R3_nx
          Metric: 40         IS (MT-IPv6) R2_xr.03
          Metric: 40         IS (MT-IPv6) R1_xe.02
          Metric: 40         IS-Extended R2_xr.03
          Metric: 40         IS-Extended R1_xe.02
          Metric: 1          IP 3.3.3.3/32
          Metric: 40         IP 10.13.115.0/24
          Metric: 40         IP 10.23.115.0/24
          Metric: 1          IPv6 (MT-IPv6) 2001:3:3:3::3/128
          Metric: 40         IPv6 (MT-IPv6) 2001:10:13:115::/64
          Metric: 40         IPv6 (MT-IPv6) 2001:10:23:115::/64
        IS-IS Level-2 Link State Database:
        LSPID                 LSP Seq Num  LSP Checksum  LSP Holdtime/Rcvd      ATT/P/OL
        R1_xe.00-00         * 0x00000164   0x9818                1075/*         0/0/0
          Area Address: 49.0001
          NLPID:        0xCC 0x8E
          Topology:     IPv4 (0x0)
                        IPv6 (0x2)
          Hostname: R1_xe
          Metric: 10         IS-Extended R1_xe.02
          Metric: 10         IS (MT-IPv6) R1_xe.02
          Metric: 10         IS-Extended R1_xe.01
          Metric: 10         IS (MT-IPv6) R1_xe.01
          IP Address:   10.13.115.1
          Metric: 10         IP 10.12.115.0/24
          Metric: 10         IP 10.13.115.0/24
          Metric: 20         IP 10.23.115.0/24
          IPv6 Address: 2001:10:13:115::1
          Metric: 10         IPv6 (MT-IPv6) 2001:10:12:115::/64
          Metric: 10         IPv6 (MT-IPv6) 2001:10:13:115::/64
          Metric: 20         IPv6 (MT-IPv6) 2001:10:23:115::/64
        R1_xe.01-00         * 0x0000015D   0x13C4                 916/*         0/0/0
          Metric: 0          IS-Extended R1_xe.00
          Metric: 0          IS-Extended R2_xr.00
        R1_xe.02-00         * 0x00000164   0xFD6B                 635/*         0/0/0
          Metric: 0          IS-Extended R1_xe.00
          Metric: 0          IS-Extended R3_nx.00
        R2_xr.00-00           0x00000165   0x8ACA                 345/1200      0/0/0
          Area Address: 49.0001
          Metric: 10         IS-Extended R1_xe.01
          Metric: 10         IS-Extended R2_xr.03
          NLPID:        0xCC 0x8E
          IP Address:   2.2.2.2
          Metric: 10         IP 2.2.2.2/32
          Metric: 10         IP 10.12.115.0/24
          Metric: 10         IP 10.23.115.0/24
          Metric: 11         IP 3.3.3.3/32
          Metric: 20         IP 10.13.115.0/24
          Hostname: R2_xr
          Metric: 10         IS (MT-IPv6) R1_xe.01
          Metric: 10         IS (MT-IPv6) R2_xr.03
          IPv6 Address: 2001:2:2:2::2
          Metric: 10         IPv6 (MT-IPv6) 2001:2:2:2::2/128
          Metric: 10         IPv6 (MT-IPv6) 2001:10:12:115::/64
          Metric: 10         IPv6 (MT-IPv6) 2001:10:23:115::/64
          Metric: 11         IPv6 (MT-IPv6) 2001:3:3:3::3/128
          Metric: 20         IPv6 (MT-IPv6) 2001:10:13:115::/64
          Topology:     IPv4 (0x0)
                        IPv6 (0x2)
        R2_xr.03-00           0x0000015E   0x6938                 947/1200      0/0/0
          Metric: 0          IS-Extended R2_xr.00
          Metric: 0          IS-Extended R3_nx.00
        R3_nx.00-00           0x000001F4   0xBD83                 697/1199      0/0/0
          Area Address: 49.0001
          NLPID:        0xCC 0x8E
          Router ID:    3.3.3.3
          IP Address:   3.3.3.3
          Topology:     IPv6 (0x2)
                        IPv4 (0x0)
          Hostname: R3_nx
          Metric: 40         IS (MT-IPv6) R2_xr.03
          Metric: 40         IS (MT-IPv6) R1_xe.02
          Metric: 40         IS-Extended R2_xr.03
          Metric: 40         IS-Extended R1_xe.02
          Metric: 1          IP 3.3.3.3/32
          Metric: 40         IP 10.13.115.0/24
          Metric: 40         IP 10.23.115.0/24
          Metric: 1          IPv6 (MT-IPv6) 2001:3:3:3::3/128
          Metric: 40         IPv6 (MT-IPv6) 2001:10:13:115::/64
          Metric: 40         IPv6 (MT-IPv6) 2001:10:23:115::/64

        Tag test1:
        IS-IS Level-1 Link State Database:
        LSPID                 LSP Seq Num  LSP Checksum  LSP Holdtime/Rcvd      ATT/P/OL
        R1_xe.00-00         * 0x00000161   0xAC87                 892/*         0/0/0
          Area Address: 49.0001
          NLPID:        0xCC 0x8E
          Topology:     IPv4 (0x0)
                        IPv6 (0x2)
          Hostname: R1_xe
          Metric: 10         IS-Extended R1_xe.02
          Metric: 10         IS (MT-IPv6) R1_xe.02
          IP Address:   10.13.115.1
          Metric: 10         IP 10.12.115.0/24
          Metric: 10         IP 10.13.115.0/24
          IPv6 Address: 2001:10:13:115::1
          Metric: 10         IPv6 (MT-IPv6) 2001:10:12:115::/64
          Metric: 10         IPv6 (MT-IPv6) 2001:10:13:115::/64
        R1_xe.02-00         * 0x0000015F   0xEFF5                 719/*         0/0/0
          Metric: 0          IS-Extended R1_xe.00
          Metric: 0          IS-Extended R3_nx.00
        R3_nx.00-00           0x000001F4   0xAE98                1170/1199      0/0/0
          Area Address: 49.0001
          NLPID:        0xCC 0x8E
          Router ID:    3.3.3.3
          IP Address:   3.3.3.3
          Topology:     IPv6 (0x2)
                        IPv4 (0x0)
          Hostname: R3_nx
          Metric: 40         IS (MT-IPv6) R1_xe.02
          Metric: 40         IS-Extended R1_xe.02
          Metric: 1          IP 3.3.3.3/32
          Metric: 40         IP 10.13.115.0/24
          Metric: 40         IP 10.23.115.0/24
          Metric: 1          IPv6 (MT-IPv6) 2001:3:3:3::3/128
          Metric: 40         IPv6 (MT-IPv6) 2001:10:13:115::/64
          Metric: 40         IPv6 (MT-IPv6) 2001:10:23:115::/64
        IS-IS Level-2 Link State Database:
        LSPID                 LSP Seq Num  LSP Checksum  LSP Holdtime/Rcvd      ATT/P/OL
        R1_xe.00-00         * 0x00000161   0x0C5D                 844/*         0/0/0
          Area Address: 49.0001
          NLPID:        0xCC 0x8E
          Topology:     IPv4 (0x0)
                        IPv6 (0x2)
          Hostname: R1_xe
          Metric: 10         IS-Extended R1_xe.02
          Metric: 10         IS (MT-IPv6) R1_xe.02
          IP Address:   10.13.115.1
          Metric: 10         IP 10.12.115.0/24
          Metric: 10         IP 10.13.115.0/24
          Metric: 50         IP 10.23.115.0/24
          IPv6 Address: 2001:10:13:115::1
          Metric: 10         IPv6 (MT-IPv6) 2001:10:12:115::/64
          Metric: 10         IPv6 (MT-IPv6) 2001:10:13:115::/64
          Metric: 50         IPv6 (MT-IPv6) 2001:10:23:115::/64
        R1_xe.02-00         * 0x00000160   0x0667                 612/*         0/0/0
          Metric: 0          IS-Extended R1_xe.00
          Metric: 0          IS-Extended R3_nx.00
        R3_nx.00-00           0x000001F4   0xAE98                 928/1199      0/0/0
          Area Address: 49.0001
          NLPID:        0xCC 0x8E
          Router ID:    3.3.3.3
          IP Address:   3.3.3.3
          Topology:     IPv6 (0x2)
                        IPv4 (0x0)
          Hostname: R3_nx
          Metric: 40         IS (MT-IPv6) R1_xe.02
          Metric: 40         IS-Extended R1_xe.02
          Metric: 1          IP 3.3.3.3/32
          Metric: 40         IP 10.13.115.0/24
          Metric: 40         IP 10.23.115.0/24
          Metric: 1          IPv6 (MT-IPv6) 2001:3:3:3::3/128
          Metric: 40         IPv6 (MT-IPv6) 2001:10:13:115::/64
          Metric: 40         IPv6 (MT-IPv6) 2001:10:23:115::/64
    """

    showClnsInterface = """\
        show clns interface
        GigabitEthernet1 is up, line protocol is up
          CLNS protocol processing disabled
        GigabitEthernet2 is up, line protocol is up
          CLNS protocol processing disabled
        GigabitEthernet2.90 is up, line protocol is up
          CLNS protocol processing disabled
        GigabitEthernet2.110 is up, line protocol is up
          CLNS protocol processing disabled
        GigabitEthernet2.115 is up, line protocol is up
          Checksums enabled, MTU 1497, Encapsulation SAP
          ERPDUs enabled, min. interval 10 msec.
          CLNS fast switching enabled
          CLNS SSE switching disabled
          DEC compatibility mode OFF for this interface
          Next ESH/ISH in 17 seconds
          Routing Protocol: IS-IS (test)
            Circuit Type: level-1-2
            Interface number 0x0, local circuit ID 0x1
            Neighbor Extended Local Circuit ID: 0x0
            Level-1 Metric: 10, Priority: 64, Circuit ID: R1_xe.01
            DR ID: R1_xe.01
            Level-1 IPv6 Metric: 10
            Number of active level-1 adjacencies: 1
            Level-2 Metric: 10, Priority: 64, Circuit ID: R1_xe.01
            DR ID: R1_xe.01
            Level-2 IPv6 Metric: 10
            Number of active level-2 adjacencies: 1
            Next IS-IS LAN Level-1 Hello in 1 seconds
            Next IS-IS LAN Level-2 Hello in 1 seconds
        GigabitEthernet2.120 is up, line protocol is up
          CLNS protocol processing disabled
        GigabitEthernet2.390 is up, line protocol is up
          CLNS protocol processing disabled
        GigabitEthernet2.410 is up, line protocol is up
          CLNS protocol processing disabled
        GigabitEthernet2.415 is up, line protocol is up
          Checksums enabled, MTU 1497, Encapsulation SAP
          ERPDUs enabled, min. interval 10 msec.
          CLNS fast switching enabled
          CLNS SSE switching disabled
          DEC compatibility mode OFF for this interface
          Next ESH/ISH in 17 seconds
          Routing Protocol: IS-IS (test1)
            Circuit Type: level-1-2
            Interface number 0x0, local circuit ID 0x1
            Neighbor Extended Local Circuit ID: 0x0
            Level-1 Metric: 10, Priority: 64, Circuit ID: R1_xe.01
            DR ID: 0000.0000.0000.00
            Level-1 IPv6 Metric: 10
            Number of active level-1 adjacencies: 0
            Level-2 Metric: 10, Priority: 64, Circuit ID: R1_xe.01
            DR ID: 0000.0000.0000.00
            Level-2 IPv6 Metric: 10
            Number of active level-2 adjacencies: 0
            Next IS-IS LAN Level-1 Hello in 2 seconds
            Next IS-IS LAN Level-2 Hello in 1 seconds
        GigabitEthernet2.420 is up, line protocol is up
          CLNS protocol processing disabled
        GigabitEthernet3 is up, line protocol is up
          CLNS protocol processing disabled
        GigabitEthernet3.90 is up, line protocol is up
          CLNS protocol processing disabled
        GigabitEthernet3.110 is up, line protocol is up
          CLNS protocol processing disabled
        GigabitEthernet3.115 is up, line protocol is up
          Checksums enabled, MTU 1497, Encapsulation SAP
          ERPDUs enabled, min. interval 10 msec.
          CLNS fast switching enabled
          CLNS SSE switching disabled
          DEC compatibility mode OFF for this interface
          Next ESH/ISH in 39 seconds
          Routing Protocol: IS-IS (test)
            Circuit Type: level-1-2
            Interface number 0x1, local circuit ID 0x2
            Neighbor Extended Local Circuit ID: 0x0
            Level-1 Metric: 10, Priority: 64, Circuit ID: R1_xe.02
            DR ID: R1_xe.02
            Level-1 IPv6 Metric: 10
            Number of active level-1 adjacencies: 1
            Level-2 Metric: 10, Priority: 64, Circuit ID: R1_xe.02
            DR ID: R1_xe.02
            Level-2 IPv6 Metric: 10
            Number of active level-2 adjacencies: 1
            Next IS-IS LAN Level-1 Hello in 2 seconds
            Next IS-IS LAN Level-2 Hello in 93 milliseconds
        GigabitEthernet3.120 is up, line protocol is up
          CLNS protocol processing disabled
        GigabitEthernet3.390 is up, line protocol is up
          CLNS protocol processing disabled
        GigabitEthernet3.410 is up, line protocol is up
          CLNS protocol processing disabled
        GigabitEthernet3.415 is up, line protocol is up
          Checksums enabled, MTU 1497, Encapsulation SAP
          ERPDUs enabled, min. interval 10 msec.
          CLNS fast switching enabled
          CLNS SSE switching disabled
          DEC compatibility mode OFF for this interface
          Next ESH/ISH in 8 seconds
          Routing Protocol: IS-IS (test1)
            Circuit Type: level-1-2
            Interface number 0x1, local circuit ID 0x2
            Neighbor Extended Local Circuit ID: 0x0
            Level-1 Metric: 10, Priority: 64, Circuit ID: R1_xe.02
            DR ID: R1_xe.02
            Level-1 IPv6 Metric: 10
            Number of active level-1 adjacencies: 1
            Level-2 Metric: 10, Priority: 64, Circuit ID: R1_xe.02
            DR ID: R1_xe.02
            Level-2 IPv6 Metric: 10
            Number of active level-2 adjacencies: 1
            Next IS-IS LAN Level-1 Hello in 2 seconds
            Next IS-IS LAN Level-2 Hello in 78 milliseconds
        GigabitEthernet3.420 is up, line protocol is up
          CLNS protocol processing disabled
        GigabitEthernet4 is up, line protocol is up
          CLNS protocol processing disabled
        GigabitEthernet5 is up, line protocol is up
          CLNS protocol processing disabled
        GigabitEthernet6 is up, line protocol is up
          CLNS protocol processing disabled
        GigabitEthernet7 is up, line protocol is up
          CLNS protocol processing disabled
        Loopback0 is up, line protocol is up
          CLNS protocol processing disabled
        Loopback300 is up, line protocol is up
          CLNS protocol processing disabled
        Port-channel12 is up, line protocol is up
          CLNS protocol processing disabled
        Port-channel13 is up, line protocol is up
          CLNS protocol processing disabled
        Tunnel0 is up, line protocol is up
          CLNS protocol processing disabled
        Tunnel1 is up, line protocol is up
          CLNS protocol processing disabled
        Tunnel2 is up, line protocol is up
          CLNS protocol processing disabled
        Tunnel3 is up, line protocol is up
          CLNS protocol processing disabled
        Tunnel4 is up, line protocol is up
          CLNS protocol processing disabled
        Tunnel5 is up, line protocol is up
          CLNS protocol processing disabled
        Tunnel6 is up, line protocol is up
          CLNS protocol processing disabled
        Tunnel7 is up, line protocol is up
          CLNS protocol processing disabled
        Tunnel8 is up, line protocol is up
          CLNS protocol processing disabled
        Tunnel9 is up, line protocol is up
          CLNS protocol processing disabled
        R1_xe#
    """

    showClnsProtocol = """\
        show clns protocol

        IS-IS Router: test (0x10000)
          System Id: 1111.1111.1111.00  IS-Type: level-1-2
          Manual area address(es):
                49.0001
          Routing for area address(es):
                49.0001
          Interfaces supported by IS-IS:
                GigabitEthernet3.115 - IP - IPv6
                GigabitEthernet2.115 - IP - IPv6
          Redistribute:
            static (on by default)
          Distance for L2 CLNS routes: 110
          RRR level: none
          Generate narrow metrics: none
          Accept narrow metrics:   none
          Generate wide metrics:   level-1-2
          Accept wide metrics:     level-1-2

        IS-IS Router: test1 (0x10001)
          System Id: 1111.1111.1111.00  IS-Type: level-1-2
          Manual area address(es):
                49.0001
          Routing for area address(es):
                49.0001
          Interfaces supported by IS-IS:
                GigabitEthernet3.415 - IP - IPv6
                GigabitEthernet2.415 - IP - IPv6
          Redistribute:
            static (on by default)
          Distance for L2 CLNS routes: 110
          RRR level: none
          Generate narrow metrics: none
          Accept narrow metrics:   none
          Generate wide metrics:   level-1-2
          Accept wide metrics:     level-1-2
    """

    showClnsNeighborsDetail = """\
        show clns neighbors detail

        Tag test:
        System Id       Interface     SNPA                State  Holdtime  Type Protocol
        R2_xr           Gi2.115       fa16.3e67.2452      Up     23        L1L2 M-ISIS
          Area Address(es): 49.0001
          IP Address(es):  10.12.115.2*
          IPv6 Address(es): FE80::F816:3EFF:FE67:2452
          Uptime: 3d04h
          NSF capable
          Topology: IPv4, IPv6
          Interface name: GigabitEthernet2.115
        R3_nx           Gi3.115       5e01.0002.0007      Up     29        L1L2 M-ISIS
          Area Address(es): 49.0001
          IP Address(es):  10.13.115.3*
          IPv6 Address(es): FE80::5C01:FF:FE02:7
          Uptime: 3d04h
          NSF capable
          Topology: IPv4, IPv6
          Interface name: GigabitEthernet3.115

        Tag test1:
        System Id       Interface     SNPA                State  Holdtime  Type Protocol
        2222.2222.2222  Gi2.415       fa16.3e67.2452      Init   29        L1L2 M-ISIS
          Area Address(es): 49.0001
          IP Address(es):  10.12.115.2*
          IPv6 Address(es): FE80::F816:3EFF:FE67:2452
          Uptime: 3d04h
          NSF capable
          Topology: IPv4, IPv6
          Interface name: GigabitEthernet2.415
        R3_nx           Gi3.415       5e01.0002.0007      Up     29        L1L2 M-ISIS
          Area Address(es): 49.0001
          IP Address(es):  10.13.115.3*
          IPv6 Address(es): FE80::5C01:FF:FE02:7
          Uptime: 3d04h
          NSF capable
          Topology: IPv4, IPv6
          Interface name: GigabitEthernet3.415
    """

    showClnsIsNeighborsDetail = """\
        show clns is-neighbors detail

        Tag test:
        System Id       Interface     State  Type Priority  Circuit Id         Format
        R2_xr           Gi2.115       Up     L1L2 64/64     R1_xe.01           Phase V
          Area Address(es): 49.0001
          IP Address(es):  10.12.115.2*
          IPv6 Address(es): FE80::F816:3EFF:FE67:2452
          Uptime: 3d04h
          NSF capable
          Topology: IPv4, IPv6
          Interface name: GigabitEthernet2.115
        R3_nx           Gi3.115       Up     L1L2 64/64     R1_xe.02           Phase V
          Area Address(es): 49.0001
          IP Address(es):  10.13.115.3*
          IPv6 Address(es): FE80::5C01:FF:FE02:7
          Uptime: 3d04h
          NSF capable
          Topology: IPv4, IPv6
          Interface name: GigabitEthernet3.115

        Tag test1:
        System Id       Interface     State  Type Priority  Circuit Id         Format
        2222.2222.2222  Gi2.415       Init   L1L2 128/128    2222.2222.2222.01  Phase V
          Area Address(es): 49.0001
          IP Address(es):  10.12.115.2*
          IPv6 Address(es): FE80::F816:3EFF:FE67:2452
          Uptime: 3d04h
          NSF capable
          Topology: IPv4, IPv6
          Interface name: GigabitEthernet2.415
        R3_nx           Gi3.415       Up     L1L2 64/64     R1_xe.02           Phase V
          Area Address(es): 49.0001
          IP Address(es):  10.13.115.3*
          IPv6 Address(es): FE80::5C01:FF:FE02:7
          Uptime: 3d04h
          NSF capable
          Topology: IPv4, IPv6
          Interface name: GigabitEthernet3.415
    """

    showClnsTraffic = """\
        show clns traffic
        CLNS:  Time since last clear: never
        CLNS & ESIS Output: 0, Input: 250750
        Dropped Protocol not enabled on interface: 0
        CLNS Local: 0, Forward: 0
        CLNS Discards:
          Hdr Syntax: 0, Checksum: 0, Lifetime: 0, Output cngstn: 0
          No Route: 0, Discard Route: 0, Dst Unreachable 0, Encaps. Failed: 0
          NLP Unknown: 0, Not an IS: 0
        CLNS Options: Packets 0, total 0 , bad 0, GQOS 0, cngstn exprncd 0
        CLNS Segments:  Segmented: 0, Failed: 0
        CLNS Broadcasts: sent: 0, rcvd: 0
        Echos: Rcvd 0 requests, 0 replies
              Sent 0 requests, 0 replies
        ESIS(sent/rcvd): ESHs: 0/0, ISHs: 0/0, RDs: 0/0, QCF: 0/0
        Tunneling (sent/rcvd): IP: 0/0, IPv6: 0/0
        Tunneling dropped (rcvd) IP/IPV6:  0
        ISO-IGRP: Querys (sent/rcvd): 0/0 Updates (sent/rcvd): 0/0
        ISO-IGRP: Router Hellos: (sent/rcvd): 0/0
        ISO-IGRP Syntax Errors: 0

        Tag test:
        IS-IS: Time since last clear: never
        IS-IS: Level-1 Hellos (sent/rcvd): 189455/61414
        IS-IS: Level-2 Hellos (sent/rcvd): 189420/61399
        IS-IS: PTP Hellos     (sent/rcvd): 0/0
        IS-IS: Level-1 LSPs sourced (new/refresh): 6/1047
        IS-IS: Level-2 LSPs sourced (new/refresh): 9/1053
        IS-IS: Level-1 LSPs flooded (sent/rcvd): 2814/1737
        IS-IS: Level-2 LSPs flooded (sent/rcvd): 2151/2381
        IS-IS: LSP Retransmissions: 0
        IS-IS: Level-1 CSNPs (sent/rcvd): 63099/0
        IS-IS: Level-2 CSNPs (sent/rcvd): 63076/0
        IS-IS: Level-1 PSNPs (sent/rcvd): 0/1
        IS-IS: Level-2 PSNPs (sent/rcvd): 0/1
        IS-IS: Level-1 DR Elections: 5
        IS-IS: Level-2 DR Elections: 4
        IS-IS: Level-1 SPF Calculations: 628
        IS-IS: Level-2 SPF Calculations: 630
        IS-IS: Level-1 Partial Route Calculations: 1
        IS-IS: Level-2 Partial Route Calculations: 4
        IS-IS: LSP checksum errors received: 0
        IS-IS: Update process queue depth: 0/200
        IS-IS: Update process packets dropped: 0

        Tag test1:
        IS-IS: Time since last clear: never
        IS-IS: Level-1 Hellos (sent/rcvd): 126381/61414
        IS-IS: Level-2 Hellos (sent/rcvd): 126368/61403
        IS-IS: PTP Hellos     (sent/rcvd): 0/0
        IS-IS: Level-1 LSPs sourced (new/refresh): 4/701
        IS-IS: Level-2 LSPs sourced (new/refresh): 5/701
        IS-IS: Level-1 LSPs flooded (sent/rcvd): 703/501
        IS-IS: Level-2 LSPs flooded (sent/rcvd): 703/499
        IS-IS: LSP Retransmissions: 0
        IS-IS: Level-1 CSNPs (sent/rcvd): 31587/0
        IS-IS: Level-2 CSNPs (sent/rcvd): 31589/0
        IS-IS: Level-1 PSNPs (sent/rcvd): 0/0
        IS-IS: Level-2 PSNPs (sent/rcvd): 0/0
        IS-IS: Level-1 DR Elections: 3
        IS-IS: Level-2 DR Elections: 3
        IS-IS: Level-1 SPF Calculations: 620
        IS-IS: Level-2 SPF Calculations: 620
        IS-IS: Level-1 Partial Route Calculations: 1
        IS-IS: Level-2 Partial Route Calculations: 3
        IS-IS: LSP checksum errors received: 0
        IS-IS: Update process queue depth: 0/200
        IS-IS: Update process packets dropped: 0
    """

    isisOpsOutput = {
        'instance': {
            'test': {
                'process_id': 'test',
                'vrf': {
                    'default': {
                        'area_address': ['49.0001'],
                        'enable': True,
                        'hostname_db': {
                            'hostname': {
                                '1111.1111.1111': {
                                    'hostname': 'R1_xe',
                                },
                                '2222.2222.2222': {
                                    'hostname': 'R2_xr',
                                },
                                '3333.3333.3333': {
                                    'hostname': 'R3_nx',
                                },
                            },
                        },
                        'interfaces': {
                            'GigabitEthernet2.115': {
                                'address_family': {
                                    'ipv4': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 10,
                                            },
                                            'level_2': {
                                                'metric': 10,
                                            },
                                        },
                                    },
                                    'ipv6': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 10,
                                            },
                                            'level_2': {
                                                'metric': 10,
                                            },
                                        },
                                    },
                                },
                                'adjacencies': {
                                    'R2_xr': {
                                        'neighbor_snpa': {
                                            'fa16.3e67.2452': {
                                                'level': {
                                                    'level-all': {
                                                        'hold_timer': 23,
                                                        'lastuptime': '3d04h',
                                                        'neighbor_extended_circuit_id': 'R1_xe.01',
                                                        'neighbor_priority': 64,
                                                        'state': 'Up',
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                'hello_interval': {
                                    'level_1': {
                                        'interval': 1,
                                    },
                                    'level_2': {
                                        'interval': 1,
                                    },
                                },
                                'level_type': 'level-1-2',
                                'name': 'GigabitEthernet2.115',
                                'priority': {
                                    'level_1': {
                                        'priority': 64,
                                    },
                                    'level_2': {
                                        'priority': 64,
                                    },
                                },
                                'topologies': {
                                    'ipv4': {
                                        'adjacencies': {
                                            'R2_xr': {
                                                'neighbor_snpa': {
                                                    'fa16.3e67.2452': {
                                                        'level': {
                                                            'level-all': {
                                                                'hold_timer': 23,
                                                                'lastuptime': '3d04h',
                                                                'neighbor_extended_circuit_id': 'R1_xe.01',
                                                                'neighbor_priority': 64,
                                                                'state': 'Up',
                                                            },
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                        'name': 'ipv4',
                                    },
                                    'ipv6': {
                                        'adjacencies': {
                                            'R2_xr': {
                                                'neighbor_snpa': {
                                                    'fa16.3e67.2452': {
                                                        'level': {
                                                            'level-all': {
                                                                'hold_timer': 23,
                                                                'lastuptime': '3d04h',
                                                                'neighbor_extended_circuit_id': 'R1_xe.01',
                                                                'neighbor_priority': 64,
                                                                'state': 'Up',
                                                            },
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                        'name': 'ipv6',
                                    },
                                },
                            },
                            'GigabitEthernet3.115': {
                                'address_family': {
                                    'ipv4': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 10,
                                            },
                                            'level_2': {
                                                'metric': 10,
                                            },
                                        },
                                    },
                                    'ipv6': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 10,
                                            },
                                            'level_2': {
                                                'metric': 10,
                                            },
                                        },
                                    },
                                },
                                'adjacencies': {
                                    'R3_nx': {
                                        'neighbor_snpa': {
                                            '5e01.0002.0007': {
                                                'level': {
                                                    'level-all': {
                                                        'hold_timer': 29,
                                                        'lastuptime': '3d04h',
                                                        'neighbor_extended_circuit_id': 'R1_xe.02',
                                                        'neighbor_priority': 64,
                                                        'state': 'Up',
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                'hello_interval': {
                                    'level_1': {
                                        'interval': 2,
                                    },
                                    'level_2': {
                                        'interval': 93,
                                    },
                                },
                                'level_type': 'level-1-2',
                                'name': 'GigabitEthernet3.115',
                                'priority': {
                                    'level_1': {
                                        'priority': 64,
                                    },
                                    'level_2': {
                                        'priority': 64,
                                    },
                                },
                                'topologies': {
                                    'ipv4': {
                                        'adjacencies': {
                                            'R3_nx': {
                                                'neighbor_snpa': {
                                                    '5e01.0002.0007': {
                                                        'level': {
                                                            'level-all': {
                                                                'hold_timer': 29,
                                                                'lastuptime': '3d04h',
                                                                'neighbor_extended_circuit_id': 'R1_xe.02',
                                                                'neighbor_priority': 64,
                                                                'state': 'Up',
                                                            },
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                        'name': 'ipv4',
                                    },
                                    'ipv6': {
                                        'adjacencies': {
                                            'R3_nx': {
                                                'neighbor_snpa': {
                                                    '5e01.0002.0007': {
                                                        'level': {
                                                            'level-all': {
                                                                'hold_timer': 29,
                                                                'lastuptime': '3d04h',
                                                                'neighbor_extended_circuit_id': 'R1_xe.02',
                                                                'neighbor_priority': 64,
                                                                'state': 'Up',
                                                            },
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                        'name': 'ipv6',
                                    },
                                },
                            },
                        },
                        'lsp_log': {
                            1: {
                                'change': 'CONFIG OTVINFOCHG',
                                'id': 1,
                                'level': 1,
                                'received_timestamp': '3d04h',
                            },
                            2: {
                                'change': 'IFDOWN',
                                'id': 2,
                                'level': 1,
                                'received_timestamp': '3d04h',
                            },
                            3: {
                                'change': 'NEWADJ DIS',
                                'id': 3,
                                'level': 1,
                                'received_timestamp': '3d04h',
                            },
                            4: {
                                'change': 'NEWADJ DIS IPV6IA ADJMTIDCHG',
                                'id': 4,
                                'level': 1,
                                'received_timestamp': '3d04h',
                            },
                            5: {
                                'change': 'CONFIG OTVINFOCHG',
                                'id': 5,
                                'level': 2,
                                'received_timestamp': '3d04h',
                            },
                            6: {
                                'change': 'IFDOWN',
                                'id': 6,
                                'level': 2,
                                'received_timestamp': '3d04h',
                            },
                            7: {
                                'change': 'NEWADJ IPIA IPV6IA',
                                'id': 7,
                                'level': 2,
                                'received_timestamp': '3d04h',
                            },
                            8: {
                                'change': 'NEWADJ DIS',
                                'id': 8,
                                'level': 2,
                                'received_timestamp': '3d04h',
                            },
                            9: {
                                'change': 'NEWADJ IPIA IPV6IA ADJMTIDCHG',
                                'id': 9,
                                'level': 2,
                                'received_timestamp': '3d04h',
                            },
                            10: {
                                'change': 'NEWADJ DIS',
                                'id': 10,
                                'level': 2,
                                'received_timestamp': '3d04h',
                            },
                            11: {
                                'change': 'IPEXT',
                                'id': 11,
                                'level': 2,
                                'received_timestamp': '3d04h',
                            },
                        },
                        'metric_type': {
                            'level_1': {
                                'value': 'wide-only',
                            },
                            'level_2': {
                                'value': 'wide-only',
                            },
                        },
                        'nsel': '00',
                        'system_counters': {
                            1: {
                                'level': 1,
                                'spf_runs': 628,
                            },
                            2: {
                                'level': 2,
                                'spf_runs': 630,
                            },
                        },
                        'system_id': '1111.1111.1111',
                        'vrf': 'default',
                    },
                },
            },
            'test1': {
                'process_id': 'test1',
                'vrf': {
                    'VRF1': {
                        'area_address': ['49.0001'],
                        'enable': True,
                        'hostname_db': {
                            'hostname': {
                                '1111.1111.1111': {
                                    'hostname': 'R1_xe',
                                },
                                '3333.3333.3333': {
                                    'hostname': 'R3_nx',
                                },
                            },
                        },
                        'interfaces': {
                            'GigabitEthernet2.415': {
                                'address_family': {
                                    'ipv4': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 10,
                                            },
                                            'level_2': {
                                                'metric': 10,
                                            },
                                        },
                                    },
                                    'ipv6': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 10,
                                            },
                                            'level_2': {
                                                'metric': 10,
                                            },
                                        },
                                    },
                                },
                                'adjacencies': {
                                    '2222.2222.2222': {
                                        'neighbor_snpa': {
                                            'fa16.3e67.2452': {
                                                'level': {
                                                    'level-all': {
                                                        'hold_timer': 29,
                                                        'lastuptime': '3d04h',
                                                        'neighbor_extended_circuit_id': '2222.2222.2222.01',
                                                        'neighbor_priority': 128,
                                                        'state': 'Init',
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                'hello_interval': {
                                    'level_1': {
                                        'interval': 2,
                                    },
                                    'level_2': {
                                        'interval': 1,
                                    },
                                },
                                'level_type': 'level-1-2',
                                'name': 'GigabitEthernet2.415',
                                'priority': {
                                    'level_1': {
                                        'priority': 64,
                                    },
                                    'level_2': {
                                        'priority': 64,
                                    },
                                },
                                'topologies': {
                                    'ipv4': {
                                        'adjacencies': {
                                            '2222.2222.2222': {
                                                'neighbor_snpa': {
                                                    'fa16.3e67.2452': {
                                                        'level': {
                                                            'level-all': {
                                                                'hold_timer': 29,
                                                                'lastuptime': '3d04h',
                                                                'neighbor_extended_circuit_id': '2222.2222.2222.01',
                                                                'neighbor_priority': 128,
                                                                'state': 'Init',
                                                            },
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                        'name': 'ipv4',
                                    },
                                    'ipv6': {
                                        'adjacencies': {
                                            '2222.2222.2222': {
                                                'neighbor_snpa': {
                                                    'fa16.3e67.2452': {
                                                        'level': {
                                                            'level-all': {
                                                                'hold_timer': 29,
                                                                'lastuptime': '3d04h',
                                                                'neighbor_extended_circuit_id': '2222.2222.2222.01',
                                                                'neighbor_priority': 128,
                                                                'state': 'Init',
                                                            },
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                        'name': 'ipv6',
                                    },
                                },
                            },
                            'GigabitEthernet3.415': {
                                'address_family': {
                                    'ipv4': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 10,
                                            },
                                            'level_2': {
                                                'metric': 10,
                                            },
                                        },
                                    },
                                    'ipv6': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 10,
                                            },
                                            'level_2': {
                                                'metric': 10,
                                            },
                                        },
                                    },
                                },
                                'adjacencies': {
                                    'R3_nx': {
                                        'neighbor_snpa': {
                                            '5e01.0002.0007': {
                                                'level': {
                                                    'level-all': {
                                                        'hold_timer': 29,
                                                        'lastuptime': '3d04h',
                                                        'neighbor_extended_circuit_id': 'R1_xe.02',
                                                        'neighbor_priority': 64,
                                                        'state': 'Up',
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                'hello_interval': {
                                    'level_1': {
                                        'interval': 2,
                                    },
                                    'level_2': {
                                        'interval': 78,
                                    },
                                },
                                'level_type': 'level-1-2',
                                'name': 'GigabitEthernet3.415',
                                'priority': {
                                    'level_1': {
                                        'priority': 64,
                                    },
                                    'level_2': {
                                        'priority': 64,
                                    },
                                },
                                'topologies': {
                                    'ipv4': {
                                        'adjacencies': {
                                            'R3_nx': {
                                                'neighbor_snpa': {
                                                    '5e01.0002.0007': {
                                                        'level': {
                                                            'level-all': {
                                                                'hold_timer': 29,
                                                                'lastuptime': '3d04h',
                                                                'neighbor_extended_circuit_id': 'R1_xe.02',
                                                                'neighbor_priority': 64,
                                                                'state': 'Up',
                                                            },
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                        'name': 'ipv4',
                                    },
                                    'ipv6': {
                                        'adjacencies': {
                                            'R3_nx': {
                                                'neighbor_snpa': {
                                                    '5e01.0002.0007': {
                                                        'level': {
                                                            'level-all': {
                                                                'hold_timer': 29,
                                                                'lastuptime': '3d04h',
                                                                'neighbor_extended_circuit_id': 'R1_xe.02',
                                                                'neighbor_priority': 64,
                                                                'state': 'Up',
                                                            },
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                        'name': 'ipv6',
                                    },
                                },
                            },
                        },
                        'lsp_log': {
                            1: {
                                'change': 'CONFIG OTVINFOCHG',
                                'id': 1,
                                'level': 1,
                                'received_timestamp': '3d04h',
                            },
                            2: {
                                'change': 'IFDOWN',
                                'id': 2,
                                'level': 1,
                                'received_timestamp': '3d04h',
                            },
                            3: {
                                'change': 'NEWADJ DIS ADJMTIDCHG',
                                'id': 3,
                                'level': 1,
                                'received_timestamp': '3d04h',
                            },
                            4: {
                                'change': 'CONFIG OTVINFOCHG',
                                'id': 4,
                                'level': 2,
                                'received_timestamp': '3d04h',
                            },
                            5: {
                                'change': 'IFDOWN',
                                'id': 5,
                                'level': 2,
                                'received_timestamp': '3d04h',
                            },
                            6: {
                                'change': 'NEWADJ IPIA IPV6IA ADJMTIDCHG',
                                'id': 6,
                                'level': 2,
                                'received_timestamp': '3d04h',
                            },
                            7: {
                                'change': 'NEWADJ DIS',
                                'id': 7,
                                'level': 2,
                                'received_timestamp': '3d04h',
                            },
                        },
                        'metric_type': {
                            'level_1': {
                                'value': 'wide-only',
                            },
                            'level_2': {
                                'value': 'wide-only',
                            },
                        },
                        'nsel': '00',
                        'system_counters': {
                            1: {
                                'level': 1,
                                'spf_runs': 620,
                            },
                            2: {
                                'level': 2,
                                'spf_runs': 620,
                            },
                        },
                        'system_id': '1111.1111.1111',
                        'vrf': 'VRF1',
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
                                'R1_xe.00-00': {
                                    'checksum': '0x94AB',
                                    'dynamic_hostname': 'R1_xe',
                                    'extended_is_neighbor': {
                                        'R1_xe.01': {
                                            'metric': 10,
                                            'neighbor_id': 'R1_xe.01',
                                        },
                                        'R1_xe.02': {
                                            'metric': 10,
                                            'neighbor_id': 'R1_xe.02',
                                        },
                                    },
                                    'ipv4_addresses': ['10.13.115.1'],
                                    'ipv4_internal_reachability': {
                                        '10.12.115.0/24': {
                                            'default_metric': 10,
                                            'ip_prefix': '10.12.115.0',
                                            'prefix_len': '24',
                                        },
                                        '10.13.115.0/24': {
                                            'default_metric': 10,
                                            'ip_prefix': '10.13.115.0',
                                            'prefix_len': '24',
                                        },
                                    },
                                    'ipv6_addresses': ['2001:10:13:115::1'],
                                    'lsp_id': 'R1_xe.00-00',
                                    'mt_entries': {
                                        'ipv4': {
                                            'attributes': '0x0',
                                            'mt_id': 'ipv4',
                                        },
                                        'ipv6': {
                                            'attributes': '0x2',
                                            'mt_id': 'ipv6',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:10:12:115::/64': {
                                            'ip_prefix': '2001:10:12:115::',
                                            'metric': 10,
                                            'prefix_len': '64',
                                        },
                                        '2001:10:13:115::/64': {
                                            'ip_prefix': '2001:10:13:115::',
                                            'metric': 10,
                                            'prefix_len': '64',
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R1_xe.01': {
                                            'metric': 10,
                                            'neighbor_id': 'R1_xe.01',
                                        },
                                        'R1_xe.02': {
                                            'metric': 10,
                                            'neighbor_id': 'R1_xe.02',
                                        },
                                    },
                                    'remaining_lifetime': 820,
                                    'sequence': '0x00000163',
                                },
                                'R1_xe.01-00': {
                                    'checksum': '0xFC53',
                                    'extended_is_neighbor': {
                                        'R1_xe.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R1_xe.00',
                                        },
                                        'R2_xr.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R2_xr.00',
                                        },
                                    },
                                    'lsp_id': 'R1_xe.01-00',
                                    'remaining_lifetime': 760,
                                    'sequence': '0x0000015C',
                                },
                                'R1_xe.02-00': {
                                    'checksum': '0xF3F3',
                                    'extended_is_neighbor': {
                                        'R1_xe.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R1_xe.00',
                                        },
                                        'R3_nx.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R3_nx.00',
                                        },
                                    },
                                    'lsp_id': 'R1_xe.02-00',
                                    'remaining_lifetime': 472,
                                    'sequence': '0x0000015D',
                                },
                                'R2_xr.00-00': {
                                    'checksum': '0x3C94',
                                    'dynamic_hostname': 'R2_xr',
                                    'extended_is_neighbor': {
                                        'R1_xe.01': {
                                            'metric': 10,
                                            'neighbor_id': 'R1_xe.01',
                                        },
                                        'R2_xr.03': {
                                            'metric': 10,
                                            'neighbor_id': 'R2_xr.03',
                                        },
                                    },
                                    'ipv4_addresses': ['2.2.2.2'],
                                    'ipv4_internal_reachability': {
                                        '10.12.115.0/24': {
                                            'default_metric': 10,
                                            'ip_prefix': '10.12.115.0',
                                            'prefix_len': '24',
                                        },
                                        '10.23.115.0/24': {
                                            'default_metric': 10,
                                            'ip_prefix': '10.23.115.0',
                                            'prefix_len': '24',
                                        },
                                        '2.2.2.2/32': {
                                            'default_metric': 10,
                                            'ip_prefix': '2.2.2.2',
                                            'prefix_len': '32',
                                        },
                                    },
                                    'ipv6_addresses': ['2001:2:2:2::2'],
                                    'lsp_id': 'R2_xr.00-00',
                                    'mt_entries': {
                                        'ipv4': {
                                            'attributes': '0x0',
                                            'mt_id': 'ipv4',
                                        },
                                        'ipv6': {
                                            'attributes': '0x2',
                                            'mt_id': 'ipv6',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:10:12:115::/64': {
                                            'ip_prefix': '2001:10:12:115::',
                                            'metric': 10,
                                            'prefix_len': '64',
                                        },
                                        '2001:10:23:115::/64': {
                                            'ip_prefix': '2001:10:23:115::',
                                            'metric': 10,
                                            'prefix_len': '64',
                                        },
                                        '2001:2:2:2::2/128': {
                                            'ip_prefix': '2001:2:2:2::2',
                                            'metric': 10,
                                            'prefix_len': '128',
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R1_xe.01': {
                                            'metric': 10,
                                            'neighbor_id': 'R1_xe.01',
                                        },
                                        'R2_xr.03': {
                                            'metric': 10,
                                            'neighbor_id': 'R2_xr.03',
                                        },
                                    },
                                    'remaining_lifetime': 979,
                                    'sequence': '0x00000166',
                                },
                                'R2_xr.03-00': {
                                    'checksum': '0x6938',
                                    'extended_is_neighbor': {
                                        'R2_xr.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R2_xr.00',
                                        },
                                        'R3_nx.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R3_nx.00',
                                        },
                                    },
                                    'lsp_id': 'R2_xr.03-00',
                                    'remaining_lifetime': 884,
                                    'sequence': '0x0000015E',
                                },
                                'R3_nx.00-00': {
                                    'checksum': '0xB985',
                                    'dynamic_hostname': 'R3_nx',
                                    'extended_is_neighbor': {
                                        'R1_xe.02': {
                                            'metric': 40,
                                            'neighbor_id': 'R1_xe.02',
                                        },
                                        'R2_xr.03': {
                                            'metric': 40,
                                            'neighbor_id': 'R2_xr.03',
                                        },
                                    },
                                    'ipv4_addresses': ['3.3.3.3'],
                                    'ipv4_internal_reachability': {
                                        '10.13.115.0/24': {
                                            'default_metric': 40,
                                            'ip_prefix': '10.13.115.0',
                                            'prefix_len': '24',
                                        },
                                        '10.23.115.0/24': {
                                            'default_metric': 40,
                                            'ip_prefix': '10.23.115.0',
                                            'prefix_len': '24',
                                        },
                                        '3.3.3.3/32': {
                                            'default_metric': 1,
                                            'ip_prefix': '3.3.3.3',
                                            'prefix_len': '32',
                                        },
                                    },
                                    'lsp_id': 'R3_nx.00-00',
                                    'mt_entries': {
                                        'ipv4': {
                                            'attributes': '0x0',
                                            'mt_id': 'ipv4',
                                        },
                                        'ipv6': {
                                            'attributes': '0x2',
                                            'mt_id': 'ipv6',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:10:13:115::/64': {
                                            'ip_prefix': '2001:10:13:115::',
                                            'metric': 40,
                                            'prefix_len': '64',
                                        },
                                        '2001:10:23:115::/64': {
                                            'ip_prefix': '2001:10:23:115::',
                                            'metric': 40,
                                            'prefix_len': '64',
                                        },
                                        '2001:3:3:3::3/128': {
                                            'ip_prefix': '2001:3:3:3::3',
                                            'metric': 1,
                                            'prefix_len': '128',
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R1_xe.02': {
                                            'metric': 40,
                                            'neighbor_id': 'R1_xe.02',
                                        },
                                        'R2_xr.03': {
                                            'metric': 40,
                                            'neighbor_id': 'R2_xr.03',
                                        },
                                    },
                                    'remaining_lifetime': 978,
                                    'sequence': '0x000001F6',
                                },
                            },
                            2: {
                                'R1_xe.00-00': {
                                    'checksum': '0x9818',
                                    'dynamic_hostname': 'R1_xe',
                                    'extended_is_neighbor': {
                                        'R1_xe.01': {
                                            'metric': 10,
                                            'neighbor_id': 'R1_xe.01',
                                        },
                                        'R1_xe.02': {
                                            'metric': 10,
                                            'neighbor_id': 'R1_xe.02',
                                        },
                                    },
                                    'ipv4_addresses': ['10.13.115.1'],
                                    'ipv4_internal_reachability': {
                                        '10.12.115.0/24': {
                                            'default_metric': 10,
                                            'ip_prefix': '10.12.115.0',
                                            'prefix_len': '24',
                                        },
                                        '10.13.115.0/24': {
                                            'default_metric': 10,
                                            'ip_prefix': '10.13.115.0',
                                            'prefix_len': '24',
                                        },
                                        '10.23.115.0/24': {
                                            'default_metric': 20,
                                            'ip_prefix': '10.23.115.0',
                                            'prefix_len': '24',
                                        },
                                    },
                                    'ipv6_addresses': ['2001:10:13:115::1'],
                                    'lsp_id': 'R1_xe.00-00',
                                    'mt_entries': {
                                        'ipv4': {
                                            'attributes': '0x0',
                                            'mt_id': 'ipv4',
                                        },
                                        'ipv6': {
                                            'attributes': '0x2',
                                            'mt_id': 'ipv6',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:10:12:115::/64': {
                                            'ip_prefix': '2001:10:12:115::',
                                            'metric': 10,
                                            'prefix_len': '64',
                                        },
                                        '2001:10:13:115::/64': {
                                            'ip_prefix': '2001:10:13:115::',
                                            'metric': 10,
                                            'prefix_len': '64',
                                        },
                                        '2001:10:23:115::/64': {
                                            'ip_prefix': '2001:10:23:115::',
                                            'metric': 20,
                                            'prefix_len': '64',
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R1_xe.01': {
                                            'metric': 10,
                                            'neighbor_id': 'R1_xe.01',
                                        },
                                        'R1_xe.02': {
                                            'metric': 10,
                                            'neighbor_id': 'R1_xe.02',
                                        },
                                    },
                                    'remaining_lifetime': 1075,
                                    'sequence': '0x00000164',
                                },
                                'R1_xe.01-00': {
                                    'checksum': '0x13C4',
                                    'extended_is_neighbor': {
                                        'R1_xe.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R1_xe.00',
                                        },
                                        'R2_xr.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R2_xr.00',
                                        },
                                    },
                                    'lsp_id': 'R1_xe.01-00',
                                    'remaining_lifetime': 916,
                                    'sequence': '0x0000015D',
                                },
                                'R1_xe.02-00': {
                                    'checksum': '0xFD6B',
                                    'extended_is_neighbor': {
                                        'R1_xe.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R1_xe.00',
                                        },
                                        'R3_nx.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R3_nx.00',
                                        },
                                    },
                                    'lsp_id': 'R1_xe.02-00',
                                    'remaining_lifetime': 635,
                                    'sequence': '0x00000164',
                                },
                                'R2_xr.00-00': {
                                    'checksum': '0x8ACA',
                                    'dynamic_hostname': 'R2_xr',
                                    'extended_is_neighbor': {
                                        'R1_xe.01': {
                                            'metric': 10,
                                            'neighbor_id': 'R1_xe.01',
                                        },
                                        'R2_xr.03': {
                                            'metric': 10,
                                            'neighbor_id': 'R2_xr.03',
                                        },
                                    },
                                    'ipv4_addresses': ['2.2.2.2'],
                                    'ipv4_internal_reachability': {
                                        '10.12.115.0/24': {
                                            'default_metric': 10,
                                            'ip_prefix': '10.12.115.0',
                                            'prefix_len': '24',
                                        },
                                        '10.13.115.0/24': {
                                            'default_metric': 20,
                                            'ip_prefix': '10.13.115.0',
                                            'prefix_len': '24',
                                        },
                                        '10.23.115.0/24': {
                                            'default_metric': 10,
                                            'ip_prefix': '10.23.115.0',
                                            'prefix_len': '24',
                                        },
                                        '2.2.2.2/32': {
                                            'default_metric': 10,
                                            'ip_prefix': '2.2.2.2',
                                            'prefix_len': '32',
                                        },
                                        '3.3.3.3/32': {
                                            'default_metric': 11,
                                            'ip_prefix': '3.3.3.3',
                                            'prefix_len': '32',
                                        },
                                    },
                                    'ipv6_addresses': ['2001:2:2:2::2'],
                                    'lsp_id': 'R2_xr.00-00',
                                    'mt_entries': {
                                        'ipv4': {
                                            'attributes': '0x0',
                                            'mt_id': 'ipv4',
                                        },
                                        'ipv6': {
                                            'attributes': '0x2',
                                            'mt_id': 'ipv6',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:10:12:115::/64': {
                                            'ip_prefix': '2001:10:12:115::',
                                            'metric': 10,
                                            'prefix_len': '64',
                                        },
                                        '2001:10:13:115::/64': {
                                            'ip_prefix': '2001:10:13:115::',
                                            'metric': 20,
                                            'prefix_len': '64',
                                        },
                                        '2001:10:23:115::/64': {
                                            'ip_prefix': '2001:10:23:115::',
                                            'metric': 10,
                                            'prefix_len': '64',
                                        },
                                        '2001:2:2:2::2/128': {
                                            'ip_prefix': '2001:2:2:2::2',
                                            'metric': 10,
                                            'prefix_len': '128',
                                        },
                                        '2001:3:3:3::3/128': {
                                            'ip_prefix': '2001:3:3:3::3',
                                            'metric': 11,
                                            'prefix_len': '128',
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R1_xe.01': {
                                            'metric': 10,
                                            'neighbor_id': 'R1_xe.01',
                                        },
                                        'R2_xr.03': {
                                            'metric': 10,
                                            'neighbor_id': 'R2_xr.03',
                                        },
                                    },
                                    'remaining_lifetime': 345,
                                    'sequence': '0x00000165',
                                },
                                'R2_xr.03-00': {
                                    'checksum': '0x6938',
                                    'extended_is_neighbor': {
                                        'R2_xr.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R2_xr.00',
                                        },
                                        'R3_nx.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R3_nx.00',
                                        },
                                    },
                                    'lsp_id': 'R2_xr.03-00',
                                    'remaining_lifetime': 947,
                                    'sequence': '0x0000015E',
                                },
                                'R3_nx.00-00': {
                                    'checksum': '0xBD83',
                                    'dynamic_hostname': 'R3_nx',
                                    'extended_is_neighbor': {
                                        'R1_xe.02': {
                                            'metric': 40,
                                            'neighbor_id': 'R1_xe.02',
                                        },
                                        'R2_xr.03': {
                                            'metric': 40,
                                            'neighbor_id': 'R2_xr.03',
                                        },
                                    },
                                    'ipv4_addresses': ['3.3.3.3'],
                                    'ipv4_internal_reachability': {
                                        '10.13.115.0/24': {
                                            'default_metric': 40,
                                            'ip_prefix': '10.13.115.0',
                                            'prefix_len': '24',
                                        },
                                        '10.23.115.0/24': {
                                            'default_metric': 40,
                                            'ip_prefix': '10.23.115.0',
                                            'prefix_len': '24',
                                        },
                                        '3.3.3.3/32': {
                                            'default_metric': 1,
                                            'ip_prefix': '3.3.3.3',
                                            'prefix_len': '32',
                                        },
                                    },
                                    'lsp_id': 'R3_nx.00-00',
                                    'mt_entries': {
                                        'ipv4': {
                                            'attributes': '0x0',
                                            'mt_id': 'ipv4',
                                        },
                                        'ipv6': {
                                            'attributes': '0x2',
                                            'mt_id': 'ipv6',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:10:13:115::/64': {
                                            'ip_prefix': '2001:10:13:115::',
                                            'metric': 40,
                                            'prefix_len': '64',
                                        },
                                        '2001:10:23:115::/64': {
                                            'ip_prefix': '2001:10:23:115::',
                                            'metric': 40,
                                            'prefix_len': '64',
                                        },
                                        '2001:3:3:3::3/128': {
                                            'ip_prefix': '2001:3:3:3::3',
                                            'metric': 1,
                                            'prefix_len': '128',
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R1_xe.02': {
                                            'metric': 40,
                                            'neighbor_id': 'R1_xe.02',
                                        },
                                        'R2_xr.03': {
                                            'metric': 40,
                                            'neighbor_id': 'R2_xr.03',
                                        },
                                    },
                                    'remaining_lifetime': 697,
                                    'sequence': '0x000001F4',
                                },
                            },
                        },
                    },
                },
            },
            'test1': {
                'vrf': {
                    'VRF1': {
                        'level_db': {
                            1: {
                                'R1_xe.00-00': {
                                    'checksum': '0xAC87',
                                    'dynamic_hostname': 'R1_xe',
                                    'extended_is_neighbor': {
                                        'R1_xe.02': {
                                            'metric': 10,
                                            'neighbor_id': 'R1_xe.02',
                                        },
                                    },
                                    'ipv4_addresses': ['10.13.115.1'],
                                    'ipv4_internal_reachability': {
                                        '10.12.115.0/24': {
                                            'default_metric': 10,
                                            'ip_prefix': '10.12.115.0',
                                            'prefix_len': '24',
                                        },
                                        '10.13.115.0/24': {
                                            'default_metric': 10,
                                            'ip_prefix': '10.13.115.0',
                                            'prefix_len': '24',
                                        },
                                    },
                                    'ipv6_addresses': ['2001:10:13:115::1'],
                                    'lsp_id': 'R1_xe.00-00',
                                    'mt_entries': {
                                        'ipv4': {
                                            'attributes': '0x0',
                                            'mt_id': 'ipv4',
                                        },
                                        'ipv6': {
                                            'attributes': '0x2',
                                            'mt_id': 'ipv6',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:10:12:115::/64': {
                                            'ip_prefix': '2001:10:12:115::',
                                            'metric': 10,
                                            'prefix_len': '64',
                                        },
                                        '2001:10:13:115::/64': {
                                            'ip_prefix': '2001:10:13:115::',
                                            'metric': 10,
                                            'prefix_len': '64',
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R1_xe.02': {
                                            'metric': 10,
                                            'neighbor_id': 'R1_xe.02',
                                        },
                                    },
                                    'remaining_lifetime': 892,
                                    'sequence': '0x00000161',
                                },
                                'R1_xe.02-00': {
                                    'checksum': '0xEFF5',
                                    'extended_is_neighbor': {
                                        'R1_xe.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R1_xe.00',
                                        },
                                        'R3_nx.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R3_nx.00',
                                        },
                                    },
                                    'lsp_id': 'R1_xe.02-00',
                                    'remaining_lifetime': 719,
                                    'sequence': '0x0000015F',
                                },
                                'R3_nx.00-00': {
                                    'checksum': '0xAE98',
                                    'dynamic_hostname': 'R3_nx',
                                    'extended_is_neighbor': {
                                        'R1_xe.02': {
                                            'metric': 40,
                                            'neighbor_id': 'R1_xe.02',
                                        },
                                    },
                                    'ipv4_addresses': ['3.3.3.3'],
                                    'ipv4_internal_reachability': {
                                        '10.13.115.0/24': {
                                            'default_metric': 40,
                                            'ip_prefix': '10.13.115.0',
                                            'prefix_len': '24',
                                        },
                                        '10.23.115.0/24': {
                                            'default_metric': 40,
                                            'ip_prefix': '10.23.115.0',
                                            'prefix_len': '24',
                                        },
                                        '3.3.3.3/32': {
                                            'default_metric': 1,
                                            'ip_prefix': '3.3.3.3',
                                            'prefix_len': '32',
                                        },
                                    },
                                    'lsp_id': 'R3_nx.00-00',
                                    'mt_entries': {
                                        'ipv4': {
                                            'attributes': '0x0',
                                            'mt_id': 'ipv4',
                                        },
                                        'ipv6': {
                                            'attributes': '0x2',
                                            'mt_id': 'ipv6',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:10:13:115::/64': {
                                            'ip_prefix': '2001:10:13:115::',
                                            'metric': 40,
                                            'prefix_len': '64',
                                        },
                                        '2001:10:23:115::/64': {
                                            'ip_prefix': '2001:10:23:115::',
                                            'metric': 40,
                                            'prefix_len': '64',
                                        },
                                        '2001:3:3:3::3/128': {
                                            'ip_prefix': '2001:3:3:3::3',
                                            'metric': 1,
                                            'prefix_len': '128',
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R1_xe.02': {
                                            'metric': 40,
                                            'neighbor_id': 'R1_xe.02',
                                        },
                                    },
                                    'remaining_lifetime': 1170,
                                    'sequence': '0x000001F4',
                                },
                            },
                            2: {
                                'R1_xe.00-00': {
                                    'checksum': '0x0C5D',
                                    'dynamic_hostname': 'R1_xe',
                                    'extended_is_neighbor': {
                                        'R1_xe.02': {
                                            'metric': 10,
                                            'neighbor_id': 'R1_xe.02',
                                        },
                                    },
                                    'ipv4_addresses': ['10.13.115.1'],
                                    'ipv4_internal_reachability': {
                                        '10.12.115.0/24': {
                                            'default_metric': 10,
                                            'ip_prefix': '10.12.115.0',
                                            'prefix_len': '24',
                                        },
                                        '10.13.115.0/24': {
                                            'default_metric': 10,
                                            'ip_prefix': '10.13.115.0',
                                            'prefix_len': '24',
                                        },
                                        '10.23.115.0/24': {
                                            'default_metric': 50,
                                            'ip_prefix': '10.23.115.0',
                                            'prefix_len': '24',
                                        },
                                    },
                                    'ipv6_addresses': ['2001:10:13:115::1'],
                                    'lsp_id': 'R1_xe.00-00',
                                    'mt_entries': {
                                        'ipv4': {
                                            'attributes': '0x0',
                                            'mt_id': 'ipv4',
                                        },
                                        'ipv6': {
                                            'attributes': '0x2',
                                            'mt_id': 'ipv6',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:10:12:115::/64': {
                                            'ip_prefix': '2001:10:12:115::',
                                            'metric': 10,
                                            'prefix_len': '64',
                                        },
                                        '2001:10:13:115::/64': {
                                            'ip_prefix': '2001:10:13:115::',
                                            'metric': 10,
                                            'prefix_len': '64',
                                        },
                                        '2001:10:23:115::/64': {
                                            'ip_prefix': '2001:10:23:115::',
                                            'metric': 50,
                                            'prefix_len': '64',
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R1_xe.02': {
                                            'metric': 10,
                                            'neighbor_id': 'R1_xe.02',
                                        },
                                    },
                                    'remaining_lifetime': 844,
                                    'sequence': '0x00000161',
                                },
                                'R1_xe.02-00': {
                                    'checksum': '0x0667',
                                    'extended_is_neighbor': {
                                        'R1_xe.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R1_xe.00',
                                        },
                                        'R3_nx.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R3_nx.00',
                                        },
                                    },
                                    'lsp_id': 'R1_xe.02-00',
                                    'remaining_lifetime': 612,
                                    'sequence': '0x00000160',
                                },
                                'R3_nx.00-00': {
                                    'checksum': '0xAE98',
                                    'dynamic_hostname': 'R3_nx',
                                    'extended_is_neighbor': {
                                        'R1_xe.02': {
                                            'metric': 40,
                                            'neighbor_id': 'R1_xe.02',
                                        },
                                    },
                                    'ipv4_addresses': ['3.3.3.3'],
                                    'ipv4_internal_reachability': {
                                        '10.13.115.0/24': {
                                            'default_metric': 40,
                                            'ip_prefix': '10.13.115.0',
                                            'prefix_len': '24',
                                        },
                                        '10.23.115.0/24': {
                                            'default_metric': 40,
                                            'ip_prefix': '10.23.115.0',
                                            'prefix_len': '24',
                                        },
                                        '3.3.3.3/32': {
                                            'default_metric': 1,
                                            'ip_prefix': '3.3.3.3',
                                            'prefix_len': '32',
                                        },
                                    },
                                    'lsp_id': 'R3_nx.00-00',
                                    'mt_entries': {
                                        'ipv4': {
                                            'attributes': '0x0',
                                            'mt_id': 'ipv4',
                                        },
                                        'ipv6': {
                                            'attributes': '0x2',
                                            'mt_id': 'ipv6',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:10:13:115::/64': {
                                            'ip_prefix': '2001:10:13:115::',
                                            'metric': 40,
                                            'prefix_len': '64',
                                        },
                                        '2001:10:23:115::/64': {
                                            'ip_prefix': '2001:10:23:115::',
                                            'metric': 40,
                                            'prefix_len': '64',
                                        },
                                        '2001:3:3:3::3/128': {
                                            'ip_prefix': '2001:3:3:3::3',
                                            'metric': 1,
                                            'prefix_len': '128',
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R1_xe.02': {
                                            'metric': 40,
                                            'neighbor_id': 'R1_xe.02',
                                        },
                                    },
                                    'remaining_lifetime': 928,
                                    'sequence': '0x000001F4',
                                },
                            },
                        },
                    },
                },
            },
        },
    }
