import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.sisf.configure import unconfigure_ipv6_dhcp_guard_on_interface


class TestUnconfigureIpv6DhcpGuardOnInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          sisf-c9500-11:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: ios
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['sisf-c9500-11']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_ipv6_dhcp_guard_on_interface(self):
        result = unconfigure_ipv6_dhcp_guard_on_interface(self.device, 'TwentyFiveGigE1/0/1')
        expected_output = None
        self.assertEqual(result, expected_output)
