from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_archive_rollback


class TestConfigureArchiveRollback(TestCase):

    def test_configure_archive_rollback(self):
        device = Mock()
        result = configure_archive_rollback(
            device,
            'retry',
            50
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['archive', 'rollback retry timeout 50'],)
        )