#!/usr/bin/env python

# Python
import unittest
from unittest.mock import Mock

# Genie
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device

# Stp
from genie.libs.conf.dot1x import Dot1x


class test_dot1x(TestCase):

    def setUp(self):
        
        # Set Genie Tb
        testbed = Testbed()
        Genie.testbed = testbed
        
        # Device
        self.dev1 = Device(name='PE1', testbed=testbed, os='iosxe')

    def test_dot1x_full_config(self):

        # For failures
        self.maxDiff = None
        
        # Pim object
        dot1x = Dot1x()
        self.dev1.add_feature(dot1x)

        #  device_attr
        dot1x.device_attr[self.dev1].system_auth_control = True
        dot1x.device_attr[self.dev1].supplicant_force_mcast = True

        #  credentials_attr
        dot1x.device_attr[self.dev1].credentials_attr['switch4']\
            .credential_username = 'switch4'
        dot1x.device_attr[self.dev1].credentials_attr['switch4']\
            .credential_pwd_type = '0'
        dot1x.device_attr[self.dev1].credentials_attr['switch4']\
            .credential_secret = 'cisco'

        #  interface_attr
        dot1x.device_attr[self.dev1].interface_attr['GigabitEthernet1/0/9']\
            .if_pae = 'supplicant'
        dot1x.device_attr[self.dev1].interface_attr['GigabitEthernet1/0/9']\
            .if_supplicant_eap_profile = 'EAP-METH'
        dot1x.device_attr[self.dev1].interface_attr['GigabitEthernet1/0/9']\
            .if_credentials = 'switch4'
        dot1x.device_attr[self.dev1].interface_attr['GigabitEthernet1/0/9']\
            .if_closed = True
        dot1x.device_attr[self.dev1].interface_attr['GigabitEthernet1/0/9']\
            .if_port_control = 'auto'
        dot1x.device_attr[self.dev1].interface_attr['GigabitEthernet1/0/9']\
            .if_host_mode = 'single-host'

        cfgs = dot1x.build_config(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.\
            join([
                'dot1x system-auth-control',
                'dot1x supplicant force-multicast',
                'dot1x credential switch4',
                ' username switch4',
                ' password 0 cisco',
                ' exit',
                'interface GigabitEthernet1/0/9',
                ' dot1x pae supplicant',
                ' dot1x supplicant eap profile EAP-METH',
                ' dot1x credentials switch4',
                ' access-session port-control auto',
                ' access-session host-mode single-host',
                ' access-session closed',
                ' exit',
            ]))

        cfgs = dot1x.build_unconfig(apply=False)

        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.\
            join([
                'no dot1x system-auth-control',
                'no dot1x supplicant force-multicast',
                'no dot1x credential switch4',
                'interface GigabitEthernet1/0/9',
                ' no dot1x pae supplicant',
                ' no dot1x supplicant eap profile EAP-METH',
                ' no dot1x credentials switch4',
                ' no access-session port-control auto',
                ' no access-session host-mode single-host',
                ' no access-session closed',
                ' exit',
            ]))

        # uncfg with attributes
        cfgs = dot1x.build_unconfig(apply=False,
                  attributes={'device_attr': {
                                self.dev1: {
                                    'system_auth_control':  None,
                                    'credentials_attr': {
                                        'switch4': {
                                            'credential_username':  None
                                        }
                                    },
                                    'interface_attr': {
                                        'GigabitEthernet1/0/9': {
                                            'if_supplicant_eap_profile':  None,
                                        }
                                    },}}})
        
        # Check config built correctly
        self.assertMultiLineEqual(str(cfgs[self.dev1.name]), '\n'.\
            join([
                'no dot1x system-auth-control',
                'dot1x credential switch4',
                ' no username switch4',
                ' exit',
                'interface GigabitEthernet1/0/9',
                ' no dot1x supplicant eap profile EAP-METH',
                ' exit',
            ]))    

if __name__ == '__main__':
    unittest.main()
