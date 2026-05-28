import unittest
from unittest.mock import patch, MagicMock
from pyats.datastructures import AttrDict

from genie.libs.filetransferutils.bases.fileutils import FileUtilsBase as FileUtils


class TestResolveServerRouteUrl(unittest.TestCase):
    """Tests for FileUtils._resolve_server_route_url"""

    def setUp(self):
        self.testbed = AttrDict(
            servers=AttrDict(
                myserver=dict(
                    server='10.1.1.1',
                    address='10.1.1.1',
                    interfaces=dict(
                        ens192=dict(ipv4='10.1.0.1/16'),
                        ens224=dict(ipv4='172.16.0.1/12'),
                    ),
                    routes=dict(
                        ipv4=[
                            dict(subnet='10.1.0.0/16', interface='ens192'),
                            dict(subnet='172.16.0.0/12', interface='ens224'),
                        ]
                    ),
                ),
            ),
        )
        self.mock_api = MagicMock()
        self.device = AttrDict(
            name='R1',
            os='iosxe',
            testbed=self.testbed,
            management=AttrDict(
                address=AttrDict(ipv4='10.1.5.10/16')
            ),
            api=self.mock_api,
        )
        self.fu = FileUtils(os='iosxe', testbed=self.testbed, device=self.device)

    def test_rewrite_url_when_route_matches(self):
        self.mock_api.find_server_ip_for_device_ip.return_value = '10.1.0.1'
        result = self.fu._resolve_server_route_url(
            'tftp://10.1.1.1/auto/image.bin', device=self.device)
        self.assertEqual(result, 'tftp://10.1.0.1/auto/image.bin')
        self.mock_api.find_server_ip_for_device_ip.assert_called_once_with(
            '10.1.5.10', self.testbed.servers,
            server_hostname='10.1.1.1')

    def test_no_rewrite_when_no_match(self):
        self.mock_api.find_server_ip_for_device_ip.return_value = None
        result = self.fu._resolve_server_route_url(
            'tftp://10.1.1.1/auto/image.bin', device=self.device)
        self.assertEqual(result, 'tftp://10.1.1.1/auto/image.bin')

    def test_no_rewrite_when_resolved_matches_current(self):
        self.mock_api.find_server_ip_for_device_ip.return_value = '10.1.1.1'
        result = self.fu._resolve_server_route_url(
            'tftp://10.1.1.1/auto/image.bin', device=self.device)
        self.assertEqual(result, 'tftp://10.1.1.1/auto/image.bin')

    def test_no_rewrite_on_local_url(self):
        result = self.fu._resolve_server_route_url(
            'flash:/image.bin', device=self.device)
        self.assertEqual(result, 'flash:/image.bin')

    def test_no_rewrite_when_device_is_none(self):
        result = self.fu._resolve_server_route_url(
            'tftp://10.1.1.1/auto/image.bin', device=None)
        self.assertEqual(result, 'tftp://10.1.1.1/auto/image.bin')

    def test_no_rewrite_when_device_info_missing(self):
        """Early return when management/testbed/address info is absent."""
        cases = [
            # no management attr
            AttrDict(name='R2', os='iosxe', testbed=self.testbed,
                     api=self.mock_api),
            # no testbed (and fu.testbed=None)
            AttrDict(name='R3', os='iosxe',
                     management=AttrDict(address=AttrDict(ipv4='10.1.5.10/16')),
                     api=self.mock_api),
            # empty address
            AttrDict(name='R4', os='iosxe', testbed=self.testbed,
                     management=AttrDict(address=AttrDict()),
                     api=self.mock_api),
        ]
        for device in cases:
            fu = FileUtils(os='iosxe', testbed=None, device=device)
            result = fu._resolve_server_route_url(
                'tftp://10.1.1.1/auto/image.bin', device=device)
            self.assertEqual(result, 'tftp://10.1.1.1/auto/image.bin',
                             f"Expected no rewrite for device {device.name}")

    def test_rewrite_with_ipv6_management(self):
        self.mock_api.find_server_ip_for_device_ip.return_value = '10.1.0.1'
        device = AttrDict(
            name='R4', os='iosxe', testbed=self.testbed,
            management=AttrDict(
                address=AttrDict(ipv6='2001:db8::1/64')
            ),
            api=self.mock_api,
        )
        result = self.fu._resolve_server_route_url(
            'tftp://10.1.1.1/auto/image.bin', device=device)
        self.assertEqual(result, 'tftp://10.1.0.1/auto/image.bin')
        self.mock_api.find_server_ip_for_device_ip.assert_called_once_with(
            '2001:db8::1', self.testbed.servers,
            server_hostname='10.1.1.1')

    def test_rewrite_preserves_auth_and_path(self):
        self.mock_api.find_server_ip_for_device_ip.return_value = '10.1.0.1'
        result = self.fu._resolve_server_route_url(
            'ftp://user:pass@10.1.1.1/auto/tftp/image.bin', device=self.device)
        self.assertEqual(result, 'ftp://user:pass@10.1.0.1/auto/tftp/image.bin')

    def test_no_rewrite_when_lookup_raises(self):
        self.mock_api.find_server_ip_for_device_ip.side_effect = Exception("lookup error")
        result = self.fu._resolve_server_route_url(
            'tftp://10.1.1.1/auto/image.bin', device=self.device)
        self.assertEqual(result, 'tftp://10.1.1.1/auto/image.bin')

    def test_rewrite_management_ip_without_prefix(self):
        self.mock_api.find_server_ip_for_device_ip.return_value = '10.1.0.1'
        device = AttrDict(
            name='R7', os='iosxe', testbed=self.testbed,
            management=AttrDict(
                address=AttrDict(ipv4='10.1.5.10')
            ),
            api=self.mock_api,
        )
        result = self.fu._resolve_server_route_url(
            'tftp://10.1.1.1/auto/image.bin', device=device)
        self.assertEqual(result, 'tftp://10.1.0.1/auto/image.bin')
        self.mock_api.find_server_ip_for_device_ip.assert_called_once_with(
            '10.1.5.10', self.testbed.servers,
            server_hostname='10.1.1.1')

    def test_device_connection_wrapper(self):
        """Test that the helper unwraps device.device if present."""
        self.mock_api.find_server_ip_for_device_ip.return_value = '10.1.0.1'
        # Simulate a connection object that wraps the actual device
        connection = AttrDict(device=self.device)
        result = self.fu._resolve_server_route_url(
            'tftp://10.1.1.1/auto/image.bin', device=connection)
        self.assertEqual(result, 'tftp://10.1.0.1/auto/image.bin')

    def test_self_testbed_fallback(self):
        """When device lacks .testbed, fall back to self.testbed."""
        self.mock_api.find_server_ip_for_device_ip.return_value = '10.1.0.1'
        device = AttrDict(
            name='R8', os='iosxe',
            management=AttrDict(address=AttrDict(ipv4='10.1.5.10/16')),
            api=self.mock_api,
        )
        # device has no .testbed, but self.fu.testbed is set from setUp
        result = self.fu._resolve_server_route_url(
            'tftp://10.1.1.1/auto/image.bin', device=device)
        self.assertEqual(result, 'tftp://10.1.0.1/auto/image.bin')
        self.mock_api.find_server_ip_for_device_ip.assert_called_once_with(
            '10.1.5.10', self.testbed.servers,
            server_hostname='10.1.1.1')

    def test_url_mapping_cn_resolved_for_lookup(self):
        """When URL hostname is a CN (via validate_and_update_url),
        resolve through url_mapping to find original server IP for lookup.
        URL should NOT be rewritten (hostname preserved for SSL cert match)."""
        self.mock_api.find_server_ip_for_device_ip.return_value = '10.1.0.1'
        # Simulate CN rewriting: url_mapping maps CN -> original server IP
        self.fu.url_mapping = {'server.example.com': '10.1.1.1'}
        result = self.fu._resolve_server_route_url(
            'https://server.example.com/auto/image.bin', device=self.device)
        # URL hostname is a DNS name — must NOT be rewritten (SSL cert CN match)
        self.assertEqual(result, 'https://server.example.com/auto/image.bin')
        # The lookup should use the resolved original IP, not the CN
        self.mock_api.find_server_ip_for_device_ip.assert_called_once_with(
            '10.1.5.10', self.testbed.servers,
            server_hostname='10.1.1.1')

    def test_url_mapping_updated_after_hostname_resolve(self):
        """After resolve, url_mapping is updated for HTTPS cert/ip-host
        even when URL is not rewritten (hostname case)."""
        self.mock_api.find_server_ip_for_device_ip.return_value = '10.1.0.1'
        # Pre-existing mapping from validate_and_update_url: CN -> orig IP
        self.fu.url_mapping = {'server.example.com': '10.1.1.1'}
        self.fu._resolve_server_route_url(
            'https://server.example.com/auto/image.bin', device=self.device)
        # (a) route_ip -> original server IP for cert fetch
        self.assertEqual(self.fu.url_mapping['10.1.0.1'], '10.1.1.1')
        # (b) CN -> route_ip for ip host command
        self.assertEqual(self.fu.url_mapping['server.example.com'], '10.1.0.1')

    def test_rewrite_url_when_hostname_is_ip(self):
        """When URL hostname is a raw IP, the URL IS rewritten."""
        self.mock_api.find_server_ip_for_device_ip.return_value = '10.1.0.1'
        result = self.fu._resolve_server_route_url(
            'https://10.1.1.1/auto/image.bin', device=self.device)
        # IP hostname — safe to rewrite (no cert CN mismatch for IPs)
        self.assertEqual(result, 'https://10.1.0.1/auto/image.bin')

    def test_rewrite_dns_hostname_for_non_https(self):
        """Non-HTTPS DNS hostnames ARE rewritten (no cert CN concern)."""
        self.mock_api.find_server_ip_for_device_ip.return_value = '10.1.0.1'
        result = self.fu._resolve_server_route_url(
            'tftp://server.example.com/auto/image.bin', device=self.device)
        # Non-HTTPS: hostname rewritten to route IP
        self.assertEqual(result, 'tftp://10.1.0.1/auto/image.bin')

    def test_idempotent_repeated_cn_resolve(self):
        """Second resolve of same HTTPS CN must NOT corrupt url_mapping.

        Simulates source+destination both using the same HTTPS CN, or
        the same FileUtils instance being reused for multiple copies.
        """
        self.mock_api.find_server_ip_for_device_ip.return_value = '10.1.0.1'
        # Pre-existing mapping from validate_and_update_url: CN -> orig IP
        self.fu.url_mapping = {'server.example.com': '10.1.1.1'}

        # First resolve (source URL)
        self.fu._resolve_server_route_url(
            'https://server.example.com/auto/source.bin', device=self.device)
        # Verify correct state after first resolve
        self.assertEqual(self.fu.url_mapping['10.1.0.1'], '10.1.1.1')
        self.assertEqual(self.fu.url_mapping['server.example.com'], '10.1.0.1')

        # Second resolve (destination URL) — same CN
        self.fu._resolve_server_route_url(
            'https://server.example.com/auto/dest.bin', device=self.device)
        # url_mapping must remain correct (NOT corrupted to route_ip -> route_ip)
        self.assertEqual(self.fu.url_mapping['10.1.0.1'], '10.1.1.1',
                         "url_mapping[route_ip] corrupted on second resolve!")
        self.assertEqual(self.fu.url_mapping['server.example.com'], '10.1.0.1')


if __name__ == '__main__':
    unittest.main()
