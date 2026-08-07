from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_system_debounce_link_up_timer_doppler
from unittest.mock import Mock


class TestConfigureSystemDebounceLinkUpTimerDoppler(TestCase):

    def test_configure_system_debounce_link_up_timer_doppler(self):
        self.device = Mock()
        result = configure_system_debounce_link_up_timer_doppler(self.device, 'tw1/0/1', '10800')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('interface tw1/0/1\nlink debounce time 10800',)
        )
