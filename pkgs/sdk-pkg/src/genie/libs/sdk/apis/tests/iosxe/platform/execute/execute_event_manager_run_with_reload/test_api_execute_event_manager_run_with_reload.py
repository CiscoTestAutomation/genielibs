import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.execute import execute_event_manager_run_with_reload


class TestExecuteEventManagerRunWithReload(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          MSFT_9500H_SPINE:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['MSFT_9500H_SPINE']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_event_manager_run_with_reload(self):
        result = execute_event_manager_run_with_reload(self.device, 'lab', 'lab', 'RELOAD', 10)
        expected_output = True
        self.assertEqual(result, expected_output)
