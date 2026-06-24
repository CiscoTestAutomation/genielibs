import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_parser_view


class TestUnconfigureParserView(unittest.TestCase):

    def test_unconfigure_parser_view(self):
        device = Mock()

        result = unconfigure_parser_view(device, 'pv1')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no parser view pv1',)
        )