from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ie3k.platform.configure import configure_sd
from unittest.mock import Mock


class TestConfigureSd(TestCase):

    def test_configure_sd(self):
        self.device = Mock()
        result = configure_sd(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no platform sd disable',)
        )
