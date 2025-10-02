from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acl.configure import configure_extended_access_list
from unittest.mock import Mock


class TestConfigureExtendedAccessList(TestCase):

    def test_configure_extended_access_list(self):
        self.device = Mock()
        result = configure_extended_access_list(self.device, '100', 130, 'permit', '131.1.1.3', '162.1.1.2', 7)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip access-list extended 100', '130 permit ip host 131.1.1.3 host 162.1.1.2 dscp 7'],)
        )
