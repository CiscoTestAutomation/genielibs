from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.iosxe.subscriber.execute import (
    execute_clear_subscriber_session_all,
    execute_clear_subscriber_session_username,
)


class TestClearSubscriberSession(TestCase):

    def test_execute_clear_subscriber_session_all(self):
        device = Mock()

        result = execute_clear_subscriber_session_all(device)

        self.assertEqual(result, device.execute.return_value)
        self.assertEqual(
            device.execute.call_args.args[0],
            "clear subscriber session all",
        )
        self.assertIn("reply", device.execute.call_args.kwargs)
        self.assertEqual(device.execute.call_args.kwargs["timeout"], 60)

    def test_execute_clear_subscriber_session_all_failure(self):
        device = Mock()
        device.execute.side_effect = SubCommandFailure("error")

        with self.assertRaises(SubCommandFailure):
            execute_clear_subscriber_session_all(device)

    def test_execute_clear_subscriber_session_username(self):
        device = Mock()

        result = execute_clear_subscriber_session_username(device, "dt_usrA")

        self.assertEqual(result, device.execute.return_value)
        self.assertEqual(
            device.execute.call_args.args[0],
            "clear subscriber session username dt_usrA",
        )
        self.assertIn("reply", device.execute.call_args.kwargs)
        self.assertEqual(device.execute.call_args.kwargs["timeout"], 60)

    def test_execute_clear_subscriber_session_username_failure(self):
        device = Mock()
        device.execute.side_effect = SubCommandFailure("error")

        with self.assertRaises(SubCommandFailure):
            execute_clear_subscriber_session_username(device, "dt_usrA")
