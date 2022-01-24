"""
test_tunnelencryption.py

"""
#python
import unittest
from unittest.mock import Mock

# Genie package
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

from genie.libs.conf.tunnel_encryption import TunnelEncryption

class test_tunnelencryption(TestCase):
    def test_basic_tunnel_config(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')
        tunnelencryption = TunnelEncryption()
        tunnelencryption.device_attr[dev1].enabled = True
        tunnelencryption.device_attr[dev1].enabled_must_secure_policy = True
        tunnelencryption.device_attr[dev1].tunnel_source_interface = 'loopback21'

        self.assertIs(tunnelencryption.testbed, testbed)
        dev1.add_feature(tunnelencryption)
        cfgs = tunnelencryption.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['feature tunnel-encryption',
             'tunnel-encryption must-secure-policy',
             'tunnel-encryption source-interface loopback21'
             ]))

        un_cfgs = tunnelencryption.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]), '\n'.join(
            ['no feature tunnel-encryption',
             ]))

    def test_tunnel_policy(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        tunnelencryption = TunnelEncryption()
        tunnelencryption.device_attr[dev1].tunnelpolicy_attr['kc1'].cipher_suite='gcm-aes-xpn-128'
        tunnelencryption.device_attr[dev1].tunnelpolicy_attr['kc1'].sak_rekey_time= 2500000

        self.assertIs(tunnelencryption.testbed, testbed)
        dev1.add_feature(tunnelencryption)
        cfgs = tunnelencryption.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['tunnel-encryption policy kc1',
             ' cipher-suite GCM-AES-XPN-128',
             ' sak-rekey-time 2500000',
             ' exit',
             ]))
        un_cfgs = tunnelencryption.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]), '\n'.join(
            ['no tunnel-encryption policy kc1',
             ]))

    def test_tunnel_peerip(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        tunnelencryption = TunnelEncryption()
        tunnelencryption.device_attr[dev1].tunnelpeerip_attr['100.100.100.2'].keychain_name='kc1'
        tunnelencryption.device_attr[dev1].tunnelpeerip_attr['100.100.100.2'].tunnelpolicy_name = 'kc1'

        self.assertIs(tunnelencryption.testbed, testbed)
        dev1.add_feature(tunnelencryption)
        cfgs = tunnelencryption.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(str(cfgs[dev1.name]), '\n'.join(
            ['tunnel-encryption peer-ip 100.100.100.2',
             ' keychain kc1 policy kc1',
             ' exit',
             ]))
        un_cfgs = tunnelencryption.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]), '\n'.join(
            ['no tunnel-encryption peer-ip 100.100.100.2',
             ]))


if __name__ == '__main__':
    unittest.main()