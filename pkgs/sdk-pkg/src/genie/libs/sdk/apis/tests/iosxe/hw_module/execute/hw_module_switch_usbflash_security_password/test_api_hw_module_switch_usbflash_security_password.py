import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.hw_module.execute import hw_module_switch_usbflash_security_password


class TestHwModuleSwitchUsbflashSecurityPassword(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-nyquist-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_hw_module_switch_usbflash_security_password(self):
        result = hw_module_switch_usbflash_security_password(self.device, 1, 'enable', 'password')
        expected_output = 'Error: USB Not Present in this Switch 1'
        self.assertEqual(result, expected_output)
