import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.logging.configure import configure_terminal_length


class TestConfigureTerminalLength(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          c2_core_sf:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['c2_core_sf']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_terminal_length(self):
        result = configure_terminal_length(self.device, 0)
        expected_output = None
        self.assertEqual(result, expected_output)
