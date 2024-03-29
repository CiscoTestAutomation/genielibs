import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.memory_states.get import get_platform_memory_status


class TestGetPlatformMemoryStatus(unittest.TestCase):

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
            platform: cat9k
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['HA-9400-S2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_platform_memory_status(self):
        result = get_platform_memory_status(self.device)
        expected_output = {'committed': [10519281664],
 'free': [7996248064],
 'slot': ['Switch2'],
 'total': [16372314112],
 'used': [8376066048]}
        self.assertEqual(result, expected_output)
