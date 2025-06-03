from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ie3k.verify import verify_ignore_startup_config


class TestVerifyIgnoreStartupConfig(TestCase):

    def test_verify_ignore_startup_config(self):
        self.device = Mock()
        verify_ignore_startup_config(self.device)
        self.assertEqual(
            self.device.parse.mock_calls[0].args,
            ('show romvar' ,)
        )
