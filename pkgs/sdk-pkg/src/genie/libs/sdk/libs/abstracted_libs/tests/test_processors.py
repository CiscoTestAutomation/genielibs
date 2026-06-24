import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from pyats.results import Passed
from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.libs.abstracted_libs import processors


class DeviceMap(dict):

    @property
    def names(self):
        return list(self.keys())

    @property
    def aliases(self):
        return []


def sync_pcall(func, cargs=(), iargs=None, ikwargs=None, ckwargs=None, **kwargs):
    results = []
    ckwargs = ckwargs or {}

    if ikwargs:
        for call_kwargs in ikwargs:
            merged_kwargs = {}
            merged_kwargs.update(ckwargs)
            merged_kwargs.update(call_kwargs)
            results.append(func(*cargs, **merged_kwargs))
        return results

    if iargs:
        for call_args in iargs:
            if not isinstance(call_args, tuple):
                call_args = (call_args,)
            results.append(func(*(tuple(cargs) + call_args), **ckwargs))
        return results

    return [func(*cargs, **ckwargs)]


class TestExecuteCommandProcessors(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = "PE1"
        self.device.connected = True
        self.device.is_connected.return_value = True
        self.device.execute.return_value = "ok"
        self.device.api.slugify.side_effect = lambda value: value
        self.device.mapping = {}
        self.device.settings = SimpleNamespace(
            ERROR_PATTERN=["^%\\s*[Ii]nvalid (command|input)"])
        devices = DeviceMap({"PE1": self.device})
        self.section = SimpleNamespace(
            uid="section",
            result=Passed,
            parent=SimpleNamespace(uid="parent"),
            parameters={
                "testbed": SimpleNamespace(devices=devices),
                "uut": self.device,
            },
            failed=Mock(side_effect=AssertionError),
            errored=Mock(side_effect=AssertionError),
        )

    @patch.object(processors, "pcall", side_effect=sync_pcall)
    def test_pre_execute_command_passes_error_pattern_without_dialog(self, _):
        processors.pre_execute_command(
            self.section,
            devices={
                "PE1": {
                    "cmds": [
                        {
                            "cmd": "show version",
                            "timeout": 30,
                            "error_pattern": ["ERROR"],
                        },
                    ],
                },
            },
            max_retry=0,
        )

        self.device.execute.assert_called_once_with(
            "show version", timeout=30, error_pattern=["ERROR"])
        self.assertEqual(
            ["^%\\s*[Ii]nvalid (command|input)"],
            self.device.settings.ERROR_PATTERN)

    @patch.object(processors, "pcall", side_effect=sync_pcall)
    def test_pre_execute_command_empty_error_pattern_clears_device_patterns(
            self, _):
        def execute(*args, **kwargs):
            self.assertEqual([], self.device.settings.ERROR_PATTERN)
            return "ok"

        self.device.execute.side_effect = execute

        processors.pre_execute_command(
            self.section,
            devices={
                "PE1": {
                    "cmds": [
                        {
                            "cmd": "show logging",
                            "timeout": 30,
                            "error_pattern": [],
                        },
                    ],
                },
            },
            max_retry=0,
        )

        self.device.execute.assert_called_once_with(
            "show logging", timeout=30, error_pattern=[])
        self.assertEqual(
            ["^%\\s*[Ii]nvalid (command|input)"],
            self.device.settings.ERROR_PATTERN)

    @patch.object(processors, "pcall", side_effect=sync_pcall)
    def test_pre_execute_command_passes_error_pattern_with_dialog(self, _):
        processors.pre_execute_command(
            self.section,
            devices={
                "PE1": {
                    "cmds": [
                        {
                            "cmd": "reload",
                            "pattern": "confirm",
                            "answer": "y",
                            "timeout": 45,
                            "error_pattern": ["ERROR"],
                        },
                    ],
                },
            },
            max_retry=0,
        )

        args, kwargs = self.device.execute.call_args
        self.assertEqual(("reload",), args)
        self.assertIn("reply", kwargs)
        self.assertEqual(45, kwargs["timeout"])
        self.assertEqual(["ERROR"], kwargs["error_pattern"])

    @patch.object(processors, "pcall", side_effect=sync_pcall)
    def test_pre_execute_command_empty_error_pattern_with_dialog_clears_device_patterns(
            self, _):
        def execute(*args, **kwargs):
            self.assertEqual([], self.device.settings.ERROR_PATTERN)
            return "ok"

        self.device.execute.side_effect = execute

        processors.pre_execute_command(
            self.section,
            devices={
                "PE1": {
                    "cmds": [
                        {
                            "cmd": "reload",
                            "pattern": "confirm",
                            "answer": "y",
                            "timeout": 45,
                            "error_pattern": [],
                        },
                    ],
                },
            },
            max_retry=0,
        )

        args, kwargs = self.device.execute.call_args
        self.assertEqual(("reload",), args)
        self.assertIn("reply", kwargs)
        self.assertEqual(45, kwargs["timeout"])
        self.assertEqual([], kwargs["error_pattern"])
        self.assertEqual(
            ["^%\\s*[Ii]nvalid (command|input)"],
            self.device.settings.ERROR_PATTERN)

    @patch.object(processors, "pcall", side_effect=sync_pcall)
    def test_post_execute_command_passes_error_pattern_without_dialog(self, _):
        processors.post_execute_command(
            self.section,
            devices={
                "PE1": {
                    "cmds": [
                        {
                            "cmd": "show logging",
                            "timeout": 20,
                            "error_pattern": ["TRACEBACK"],
                        },
                    ],
                },
            },
            max_retry=0,
        )

        self.device.execute.assert_called_once_with(
            "show logging", error_pattern=["TRACEBACK"], timeout=20)
        self.assertEqual(
            ["^%\\s*[Ii]nvalid (command|input)"],
            self.device.settings.ERROR_PATTERN)

    @patch.object(processors, "pcall", side_effect=sync_pcall)
    def test_post_execute_command_empty_error_pattern_clears_device_patterns(
            self, _):
        def execute(*args, **kwargs):
            self.assertEqual([], self.device.settings.ERROR_PATTERN)
            return "ok"

        self.device.execute.side_effect = execute

        processors.post_execute_command(
            self.section,
            devices={
                "PE1": {
                    "cmds": [
                        {
                            "cmd": "show logging process dmiauthd",
                            "timeout": 20,
                            "error_pattern": [],
                        },
                    ],
                },
            },
            max_retry=0,
        )

        self.device.execute.assert_called_once_with(
            "show logging process dmiauthd", error_pattern=[], timeout=20)
        self.assertEqual(
            ["^%\\s*[Ii]nvalid (command|input)"],
            self.device.settings.ERROR_PATTERN)

    @patch.object(processors, "pcall", side_effect=sync_pcall)
    def test_post_execute_command_passes_error_pattern_with_dialog(self, _):
        processors.post_execute_command(
            self.section,
            devices={
                "PE1": {
                    "cmds": [
                        {
                            "cmd": "clear counters",
                            "pattern": "confirm",
                            "answer": "y",
                            "timeout": 20,
                            "error_pattern": ["ERROR"],
                        },
                    ],
                },
            },
            max_retry=0,
        )

        args, kwargs = self.device.execute.call_args
        self.assertEqual(("clear counters",), args)
        self.assertIn("reply", kwargs)
        self.assertEqual(20, kwargs["timeout"])
        self.assertEqual(["ERROR"], kwargs["error_pattern"])

    @patch.object(processors, "pcall", side_effect=sync_pcall)
    def test_post_execute_command_empty_error_pattern_with_dialog_clears_device_patterns(
            self, _):
        def execute(*args, **kwargs):
            self.assertEqual([], self.device.settings.ERROR_PATTERN)
            return "ok"

        self.device.execute.side_effect = execute

        processors.post_execute_command(
            self.section,
            devices={
                "PE1": {
                    "cmds": [
                        {
                            "cmd": "clear counters",
                            "pattern": "confirm",
                            "answer": "y",
                            "timeout": 20,
                            "error_pattern": [],
                        },
                    ],
                },
            },
            max_retry=0,
        )

        args, kwargs = self.device.execute.call_args
        self.assertEqual(("clear counters",), args)
        self.assertIn("reply", kwargs)
        self.assertEqual(20, kwargs["timeout"])
        self.assertEqual([], kwargs["error_pattern"])
        self.assertEqual(
            ["^%\\s*[Ii]nvalid (command|input)"],
            self.device.settings.ERROR_PATTERN)

    @patch.object(processors, "pcall", side_effect=sync_pcall)
    @patch.object(processors, "connect_device")
    def test_post_execute_command_reconnect_failure_keeps_original_failure(
            self, connect_device_mock, _):
        self.device.execute.side_effect = SubCommandFailure(
            "original execute failure")
        self.device.api.reconnect_device.side_effect = KeyError(
            "'cli' was not defined")

        with self.assertRaises(AssertionError):
            processors.post_execute_command(
                self.section,
                devices={
                    "PE1": {
                        "cmds": [
                            {
                                "cmd": "show logging process dmiauthd",
                                "timeout": 20,
                                "error_pattern": [],
                            },
                        ],
                    },
                },
                max_retry=0,
            )

        connect_device_mock.assert_not_called()
        failed_message = self.section.failed.call_args[0][0]
        self.assertIn("show logging process dmiauthd", failed_message)
        self.assertIn("original execute failure", failed_message)
        self.assertNotIn("'cli' was not defined", failed_message)
        self.assertEqual(
            ["^%\\s*[Ii]nvalid (command|input)"],
            self.device.settings.ERROR_PATTERN)


if __name__ == "__main__":
    unittest.main()
