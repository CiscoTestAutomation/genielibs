import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_archive_rollback


class TestUnconfigureArchiveRollback(unittest.TestCase):

    def test_unconfigure_archive_rollback(self):
        device = Mock()

        result = unconfigure_archive_rollback(device, 'retry')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['archive', 'no rollback retry timeout'],)
        )