import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_service_timestamps


class TestConfigureServiceTimestamps(unittest.TestCase):

    def test_configure_service_timestamps(self):
        device = Mock()

        result = configure_service_timestamps(device, 'log', 'datetime', 'year')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['service timestamps log datetime year'],)
        )