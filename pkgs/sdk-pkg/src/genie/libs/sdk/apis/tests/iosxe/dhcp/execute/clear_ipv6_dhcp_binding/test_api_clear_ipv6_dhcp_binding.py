import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcp.execute import clear_ipv6_dhcp_binding


class TestClearIpv6DhcpBinding(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          DHCP_SERVER1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: ios
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['DHCP_SERVER1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_clear_ipv6_dhcp_binding(self):
        result = clear_ipv6_dhcp_binding(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
