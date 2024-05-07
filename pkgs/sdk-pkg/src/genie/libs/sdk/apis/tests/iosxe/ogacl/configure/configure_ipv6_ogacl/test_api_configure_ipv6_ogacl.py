import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ogacl.configure import configure_ipv6_ogacl


class TestConfigureIpv6Ogacl(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Intrepid-DUT-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            model: c9600
            type: C9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Intrepid-DUT-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ipv6_ogacl(self):
        result = configure_ipv6_ogacl(device=self.device, acl_name='ipv6-all-2', service_og='v6-serv-all', src_nw='v6-srcnet-all', dst_nw='any', rule='permit', service_type='', log_option='log', sequence_num=100)
        expected_output = None
        self.assertEqual(result, expected_output)
