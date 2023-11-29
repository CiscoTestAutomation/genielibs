import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ipv6.clear import clear_ipv6_neighbors


class TestClearIpv6Neighbors(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          uut-9300:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['uut-9300']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_clear_ipv6_neighbors(self):
        result = clear_ipv6_neighbors(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
