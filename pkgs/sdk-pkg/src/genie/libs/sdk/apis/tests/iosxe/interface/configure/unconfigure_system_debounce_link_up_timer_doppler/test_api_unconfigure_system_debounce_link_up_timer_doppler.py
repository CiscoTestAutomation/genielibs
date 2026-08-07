from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_system_debounce_link_up_timer_doppler
from unittest.mock import Mock


class TestUnconfigureSystemDebounceLinkUpTimerDoppler(TestCase):

    def test_unconfigure_system_debounce_link_up_timer_doppler(self):
        self.device = Mock()
        result = unconfigure_system_debounce_link_up_timer_doppler(self.device, 'tw1/0/1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('interface tw1/0/1\nno link debounce time',)
        )
