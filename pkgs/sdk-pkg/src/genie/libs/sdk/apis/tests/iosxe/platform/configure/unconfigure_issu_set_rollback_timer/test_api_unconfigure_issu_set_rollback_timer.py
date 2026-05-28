import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_issu_set_rollback_timer


class TestUnconfigureIssuSetRollbackTimer(unittest.TestCase):

    def test_unconfigure_issu_set_rollback_timer(self):
        device = Mock()

        result = unconfigure_issu_set_rollback_timer(device, 5)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no issu set rollback-timer 5',)
        )