import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.configure_ipv6_traffic_filter_acl.configure import configure_ipv6_traffic_filter_acl


class TestConfigureIpv6TrafficFilterAcl(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          A1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: single_rp
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['A1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ipv6_traffic_filter_acl(self):
        result = configure_ipv6_traffic_filter_acl(self.device, 11, 20, 'ipv6_md_acl', 'in')
        expected_output = None
        self.assertEqual(result, expected_output)
