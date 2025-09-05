from unittest import TestCase
from genie.libs.sdk.apis.iosxe.rep.configure import configure_rep_ztp
from unittest.mock import Mock


class TestConfigureRepZtp(TestCase):

    def test_configure_rep_ztp(self):
        self.device = Mock()
        result = configure_rep_ztp(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('rep ztp',)
        )
