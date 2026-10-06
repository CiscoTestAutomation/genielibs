import unittest
from unittest.mock import Mock, call, patch

from genie.libs.clean.stages.iosxe.stages import EraseCertificates
from genie.libs.clean.stages.tests.utils import (
    CommonStageTests,
    create_test_device,
)
from pyats.aetest.signals import TerminateStepSignal
from pyats.aetest.steps import Steps
from pyats.results import Failed, Passed


CURRENT = "nvram:IOS-Self-Sig#20B.cer"
STALE = "nvram:IOS-Self-Sig#20A.cer"


class TestEraseCertificates(CommonStageTests, unittest.TestCase):
    def setUp(self):
        self.cls = EraseCertificates()
        self.device = create_test_device("PE1", os="iosxe")
        self.locations = {"active": ["nvram:"]}
        self.references = {
            "running_config": [],
            "startup_config": [CURRENT],
        }
        self.before_usage = {
            "nvram:": {"total": 2097152, "free": 1506879,
                       "used": 590273},
        }
        self.after_usage = {
            "nvram:": {"total": 2097152, "free": 1507903,
                       "used": 589249},
        }
        self.before_files = {"nvram:": [CURRENT, STALE]}
        self.after_files = {"nvram:": [CURRENT]}

        self.device.api.get_certificate_storage_locations = Mock(
            return_value=self.locations)
        self.device.api.get_certificate_references = Mock(
            return_value=self.references)
        self.device.api.verify_certificate_references = Mock(
            side_effect=[True, True])
        self.device.api.get_certificate_storage_usage = Mock(
            side_effect=[self.before_usage, self.after_usage])
        self.device.api.get_certificate_files = Mock(
            side_effect=[self.before_files, self.after_files])
        self.device.api.delete_certificate_files = Mock(
            return_value={"nvram:": [STALE]})

    def test_preserves_current_certificate_and_erases_stale_file(self):
        steps = Steps()

        self.cls(steps=steps, device=self.device)

        self.device.api.delete_certificate_files.assert_called_once_with(
            files={"nvram:": [STALE]})
        self.assertEqual(
            {"nvram:": 1024}, self.cls.reclaimed_certificate_storage)
        self.assertEqual([Passed, Passed, Passed],
                         [detail.result for detail in steps.details])

    def test_preserves_running_config_reference_and_erases_stale_file(self):
        steps = Steps()
        self.references = {
            "running_config": [CURRENT],
            "startup_config": [],
        }
        self.device.api.get_certificate_references.return_value = (
            self.references)

        self.cls(steps=steps, device=self.device)

        self.device.api.delete_certificate_files.assert_called_once_with(
            files={"nvram:": [STALE]})
        self.assertEqual(
            [Passed, Passed, Passed],
            [detail.result for detail in steps.details],
        )

    def test_default_preserves_reference_on_each_stack_local_nvram(self):
        steps = Steps()
        self.locations = {
            "active": ["nvram:"],
            "standby": ["nvram:"],
        }
        self.device.api.get_certificate_storage_locations.return_value = (
            self.locations)
        self.device.api.get_certificate_files.side_effect = [
            {
                "active": [CURRENT, STALE],
                "standby": [CURRENT, STALE],
            },
            {
                "active": [CURRENT],
                "standby": [CURRENT],
            },
        ]
        self.device.api.get_certificate_storage_usage.side_effect = [
            {"active": self.before_usage["nvram:"],
             "standby": self.before_usage["nvram:"]},
            {"active": self.after_usage["nvram:"],
             "standby": self.after_usage["nvram:"]},
        ]
        self.device.api.delete_certificate_files.return_value = {
            "active": [STALE],
            "standby": [STALE],
        }

        self.cls(steps=steps, device=self.device)

        self.device.api.delete_certificate_files.assert_called_once_with(
            files={
                "active": [STALE],
                "standby": [STALE],
            })
        self.device.api.verify_certificate_references.assert_has_calls([
            call(references=self.references),
            call(references=self.references),
        ])

    @patch("genie.libs.clean.stages.iosxe.stages.log.warning")
    def test_explicitly_allows_erasing_current_certificate(self, warning):
        steps = Steps()
        self.device.api.verify_certificate_references.side_effect = None
        self.device.api.get_certificate_files.side_effect = [
            self.before_files,
            {"nvram:": []},
        ]
        self.device.api.delete_certificate_files.return_value = {
            "nvram:": [CURRENT, STALE],
        }

        self.cls(
            steps=steps,
            device=self.device,
            keep_current_certificate=False,
        )

        self.device.api.delete_certificate_files.assert_called_once_with(
            files={"nvram:": [CURRENT, STALE]})
        self.device.api.verify_certificate_references.assert_not_called()
        warning.assert_called_once()

    def test_fails_safely_when_referenced_certificate_is_missing(self):
        steps = Steps()
        self.device.api.verify_certificate_references.side_effect = None
        self.device.api.verify_certificate_references.return_value = False

        with self.assertRaises(TerminateStepSignal):
            self.cls(steps=steps, device=self.device)

        self.device.api.delete_certificate_files.assert_not_called()
        self.assertEqual(Failed, steps.details[0].result)

    def test_fails_when_a_selected_file_remains(self):
        steps = Steps()
        self.device.api.get_certificate_files.side_effect = [
            self.before_files,
            self.before_files,
        ]

        with self.assertRaises(TerminateStepSignal):
            self.cls(steps=steps, device=self.device)

        self.assertEqual(Failed, steps.details[-1].result)

    def test_no_stale_files_is_a_successful_noop(self):
        steps = Steps()
        self.device.api.get_certificate_files.side_effect = [
            {"nvram:": [CURRENT]},
            {"nvram:": [CURRENT]},
        ]
        self.device.api.get_certificate_storage_usage.side_effect = [
            self.before_usage,
            self.before_usage,
        ]

        self.cls(steps=steps, device=self.device)

        self.device.api.delete_certificate_files.assert_not_called()
        self.assertEqual({}, self.cls.deleted_certificate_files)

    def test_custom_patterns_are_dispatched_through_device_apis(self):
        steps = Steps()
        patterns = ["custom-*.cer"]

        self.cls(steps=steps, device=self.device,
                 certificate_patterns=patterns)

        self.device.api.get_certificate_references.assert_called_once_with(
            patterns=tuple(patterns))
        self.device.api.get_certificate_files.assert_any_call(
            locations=self.locations, patterns=tuple(patterns))
