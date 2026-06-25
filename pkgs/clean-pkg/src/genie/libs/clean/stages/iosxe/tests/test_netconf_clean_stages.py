import logging
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from genie.libs.clean.stages.iosxe import stages as iosxe_stages
from genie.libs.clean.stages.iosxe.stages import (
    ConfigureNetconfYang,
    VerifyNetconfProcesses,
)
from genie.metaparser.util.exceptions import SchemaEmptyParserError

from pyats.aetest.signals import TerminateStepSignal
from pyats.aetest.steps import Steps
from pyats.results import Failed, Passed, Passx, Skipped


logging.disable(logging.CRITICAL)


class FakeTimeout(object):

    iterations = 1

    def __init__(self, max_time, interval):
        self.remaining = self.iterations

    def iterate(self):
        if self.remaining:
            self.remaining -= 1
            return True
        return False

    def sleep(self):
        pass


def netconf_process_output(ncsshd_state="Active"):
    return {
        "confd-status": "Started",
        "processes": {
            "nesd": {"status": "Running", "state": "Active"},
            "syncfd": {"status": "Running", "state": "Active"},
            "ncsshd": {"status": "Running", "state": ncsshd_state},
            "dmiauthd": {"status": "Running", "state": "Active"},
            "ndbmand": {"status": "Running", "state": "Active"},
            "pubd": {"status": "Running", "state": "Active"},
        },
    }


def netconf_process_cli_output(ncsshd_state="Active"):
    return f"""
Confd Status: Started

Process              Status              State
-------------------------------------------------------
nesd                 Running             Active
syncfd               Running             Active
ncsshd               Running             {ncsshd_state}
dmiauthd             Running             Active
nginx                Running             Not Applicable
ndbmand              Running             Active
pubd                 Running             Active
gnmib                Not Running         Not Applicable
"""


class TestVerifyNetconfProcesses(unittest.TestCase):

    def setUp(self):
        self.cls = VerifyNetconfProcesses()
        self.device = Mock()
        self.device.name = "PE1"

    @patch.object(iosxe_stages, "Timeout", FakeTimeout)
    def test_verify_processes_pass(self):
        steps = Steps()
        self.device.parse.return_value = netconf_process_output()

        self.cls.verify_netconf_processes(
            steps=steps, device=self.device, process_timeout=1,
            check_interval=1)

        self.assertEqual(Passed, steps.details[0].result)
        self.device.parse.assert_called_with(
            "show platform software yang-management process state")

    @patch.object(iosxe_stages, "Timeout", FakeTimeout)
    def test_verify_processes_allows_ncsshd_not_applicable(self):
        steps = Steps()
        self.device.parse.return_value = netconf_process_output(
            ncsshd_state="Not Applicable")

        self.cls.verify_netconf_processes(
            steps=steps, device=self.device, process_timeout=1,
            check_interval=1)

        self.assertEqual(Passed, steps.details[0].result)

    @patch.object(iosxe_stages, "Timeout", FakeTimeout)
    def test_verify_processes_retries_parser_error(self):
        steps = Steps()
        FakeTimeout.iterations = 2
        self.addCleanup(setattr, FakeTimeout, "iterations", 1)
        self.device.parse.side_effect = [
            SchemaEmptyParserError("empty output"),
            netconf_process_output(),
        ]
        self.device.execute.side_effect = [
            Exception("CLI output not ready"),
        ]

        self.cls.verify_netconf_processes(
            steps=steps, device=self.device, process_timeout=1,
            check_interval=1)

        self.assertEqual(Passed, steps.details[0].result)
        self.assertEqual(2, self.device.parse.call_count)

    @patch.object(iosxe_stages, "Timeout", FakeTimeout)
    def test_verify_processes_falls_back_to_raw_cli_output(self):
        steps = Steps()
        self.device.parse.side_effect = SchemaEmptyParserError("empty output")
        self.device.execute.return_value = netconf_process_cli_output()

        self.cls.verify_netconf_processes(
            steps=steps, device=self.device, process_timeout=1,
            check_interval=1)

        self.assertEqual(Passed, steps.details[0].result)
        self.device.execute.assert_called_once_with(
            "show platform software yang-management process state")

    @patch.object(iosxe_stages, "Timeout", FakeTimeout)
    def test_verify_processes_fails_when_not_ready(self):
        steps = Steps()
        output = netconf_process_output()
        output["processes"]["pubd"]["state"] = "Not Running"
        self.device.parse.return_value = output

        with self.assertRaises(TerminateStepSignal):
            self.cls.verify_netconf_processes(
                steps=steps, device=self.device, process_timeout=1,
                check_interval=1)

        self.assertEqual(Failed, steps.details[0].result)

    @patch.object(iosxe_stages, "Timeout", FakeTimeout)
    def test_verify_sync_pass(self):
        steps = Steps()
        self.device.execute.side_effect = [
            "%DMI-5-SYNC_START: NETCONF running data store has started",
            "%DMI-5-SYNC_COMPLETE: running configuration has been "
            "synchronized to the NETCONF running data store",
        ]

        self.cls.verify_netconf_sync(
            steps=steps, device=self.device, sync_timeout=1,
            check_interval=1)

        self.assertEqual(Passed, steps.details[0].result)

    @patch.object(iosxe_stages, "Timeout", FakeTimeout)
    def test_verify_sync_passx_when_not_started(self):
        steps = Steps()
        self.device.execute.return_value = ""

        self.cls.verify_netconf_sync(
            steps=steps, device=self.device, sync_timeout=1,
            check_interval=1)

        self.assertEqual(Passx, steps.details[0].result)

    @patch.object(iosxe_stages, "Timeout", FakeTimeout)
    def test_verify_sync_fails_on_timeout(self):
        steps = Steps()
        self.device.execute.side_effect = [
            "%DMI-5-SYNC_START: NETCONF running data store has started",
            "",
        ]

        with self.assertRaises(TerminateStepSignal):
            self.cls.verify_netconf_sync(
                steps=steps, device=self.device, sync_timeout=1,
                check_interval=1)

        self.assertEqual(Failed, steps.details[0].result)


