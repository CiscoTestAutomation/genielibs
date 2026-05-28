import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_no_boot_system_switch_all


class TestConfigureNoBootSystemSwitchAll(unittest.TestCase):

    def test_configure_no_boot_system_switch_all(self):
        device = Mock()

        result = configure_no_boot_system_switch_all(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no boot system switch all',)
        )