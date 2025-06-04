from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import configure_file_verify_auto
from unittest.mock import Mock


class TestConfigureFileVerifyAuto(TestCase):

    def test_configure_file_verify_auto(self):
        self.device = Mock()
        result = configure_file_verify_auto(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['file verify auto'],)
        )
