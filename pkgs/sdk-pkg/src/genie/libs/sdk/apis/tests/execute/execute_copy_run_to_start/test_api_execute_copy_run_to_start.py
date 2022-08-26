import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.execute import execute_copy_run_to_start


class TestExecuteCopyRunToStart(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          FW-9800-7:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9800
            type: c9800
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['FW-9800-7']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_copy_run_to_start(self):
        result = execute_copy_run_to_start(self.device, 60, 30, 10, False)
        expected_output = None
        self.assertEqual(result, expected_output)
