import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_service_timestamps


class TestUnconfigureServiceTimestamps(unittest.TestCase):

    def test_unconfigure_service_timestamps(self):
        device = Mock()

        result = unconfigure_service_timestamps(
            device,
            'log'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no service timestamps log'],)
        )