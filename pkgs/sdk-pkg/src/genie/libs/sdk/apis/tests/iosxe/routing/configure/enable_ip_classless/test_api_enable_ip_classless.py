from unittest import TestCase
from genie.libs.sdk.apis.iosxe.routing.configure import enable_ip_classless
from unittest.mock import Mock


class TestEnableIpClassless(TestCase):

    def test_enable_ip_classless(self):
        self.device = Mock()
        result = enable_ip_classless(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ip classless',)
        )
