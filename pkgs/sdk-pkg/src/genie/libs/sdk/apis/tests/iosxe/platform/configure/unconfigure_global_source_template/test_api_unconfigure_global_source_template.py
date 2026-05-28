import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_global_source_template


class TestUnconfigureGlobalSourceTemplate(unittest.TestCase):

    def test_unconfigure_global_source_template(self):
        device = Mock()

        result = unconfigure_global_source_template(device, 'user_template')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no source template user_template',)
        )