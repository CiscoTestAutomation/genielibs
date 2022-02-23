import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ipsec.configure import unconfigure_crypto_transform_set


class TestUnconfigureCryptoTransformSet(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          9300x-A:
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
        self.device = self.testbed.devices['9300x-A']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_crypto_transform_set(self):
        result = unconfigure_crypto_transform_set(self.device, 'test_transform_name')
        expected_output = None
        self.assertEqual(result, expected_output)
