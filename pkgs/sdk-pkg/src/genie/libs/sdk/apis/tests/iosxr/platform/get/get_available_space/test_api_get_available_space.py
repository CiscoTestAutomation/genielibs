import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxr.platform.get import get_available_space


class TestGetAvailableSpace(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          R2_xr:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxr --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxr
            platform: iosxrv9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R2_xr']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_available_space(self):
        result = get_available_space(self.device)
        expected_output = 933916000
        self.assertEqual(result, expected_output)
