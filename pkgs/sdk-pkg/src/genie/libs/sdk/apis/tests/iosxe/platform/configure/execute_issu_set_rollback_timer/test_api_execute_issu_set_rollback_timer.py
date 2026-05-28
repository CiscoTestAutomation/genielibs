import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import execute_issu_set_rollback_timer


class TestExecuteIssuSetRollbackTimer(unittest.TestCase):

    def test_execute_issu_set_rollback_timer(self):
        device = Mock()

        result = execute_issu_set_rollback_timer(device, 5)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('issu set rollback-timer 5',)
        )