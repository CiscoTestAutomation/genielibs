import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import config_access_session_accnt_attr_filter_spec_include_list

class TestConfigAccessSessionAccntAttrFilterSpecIncludeList(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_config_access_session_accnt_attr_filter_spec_include_list(self):
        config_access_session_accnt_attr_filter_spec_include_list(self.device, 'aaa_attr')
        self.device.configure.assert_called_once_with([
            'access-session accounting attributes filter-spec include list aaa_attr'
        ])
