#!/usr/bin/env python

# Python
import unittest
from unittest.mock import Mock

# Genie
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device
from genie.conf.base.attributes import UnsupportedAttributeWarning

# Vpc
from genie.libs.conf.vpc import Vpc


class test_vpc(TestCase):

    def setUp(self):

        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed

        # Device
        self.dev = Device(name='node01', testbed=testbed, os='nxos')

        # Vpc object
        self.vpc = Vpc()
        self.dev.add_feature(self.vpc)

    def test_vpc_config(self):

        self.maxDiff = None

        self.vpc.enabled = True
        self.vpc.device_attr[self.dev].enabled = True
        self.vpc.device_attr[self.dev].domain_attr[100]
        self.vpc.device_attr[self.dev].domain_attr[100].auto_recovery_enabled = True
        self.vpc.device_attr[self.dev].domain_attr[100].auto_recovery_interval = 60
        self.vpc.device_attr[self.dev].domain_attr[100].delay_restore_vpc = 1
        self.vpc.device_attr[self.dev].domain_attr[100].delay_restore_svi = 10
        self.vpc.device_attr[self.dev].domain_attr[100].delay_restore_orphan = 100
        self.vpc.device_attr[self.dev].domain_attr[100].dual_active_exclude_svi = 300
        self.vpc.device_attr[self.dev].domain_attr[100].fast_convergence_enabled = True
        self.vpc.device_attr[self.dev].domain_attr[100].graceful_cc_enabled = True
        self.vpc.device_attr[self.dev].domain_attr[100].ip_arp_sync_enabled = True
        self.vpc.device_attr[self.dev].domain_attr[100].ipv6_nd_sync_enabled = True
        self.vpc.device_attr[self.dev].domain_attr[100].l3_peer_router_enabled = True
        self.vpc.device_attr[self.dev].domain_attr[100].l3_peer_router_syslog_enabled = True
        self.vpc.device_attr[self.dev].domain_attr[100].l3_peer_router_syslog_intvl = 15
        self.vpc.device_attr[self.dev].domain_attr[100].mac_bpdu_src_ver = 1
        self.vpc.device_attr[self.dev].domain_attr[100].peer_gw_enabled = True
        self.vpc.device_attr[self.dev].domain_attr[100].peer_gw_exlude_vlan = 50
        self.vpc.device_attr[self.dev].domain_attr[100].peer_switch_enabled = True
        self.vpc.device_attr[self.dev].domain_attr[100].role_priority = 600
        self.vpc.device_attr[self.dev].domain_attr[100].shutdown = True
        self.vpc.device_attr[self.dev].domain_attr[100].system_mac = '2.2.2'
        self.vpc.device_attr[self.dev].domain_attr[100].system_priority = 601
        self.vpc.device_attr[self.dev].domain_attr[100].track = 201
        self.vpc.device_attr[self.dev].domain_attr[100].virtual_peer_link_ip = '2.2.2.2'
        self.vpc.device_attr[self.dev].domain_attr[100].keepalive_dst_ip = '10.1.1.1'
        self.vpc.device_attr[self.dev].domain_attr[100].keepalive_src_ip = '10.2.2.2'
        self.vpc.device_attr[self.dev].domain_attr[100].keepalive_vrf = 'default'
        self.vpc.device_attr[self.dev].domain_attr[100].keepalive_udp_port = 2000

        # Build vpc configuration
        cfgs = self.vpc.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev.name]),
            '\n'.join([
                'feature vpc',
                'vpc domain 100',
                ' auto-recovery',
                ' auto-recovery reload-delay 60',
                ' delay restore 1',
                ' delay restore interface-vlan 10',
                ' delay restore orphan-port 100',
                ' dual-active exclude interface-vlan 300',
                ' fast-convergence',
                ' graceful consistency-check',
                ' ip arp synchronize',
                ' ipv6 nd synchronize',
                ' layer3 peer-router',
                ' layer3 peer-router syslog',
                ' layer3 peer-router syslog interval 15',
                ' mac-address bpdu source version 1',
                ' peer-gateway',
                ' peer-gateway exclude-vlan 50',
                ' peer-switch',
                ' role priority 600',
                ' shutdown',
                ' system-mac 2.2.2',
                ' system-priority 601',
                ' track 201',
                ' virtual peer-link destination 2.2.2.2',
                ' peer-keepalive destination 10.1.1.1 source 10.2.2.2 vrf default udp-port 2000 ',
                ' exit'
            ]))

        cfgs = self.vpc.build_config(apply=False, attributes={'device_attr': {
                                     self.dev.name: {'domain_attr': {'*': {'track': 201}}}}})

        self.assertMultiLineEqual(
            str(cfgs[self.dev.name]),
            '\n'.join([
                'vpc domain 100',
                ' track 201',
                ' exit'
            ]))

        cfgs = self.vpc.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev.name]),
            '\n'.join([
                'no feature vpc',
            ]))


if __name__ == '__main__':
    unittest.main()
