import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_macro_global_apply


class TestConfigureMacroGlobalApply(unittest.TestCase):

    def test_configure_macro_global_apply(self):
        device = Mock()

        result = configure_macro_global_apply(device, 'm-qos', '$interface', '"range gi1/0/1-48"', 60)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('macro global apply m-qos $interface "range gi1/0/1-48"',)
        )