import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nat.execute import execute_clear_nat64_statistics_interface


class TestExecuteClearNat64StatisticsInterface(unittest.TestCase):

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

    def test_execute_clear_nat64_statistics_interface(self):
        result = execute_clear_nat64_statistics_interface(self.device, 'TenGigabitEthernet1/2/0/35')
        expected_output = None
        self.assertEqual(result, expected_output)
