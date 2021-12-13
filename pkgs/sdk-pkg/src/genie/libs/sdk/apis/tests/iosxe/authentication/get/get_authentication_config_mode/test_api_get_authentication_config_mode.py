import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.authentication.get import get_authentication_config_mode


class TestGetAuthenticationConfigMode(unittest.TestCase):

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

    def test_get_authentication_config_mode(self):
        result = get_authentication_config_mode(device=self.device)
        expected_output = {'current_config_mode': 'legacy'}
        self.assertEqual(result, expected_output)
