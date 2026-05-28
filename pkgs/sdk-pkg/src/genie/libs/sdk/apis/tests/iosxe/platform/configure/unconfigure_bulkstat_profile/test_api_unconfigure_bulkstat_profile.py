import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_bulkstat_profile


class TestUnconfigureBulkstatProfile(unittest.TestCase):

    def test_unconfigure_bulkstat_profile(self):
        device = Mock()

        result = unconfigure_bulkstat_profile(device, 'test')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no bulkstat profile test'],)
        )