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
from genie.libs.conf.acl import Acl


class test_acl(TestCase):

    def setUp(self):
        
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed
        
        # Device
        self.dev1 = Device(name='PE1', testbed=testbed, os='iosxe')

    def test_acl_full_config(self):

        # For failures
        self.maxDiff = None
        
        # Pim object
        acl = Acl()
        self.dev1.add_feature(acl)

        #  ipv4
        acl.device_attr[self.dev1].acl_attr['ipv4_acl']\
            .acl_type = 'ipv4-acl-type'
        acl.device_attr[self.dev1].acl_attr['ipv4_acl']\
            .ace_attr['20'].actions_forwarding = 'permit'
        acl.device_attr[self.dev1].acl_attr['ipv4_acl']\
            .ace_attr['20'].protocol = 'ip'
        acl.device_attr[self.dev1].acl_attr['ipv4_acl']\
            .ace_attr['20'].src = 'any'
        acl.device_attr[self.dev1].acl_attr['ipv4_acl']\
            .ace_attr['20'].dst = 'any'

        acl.device_attr[self.dev1].acl_attr['ipv4_acl']\
            .ace_attr['10'].actions_forwarding = 'deny'
        acl.device_attr[self.dev1].acl_attr['ipv4_acl']\
            .ace_attr['10'].protocol = 'tcp'
        acl.device_attr[self.dev1].acl_attr['ipv4_acl']\
            .ace_attr['10'].src = '1.1.1.1 255.255.255.0'
        acl.device_attr[self.dev1].acl_attr['ipv4_acl']\
            .ace_attr['10'].src_operator = 'eq'
        acl.device_attr[self.dev1].acl_attr['ipv4_acl']\
            .ace_attr['10'].src_port = '37 32 www'
        acl.device_attr[self.dev1].acl_attr['ipv4_acl']\
            .ace_attr['10'].dst = 'host 2.2.2.2'
        acl.device_attr[self.dev1].acl_attr['ipv4_acl']\
            .ace_attr['10'].dst_operator = 'lt'
        acl.device_attr[self.dev1].acl_attr['ipv4_acl']\
            .ace_attr['10'].dst_port = '20'
        acl.device_attr[self.dev1].acl_attr['ipv4_acl']\
            .ace_attr['10'].established = True
        acl.device_attr[self.dev1].acl_attr['ipv4_acl']\
            .ace_attr['10'].precedence = 'flash'
        acl.device_attr[self.dev1].acl_attr['ipv4_acl']\
            .ace_attr['10'].option = 'ssr'
        acl.device_attr[self.dev1].acl_attr['ipv4_acl']\
            .ace_attr['10'].actions_logging = 'log-syslog'
        acl.device_attr[self.dev1].acl_attr['ipv4_acl']\
            .interface_attr['GigabitEthernet2/0/15'].if_in = True

        # ipv6
        acl.device_attr[self.dev1].acl_attr['ipv6_acl']\
            .acl_type = 'ipv6-acl-type'
        acl.device_attr[self.dev1].acl_attr['ipv6_acl']\
            .ace_attr['20'].actions_forwarding = 'permit'
        acl.device_attr[self.dev1].acl_attr['ipv6_acl']\
            .ace_attr['20'].protocol = 'ipv6'
        acl.device_attr[self.dev1].acl_attr['ipv6_acl']\
            .ace_attr['20'].src = 'any'
        acl.device_attr[self.dev1].acl_attr['ipv6_acl']\
            .ace_attr['20'].dst = 'any'
        acl.device_attr[self.dev1].acl_attr['ipv6_acl']\
            .ace_attr['20'].dscp = 'cs7'
        acl.device_attr[self.dev1].acl_attr['ipv6_acl']\
            .ace_attr['20'].actions_logging = 'log-syslog'

        acl.device_attr[self.dev1].acl_attr['ipv6_acl']\
            .ace_attr['10'].actions_forwarding = 'deny'
        acl.device_attr[self.dev1].acl_attr['ipv6_acl']\
            .ace_attr['10'].protocol = 'tcp'
        acl.device_attr[self.dev1].acl_attr['ipv6_acl']\
            .ace_attr['10'].src = 'any'
        acl.device_attr[self.dev1].acl_attr['ipv6_acl']\
            .ace_attr['10'].src_operator = 'eq'
        acl.device_attr[self.dev1].acl_attr['ipv6_acl']\
            .ace_attr['10'].src_port = 'www 8443'
        acl.device_attr[self.dev1].acl_attr['ipv6_acl']\
            .ace_attr['10'].dst = 'host 2001:2::2'
        acl.device_attr[self.dev1].acl_attr['ipv6_acl']\
            .interface_attr['GigabitEthernet2/0/15'].if_in = True

        # mac
        acl.device_attr[self.dev1].acl_attr['mac_acl']\
            .acl_type = 'eth-acl-type'
        acl.device_attr[self.dev1].acl_attr['mac_acl']\
            .ace_attr['20'].actions_forwarding = 'permit'
        acl.device_attr[self.dev1].acl_attr['mac_acl']\
            .ace_attr['20'].src = 'host aaaa.aaaa.aaaa'
        acl.device_attr[self.dev1].acl_attr['mac_acl']\
            .ace_attr['20'].dst = 'host bbbb.bbbb.bbbb'
        acl.device_attr[self.dev1].acl_attr['mac_acl']\
            .ace_attr['20'].ether_type = 'aarp'

        acl.device_attr[self.dev1].acl_attr['mac_acl']\
            .ace_attr['10'].actions_forwarding = 'deny'
        acl.device_attr[self.dev1].acl_attr['mac_acl']\
            .ace_attr['10'].src = 'host 0000.0000.0000'
        acl.device_attr[self.dev1].acl_attr['mac_acl']\
            .ace_attr['10'].dst = 'host 0000.0000.0000'

        acl.device_attr[self.dev1].acl_attr['mac_acl']\
            .interface_attr['GigabitEthernet2/0/15'].if_in = True

        cfgs = acl.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.\
            join([
                'ip access-list extended ipv4_acl',
                ' 10 deny tcp 1.1.1.1 255.255.255.0 eq 37 32 www host 2.2.2.2 lt 20 option ssr precedence flash established log',
                ' 20 permit ip any any',
                ' exit',
                'interface GigabitEthernet2/0/15',
                ' ip access-group ipv4_acl in',
                ' exit',
                'ipv6 access-list ipv6_acl',
                ' sequence 10 deny tcp any eq www 8443 host 2001:2::2',
                ' sequence 20 permit ipv6 any any dscp cs7 log',
                ' exit',
                'interface GigabitEthernet2/0/15',
                ' ipv6 traffic-filter ipv6_acl in',
                ' exit',
                'mac access-list extended mac_acl',
                ' deny host 0000.0000.0000 host 0000.0000.0000',
                ' permit host aaaa.aaaa.aaaa host bbbb.bbbb.bbbb aarp',
                ' exit',
                'interface GigabitEthernet2/0/15',
                ' mac access-group mac_acl in',
                ' exit',
                
            ]))

        cfgs = acl.build_unconfig(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.\
            join([
                'no ip access-list extended ipv4_acl',
                'interface GigabitEthernet2/0/15',
                ' no ip access-group ipv4_acl in',
                ' exit',
                'no ipv6 access-list ipv6_acl',
                'interface GigabitEthernet2/0/15',
                ' no ipv6 traffic-filter ipv6_acl in',
                ' exit',
                'no mac access-list extended mac_acl',
                'interface GigabitEthernet2/0/15',
                ' no mac access-group mac_acl in',
                ' exit',
            ]))

        # uncfg with attributes
        cfgs = acl.build_unconfig(apply=False,
                  attributes={'device_attr': {
                                self.dev1: {
                                    'acl_attr': {
                                        'ipv4_acl': {
                                            'acl_type': None,
                                            'ace_attr': {
                                                '20': {
                                                    'protocol': None,
                                                    'actions_forwarding': None,
                                                    'src': None,
                                                    'dst': None
                                                }
                                            }
                                        },
                                        'ipv6_acl': {
                                            'acl_type': None,
                                            'ace_attr': {
                                                '20': {
                                                    'protocol': None,
                                                    'actions_forwarding': None,
                                                    'src': None,
                                                    'dst': None,
                                                    'dscp': None,
                                                    'actions_logging': None
                                                }
                                            }
                                        },
                                        'mac_acl': {
                                            'acl_type': None,
                                            'ace_attr': {
                                                '10': {
                                                    'actions_forwarding': None,
                                                    'src': None,
                                                    'dst': None,
                                                }
                                            }
                                        },
                                    },}}})
        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.\
            join([
                'ip access-list extended ipv4_acl',
                ' no 20 permit ip any any',
                ' exit',
                'ipv6 access-list ipv6_acl',
                ' no sequence 20 permit ipv6 any any dscp cs7 log',
                ' exit',
                'mac access-list extended mac_acl',
                ' no deny host 0000.0000.0000 host 0000.0000.0000',
                ' exit',
            ]))    

if __name__ == '__main__':
    unittest.main()
