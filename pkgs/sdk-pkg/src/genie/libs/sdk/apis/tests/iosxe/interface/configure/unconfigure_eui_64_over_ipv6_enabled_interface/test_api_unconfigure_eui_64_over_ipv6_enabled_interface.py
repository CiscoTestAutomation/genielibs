import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_eui_64_over_ipv6_enabled_interface


class TestUnconfigureEui64OverIpv6EnabledInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Starfleet:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9500
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Starfleet']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_eui_64_over_ipv6_enabled_interface(self):
        result = unconfigure_eui_64_over_ipv6_enabled_interface(self.device, 'TwentyFiveGigE1/0/23', '2009::2/64')
        expected_output = None
        self.assertEqual(result, expected_output)
