from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import config_access_session_auth_attr_filter_spec_include_list

class TestConfigAccessSessionAuthAttrFilterSpecIncludeList(TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_config_access_session_auth_attr_filter_spec_include_list(self):
        config_access_session_auth_attr_filter_spec_include_list(self.device, 'aaa_attr')
        self.device.configure.assert_called_with([
            'access-session authentication attributes filter-spec include list aaa_attr'
        ])

