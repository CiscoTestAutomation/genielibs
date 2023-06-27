import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_dhcp_pool_dns_server


class TestConfigureDhcpPoolDnsServer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-nyquist-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_dhcp_pool_dns_server(self):
        result = configure_dhcp_pool_dns_server(self.device, 'ipv6', 'test', '2001::26')
        expected_output = None
        self.assertEqual(result, expected_output)
