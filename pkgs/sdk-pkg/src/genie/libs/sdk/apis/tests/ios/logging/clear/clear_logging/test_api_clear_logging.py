from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.ios.logging.clear import clear_logging
from unicon.core.errors import SubCommandFailure


class TestClearLogging(TestCase):

    def test_clear_logging(self):
        self.device = Mock()
        self.device.execute.return_value = ''
        clear_logging(self.device)
        self.assertIn(
            'clear logging',
            self.device.execute.call_args_list[0][0]
        )

    def test_clear_logging_failure(self):
        self.device = Mock()
        self.device.execute.side_effect = SubCommandFailure('Test error')
        with self.assertRaises(SubCommandFailure):
            clear_logging(self.device)
