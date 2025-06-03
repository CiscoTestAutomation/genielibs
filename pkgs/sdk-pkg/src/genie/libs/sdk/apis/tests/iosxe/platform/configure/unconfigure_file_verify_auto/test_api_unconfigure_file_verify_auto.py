from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_file_verify_auto
from unittest.mock import Mock


class TestUnconfigureFileVerifyAuto(TestCase):

    def test_unconfigure_file_verify_auto(self):
        self.device = Mock()
        result = unconfigure_file_verify_auto(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no file verify auto'],)
        )
