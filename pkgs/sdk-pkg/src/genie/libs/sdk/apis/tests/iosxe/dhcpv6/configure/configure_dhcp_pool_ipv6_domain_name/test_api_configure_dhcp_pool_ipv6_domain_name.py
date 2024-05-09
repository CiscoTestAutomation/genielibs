import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_dhcp_pool_ipv6_domain_name


class TestConfigureDhcpPoolIpv6DomainName(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          T1-9300-SW1:
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
        self.device = self.testbed.devices['T1-9300-SW1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_dhcp_pool_ipv6_domain_name(self):
        result = configure_dhcp_pool_ipv6_domain_name(self.device, 'DHCPPOOL', 'cisco.com', '2001:100:0:1::1')
        expected_output = None
        self.assertEqual(result, expected_output)
