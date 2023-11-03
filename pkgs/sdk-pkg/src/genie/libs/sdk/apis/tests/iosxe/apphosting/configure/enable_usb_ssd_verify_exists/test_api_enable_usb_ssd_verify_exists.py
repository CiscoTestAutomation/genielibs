import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.apphosting.configure import enable_usb_ssd_verify_exists


class TestEnableUsbSsdVerifyExists(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          javelin-morph-mini1a-c9300-stack:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['javelin-morph-mini1a-c9300-stack']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_enable_usb_ssd_verify_exists(self):
        result = enable_usb_ssd_verify_exists(self.device, 'usbflash1:.', 30)
        expected_output = True
        self.assertEqual(result, expected_output)
