import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import configure_exec_prompt_timestamp


class TestConfigureExecPromptTimestamp(unittest.TestCase):

    def test_configure_exec_prompt_timestamp(self):
        device = Mock()

        result = configure_exec_prompt_timestamp(
            device,
            '0',
            '4'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['line vty 0 4', 'exec prompt timestamp'],)
        )