import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_macro_auto_sticky


class TestConfigureMacroAutoSticky(unittest.TestCase):

    def test_configure_macro_auto_sticky(self):
        device = Mock()

        result = configure_macro_auto_sticky(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('macro auto sticky',)
        )