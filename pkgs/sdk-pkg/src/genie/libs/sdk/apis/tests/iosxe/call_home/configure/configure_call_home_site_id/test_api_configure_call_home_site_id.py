from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_site_id


class TestConfigureCallHomeSiteId(TestCase):

    def test_configure_call_home_site_id(self):
        device = Mock()
        result = configure_call_home_site_id(device, 'test_site')
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['call-home', 'site-id test_site'],)
        )
