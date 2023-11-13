import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.device_tracking.configure import configure_device_policy_tracking


class TestConfigureDevicePolicyTracking(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9404_SVL_UUT2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9404_SVL_UUT2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_device_policy_tracking(self):
        result = configure_device_policy_tracking(self.device, 'SISF_1', True)
        expected_output = None
        self.assertEqual(result, expected_output)
