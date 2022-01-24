import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.macsec.configure import config_mka_keychain_on_interface


class TestConfigMkaKeychainOnInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          LG-PK:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['LG-PK']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_config_mka_keychain_on_interface(self):
        result = config_mka_keychain_on_interface(device=self.device, interface='TwentyFiveGigE 1/0/7', key_string='mss', key_chain='fss')
        expected_output = None
        self.assertEqual(result, expected_output)
