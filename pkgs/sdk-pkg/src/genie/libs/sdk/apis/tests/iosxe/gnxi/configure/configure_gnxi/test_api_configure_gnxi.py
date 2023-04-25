import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.gnxi.configure import configure_gnxi


class TestConfigureGnxi(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          ott-c9300-09:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['ott-c9300-09']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_gnxi_enable(self):
        result = configure_gnxi(self.device)
        expected_output = ['gnxi']
        self.assertEqual(result, expected_output)

    def test_configure_gnxi_port(self):
        result = configure_gnxi(self.device, port=8080)
        expected_output = ['gnxi', 'gnxi port 8080']
        self.assertEqual(result, expected_output)

    def test_configure_gnxi_secure_port(self):
        result = configure_gnxi(self.device, secure_port=443)
        expected_output = ['gnxi', 'gnxi secure-port 443']
        self.assertEqual(result, expected_output)

    def test_configure_gnxi_secure_allow_self_signed_trustpoint(self):
        result = configure_gnxi(self.device, secure_allow_self_signed_trustpoint=True)
        expected_output = ['gnxi', 'gnxi secure-allow-self-signed-trustpoint']
        self.assertEqual(result, expected_output)

    def test_configure_gnxi_secure_client_auth(self):
        result = configure_gnxi(self.device, secure_client_auth=True)
        expected_output = ['gnxi', 'gnxi secure-client-auth']
        self.assertEqual(result, expected_output)

    def test_configure_gnxi_secure_password_auth(self):
        result = configure_gnxi(self.device, secure_password_auth=True)
        expected_output = ['gnxi', 'gnxi secure-password-auth']
        self.assertEqual(result, expected_output)

    def test_configure_gnxi_secure_peer_verify_trustpoint(self):
        result = configure_gnxi(self.device, secure_peer_verify_trustpoint='gnoi_tp')
        expected_output = ['gnxi', 'gnxi secure-peer-verify-trustpoint gnoi_tp']
        self.assertEqual(result, expected_output)

    def test_configure_gnxi_secure_trustpoint(self):
        result = configure_gnxi(self.device, secure_trustpoint='gnoi_tp')
        expected_output = ['gnxi', 'gnxi secure-trustpoint gnoi_tp']
        self.assertEqual(result, expected_output)

    def test_configure_gnxi_secure_init(self):
        result = configure_gnxi(self.device, secure_init=True)
        expected_output = ['gnxi', 'gnxi secure-init']
        self.assertEqual(result, expected_output)

    def test_configure_gnxi_server(self):
        result = configure_gnxi(self.device, server=True)
        expected_output = ['gnxi', 'gnxi server']
        self.assertEqual(result, expected_output)

    def test_configure_gnxi_secure_server(self):
        result = configure_gnxi(self.device, secure_server=True)
        expected_output = ['gnxi', 'gnxi secure-server']
        self.assertEqual(result, expected_output)

    def test_configure_gnxi_secure_server_port(self):
        result = configure_gnxi(self.device, secure_port=443, secure_server=True)
        expected_output = ['gnxi', 'gnxi secure-port 443', 'gnxi secure-server']
        self.assertEqual(result, expected_output)

    def test_configure_gnxi_server_port(self):
        result = configure_gnxi(self.device, port=8080, server=True)
        expected_output = ['gnxi', 'gnxi port 8080', 'gnxi server']
        self.assertEqual(result, expected_output)

    def test_configure_gnxi_servers(self):
      result = configure_gnxi(self.device, server=True, secure_server=True)
      expected_output = ['gnxi', 'gnxi server', 'gnxi secure-server']
      self.assertEqual(result, expected_output)

    def test_configure_gnxi_secure_init_password_auth(self):
        result = configure_gnxi(self.device, secure_password_auth=True, secure_init=True)
        expected_output = ['gnxi', 'gnxi secure-password-auth', 'gnxi secure-init']
        self.assertEqual(result, expected_output)

    def test_configure_gnxi_secure_peer_verify_trustpoint_and_trustpoint(self):
        result = configure_gnxi(self.device, secure_peer_verify_trustpoint='gnoi_tp', secure_trustpoint='gnoi_tp', server=True, port=None)
        expected_output = ['gnxi', 'gnxi secure-peer-verify-trustpoint gnoi_tp', 'gnxi secure-trustpoint gnoi_tp', 'gnxi server']
        self.assertEqual(result, expected_output)

    def test_configure_gnxi_disable_server(self):
        result = configure_gnxi(self.device, enable=False, server=True)
        expected_output = ['gnxi server']
        self.assertEqual(result, expected_output)

    def test_configure_gnxi_disable_secure_init(self):
        result = configure_gnxi(self.device, enable=False, secure_init=True)
        expected_output = ['gnxi secure-init']
        self.assertEqual(result, expected_output)

    def test_configure_gnxi_disable_secure_password_auth(self):
        result = configure_gnxi(self.device, enable=False, secure_password_auth=True)
        expected_output = ['gnxi secure-password-auth']
        self.assertEqual(result, expected_output)

    def test_configure_gnxi_all_params(self):
        result = configure_gnxi(self.device, enable=True, server=True, secure_server=True, secure_port=443, port=8080,
                                secure_allow_self_signed_trustpoint=True, secure_client_auth=True, secure_init=True,
                                secure_password_auth=True, secure_peer_verify_trustpoint='gnoi_tp',
                                secure_trustpoint='gnoi_tp')
        expected_output = ['gnxi', 'gnxi secure-port 443', 'gnxi port 8080', 'gnxi secure-allow-self-signed-trustpoint',
                            'gnxi secure-client-auth', 'gnxi secure-password-auth',
                            'gnxi secure-peer-verify-trustpoint gnoi_tp', 'gnxi secure-trustpoint gnoi_tp',
                            'gnxi secure-init', 'gnxi server', 'gnxi secure-server']
        self.assertEqual(result, expected_output)
