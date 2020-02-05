#!/usr/bin/env python

# Python
import unittest
from unittest.mock import Mock

# Genie
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device
from genie.conf.base.attributes import UnsupportedAttributeWarning

# Ntp
from genie.libs.conf.ntp import Ntp

# Vrf
from genie.libs.conf.vrf import Vrf


class test_ntp(TestCase):

    def setUp(self):
        
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed
        
        # Device
        self.dev1 = Device(name='PE1', testbed=testbed, os='nxos')
        
        # Ntp object
        self.ntp = Ntp()

    def test_ntp_config(self):

        # For failures
        self.maxDiff = None

        # VRF configuration
        vrf1 = Vrf('VRF1')
        self.ntp.device_attr[self.dev1].enabled = True
        self.ntp.device_attr[self.dev1].master_stratum = 10
        self.ntp.device_attr[self.dev1].auth_enabled = True

        self.ntp.device_attr[self.dev1].vrf_attr[vrf1].server_attr['1.1.1.1']\
            .server_key_id = 1
        self.ntp.device_attr[self.dev1].vrf_attr[vrf1].server_attr['1.1.1.1']\
            .server_minpoll = 5
        self.ntp.device_attr[self.dev1].vrf_attr[vrf1].server_attr['1.1.1.1']\
            .server_maxpoll = 15
        self.ntp.device_attr[self.dev1].vrf_attr[vrf1].server_attr['1.1.1.1']\
            .server_prefer = True
        self.ntp.device_attr[self.dev1].vrf_attr[vrf1].peer_attr['3.3.3.3']\
            .peer_key_id = 3
        self.ntp.device_attr[self.dev1].vrf_attr[vrf1].peer_attr['3.3.3.3']\
            .peer_prefer = True
        # non-default vrf won't have source_interface configured even if 
        # register the attribute
        self.ntp.device_attr[self.dev1].vrf_attr[vrf1].source_interface = 'Ethernet2/1'

        
        vrf2 = Vrf('default')
        self.ntp.device_attr[self.dev1].vrf_attr[vrf2].server_attr['2.2.2.2']\
            .server_key_id = 2
        self.ntp.device_attr[self.dev1].vrf_attr[vrf2].server_attr['2.2.2.2']\
            .server_prefer = True
        self.ntp.device_attr[self.dev1].vrf_attr[vrf2].peer_attr['4.4.4.4']\
            .peer_key_id = 4
        self.ntp.device_attr[self.dev1].vrf_attr[vrf2].peer_attr['4.4.4.4']\
            .peer_minpoll = 6
        self.ntp.device_attr[self.dev1].vrf_attr[vrf2].peer_attr['4.4.4.4']\
            .peer_maxpoll = 16
        self.ntp.device_attr[self.dev1].vrf_attr[vrf2].peer_attr['4.4.4.4']\
            .peer_prefer = True
        self.ntp.device_attr[self.dev1].vrf_attr[vrf2].source_interface = 'Ethernet2/1'


        self.ntp.device_attr[self.dev1].auth_key_attr[1].auth_algorithm = 'md5'
        self.ntp.device_attr[self.dev1].auth_key_attr[1].auth_key = 'wawy 7'
        self.ntp.device_attr[self.dev1].auth_key_attr[1].auth_trusted_key = True


        # Build ntp configuration
        cfgs = self.ntp.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'feature ntp',
                'ntp master 10',
                'ntp authenticate',
                'ntp source-interface Ethernet2/1',
                'ntp server 2.2.2.2 key 2 prefer',
                'ntp peer 4.4.4.4 key 4 maxpoll 16 minpoll 6 prefer',
                'ntp server 1.1.1.1 key 1 maxpoll 15 minpoll 5 prefer use-vrf VRF1',
                'ntp peer 3.3.3.3 key 3 prefer use-vrf VRF1',
                'ntp authentication-key 1 md5 wawy 7',
                'ntp trusted-key 1',
            ]))

        # Build unconfig
        cfgs = self.ntp.build_unconfig(apply=False)

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no feature ntp',
            ]))

        # Build unconfig with attribute
        cfgs = self.ntp.build_unconfig(apply=False,
                                        attributes={'device_attr': {
                                                        self.dev1: {
                                                            'auth_enabled': None,
                                                            'vrf_attr': {
                                                                vrf1: {
                                                                    'peer_attr': {
                                                                        '3.3.3.3': {
                                                                            'peer_key_id': None,
                                                                            'peer_prefer': None
                                                                        }
                                                                    }
                                                                },
                                                                vrf2: {
                                                                    'peer_attr': None,
                                                                }
                                                            },
                                                            'auth_key_attr': {
                                                                1: {
                                                                    'auth_trusted_key': None,
                                                                }
                                                            }}}})

        # Check config correctly unconfigured
        self.assertMultiLineEqual(
            str(cfgs[self.dev1.name]),
            '\n'.join([
                'no ntp authenticate',
                'no ntp peer 4.4.4.4 key 4 maxpoll 16 minpoll 6 prefer',
                'no ntp peer 3.3.3.3 key 3 prefer use-vrf VRF1',
                'no ntp trusted-key 1'
        ]))


if __name__ == '__main__':
    unittest.main()
