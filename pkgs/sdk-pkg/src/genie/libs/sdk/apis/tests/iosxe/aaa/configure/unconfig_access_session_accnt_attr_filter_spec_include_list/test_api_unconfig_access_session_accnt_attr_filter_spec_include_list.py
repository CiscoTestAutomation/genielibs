import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfig_access_session_accnt_attr_filter_spec_include_list


class TestUnconfigAccessSessionAccntAttrFilterSpecIncludeList(unittest.TestCase):

    def test_unconfig_access_session_accnt_attr_filter_spec_include_list(self):
        self.device = Mock()
        unconfig_access_session_accnt_attr_filter_spec_include_list(self.device, 'aaa_attr')
        self.device.configure.assert_called_once_with([
            "no access-session accounting attributes filter-spec include list aaa_attr"
        ])
