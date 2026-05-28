import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_ip_http_client_source_interface_vlan_domain_lookup


class TestConfigureIpHttpClientSourceInterfaceVlanDomainLookup(unittest.TestCase):

    def test_configure_ip_http_client_source_interface_vlan_domain_lookup(self):
        device = Mock()

        result = configure_ip_http_client_source_interface_vlan_domain_lookup(device, '4')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ip http client source-interface vlan 4'],)
        )