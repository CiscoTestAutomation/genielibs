import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.sudi.verify import verify_crypto_entropy_status


class TestVerifyCryptoEntropyStatus(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Switch:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: Switch
            type: Switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_crypto_entropy_status(self):
        result = verify_crypto_entropy_status(self.device, ['ACT-2', 'randfill', 'getrandombytes'], 15, 5)
        expected_output = True
        self.assertEqual(result, expected_output)
