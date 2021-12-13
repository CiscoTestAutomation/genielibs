import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ipsec.configure import clear_crypto_sa_counters


class TestClearCryptoSaCounters(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          rad-vtep1:
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
        self.device = self.testbed.devices['rad-vtep1']
        self.device.connect()

    def test_clear_crypto_sa_counters(self):
        result = clear_crypto_sa_counters(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
