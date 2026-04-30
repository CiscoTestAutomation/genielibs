from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_absolute_time_range


class TestConfigureAbsoluteTimeRange(TestCase):

    def test_configure_absolute_time_range(self):
        device = Mock()
        result = configure_absolute_time_range(
            device,
            'time1',
            'start',
            '22:40',
            '7',
            'Jan',
            '2000'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['time-range time1', 'absolute start 22:40 7 Jan 2000'],)
        )