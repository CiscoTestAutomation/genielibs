import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.execute import test_platform_software_usb_fake_insert_remove


class TestTestPlatformSoftwareUsbFakeInsertRemove(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack-9350:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack-9350']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_test_platform_software_usb_fake_insert_remove(self):
        result = test_platform_software_usb_fake_insert_remove(self.device, 1, 'usbflash1', 'fake-insert')
        expected_output = None
        self.assertEqual(result, expected_output)
