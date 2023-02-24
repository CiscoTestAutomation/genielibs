import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.csdl.configure import unconfigure_hw_module_switch_number_usbflash


class TestUnconfigureHwModuleSwitchNumberUsbflash(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          3850-48XS-CE3:
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
        self.device = self.testbed.devices['3850-48XS-CE3']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_hw_module_switch_number_usbflash(self):
        result = unconfigure_hw_module_switch_number_usbflash(self.device, '1')
        expected_output = None
        self.assertEqual(result, expected_output)
