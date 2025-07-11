from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_copy_profile


class TestConfigureCallHomeCopyProfile(TestCase):

    def test_configure_call_home_copy_profile(self):
        self.device = Mock()
        result = configure_call_home_copy_profile(self.device, 'test_source', 'test_target')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['call-home', 'copy profile test_source test_target'],)
        )
