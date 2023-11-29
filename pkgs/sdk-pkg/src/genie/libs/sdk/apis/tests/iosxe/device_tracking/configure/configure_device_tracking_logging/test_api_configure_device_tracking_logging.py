import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.device_tracking.configure import configure_device_tracking_logging


class TestConfigureDeviceTrackingLogging(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          T4-9300-SW1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['T4-9300-SW1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_device_tracking_logging(self):
        result = configure_device_tracking_logging(self.device, 'packet')
        expected_output = None
        self.assertEqual(result, expected_output)
