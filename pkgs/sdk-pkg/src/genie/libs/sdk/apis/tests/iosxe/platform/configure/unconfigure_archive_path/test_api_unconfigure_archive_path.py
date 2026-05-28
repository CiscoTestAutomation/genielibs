import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_archive_path


class TestUnconfigureArchivePath(unittest.TestCase):

    def test_unconfigure_archive_path(self):
        device = Mock()

        result = unconfigure_archive_path(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['archive', 'no path'],)
        )