import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.pki.configure import configure_trustpoint


class TestConfigureTrustpoint(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          crypto-reg4:
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
        self.device = self.testbed.devices['crypto-reg4']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_trustpoint(self):
        result = configure_trustpoint(self.device, 'test', 'crl', '1024', 'True', 'regenerate', 'True', 'yes', None, 'test', 'yes', 'yes', 'all', 100, 'True', 'linux', '10.0.0.1', 'bootflash:tp_chain_location_test', 'True', 'True', 'C = IN', 'True', '100', '100', 'authorization list', 'test', 'client-auth', 'True', 'profile test', 'bootflash:test_enroll_url', '10', '10', 'True', None, 'none', 'sha512', 'test 1000', 'none', 'inherit ipv4', 'eku client-auth', 'vrf', '10.0.0.1', '80', 'True', None, 'test', 'True', 'True', 'none', 'proxy http://10.20.20.2', 'none', 'True', 'GigabitEthernet10', None, 'test', 'ike', 'test')
        expected_output = True
        self.assertEqual(result, expected_output)
