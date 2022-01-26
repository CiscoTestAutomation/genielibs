import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_dhcp_pool_ipv6_domain_name


class TestConfigureDhcpPoolIpv6DomainName(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Intrepid-DUT-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: C9600
            type: C9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Intrepid-DUT-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_dhcp_pool_ipv6_domain_name(self):
        result = configure_dhcp_pool_ipv6_domain_name(device=self.device, pool_name='pool1', domain_name='cisco.com')
        expected_output = None
        self.assertEqual(result, expected_output)
