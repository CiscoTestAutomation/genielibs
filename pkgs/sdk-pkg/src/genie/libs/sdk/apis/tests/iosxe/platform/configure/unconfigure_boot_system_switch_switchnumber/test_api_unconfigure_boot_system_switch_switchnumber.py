import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_boot_system_switch_switchnumber


class TestUnconfigureBootSystemSwitchSwitchnumber(unittest.TestCase):

    def test_unconfigure_boot_system_switch_switchnumber(self):
        device = Mock()

        result = unconfigure_boot_system_switch_switchnumber(device, 1)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no boot system switch 1',)
        )