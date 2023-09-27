import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.get import get_interface_capabilities_multiple_media_types


class TestGetInterfaceCapabilitiesMultipleMediaTypes(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          IE-3105-18T2C-uut1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: s5k
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['IE-3105-18T2C-uut1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_interface_capabilities_multiple_media_types(self):
        result = get_interface_capabilities_multiple_media_types(self.device, 'GigabitEthernet1/1')
        expected_output = 'rj45, sfp, auto-select'
        self.assertEqual(result, expected_output)
