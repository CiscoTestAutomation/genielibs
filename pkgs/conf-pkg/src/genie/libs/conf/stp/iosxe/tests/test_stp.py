#!/usr/bin/env python

# Python
import unittest
from unittest.mock import Mock

# Genie
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface
from genie.conf.base.attributes import UnsupportedAttributeWarning

# Stp
from genie.libs.conf.stp import Stp


class test_stp(TestCase):

    def setUp(self):
        
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed
        
        # Device
        self.dev1 = Device(name='PE1', testbed=testbed, os='iosxe')

    def test_stp_mst_full_config(self):

        # For failures
        self.maxDiff = None
        
        # Pim object
        stp = Stp()
        self.dev1.add_feature(stp)

        # bridge_assurance command rejected by router
        stp.device_attr[self.dev1].etherchannel_misconfig_guard = True
        stp.device_attr[self.dev1].bpduguard_timeout_recovery = 333
        stp.device_attr[self.dev1].loop_guard = True
        stp.device_attr[self.dev1].bpdu_guard = True
        stp.device_attr[self.dev1].bpdu_filter = True

        # mode_attr
        stp.device_attr[self.dev1].mode_attr['mstp'].hold_count = 10

        # mst_attr
        stp.device_attr[self.dev1].mode_attr['mstp'].mst_attr['default'].m_max_hop = 30
        stp.device_attr[self.dev1].mode_attr['mstp'].mst_attr['default'].m_hello_time = 5
        stp.device_attr[self.dev1].mode_attr['mstp'].mst_attr['default'].m_max_age = 10
        stp.device_attr[self.dev1].mode_attr['mstp'].mst_attr['default'].m_forwarding_delay = 4

        # instance_attr
        stp.device_attr[self.dev1].mode_attr['mstp'].mst_attr['default'].\
            instance_attr[100].m_vlans = '200-210'
        stp.device_attr[self.dev1].mode_attr['mstp'].mst_attr['default'].\
            instance_attr[100].m_name = 'MST'
        stp.device_attr[self.dev1].mode_attr['mstp'].mst_attr['default'].\
            instance_attr[100].m_revision = 300
        stp.device_attr[self.dev1].mode_attr['mstp'].mst_attr['default'].\
            instance_attr[10].m_bridge_priority = 4096

        stp.device_attr[self.dev1].mode_attr['mstp'].mst_attr['default'].\
            instance_attr[10].interface_attr['GigabitEthernet1/0/15'].m_inst_if_cost = '123'
        stp.device_attr[self.dev1].mode_attr['mstp'].mst_attr['default'].\
            instance_attr[10].interface_attr['GigabitEthernet1/0/15'].m_inst_if_port_priority = 32

        # interface_attr
        stp.device_attr[self.dev1].mode_attr['mstp'].mst_attr['default'].\
            interface_attr['GigabitEthernet1/0/15'].m_if_edge_port = 'edge_enable'
        stp.device_attr[self.dev1].mode_attr['mstp'].mst_attr['default'].\
            interface_attr['GigabitEthernet1/0/15'].m_if_link_type = 'p2p'
        stp.device_attr[self.dev1].mode_attr['mstp'].mst_attr['default'].\
            interface_attr['GigabitEthernet1/0/15'].m_if_guard = 'none'
        stp.device_attr[self.dev1].mode_attr['mstp'].mst_attr['default'].\
            interface_attr['GigabitEthernet1/0/15'].m_if_bpdu_guard = True
        stp.device_attr[self.dev1].mode_attr['mstp'].mst_attr['default'].\
            interface_attr['GigabitEthernet1/0/15'].m_if_bpdu_filter = True

        cfgs = stp.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.\
            join([
                'spanning-tree etherchannel guard misconfig',
                'errdisable recovery interval 333',
                'spanning-tree loopguard default',
                'spanning-tree portfast bpduguard default',
                'spanning-tree portfast bpdufilter default',
                'spanning-tree mode mst',
                'spanning-tree transmit hold-count 10',
                'spanning-tree mst max-hops 30',
                'spanning-tree mst hello-time 5',
                'spanning-tree mst max-age 10',
                'spanning-tree mst forward-time 4',
                'spanning-tree mst 10 priority 4096',
                'interface GigabitEthernet1/0/15',
                ' spanning-tree mst 10 cost 123',
                ' spanning-tree mst 10 port-priority 32',
                ' exit',
                'spanning-tree mst configuration',
                ' instance 100 vlan 200-210',
                ' name MST',
                ' revision 300',
                ' exit',
                'interface GigabitEthernet1/0/15',
                ' spanning-tree portfast',
                ' spanning-tree link-type point-to-point',
                ' spanning-tree guard none',
                ' spanning-tree bpduguard enable',
                ' spanning-tree bpdufilter enable',
                ' exit',
            ]))

        cfgs = stp.build_unconfig(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.\
            join([
                'no spanning-tree etherchannel guard misconfig',
                'no errdisable recovery interval 333',
                'no spanning-tree loopguard default',
                'no spanning-tree portfast bpduguard default',
                'no spanning-tree portfast bpdufilter default',
                'no spanning-tree mode mst',
                'no spanning-tree transmit hold-count 10',
                'no spanning-tree mst max-hops 30',
                'no spanning-tree mst hello-time 5',
                'no spanning-tree mst max-age 10',
                'no spanning-tree mst forward-time 4',
                'no spanning-tree mst 10 priority 4096',
                'interface GigabitEthernet1/0/15',
                ' no spanning-tree mst 10 cost 123',
                ' no spanning-tree mst 10 port-priority 32',
                ' exit',
                'spanning-tree mst configuration',
                ' no instance 100 vlan 200-210',
                ' no name MST',
                ' no revision 300',
                ' exit',
                'interface GigabitEthernet1/0/15',
                ' no spanning-tree portfast',
                ' no spanning-tree link-type point-to-point',
                ' no spanning-tree guard none',
                ' no spanning-tree bpduguard enable',
                ' no spanning-tree bpdufilter enable',
                ' exit',
            ]))

        # uncfg with attributes
        cfgs = stp.build_unconfig(apply=False,
                                  attributes={'device_attr': {
                                                self.dev1: {
                                                    'mode_attr': {
                                                        'mstp': {
                                                            'mst_attr': {
                                                                'default': {
                                                                    'm_max_age': None,
                                                                    'instance_attr': {
                                                                        100: {
                                                                            'm_name': None,
                                                                        },
                                                                        10: {
                                                                            'm_bridge_priority': None,
                                                                            'interface_attr': {
                                                                                'GigabitEthernet1/0/15': {
                                                                                    'm_inst_if_port_priority': None,
                                                                                }
                                                                            }
                                                                        }
                                                                    },
                                                                    'interface_attr': {
                                                                        'GigabitEthernet1/0/15': {
                                                                            'm_if_bpdu_filter': None
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
        }}})

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.\
            join([
                'no spanning-tree mst max-age 10',
                'no spanning-tree mst 10 priority 4096',
                'interface GigabitEthernet1/0/15',
                ' no spanning-tree mst 10 port-priority 32',
                ' exit',
                'spanning-tree mst configuration',
                ' no name MST',
                ' exit',
                'interface GigabitEthernet1/0/15',
                ' no spanning-tree bpdufilter enable',
                ' exit',
            ]))

    def test_stp_pvst_full_config(self):

        # For failures
        self.maxDiff = None
        
        # Pim object
        stp = Stp()
        self.dev1.add_feature(stp)

        # bridge_assurance command rejected by router
        stp.device_attr[self.dev1].etherchannel_misconfig_guard = True
        stp.device_attr[self.dev1].bpduguard_timeout_recovery = 333
        stp.device_attr[self.dev1].loop_guard = True
        stp.device_attr[self.dev1].bpdu_guard = True
        stp.device_attr[self.dev1].bpdu_filter = True

        # vlan_attr
        stp.device_attr[self.dev1].mode_attr['pvst'].pvst_attr['default'].\
            vlan_attr['500'].v_hello_time = 5
        stp.device_attr[self.dev1].mode_attr['pvst'].pvst_attr['default'].\
            vlan_attr['500'].v_max_age = 10
        stp.device_attr[self.dev1].mode_attr['pvst'].pvst_attr['default'].\
            vlan_attr['500'].v_forwarding_delay = 15
        stp.device_attr[self.dev1].mode_attr['pvst'].pvst_attr['default'].\
            vlan_attr['500'].v_bridge_priority = 4096
        stp.device_attr[self.dev1].mode_attr['pvst'].pvst_attr['default'].\
            vlan_attr['666'].vlan_id = '666'

        stp.device_attr[self.dev1].mode_attr['pvst'].pvst_attr['default'].\
            vlan_attr['500'].interface_attr['GigabitEthernet1/0/15'].v_if_cost = '123'
        stp.device_attr[self.dev1].mode_attr['pvst'].pvst_attr['default'].\
            vlan_attr['500'].interface_attr['GigabitEthernet1/0/15'].v_if_port_priority = 16

        # interface_attr
        stp.device_attr[self.dev1].mode_attr['pvst'].pvst_attr['default'].\
            interface_attr['GigabitEthernet1/0/15'].p_if_edge_port = 'edge_enable'
        stp.device_attr[self.dev1].mode_attr['pvst'].pvst_attr['default'].\
            interface_attr['GigabitEthernet1/0/15'].p_if_link_type = 'shared'
        stp.device_attr[self.dev1].mode_attr['pvst'].pvst_attr['default'].\
            interface_attr['GigabitEthernet1/0/15'].p_if_guard = 'root'
        stp.device_attr[self.dev1].mode_attr['pvst'].pvst_attr['default'].\
            interface_attr['GigabitEthernet1/0/15'].p_if_bpdu_guard = True
        stp.device_attr[self.dev1].mode_attr['pvst'].pvst_attr['default'].\
            interface_attr['GigabitEthernet1/0/15'].p_if_bpdu_filter = True

        cfgs = stp.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.\
            join([
                'spanning-tree etherchannel guard misconfig',
                'errdisable recovery interval 333',
                'spanning-tree loopguard default',
                'spanning-tree portfast bpduguard default',
                'spanning-tree portfast bpdufilter default',
                'spanning-tree mode pvst',
                'spanning-tree vlan 500 hello-time 5',
                'spanning-tree vlan 500 max-age 10',
                'spanning-tree vlan 500 forward-time 15',
                'spanning-tree vlan 500 priority 4096',
                'interface GigabitEthernet1/0/15',
                ' spanning-tree vlan 500 cost 123',
                ' spanning-tree vlan 500 port-priority 16',
                ' exit',
                'spanning-tree vlan 666',
                'interface GigabitEthernet1/0/15',
                ' spanning-tree portfast',
                ' spanning-tree link-type shared',
                ' spanning-tree guard root',
                ' spanning-tree bpduguard enable',
                ' spanning-tree bpdufilter enable',
                ' exit',
            ]))

        cfgs = stp.build_unconfig(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.\
            join([
                'no spanning-tree etherchannel guard misconfig',
                'no errdisable recovery interval 333',
                'no spanning-tree loopguard default',
                'no spanning-tree portfast bpduguard default',
                'no spanning-tree portfast bpdufilter default',
                'no spanning-tree mode pvst',
                'no spanning-tree vlan 500 hello-time 5',
                'no spanning-tree vlan 500 max-age 10',
                'no spanning-tree vlan 500 forward-time 15',
                'no spanning-tree vlan 500 priority 4096',
                'interface GigabitEthernet1/0/15',
                ' no spanning-tree vlan 500 cost 123',
                ' no spanning-tree vlan 500 port-priority 16',
                ' exit',
                'no spanning-tree vlan 666',
                'interface GigabitEthernet1/0/15',
                ' no spanning-tree portfast',
                ' no spanning-tree link-type shared',
                ' no spanning-tree guard root',
                ' no spanning-tree bpduguard enable',
                ' no spanning-tree bpdufilter enable',
                ' exit',
            ]))

        # uncfg with attributes
        cfgs = stp.build_unconfig(apply=False,
                                  attributes={'device_attr': {
                                                self.dev1: {
                                                    'mode_attr': {
                                                        'pvst': {
                                                            'pvst_attr': {
                                                                'default': {
                                                                    'vlan_attr': {
                                                                        '500': {
                                                                            'v_bridge_priority': None,
                                                                            'interface_attr': {
                                                                                'GigabitEthernet1/0/15': {
                                                                                    'v_if_cost': None
                                                                                }
                                                                            }
                                                                        }
                                                                    },
                                                                    'interface_attr': {
                                                                        'GigabitEthernet1/0/15': {
                                                                            'p_if_bpdu_filter': None
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
        }}})

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.\
            join([
                'no spanning-tree vlan 500 priority 4096',
                'interface GigabitEthernet1/0/15',
                ' no spanning-tree vlan 500 cost 123',
                ' exit',
                'interface GigabitEthernet1/0/15',
                ' no spanning-tree bpdufilter enable',
                ' exit',
            ]))
    

    def test_stp_rapid_pvst_full_config(self):

        # For failures
        self.maxDiff = None
        
        # Pim object
        stp = Stp()
        self.dev1.add_feature(stp)

        # bridge_assurance command rejected by router
        stp.device_attr[self.dev1].etherchannel_misconfig_guard = True
        stp.device_attr[self.dev1].bpduguard_timeout_recovery = 333
        stp.device_attr[self.dev1].loop_guard = True
        stp.device_attr[self.dev1].bpdu_guard = True
        stp.device_attr[self.dev1].bpdu_filter = True

        # vlan_attr
        stp.device_attr[self.dev1].mode_attr['rapid-pvst'].pvst_attr['default'].\
            vlan_attr['500'].v_hello_time = 5
        stp.device_attr[self.dev1].mode_attr['rapid-pvst'].pvst_attr['default'].\
            vlan_attr['500'].v_max_age = 10
        stp.device_attr[self.dev1].mode_attr['rapid-pvst'].pvst_attr['default'].\
            vlan_attr['500'].v_forwarding_delay = 15
        stp.device_attr[self.dev1].mode_attr['rapid-pvst'].pvst_attr['default'].\
            vlan_attr['500'].v_bridge_priority = 4096

        stp.device_attr[self.dev1].mode_attr['rapid-pvst'].pvst_attr['default'].\
            vlan_attr['500'].interface_attr['GigabitEthernet1/0/15'].v_if_cost = '123'
        stp.device_attr[self.dev1].mode_attr['rapid-pvst'].pvst_attr['default'].\
            vlan_attr['500'].interface_attr['GigabitEthernet1/0/15'].v_if_port_priority = 16

        # interface_attr
        stp.device_attr[self.dev1].mode_attr['rapid-pvst'].pvst_attr['default'].\
            interface_attr['GigabitEthernet1/0/15'].p_if_edge_port = 'edge_enable'
        stp.device_attr[self.dev1].mode_attr['rapid-pvst'].pvst_attr['default'].\
            interface_attr['GigabitEthernet1/0/15'].p_if_link_type = 'shared'
        stp.device_attr[self.dev1].mode_attr['rapid-pvst'].pvst_attr['default'].\
            interface_attr['GigabitEthernet1/0/15'].p_if_guard = 'root'
        stp.device_attr[self.dev1].mode_attr['rapid-pvst'].pvst_attr['default'].\
            interface_attr['GigabitEthernet1/0/15'].p_if_bpdu_guard = True
        stp.device_attr[self.dev1].mode_attr['rapid-pvst'].pvst_attr['default'].\
            interface_attr['GigabitEthernet1/0/15'].p_if_bpdu_filter = True

        cfgs = stp.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.\
            join([
                'spanning-tree etherchannel guard misconfig',
                'errdisable recovery interval 333',
                'spanning-tree loopguard default',
                'spanning-tree portfast bpduguard default',
                'spanning-tree portfast bpdufilter default',
                'spanning-tree mode rapid-pvst',
                'spanning-tree vlan 500 hello-time 5',
                'spanning-tree vlan 500 max-age 10',
                'spanning-tree vlan 500 forward-time 15',
                'spanning-tree vlan 500 priority 4096',
                'interface GigabitEthernet1/0/15',
                ' spanning-tree vlan 500 cost 123',
                ' spanning-tree vlan 500 port-priority 16',
                ' exit',
                'interface GigabitEthernet1/0/15',
                ' spanning-tree portfast',
                ' spanning-tree link-type shared',
                ' spanning-tree guard root',
                ' spanning-tree bpduguard enable',
                ' spanning-tree bpdufilter enable',
                ' exit',
            ]))

        cfgs = stp.build_unconfig(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.\
            join([
                'no spanning-tree etherchannel guard misconfig',
                'no errdisable recovery interval 333',
                'no spanning-tree loopguard default',
                'no spanning-tree portfast bpduguard default',
                'no spanning-tree portfast bpdufilter default',
                'no spanning-tree mode rapid-pvst',
                'no spanning-tree vlan 500 hello-time 5',
                'no spanning-tree vlan 500 max-age 10',
                'no spanning-tree vlan 500 forward-time 15',
                'no spanning-tree vlan 500 priority 4096',
                'interface GigabitEthernet1/0/15',
                ' no spanning-tree vlan 500 cost 123',
                ' no spanning-tree vlan 500 port-priority 16',
                ' exit',
                'interface GigabitEthernet1/0/15',
                ' no spanning-tree portfast',
                ' no spanning-tree link-type shared',
                ' no spanning-tree guard root',
                ' no spanning-tree bpduguard enable',
                ' no spanning-tree bpdufilter enable',
                ' exit',
            ]))

        # uncfg with attributes
        cfgs = stp.build_unconfig(apply=False,
                                  attributes={'device_attr': {
                                                self.dev1: {
                                                    'mode_attr': {
                                                        'rapid-pvst': {
                                                            'pvst_attr': {
                                                                'default': {
                                                                    'm_max_age': None,
                                                                    'vlan_attr': {
                                                                        '500': {
                                                                            'v_bridge_priority': None
                                                                        }
                                                                    },
                                                                    'interface_attr': {
                                                                        'GigabitEthernet1/0/15': {
                                                                            'p_if_bpdu_filter': None
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
        }}})

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.\
            join([
                'no spanning-tree vlan 500 priority 4096',
                'interface GigabitEthernet1/0/15',
                ' no spanning-tree bpdufilter enable',
                ' exit',
            ]))
    

if __name__ == '__main__':
    unittest.main()
