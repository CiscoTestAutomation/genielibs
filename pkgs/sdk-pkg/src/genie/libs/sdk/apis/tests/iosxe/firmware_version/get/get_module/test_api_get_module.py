import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.firmware_version.get import get_module


class TestGetModule(unittest.TestCase):

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

    def test_get_module(self):
        result = get_module(self.device)
        expected_output = []
        self.assertEqual(result, expected_output)
