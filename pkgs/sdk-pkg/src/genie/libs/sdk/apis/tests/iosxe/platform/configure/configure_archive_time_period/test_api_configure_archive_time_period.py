from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_archive_time_period


class TestConfigureArchiveTimePeriod(TestCase):

    def test_configure_archive_time_period(self):
        device = Mock()
        result = configure_archive_time_period(
            device,
            23
        )
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['archive', 'time-period 23'],)
        )