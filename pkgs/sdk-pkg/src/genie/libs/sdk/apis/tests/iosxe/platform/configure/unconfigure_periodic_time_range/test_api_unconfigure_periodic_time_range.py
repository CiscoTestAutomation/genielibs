import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_periodic_time_range


class TestUnconfigurePeriodicTimeRange(unittest.TestCase):

    def test_unconfigure_periodic_time_range(self):
        device = Mock()

        result = unconfigure_periodic_time_range(device, 'time1', 'daily', '22:40', '22:41')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['time-range time1', 'no periodic daily 22:40 to 22:41'],)
        )