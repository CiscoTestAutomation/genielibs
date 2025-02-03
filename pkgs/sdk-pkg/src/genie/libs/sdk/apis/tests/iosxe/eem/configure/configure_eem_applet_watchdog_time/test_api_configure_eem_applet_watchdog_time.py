from unittest import TestCase
from genie.libs.sdk.apis.iosxe.eem.configure import configure_eem_applet_watchdog_time
from unittest.mock import Mock


class TestConfigureEemAppletWatchdogTime(TestCase):

    def test_configure_eem_applet_watchdog_time(self):
        self.device = Mock()
        result = configure_eem_applet_watchdog_time(self.device, 'WRITE_MEM_EEM', 10)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['event manager applet WRITE_MEM_EEM', 'event timer watchdog time 10'],)
        )
