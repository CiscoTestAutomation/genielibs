import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.get import get_cpu_min_max_avg


class TestGetCpuMinMaxAvg(unittest.TestCase):

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

    def test_get_cpu_min_max_avg(self):
        result = get_cpu_min_max_avg(self.device)
        expected_output = {'avg': [1.4], 'max': [3], 'min': [1], 'slot': ['Switch2']}
        self.assertEqual(result, expected_output)
