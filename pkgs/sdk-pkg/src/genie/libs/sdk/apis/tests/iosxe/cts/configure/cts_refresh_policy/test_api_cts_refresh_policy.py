from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import cts_refresh_policy
from unittest.mock import Mock

class TestCtsRefreshPolicy(TestCase):

    def test_cts_refresh_policy(self):
        self.device = Mock()
        cts_refresh_policy(self.device, False, None, False, None)
        self.device.execute.assert_called_once_with('cts refresh policy')

    def test_cts_refresh_policy_1(self):
        self.device = Mock()
        cts_refresh_policy(self.device, True, None, False, None)
        self.device.execute.assert_called_once_with('cts refresh policy peer')
        
    def test_cts_refresh_policy_2(self):
        self.device = Mock()
        cts_refresh_policy(self.device, True, 'peer1', False, None)
        self.device.execute.assert_called_once_with('cts refresh policy peer peer1')

    def test_cts_refresh_policy_3(self):
        self.device = Mock()
        cts_refresh_policy(self.device, False, None, True, 'unknown')
        self.device.execute.assert_called_once_with('cts refresh policy sgt unknown')

    def test_cts_refresh_policy_4(self):
        self.device = Mock()
        cts_refresh_policy(self.device, False, None, True, 'default')
        self.device.execute.assert_called_once_with('cts refresh policy sgt default')

    def test_cts_refresh_policy_5(self):
        self.device = Mock()
        cts_refresh_policy(self.device, False, None, True, '10')
        self.device.execute.assert_called_once_with('cts refresh policy sgt 10')

    def test_cts_refresh_policy_6(self):
        self.device = Mock()
        cts_refresh_policy(self.device, False, None, True, 'x10y')
        self.device.execute.assert_not_called()

       