import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.execute import execute_test_crash


class TestExecuteTestCrash(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          startrek-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9300X
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['startrek-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_test_crash(self):
        result = execute_test_crash(self.device, '6', 500, 200)
        expected_output = None
        self.assertEqual(result, expected_output)
