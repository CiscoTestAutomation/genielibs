import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_interface_range_dhcp_channel_group_mode


class TestUnconfigureInterfaceRangeDhcpChannelGroupMode(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9404-Access:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9404-Access']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_interface_range_dhcp_channel_group_mode(self):
        result = unconfigure_interface_range_dhcp_channel_group_mode(self.device, 'Gi1/0/39', '41', '200', 'desirable')
        expected_output = None
        self.assertEqual(result, expected_output)
