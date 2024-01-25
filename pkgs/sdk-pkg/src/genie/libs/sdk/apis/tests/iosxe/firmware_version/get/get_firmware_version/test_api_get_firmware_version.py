import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.firmware_version.get import get_firmware_version


class TestGetFirmwareVersion(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          HA-9400-S2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['HA-9400-S2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_firmware_version(self):
        result = get_firmware_version(self.device)
        expected_output = {'firmware_version': [['17050302'], ['17.10.1r', '(7.3, 7.0, 6.0)']],
 'name': [['Fan2/Tray'], ['Switch 2 Slot 3 Supervisor', 'PowerSupplyModule1']]}
        self.assertEqual(result, expected_output)
