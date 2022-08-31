import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_sks_client


class TestConfigureSksClient(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Hub:
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
        self.device = self.testbed.devices['Hub']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_sks_client(self):
        result = configure_sks_client(self.device, 'test_block_1', 'ipv6', '9e21:953d:1870:c090:4cf3:51a6:cce8:3337', '4321', 'test_psk_1', 'test_password_1')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_sks_client_1(self):
        result = configure_sks_client(self.device, 'test_block_2', 'ipv4', '23.45.21.43', '9675', 'test_psk_2', 'test_password_2')
        expected_output = None
        self.assertEqual(result, expected_output)
