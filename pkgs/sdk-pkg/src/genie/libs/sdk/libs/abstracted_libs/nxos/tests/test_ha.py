import unittest
from unittest.mock import Mock
from unittest.mock import patch

from genie.libs.sdk.libs.abstracted_libs.nxos import ha


class StopFlow(Exception):
    pass


class DummyStep(object):
    def __init__(self):
        self.passed_messages = []

    def passed(self, message):
        self.passed_messages.append(message)

    def failed(self, message):
        raise AssertionError(message)


class DummyStepContext(object):
    def __init__(self, step):
        self.step = step

    def __enter__(self):
        return self.step

    def __exit__(self, exc_type, exc, tb):
        return False


class DummySteps(object):
    def __init__(self):
        self._count = 0
        self.first_step = DummyStep()

    def start(self, _message):
        self._count += 1
        if self._count == 1:
            return DummyStepContext(self.first_step)
        raise StopFlow()


class TestNxosHaEorBootMode(unittest.TestCase):

    def test_is_eor_platform_true(self):
        device = Mock()
        device.hostname = "uut1"
        device.execute.return_value = "Supervisor Module\n"
        self.assertTrue(ha._is_eor_platform(device))

    def test_is_eor_platform_false_for_tor_virtual_sup(self):
        device = Mock()
        device.hostname = "uut1"
        device.execute.return_value = "Virtual Supervisor Module\n"
        self.assertFalse(ha._is_eor_platform(device))

    @patch("genie.libs.sdk.libs.abstracted_libs.nxos.ha.FileUtils.from_device")
    @patch("genie.libs.sdk.libs.abstracted_libs.nxos.ha.Lookup.from_device")
    @patch("genie.libs.sdk.libs.abstracted_libs.nxos.ha._is_eor_platform", return_value=True)
    def test_perform_issu_skips_show_boot_mode_on_eor(
        self,
        _is_eor_platform_mock,
        _lookup_mock,
        _fileutils_mock,
    ):
        obj = object.__new__(ha.HA)
        obj.parameters = {"mode": "lxc"}
        obj.device = Mock()
        obj.device.hostname = "uut1"
        obj.device.execute = Mock()

        steps = DummySteps()

        with self.assertRaises(StopFlow):
            obj._perform_issu(steps=steps, upgrade_image="bootflash:nxos.bin")

        self.assertFalse(obj.device.execute.called)
        self.assertTrue(
            any(
                "Skipping 'show boot mode' check on EOR platform" in msg
                for msg in steps.first_step.passed_messages
            )
        )

    @patch("genie.libs.sdk.libs.abstracted_libs.nxos.ha.FileUtils.from_device")
    @patch("genie.libs.sdk.libs.abstracted_libs.nxos.ha.Lookup.from_device")
    @patch("genie.libs.sdk.libs.abstracted_libs.nxos.ha._is_eor_platform", return_value=False)
    def test_perform_issu_non_eor_boot_mode_match_passes(
        self,
        _is_eor_platform_mock,
        _lookup_mock,
        _fileutils_mock,
    ):
        obj = object.__new__(ha.HA)
        obj.parameters = {"mode": "native"}
        obj.device = Mock()
        obj.device.hostname = "uut1"
        obj.device.execute = Mock(return_value="Current mode is native.\n")

        steps = DummySteps()

        with self.assertRaises(StopFlow):
            obj._perform_issu(steps=steps, upgrade_image="bootflash:nxos.bin")

        obj.device.execute.assert_called_once_with("show boot mode")
        self.assertTrue(
            any(
                "System boot mode native matches user expected boot mode native" in msg
                for msg in steps.first_step.passed_messages
            )
        )

    @patch("genie.libs.sdk.libs.abstracted_libs.nxos.ha.FileUtils.from_device")
    @patch("genie.libs.sdk.libs.abstracted_libs.nxos.ha.Lookup.from_device")
    @patch("genie.libs.sdk.libs.abstracted_libs.nxos.ha._is_eor_platform", return_value=False)
    def test_perform_issu_non_eor_boot_mode_mismatch_fails(
        self,
        _is_eor_platform_mock,
        _lookup_mock,
        _fileutils_mock,
    ):
        obj = object.__new__(ha.HA)
        obj.parameters = {"mode": "native"}
        obj.device = Mock()
        obj.device.hostname = "uut1"
        obj.device.execute = Mock(return_value="Current mode is lxc.\n")

        steps = DummySteps()

        with self.assertRaisesRegex(
            AssertionError,
            "System boot mode lxc does not match user expected boot mode native",
        ):
            obj._perform_issu(steps=steps, upgrade_image="bootflash:nxos.bin")

    @patch("genie.libs.sdk.libs.abstracted_libs.nxos.ha.FileUtils.from_device")
    @patch("genie.libs.sdk.libs.abstracted_libs.nxos.ha.Lookup.from_device")
    @patch("genie.libs.sdk.libs.abstracted_libs.nxos.ha._is_eor_platform", return_value=False)
    def test_perform_issu_non_eor_invalid_command_defaults_to_lxc_passes(
        self,
        _is_eor_platform_mock,
        _lookup_mock,
        _fileutils_mock,
    ):
        obj = object.__new__(ha.HA)
        obj.parameters = {}
        obj.device = Mock()
        obj.device.hostname = "uut1"
        obj.device.execute = Mock(return_value="% Invalid command at '^ ' marker.\n")

        steps = DummySteps()

        with self.assertRaises(StopFlow):
            obj._perform_issu(steps=steps, upgrade_image="bootflash:nxos.bin")

        self.assertTrue(
            any(
                "System boot mode lxc matches user expected boot mode lxc" in msg
                for msg in steps.first_step.passed_messages
            )
        )

    @patch("genie.libs.sdk.libs.abstracted_libs.nxos.ha.FileUtils.from_device")
    @patch("genie.libs.sdk.libs.abstracted_libs.nxos.ha.Lookup.from_device")
    @patch("genie.libs.sdk.libs.abstracted_libs.nxos.ha._is_eor_platform", return_value=False)
    def test_perform_issu_non_eor_invalid_command_non_lxc_fails(
        self,
        _is_eor_platform_mock,
        _lookup_mock,
        _fileutils_mock,
    ):
        obj = object.__new__(ha.HA)
        obj.parameters = {"mode": "native"}
        obj.device = Mock()
        obj.device.hostname = "uut1"
        obj.device.execute = Mock(return_value="% Invalid command at '^ ' marker.\n")

        steps = DummySteps()

        with self.assertRaisesRegex(
            AssertionError,
            "System only supports lxc mode. Invalid user expected boot mode input native",
        ):
            obj._perform_issu(steps=steps, upgrade_image="bootflash:nxos.bin")


if __name__ == "__main__":
    unittest.main()