class TestConfigureNetconfYang(unittest.TestCase):

    def setUp(self):
        self.cls = ConfigureNetconfYang()
        self.device = Mock()
        self.device.name = "PE1"

    @patch.object(iosxe_stages.time, "sleep")
    def test_default_configuration(self, _):
        steps = Steps()

        self.cls.configure_netconf_yang(steps=steps, device=self.device)

        self.assertEqual(Passed, steps.details[0].result)
        self.device.configure.assert_called_once_with([
            "no netconf-yang",
            "netconf-yang",
            "no netconf-yang feature candidate-datastore",
            "no yang-interfaces feature atomic-config",
            "yang-interfaces feature deprecated enable",
        ])

    @patch.object(iosxe_stages.time, "sleep")
    def test_candidate_two_stage_deprecated_disable_configuration(self, _):
        steps = Steps()

        self.cls.configure_netconf_yang(
            steps=steps,
            device=self.device,
            candidate=True,
            two_stage=True,
            deprecated_disable=True,
        )

        self.device.configure.assert_called_once_with([
            "no netconf-yang",
            "netconf-yang",
            "netconf-yang feature candidate-datastore",
            "yang-interfaces feature atomic-config",
            "yang-interfaces feature deprecated disable",
        ])

    @patch.object(iosxe_stages.time, "sleep")
    def test_netconf_disabled_configuration(self, _):
        steps = Steps()

        self.cls.configure_netconf_yang(
            steps=steps, device=self.device, netconf=False)

        self.device.configure.assert_called_once_with(["no netconf-yang"])

    def test_netconf_disabled_skips_verification(self):
        steps = Steps()

        self.cls.verify_netconf_processes(
            steps=steps, device=self.device, netconf=False)

        self.assertEqual(Skipped, steps.details[0].result)
        self.device.execute.assert_not_called()
        self.device.parse.assert_not_called()

    @patch.object(iosxe_stages.time, "sleep")
    @patch.object(iosxe_stages, "Timeout", FakeTimeout)
    def test_process_and_sync_verification_pass(self, _):
        steps = Steps()
        self.device.parse.return_value = netconf_process_output()
        self.device.execute.side_effect = [
            "clear logging",
            "%DMI-5-SYNC_START: NETCONF running data store has started",
            "%DMI-5-SYNC_COMPLETE: running configuration has been "
            "synchronized to the NETCONF running data store",
        ]
        self.device.api.get_ncdiff_connection.return_value = SimpleNamespace(
            connected=True)

        self.cls.verify_netconf_processes(
            steps=steps, device=self.device, process_timeout=1,
            sync_timeout=1, check_interval=1)

        self.assertEqual(Passed, steps.details[0].result)
        self.assertEqual(Passed, steps.details[1].result)


if __name__ == "__main__":
    unittest.main()
