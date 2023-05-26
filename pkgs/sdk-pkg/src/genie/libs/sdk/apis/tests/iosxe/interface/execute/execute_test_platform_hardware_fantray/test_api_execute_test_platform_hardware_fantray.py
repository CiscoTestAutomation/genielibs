import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.execute import execute_test_platform_hardware_fantray


class TestExecuteTestPlatformHardwareFantray(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          NG_SVL_AUT1:
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
        self.device = self.testbed.devices['NG_SVL_AUT1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_test_platform_hardware_fantray(self):
        result = execute_test_platform_hardware_fantray(self.device, 'On', 2)
        expected_output = ('Fantray speed(RPM)\r\n'
 'Row  Fan1   | Fan2   | Fan3   | Throttle | Interrupt Source\r\n'
 '---  ------   ------ ------   --------   ----------------\r\n'
 '1    7950     8010    8040     58%        0               \r\n'
 '2    7950     8010    8010     58%        0               \r\n'
 '3    8010     8010    8010     58%        0               \r\n'
 'Fantray global interrupt source register = 0x8700\r\n'
 'Fantray global version : 0x18101008\r\n'
 'Fantray AIRDAM Status : 0x84\r\n'
 'Fantray beacon LED status: off\r\n'
 'Fantray status LED: green')
        self.assertEqual(result, expected_output)
