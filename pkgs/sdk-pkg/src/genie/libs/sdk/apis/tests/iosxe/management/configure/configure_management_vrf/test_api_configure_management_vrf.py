from unittest import TestCase
from genie.libs.sdk.apis.iosxe.management.configure import configure_management_vrf
from unittest.mock import Mock, MagicMock


class TestConfigureManagementVrf(TestCase):

    def test_configure_management_vrf(self):
        self.device = Mock()
        self.device.parse = Mock(return_value={'vrf': {'Mgmt-intf': {'route_distinguisher': '<not set>', 'protocols': ['ipv4']}}})
        result = configure_management_vrf(self.device, vrf='Mgmt-intf')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['vrf definition Mgmt-intf','address-family ipv6', 'exit-address-family'],)
        )
