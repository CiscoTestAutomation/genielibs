import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.gdoi.configure import configure_crypto_map_for_gdoi


class TestConfigureCryptoMapForGdoi(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Router:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Router']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_crypto_map_for_gdoi(self):
        result = configure_crypto_map_for_gdoi(self.device, 'test_map_ipv6', '12', 'gp_2', 'This is a ipv6 crypto map', True)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_crypto_map_for_gdoi_1(self):
        result = configure_crypto_map_for_gdoi(self.device, 'test_map_ipv4', '10', 'gp_1', 'This is a ipv4 crypto map', False)
        expected_output = None
        self.assertEqual(result, expected_output)
