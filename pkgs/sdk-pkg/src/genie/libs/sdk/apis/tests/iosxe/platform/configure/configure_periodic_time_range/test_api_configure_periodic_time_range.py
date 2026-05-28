import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_periodic_time_range


class TestConfigurePeriodicTimeRange(unittest.TestCase):

    def test_configure_periodic_time_range(self):
        device = Mock()

        result = configure_periodic_time_range(device, 'time1', 'daily', '22:40', '22:41')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['time-range time1', 'periodic daily 22:40 to 22:41'],)
        )