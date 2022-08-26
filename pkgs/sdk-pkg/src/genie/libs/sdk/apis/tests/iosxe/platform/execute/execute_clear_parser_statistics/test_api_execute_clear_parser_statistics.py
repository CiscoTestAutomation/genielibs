import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.execute import execute_clear_parser_statistics


class TestExecuteClearParserStatistics(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          CAT9400_HA_IOX:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: None
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['CAT9400_HA_IOX']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_clear_parser_statistics(self):
        result = execute_clear_parser_statistics(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
