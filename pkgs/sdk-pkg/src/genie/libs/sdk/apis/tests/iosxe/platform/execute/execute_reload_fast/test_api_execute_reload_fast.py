import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.execute import execute_reload_fast


class TestExecuteReloadFast(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          AMZ-Acc-4:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['AMZ-Acc-4']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_reload_fast(self):
        result = execute_reload_fast(self.device, None, 'lab', 'lab', 10, 600)
        expected_output = True
        self.assertEqual(result, expected_output)
