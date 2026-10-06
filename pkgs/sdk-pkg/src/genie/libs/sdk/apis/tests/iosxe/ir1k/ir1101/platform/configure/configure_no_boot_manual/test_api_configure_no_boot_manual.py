import unittest
from unittest.mock import Mock

from genie.conf.base.device import Device
from genie.libs.sdk.apis.iosxe.ir1k.ir1101.platform.configure import (
    configure_no_boot_manual,
)
from genie.libs.sdk.apis.iosxe.platform.configure import configure_autoboot
from unicon.core.errors import SubCommandFailure


class TestConfigureNoBootManual(unittest.TestCase):

    def test_configure_no_boot_manual(self):
        device = Mock()
        device.api.configure_autoboot.side_effect = (
            lambda: configure_autoboot(device)
        )

        configure_no_boot_manual(device)

        device.api.configure_autoboot.assert_called_once_with()
        device.api.execute_set_config_register.assert_called_once_with(
            config_register='0x2102'
        )

    def test_configure_no_boot_manual_failure(self):
        device = Mock()
        error = SubCommandFailure('Unable to configure autoboot')
        device.api.configure_autoboot.side_effect = error

        with self.assertRaises(SubCommandFailure) as raised:
            configure_no_boot_manual(device)

        self.assertIs(raised.exception, error)

    def test_ir1101_resolves_to_platform_implementation(self):
        device = Device(
            name='ir1101', os='iosxe', platform='ir1k', model='ir1101'
        )

        resolved_api = device.api.get_api('configure_no_boot_manual', device)

        self.assertIs(resolved_api, configure_no_boot_manual)
