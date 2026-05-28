import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_archive_maximum


class TestUnconfigureArchiveMaximum(unittest.TestCase):

    def test_unconfigure_archive_maximum(self):
        device = Mock()

        result = unconfigure_archive_maximum(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['archive', 'no maximum'],)
        )