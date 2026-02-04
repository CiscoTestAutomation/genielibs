from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_rename_profile


class TestConfigureCallHomeRenameProfile(TestCase):

    def test_configure_call_home_rename_profile(self):
        device = Mock()
        result = configure_call_home_rename_profile(device, 'test_abc', 'test_123')
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['call-home', 'rename profile test_abc test_123'],)
        )
