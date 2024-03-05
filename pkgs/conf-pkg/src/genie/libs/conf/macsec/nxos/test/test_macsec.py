#!/usr/bin/env python

# import python
import unittest

# import genie
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Interface

# import genie.libs
from genie.libs.conf.macsec import Macsec

class test_macsec(TestCase):
    def test_macsec_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        macsec = Macsec()

        self.assertIs(macsec.testbed, testbed)
        dev1.add_feature(macsec)

        macsec.device_attr[dev1].macsec_policy_attr['MP1'].key_server_priority = 32
        macsec.device_attr[dev1].macsec_policy_attr['MP1'].cipher_suite = 'GCM-AES-128'
        macsec.device_attr[dev1].macsec_policy_attr['MP1'].conf_offset = 'CONF-OFFSET-30'
        macsec.device_attr[dev1].macsec_policy_attr['MP1'].security_policy = 'must-secure'
        macsec.device_attr[dev1].macsec_policy_attr['MP1'].sak_expiry_timer = 70
        macsec.device_attr[dev1].macsec_policy_attr['MP1'].include_icv_indicator = True 
        macsec.device_attr[dev1].macsec_policy_attr['MP1'].include_sci = False 
        macsec.device_attr[dev1].macsec_policy_attr['MP1'].window_size = 100000
        macsec.device_attr[dev1].macsec_policy_attr['MP1'].ppk_profile_name = 'QKD1'
        
        cfgs = macsec.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]), '\n'.join([
                'macsec policy MP1', ' key-server-priority 32', ' cipher-suite GCM-AES-128',
                ' conf-offset CONF-OFFSET-30',
                ' security-policy must-secure',
                ' sak-expiry-time 70',
                ' include-icv-indicator',
                ' no include-sci',
                ' window-size 100000',
                ' ppk crypto-qkd-profile QKD1',
                ' exit'
            ]))

        un_cfgs = macsec.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]),
                         '\n'.join(['no macsec policy MP1']))
    
    def test_macsec_cipher_enforce_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        macsec = Macsec()

        self.assertIs(macsec.testbed, testbed)
        dev1.add_feature(macsec)
        macsec.device_attr[dev1].macsec_policy_attr['MP2'].enforce_cipher_suite = 'GCM-AES-256'
        
        cfgs = macsec.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]), '\n'.join([
                'macsec policy MP2', ' cipher-suite enforce-peer GCM-AES-256',
                ' exit'
            ]))

        un_cfgs = macsec.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]),
                         '\n'.join(['no macsec policy MP2']))


    def test_macsec_interface_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        macsec = Macsec()

        self.assertIs(macsec.testbed, testbed)
        dev1.add_feature(macsec)
        
        macsec.device_attr[dev1].interface_attr['Eth1/1'].macsec_policy_name = 'MP1'
        macsec.device_attr[dev1].interface_attr['Eth1/1'].key_chain = 'KC1'
        macsec.device_attr[dev1].interface_attr['Eth1/1'].eapol_mac_address = '0001.0002.0003'
        macsec.device_attr[dev1].interface_attr['Eth1/1'].ether_type = '888E'    
        
        cfgs = macsec.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]), '\n'.join([
                'interface Eth1/1', ' macsec keychain KC1 policy MP1',
                ' eapol mac-address 0001.0002.0003 ethertype 0x888E',
                ' exit'
            ]))

        un_cfgs = macsec.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(
            str(un_cfgs[dev1.name]), '\n'.join([
                'interface Eth1/1', ' no macsec keychain KC1 policy MP1',
                ' no eapol mac-address 0001.0002.0003 ethertype 0x888E',
                ' exit'
            ]))
        
if __name__ == '__main__':
    unittest.main()
