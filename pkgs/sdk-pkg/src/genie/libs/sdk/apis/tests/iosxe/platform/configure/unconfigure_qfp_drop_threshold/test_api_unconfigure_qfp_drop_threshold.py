import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_qfp_drop_threshold


class TestUnconfigureQfpDropThreshold(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Router:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: ASR1K
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Router']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_qfp_drop_threshold_percause(self):
        result = unconfigure_qfp_drop_threshold(self.device, 10, drop_id=2)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_qfp_drop_threshold_total(self):
        result = unconfigure_qfp_drop_threshold(self.device, 20)
        expected_output = None
        self.assertEqual(result, expected_output)
