import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nhrp.clear import clear_dmvpn_crypto_nhrp_ike_stats


class TestClearDmvpnCryptoNhrpIkeStats(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          ASR_2hx:
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
        self.device = self.testbed.devices['ASR_2hx']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_clear_dmvpn_crypto_nhrp_ike_stats(self):
        result = clear_dmvpn_crypto_nhrp_ike_stats(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
