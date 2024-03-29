import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ip_dhcp_pool_address


class TestConfigureIpDhcpPoolAddress(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Switch:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9200
            type: c9200
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ip_dhcp_pool_address(self):
        result = configure_ip_dhcp_pool_address(self.device, 'vlan501', '1.1.1.1', '0063.6973.636f.2d30.3062.362e.3730.3337.2e39.6630.302d.4769.302f.30')
        expected_output = None
        self.assertEqual(result, expected_output)
