from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import configure_type_access_list_action


class TestConfigureTypeAccessListAction(TestCase):

    def test_configure_type_access_list_action(self):
        self.device = Mock()
        configure_type_access_list_action(self.device, 'Mac', 'VACL_MAC', 'permit', None, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['Mac access-list extended VACL_MAC', 'permit any any'] ,)
        )
