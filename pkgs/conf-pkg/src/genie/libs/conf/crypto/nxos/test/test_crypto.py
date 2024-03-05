#!/usr/bin/env python

# import python
import unittest

# import genie
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Interface

# import genie.libs
from genie.libs.conf.crypto import Crypto

class test_crypto(TestCase):
    def test_crypto_feature_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        crypto = Crypto()

        self.assertIs(crypto.testbed, testbed)
        dev1.add_feature(crypto)
        
        crypto.device_attr[dev1].enabled = True 
        
        cfgs = crypto.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]), '\n'.join([
                'feature cryptopqc'
            ]))

        un_cfgs = crypto.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]),
                         '\n'.join(['no feature cryptopqc']))
        
    def test_crypto_qkd_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        crypto = Crypto()

        self.assertIs(crypto.testbed, testbed)
        dev1.add_feature(crypto)
        
        crypto.device_attr[dev1].crypto_qkd_attr['QKD1'].kme_server_ip = '172.160.10.10'
        crypto.device_attr[dev1].crypto_qkd_attr['QKD1'].kme_server_http_port = 6000
        crypto.device_attr[dev1].crypto_qkd_attr['QKD1'].tls_auth_type = 'trustpoint'
        crypto.device_attr[dev1].crypto_qkd_attr['QKD1'].tls_trustpoint_name = 'tp1'
        
        
        cfgs = crypto.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]), '\n'.join([
                'crypto qkd profile QKD1', 
                ' kme server 172.160.10.10  port 6000',
                ' transport tls authentication-type trustpoint tp1',
                ' exit'
            ]))

        un_cfgs = crypto.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]),
                         '\n'.join(['no crypto qkd profile QKD1']))
    
    
if __name__ == '__main__':
    unittest.main()
