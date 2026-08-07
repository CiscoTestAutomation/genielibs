from unittest import TestCase
from genie.libs.sdk.apis.iosxe.management.configure import unconfigure_management_restconf
from unittest.mock import Mock


class TestUnconfigureManagementRestconf(TestCase):

    def setUp(self):
        self.device = Mock()

    def test_unconfigure_management_restconf(self):
        """Test unconfiguring RESTCONF"""
        result = unconfigure_management_restconf(self.device)
        self.device.configure.assert_called_once_with(['no restconf'])
        self.assertEqual(result, None)
