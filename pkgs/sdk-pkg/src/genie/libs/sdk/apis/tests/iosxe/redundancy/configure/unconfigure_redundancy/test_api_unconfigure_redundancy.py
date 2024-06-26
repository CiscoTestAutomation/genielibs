import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.redundancy.configure import unconfigure_redundancy


class TestUnconfigureRedundancy(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          encore_sanity:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat8k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['encore_sanity']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_redundancy(self):
        result = unconfigure_redundancy(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
