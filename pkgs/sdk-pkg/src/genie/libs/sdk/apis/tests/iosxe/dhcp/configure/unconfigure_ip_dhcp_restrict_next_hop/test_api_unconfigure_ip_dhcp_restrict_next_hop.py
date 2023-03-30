import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_ip_dhcp_restrict_next_hop


class TestUnconfigureIpDhcpRestrictNextHop(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          T1_switch:
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
        self.device = self.testbed.devices['T1_switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_ip_dhcp_restrict_next_hop(self):
        result = unconfigure_ip_dhcp_restrict_next_hop(self.device, 'GigabitEthernet1/0/1')
        expected_output = None
        self.assertEqual(result, expected_output)
