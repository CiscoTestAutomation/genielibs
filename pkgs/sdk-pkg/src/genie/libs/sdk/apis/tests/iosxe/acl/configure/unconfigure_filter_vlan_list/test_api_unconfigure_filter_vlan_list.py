from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import unconfigure_filter_vlan_list


class TestUnconfigureFilterVlanList(TestCase):

    def test_unconfigure_filter_vlan_list(self):
        self.device = Mock()
        unconfigure_filter_vlan_list(self.device, 'mymap', '100')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no vlan filter mymap vlan-list 100' ,)
        )
