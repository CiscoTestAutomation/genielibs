import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.macsec.configure import config_mka_policy


class TestConfigMkaPolicy(unittest.TestCase):

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

    def test_config_mka_policy(self):
        result = config_mka_policy(device=self.device, global_level=True, interface='TwentyFiveGigE 1/0/7', cipher='GCM-AES-128', send_secure_announcements='', sak_rekey_int=180, key_server_priority=255, sak_rekey_on_live_peer_loss=True, conf_offset=30, policy_name='MKA_policy1', delay_protection=True)
        expected_output = None
        self.assertEqual(result, expected_output)
