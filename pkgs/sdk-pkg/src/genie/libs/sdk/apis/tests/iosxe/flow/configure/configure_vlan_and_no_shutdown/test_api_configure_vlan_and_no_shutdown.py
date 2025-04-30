from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.configure import configure_vlan_and_no_shutdown
from unittest.mock import Mock


class TestConfigureVlanAndNoShutdown(TestCase):

    def test_configure_vlan_and_no_shutdown(self):
        self.device = Mock()
        result = configure_vlan_and_no_shutdown(self.device, 100)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface vlan 100', 'no shutdown', 'vlan 100', 'no shutdown'],)
        )
