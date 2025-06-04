from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import configure_filter_vlan_list


class TestConfigureFilterVlanList(TestCase):

    def test_configure_filter_vlan_list(self):
        self.device = Mock()
        configure_filter_vlan_list(self.device, 'ana', '1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['vlan filter ana vlan-list 1'] ,)
        )
