import unittest

from unittest import mock

from genie.libs.clean.stages.iosxe.ie3k.stages import RommonBoot, WriteErase
from genie.libs.clean.stages.tests.utils import create_test_device


class TestWriteErase(unittest.TestCase):

    def setUp(self):
        self.cls = WriteErase()
        self.device = create_test_device('PE1', os='iosxe', platform='ie3k')

    def test_remove_nvram_config_files_filters_unavailable_filesystems(self):
        steps = mock.MagicMock()
        with mock.patch.object(self.device.api, 'get_filesystems', create=True, return_value=['flash:', 'bootflash:', 'sdflash:']) as get_filesystems, \
             mock.patch.object(self.device.api, 'delete_files', create=True) as delete_files:
            self.cls.remove_nvram_config_files(steps=steps, device=self.device)

            get_filesystems.assert_called_once_with()
            delete_files.assert_called_once_with(
                locations=['sdflash:'],
                filenames=['nvram_config'],
            )

    def test_remove_nvram_config_files_skips_when_no_requested_filesystems_exist(self):
        steps = mock.MagicMock()
        step_context = steps.start.return_value.__enter__.return_value
        with mock.patch.object(self.device.api, 'get_filesystems', create=True, return_value=['flash:', 'bootflash:']) as get_filesystems, \
             mock.patch.object(self.device.api, 'delete_files', create=True) as delete_files:
            self.cls.remove_nvram_config_files(steps=steps, device=self.device)

            get_filesystems.assert_called_once_with()
            delete_files.assert_not_called()
            step_context.skipped.assert_called_once_with(
                "No requested filesystems are available from ['sdflash:', 'usbflash0:', 'usbflash1:'] to remove nvram_config files from"
            )


class TestRommonBoot(unittest.TestCase):

    def setUp(self):
        self.cls = RommonBoot()
        self.device = create_test_device('PE1', os='iosxe', platform='ie3k')

    def test_go_to_rommon_calls_device_rommon(self):
        steps = mock.MagicMock()
        with mock.patch.object(self.device, 'rommon', create=True) as rommon:
            self.cls.go_to_rommon(steps=steps, device=self.device)

            rommon.assert_called_once_with()

    def test_rommon_boot_calls_device_rommon_boot_api_with_expected_args(self):
        steps = mock.MagicMock()
        with mock.patch.object(self.device.api, 'device_rommon_boot', create=True) as device_rommon_boot:
            self.cls.rommon_boot(
                steps=steps,
                device=self.device,
                image=['bootflash:/test.bin'],
                timeout=321,
            )

            device_rommon_boot.assert_called_once_with(
                tftp_boot=None,
                golden_image='bootflash:/test.bin',
                grub_activity_pattern=None,
                timeout=321,
            )