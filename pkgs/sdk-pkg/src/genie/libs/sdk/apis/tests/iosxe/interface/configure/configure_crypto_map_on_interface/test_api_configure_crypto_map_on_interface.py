import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_crypto_map_on_interface


class TestConfigureCryptoMapOnInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          CSR4:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['CSR4']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_crypto_map_on_interface(self):
        result = configure_crypto_map_on_interface(self.device, 'GigabitEthernet2', 'map_10', False)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_crypto_map_on_interface_1(self):
        result = configure_crypto_map_on_interface(self.device, 'GigabitEthernet4', 'map_20', True)
        expected_output = None
        self.assertEqual(result, expected_output)
