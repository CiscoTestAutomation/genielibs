from unittest import TestCase
from genie.libs.sdk.apis.iosxe.nat.configure import configure_standard_access_list
from unittest.mock import Mock


class TestConfigureStandardAccessList(TestCase):

    def test_configure_standard_access_list(self):
        self.device = Mock()
        result = configure_standard_access_list(self.device, '11', 'permit', 'any', None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['access-list 11 permit any'],)
        )
