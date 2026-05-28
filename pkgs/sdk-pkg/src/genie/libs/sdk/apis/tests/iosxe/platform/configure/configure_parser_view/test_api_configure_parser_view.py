import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_parser_view


class TestConfigureParserView(unittest.TestCase):

    def test_configure_parser_view(self):
        device = Mock()

        result = configure_parser_view(device, 'pv1', 'pass', ['show vrrp'])

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['parser view pv1', 'secret 0 pass', 'command exec include show vrrp', 'end'],)
        )