import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_system_disable_password_recovery_switch_all


class TestConfigureSystemDisablePasswordRecoverySwitchAll(unittest.TestCase):

    def test_configure_system_disable_password_recovery_switch_all(self):
        device = Mock()

        result = configure_system_disable_password_recovery_switch_all(device, 'False', None)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('system disable password recovery',)
        )