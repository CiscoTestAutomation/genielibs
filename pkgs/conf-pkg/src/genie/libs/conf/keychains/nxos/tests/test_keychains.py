#!/usr/bin/env python

# import python
import unittest

# import genie
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Interface

# import genie.libs
from genie.libs.conf.keychains import Keychains


class test_keychains(TestCase):
    def test_keychains_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        keychains = Keychains()

        self.assertIs(keychains.testbed, testbed)
        dev1.add_feature(keychains)

        keychains.device_attr[dev1].keychain_attr['1'].key_id_attr[
            '2'].key_string = 'test'

        cfgs = keychains.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]), '\n'.join([
                'key chain 1', ' key 2', '  key-string test', '  exit', ' exit'
            ]))

        un_cfgs = keychains.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]),
                         '\n'.join(['no key chain 1']))

        keychains.device_attr[dev1].keychain_attr['1'].key_id_attr[
            '2'].key_string = 'test'
        keychains.device_attr[dev1].keychain_attr['1'].key_id_attr[
            '2'].key_enc_type = 7

        cfgs = keychains.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]), '\n'.join([
                'key chain 1', ' key 2', '  key-string 7 test', '  exit',
                ' exit'
            ]))

        un_cfgs = keychains.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]),
                         '\n'.join(['no key chain 1']))

    def test_ms_keychains_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        keychains = Keychains()

        self.assertIs(keychains.testbed, testbed)
        dev1.add_feature(keychains)

        keychains.device_attr[dev1].ms_keychain_attr['1'].key_id_attr[
            '2'].key_string = 'test'

        cfgs = keychains.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]), '\n'.join([
                'key chain 1 macsec', ' key 2', '  key-octet-string test',
                '  exit', ' exit'
            ]))

        un_cfgs = keychains.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]),
                         '\n'.join(['no key chain 1 macsec']))

        keychains.device_attr[dev1].ms_keychain_attr['1'].key_id_attr[
            '2'].key_string = 'test'
        keychains.device_attr[dev1].ms_keychain_attr['1'].key_id_attr[
            '2'].key_enc_type = 7
        keychains.device_attr[dev1].ms_keychain_attr['1'].key_id_attr[
            '2'].crypto_algo = 'aes-128-cmac'

        cfgs = keychains.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]), '\n'.join([
                'key chain 1 macsec', ' key 2',
                '  key-octet-string 7 test cryptographic-algorithm AES_128_CMAC',
                '  exit', ' exit'
            ]))

        un_cfgs = keychains.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]),
                         '\n'.join(['no key chain 1 macsec']))

    def test_te_keychains_cfg(self):
        Genie.testbed = testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='nxos')

        keychains = Keychains()

        self.assertIs(keychains.testbed, testbed)
        dev1.add_feature(keychains)

        keychains.device_attr[dev1].te_keychain_attr['1'].key_id_attr[
            '2'].key_string = 'test'

        cfgs = keychains.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]), '\n'.join([
                'key chain 1 tunnel-encryption', ' key 2',
                '  key-octet-string test', '  exit', ' exit'
            ]))

        un_cfgs = keychains.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]),
                         '\n'.join(['no key chain 1 tunnel-encryption']))

        keychains.device_attr[dev1].te_keychain_attr['1'].key_id_attr[
            '2'].key_string = 'test'
        keychains.device_attr[dev1].te_keychain_attr['1'].key_id_attr[
            '2'].key_enc_type = 7
        keychains.device_attr[dev1].te_keychain_attr['1'].key_id_attr[
            '2'].crypto_algo = 'aes-128-cmac'
        keychains.device_attr[dev1].te_keychain_attr['1'].key_id_attr[
            '2'].lifetime_start = '23:00:00 Jul 31 2021'
        keychains.device_attr[dev1].te_keychain_attr['1'].key_id_attr[
            '2'].lifetime_duration = 1800

        cfgs = keychains.build_config(apply=False)
        self.assertCountEqual(cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertMultiLineEqual(
            str(cfgs[dev1.name]), '\n'.join([
                'key chain 1 tunnel-encryption', ' key 2',
                '  key-octet-string 7 test cryptographic-algorithm AES_128_CMAC',
                '  send-lifetime 23:00:00 Jul 31 2021 duration 1800', '  exit',
                ' exit'
            ]))

        un_cfgs = keychains.build_unconfig(apply=False)
        self.assertCountEqual(un_cfgs.keys(), [dev1.name])
        self.maxDiff = None
        self.assertEqual(str(un_cfgs[dev1.name]),
                         '\n'.join(['no key chain 1 tunnel-encryption']))


if __name__ == '__main__':
    unittest.main()
