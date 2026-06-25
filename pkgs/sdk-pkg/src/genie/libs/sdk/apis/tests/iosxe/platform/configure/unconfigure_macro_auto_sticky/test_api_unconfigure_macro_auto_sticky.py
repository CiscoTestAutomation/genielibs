import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_macro_auto_sticky


class TestUnconfigureMacroAutoSticky(unittest.TestCase):

    def test_unconfigure_macro_auto_sticky(self):
        device = Mock()

        result = unconfigure_macro_auto_sticky(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no macro auto sticky',)
        )