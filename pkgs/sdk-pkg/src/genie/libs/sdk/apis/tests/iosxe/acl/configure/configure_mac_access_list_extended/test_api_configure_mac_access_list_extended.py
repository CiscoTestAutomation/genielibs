from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acl.configure import configure_mac_access_list_extended
from unittest.mock import Mock


class TestConfigureMacAccessListExtended(TestCase):

    def test_configure_mac_access_list_extended(self):
        self.device = Mock()
        result = configure_mac_access_list_extended(self.device, 'dummy')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['mac access-list extended dummy'],)
        )
