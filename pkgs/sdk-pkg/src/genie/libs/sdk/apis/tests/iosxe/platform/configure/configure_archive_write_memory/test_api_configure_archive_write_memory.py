from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_archive_write_memory


class TestConfigureArchiveWriteMemory(TestCase):

    def test_configure_archive_write_memory(self):
        device = Mock()
        result = configure_archive_write_memory(device)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['archive', 'write-memory'],)
        )