from unittest import TestCase
from genie.libs.sdk.apis.iosxe.utils import configure_generic_command
from unittest.mock import Mock


class TestConfigureGenericCommand(TestCase):

    def test_configure_generic_command(self):
        self.device = Mock()
        result = configure_generic_command(self.device, 'ip source-route')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ip source-route',)
        )
