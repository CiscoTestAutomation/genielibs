import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.mpls.configure import debug_lfd_label_statistics


class TestDebugLfdLabelStatistics(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          T1-9400-Act:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9400
            type: c9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['T1-9400-Act']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_debug_lfd_label_statistics(self):
        result = debug_lfd_label_statistics(self.device, 19)
        expected_output = None
        self.assertEqual(result, expected_output)
