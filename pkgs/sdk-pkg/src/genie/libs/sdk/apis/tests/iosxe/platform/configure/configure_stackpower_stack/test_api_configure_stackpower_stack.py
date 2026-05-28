import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_stackpower_stack


class TestConfigureStackpowerStack(unittest.TestCase):

    def test_configure_stackpower_stack(self):
        device = Mock()

        result = configure_stackpower_stack(device, 'Powerstack-Ring-1', None, False)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['stack-power stack Powerstack-Ring-1'],)
        )