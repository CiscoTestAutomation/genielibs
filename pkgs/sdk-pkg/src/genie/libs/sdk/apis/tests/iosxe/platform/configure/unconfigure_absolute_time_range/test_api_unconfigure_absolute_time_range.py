import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_absolute_time_range


class TestUnconfigureAbsoluteTimeRange(unittest.TestCase):

    def test_unconfigure_absolute_time_range(self):
        device = Mock()

        result = unconfigure_absolute_time_range(
            device, 'time1', 'start', '22:40', '7', 'Jan', '2000'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['time-range time1', 'no absolute start 22:40 7 Jan 2000'],)
        )