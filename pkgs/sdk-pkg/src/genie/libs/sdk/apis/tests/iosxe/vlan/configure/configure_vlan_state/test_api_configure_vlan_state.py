from unittest import TestCase
from genie.libs.sdk.apis.iosxe.vlan.configure import configure_vlan_state
from unittest.mock import Mock


class TestConfigureVlanState(TestCase):

    def test_configure_vlan_state(self):
        self.device = Mock()
        result = configure_vlan_state(self.device, '100', 'active')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['vlan 100', 'state active'],)
        )
