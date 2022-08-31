import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cts.configure import cts_refresh_environment_data


class TestCtsRefreshEnvironmentData(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          CTS-AUTO-C9500:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['CTS-AUTO-C9500']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_cts_refresh_environment_data(self):
        result = cts_refresh_environment_data(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
