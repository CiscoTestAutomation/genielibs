from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import cts_refresh_pac
from unittest.mock import Mock

class TestCtsRefreshPac(TestCase):

    def test_cts_refresh_pac(self):
        self.device = Mock()
        cts_refresh_pac(self.device)
        self.device.execute.assert_called_once_with('cts refresh pac')