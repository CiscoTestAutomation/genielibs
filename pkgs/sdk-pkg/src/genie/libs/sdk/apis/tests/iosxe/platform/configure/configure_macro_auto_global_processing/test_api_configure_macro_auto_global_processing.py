import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_macro_auto_global_processing


class TestConfigureMacroAutoGlobalProcessing(unittest.TestCase):

    def test_configure_macro_auto_global_processing(self):
        device = Mock()

        result = configure_macro_auto_global_processing(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('macro auto global processing',)
        )