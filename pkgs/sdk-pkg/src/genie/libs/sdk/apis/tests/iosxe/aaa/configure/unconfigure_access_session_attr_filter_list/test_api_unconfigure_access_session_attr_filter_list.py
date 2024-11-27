import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_access_session_attr_filter_list


class TestUnconfigureAccessSessionAttrFilterList(unittest.TestCase):

    def test_unconfigure_access_session_attr_filter_list(self):
        self.device = Mock()
        unconfigure_access_session_attr_filter_list(self.device, 'aaa_attr')
        self.device.configure.assert_called_once_with([
            "no access-session attributes filter-list list aaa_attr"
        ])
