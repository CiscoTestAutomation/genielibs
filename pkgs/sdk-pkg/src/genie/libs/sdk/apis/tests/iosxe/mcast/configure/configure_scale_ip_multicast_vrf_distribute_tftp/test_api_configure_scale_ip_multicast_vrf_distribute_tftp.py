import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.mcast.configure import configure_scale_ip_multicast_vrf_distribute_tftp


class TestConfigureScaleIpMulticastVrfDistributeTftp(unittest.TestCase):

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

    def test_configure_scale_ip_multicast_vrf_distribute_tftp(self):
        result = configure_scale_ip_multicast_vrf_distribute_tftp(self.device, {'myftpserver': {'custom': {'scale_config_path': '/auto/tftp-sjc-users4/siwwu/'},
                 'dynamic': True,
                 'protocol': 'ftp'}}, 2, 1, 10, False, False)
        expected_output = ('\n'
 '         ip multicast-routing vrf 2 distributed\n'
 '        \n'
 '         ip multicast-routing vrf 3 distributed\n'
 '        \n'
 '         ip multicast-routing vrf 4 distributed\n'
 '        \n'
 '         ip multicast-routing vrf 5 distributed\n'
 '        \n'
 '         ip multicast-routing vrf 6 distributed\n'
 '        \n'
 '         ip multicast-routing vrf 7 distributed\n'
 '        \n'
 '         ip multicast-routing vrf 8 distributed\n'
 '        \n'
 '         ip multicast-routing vrf 9 distributed\n'
 '        \n'
 '         ip multicast-routing vrf 10 distributed\n'
 '        \n'
 '         ip multicast-routing vrf 11 distributed\n'
 '        ')
        self.assertEqual(result, expected_output)
