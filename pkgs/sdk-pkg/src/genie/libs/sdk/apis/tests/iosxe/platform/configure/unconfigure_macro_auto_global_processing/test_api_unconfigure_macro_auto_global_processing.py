import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_macro_auto_global_processing


class TestUnconfigureMacroAutoGlobalProcessing(unittest.TestCase):

    def test_unconfigure_macro_auto_global_processing(self):
        device = Mock()

        result = unconfigure_macro_auto_global_processing(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no macro auto global processing',)
        )