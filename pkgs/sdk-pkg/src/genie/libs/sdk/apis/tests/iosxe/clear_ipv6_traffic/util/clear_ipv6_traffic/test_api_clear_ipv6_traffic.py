import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.clear_ipv6_traffic.util import clear_ipv6_traffic


class TestClearIpv6Traffic(unittest.TestCase):

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

    def test_clear_ipv6_traffic(self):
        result = clear_ipv6_traffic(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
