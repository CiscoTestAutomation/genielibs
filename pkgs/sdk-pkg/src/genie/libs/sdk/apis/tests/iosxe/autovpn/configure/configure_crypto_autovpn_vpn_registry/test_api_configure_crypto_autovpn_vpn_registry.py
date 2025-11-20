from unittest import TestCase
from genie.libs.sdk.apis.iosxe.autovpn.configure import configure_crypto_autovpn_vpn_registry
from unittest.mock import Mock


class TestConfigureCryptoAutovpnVpnRegistry(TestCase):

    def test_configure_crypto_autovpn_vpn_registry(self):
        self.device = Mock()
        result = configure_crypto_autovpn_vpn_registry(self.device, 'deep', '1.1.1.1', 9351, '2.2.2.2', 9352, {'device_id': 'FFFFF',
 'device_num': 34523,
 'is_hub': True,
 'load_balance': True,
 'multi_uplink_tunnels': True,
 'uplink0_name': 'Loopback0',
 'uplink1_name': 'Loopback1'}, [{'device_id': 'ABCDEF1234567890',
  'device_num': 12345,
  'is_hub': False,
  'multi_uplink_tunnels': False,
  'peer_psk': 'mySecretKey1'}])
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto autovpn deep', 'vpn-registry server ipv4 1.1.1.1 9351 2.2.2.2 9352', 'local 34523 FFFFF true true true Loopback0 Loopback1', 'remote 12345 ABCDEF1234567890 false false mySecretKey1', 'exit'],)
        )
