import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nat.execute import execute_clear_nat64_statistics_global


class TestExecuteClearNat64StatisticsGlobal(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Stargazer:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9600
            type: c9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Stargazer']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_clear_nat64_statistics_global(self):
        result = execute_clear_nat64_statistics_global(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
