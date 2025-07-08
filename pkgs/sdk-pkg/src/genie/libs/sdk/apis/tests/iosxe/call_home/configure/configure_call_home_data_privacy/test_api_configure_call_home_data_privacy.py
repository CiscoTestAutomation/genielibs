from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_data_privacy


class TestConfigureCallHomeDataPrivacy(TestCase):

    def test_configure_call_home_data_privacy(self):
        self.device = Mock()
        result = configure_call_home_data_privacy(self.device, 'high')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['call-home', 'data-privacy level high'],)
        )
