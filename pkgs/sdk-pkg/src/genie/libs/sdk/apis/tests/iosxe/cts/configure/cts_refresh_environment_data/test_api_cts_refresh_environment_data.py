from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import cts_refresh_environment_data
from unittest.mock import Mock

class TestCtsRefreshEnvironmentData(TestCase):

    def test_cts_refresh_environment_data(self):
        self.device = Mock()
        cts_refresh_environment_data(self.device)
        self.device.execute.assert_called_once_with('cts refresh environment-data')

   