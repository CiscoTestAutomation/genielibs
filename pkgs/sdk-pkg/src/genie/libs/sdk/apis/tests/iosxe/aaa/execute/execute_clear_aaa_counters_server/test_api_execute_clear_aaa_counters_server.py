import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.aaa.execute import execute_clear_aaa_counters_server


class TestExecuteClearAaaCountersServer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9300_UUT1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9300_UUT1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_clear_aaa_counters_server(self):
        result = execute_clear_aaa_counters_server(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
