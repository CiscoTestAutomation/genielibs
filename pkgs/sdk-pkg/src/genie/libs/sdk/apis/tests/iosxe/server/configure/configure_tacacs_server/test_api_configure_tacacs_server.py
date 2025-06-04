from unittest import TestCase
from genie.libs.sdk.apis.iosxe.server.configure import configure_tacacs_server
from unittest.mock import Mock


class TestConfigureTacacsServer(TestCase):

    def test_configure_tacacs_server(self):
        self.device = Mock()
        result = configure_tacacs_server(self.device, [{
            'host': 'TAC',
  'key': 'cisco',
  'key_type': '7',
  'server': '10.76.239.47',
  'timeout': '5',
  'tls_connection_timeout': '32',
  'tls_idle_timeout': '61',
  'tls_ip_tacacs_source_interface': 'GigabitEthernet1',
  'tls_ip_vrf_forwarding': 'Mgmt-vrf',
  'tls_ipv6_tacacs_source_interface': 'GigabitEthernet1',
  'tls_ipv6_vrf_forwarding': 'Mgmt-vrf',
  'tls_match_server_identity_dns_id': 'cisco.com',
  'tls_match_server_identity_ip_address': 'cisco.com',
  'tls_match_server_identity_srv_id': 'cisco.com',
  'tls_port': '6049',
  'tls_retries': '2',
  'tls_trustpoint_client': 'TLS_IP_SELF_SIGNED',
  'tls_trustpoint_server': 'TLS_IP_SELF_SIGNED'}])
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (('tacacs server TAC\n'
 'address ipv4 10.76.239.47\n'
 'timeout 5\n'
 'key 7 cisco\n'
 'tls port 6049\n'
 'tls idle-timeout 61\n'
 'tls connection-timeout 32\n'
 'tls retries 2\n'
 'tls trustpoint client TLS_IP_SELF_SIGNED\n'
 'tls trustpoint server TLS_IP_SELF_SIGNED\n'
 'tls ip tacacs source-interface GigabitEthernet1\n'
 'tls ip vrf forwarding Mgmt-vrf\n'
 'tls ipv6 tacacs source-interface GigabitEthernet1\n'
 'tls ipv6 vrf forwarding Mgmt-vrf\n'
 'tls match-server-identity dns-id cisco.com\n'
 'tls match-server-identity ip-address cisco.com\n'
 'tls match-server-identity srv-id cisco.com\n'
 'exit\n'),)
        )
