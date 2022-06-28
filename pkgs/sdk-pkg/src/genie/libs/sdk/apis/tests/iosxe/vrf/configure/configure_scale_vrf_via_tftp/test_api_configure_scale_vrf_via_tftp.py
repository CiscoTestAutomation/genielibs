import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.vrf.configure import configure_scale_vrf_via_tftp


class TestConfigureScaleVrfViaTftp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Organ:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: router
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Organ']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_scale_vrf_via_tftp(self):
        result = configure_scale_vrf_via_tftp(self.device, {'myftpserver': {'custom': {'scale_config_path': '/auto/tftp-sjc-users4/siwwu/'},
                 'dynamic': True,
                 'protocol': 'ftp'}}, 2, 1, 10, False, False)
        expected_output = ('\n'
 '            vrf definition 2\n'
 '                address-family ipv4\n'
 '                address-family ipv6\n'
 '            exit\n'
 '            \n'
 '            vrf definition 3\n'
 '                address-family ipv4\n'
 '                address-family ipv6\n'
 '            exit\n'
 '            \n'
 '            vrf definition 4\n'
 '                address-family ipv4\n'
 '                address-family ipv6\n'
 '            exit\n'
 '            \n'
 '            vrf definition 5\n'
 '                address-family ipv4\n'
 '                address-family ipv6\n'
 '            exit\n'
 '            \n'
 '            vrf definition 6\n'
 '                address-family ipv4\n'
 '                address-family ipv6\n'
 '            exit\n'
 '            \n'
 '            vrf definition 7\n'
 '                address-family ipv4\n'
 '                address-family ipv6\n'
 '            exit\n'
 '            \n'
 '            vrf definition 8\n'
 '                address-family ipv4\n'
 '                address-family ipv6\n'
 '            exit\n'
 '            \n'
 '            vrf definition 9\n'
 '                address-family ipv4\n'
 '                address-family ipv6\n'
 '            exit\n'
 '            \n'
 '            vrf definition 10\n'
 '                address-family ipv4\n'
 '                address-family ipv6\n'
 '            exit\n'
 '            \n'
 '            vrf definition 11\n'
 '                address-family ipv4\n'
 '                address-family ipv6\n'
 '            exit\n'
 '            ')
        self.assertEqual(result, expected_output)
