import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_ip_http_client_source_interface_vlan_domain_lookup_name_server_vrf_mgmt_vrf


class TestConfigureIpHttpClientSourceInterfaceVlanDomainLookupNameServerVrfMgmtVrf(unittest.TestCase):

    def test_configure_ip_http_client_source_interface_vlan_domain_lookup_name_server_vrf_mgmt_vrf(self):
        device = Mock()

        result = configure_ip_http_client_source_interface_vlan_domain_lookup_name_server_vrf_mgmt_vrf(device, 'g1/1/3')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no ip name-server vrf mgmt-vrf', 'interface g1/1/3'],)
        )