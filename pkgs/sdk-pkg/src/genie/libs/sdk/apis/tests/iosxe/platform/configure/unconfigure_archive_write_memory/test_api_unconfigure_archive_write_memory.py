import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_archive_write_memory


class TestUnconfigureArchiveWriteMemory(unittest.TestCase):

    def test_unconfigure_archive_write_memory(self):
        device = Mock()

        result = unconfigure_archive_write_memory(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['archive', 'no write-memory'],)
        )