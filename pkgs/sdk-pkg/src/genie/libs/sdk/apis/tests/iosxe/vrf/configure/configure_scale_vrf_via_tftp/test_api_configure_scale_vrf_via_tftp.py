import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.vrf.configure import configure_scale_vrf_via_tftp


class TestConfigureScaleVrfViaTftp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Minuet:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: router
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Minuet']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_scale_vrf_via_tftp(self):
        result = configure_scale_vrf_via_tftp(self.device, {'myftpserver': {'address': None,
                 'custom': {'scale_config_path': '/auto/tftp-sjc-users4/siwwu/'},
                 'dynamic': True,
                 'path': '/',
                 'protocol': 'ftp',
                 'subnet': '171.70.0.0/16'}}, 1, 1, 5, False, False)
        expected_output = ('\n'
 '            vrf definition 1\n'
 '                rd 1:1\n'
 '                !\n'
 '                address-family ipv4\n'
 '                exit-address-family\n'
 '                !\n'
 '                address-family ipv6\n'
 '                exit-address-family\n'
 '            !\n'
 '            \n'
 '            vrf definition 2\n'
 '                rd 2:2\n'
 '                !\n'
 '                address-family ipv4\n'
 '                exit-address-family\n'
 '                !\n'
 '                address-family ipv6\n'
 '                exit-address-family\n'
 '            !\n'
 '            \n'
 '            vrf definition 3\n'
 '                rd 3:3\n'
 '                !\n'
 '                address-family ipv4\n'
 '                exit-address-family\n'
 '                !\n'
 '                address-family ipv6\n'
 '                exit-address-family\n'
 '            !\n'
 '            \n'
 '            vrf definition 4\n'
 '                rd 4:4\n'
 '                !\n'
 '                address-family ipv4\n'
 '                exit-address-family\n'
 '                !\n'
 '                address-family ipv6\n'
 '                exit-address-family\n'
 '            !\n'
 '            \n'
 '            vrf definition 5\n'
 '                rd 5:5\n'
 '                !\n'
 '                address-family ipv4\n'
 '                exit-address-family\n'
 '                !\n'
 '                address-family ipv6\n'
 '                exit-address-family\n'
 '            !\n'
 '            ')
        self.assertEqual(result, expected_output)
