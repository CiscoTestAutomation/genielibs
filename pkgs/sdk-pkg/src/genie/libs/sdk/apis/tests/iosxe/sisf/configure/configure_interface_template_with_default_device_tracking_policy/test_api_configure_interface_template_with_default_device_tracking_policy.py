import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.sisf.configure import configure_interface_template_with_default_device_tracking_policy


class TestConfigureInterfaceTemplateWithDefaultDeviceTrackingPolicy(unittest.TestCase):

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

    def test_configure_interface_template_with_default_device_tracking_policy(self):
        result = configure_interface_template_with_default_device_tracking_policy(self.device, 'template_test', None)
        expected_output = None
        self.assertEqual(result, expected_output)
