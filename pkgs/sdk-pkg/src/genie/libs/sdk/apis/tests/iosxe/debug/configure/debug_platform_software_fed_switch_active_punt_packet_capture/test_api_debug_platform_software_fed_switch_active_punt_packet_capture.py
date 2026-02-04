from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.debug.configure import debug_platform_software_fed_switch_active_punt_packet_capture


class TestDebugPlatformSoftwareFedSwitchActivePuntPacketCapture(TestCase):
    def test_debug_platform_software_fed_switch_active_punt_packet_capture(self):
        device = Mock()
        result = debug_platform_software_fed_switch_active_punt_packet_capture(
            device, True, 10000, True, 257, True, 'ip', True, True, True
        )
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            (['debug platform software fed switch active punt packet-capture buffer limit 10000',
              'debug platform software fed switch active punt packet-capture buffer circular limit 257',
              'debug platform software fed switch active punt packet-capture set-filter ip',
              'debug platform software fed switch active punt packet-capture clear-filter',
              'debug platform software fed switch active punt packet-capture start',
              'debug platform software fed switch active punt packet-capture stop'],)
        )