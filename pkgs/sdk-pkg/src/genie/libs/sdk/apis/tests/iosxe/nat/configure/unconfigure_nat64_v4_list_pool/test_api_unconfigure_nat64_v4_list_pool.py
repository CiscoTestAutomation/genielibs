import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_nat64_v4_list_pool


class TestUnconfigureNat64V4ListPool(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Stargazer:
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
        self.device = self.testbed.devices['Stargazer']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_nat64_v4_list_pool(self):
        result = unconfigure_nat64_v4_list_pool(self.device, 'acl_1', 'pool_1', 'vrf1', None)
        expected_output = None
        self.assertEqual(result, expected_output)
