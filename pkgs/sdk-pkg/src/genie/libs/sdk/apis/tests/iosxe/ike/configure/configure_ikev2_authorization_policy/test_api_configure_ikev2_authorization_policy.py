import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ike.configure import configure_ikev2_authorization_policy


class TestConfigureIkev2AuthorizationPolicy(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          TLS_Mad2:
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
        self.device = self.testbed.devices['TLS_Mad2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ikev2_authorization_policy(self):
        result = configure_ikev2_authorization_policy(self.device, 'IKEv2_AUTH_POLICY', True, None, 'ipv4_acl', 'ipv6_acl', '20.20.20.0', '255.255.255.0', '2001::', '64', '30.30.30.0', '255.255.255.255', '3001::', '64', '100.100.100.1', '50.50.50.1', '30', 'ppool', '100', '1.1.1.1', '2.2.2.2', 'test', '255.255.255.0', True, '5001::1', 'ipv6_pool', '128', '1200', None, '5', '200.200.200.1', 'cisco.com', '1.1.1.1')
        expected_output = None
        self.assertEqual(result, expected_output)
