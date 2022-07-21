import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.umbrella_odns.execute import execute_clear_dns_statistics


class TestExecuteClearDnsStatistics(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          uut1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9200
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['uut1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_clear_dns_statistics(self):
        result = execute_clear_dns_statistics(self.device)
        expected_output = ''
        self.assertEqual(result, expected_output)
