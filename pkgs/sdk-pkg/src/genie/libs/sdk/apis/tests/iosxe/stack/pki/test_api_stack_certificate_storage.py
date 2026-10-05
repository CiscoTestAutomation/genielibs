from unittest import TestCase
from unittest.mock import Mock, call

from genie.libs.sdk.apis.iosxe.stack.pki import utils


DIRECTORY = """
Directory of nvram:/
  11  -rw-  1076  IOS-Self-Sig#1.cer
1048576 bytes total (1032192 bytes free)
"""


def connection(role, alias):
    con = Mock()
    con.role = role
    con.alias = alias
    con.execute.return_value = DIRECTORY
    return con


class TestStackCertificateStorage(TestCase):
    def setUp(self):
        self.active = connection("active", "a")
        self.standby = connection("standby", "b")
        self.device = Mock()
        self.device.subconnections = [self.active, self.standby]

    def test_discovers_each_subconnection_local_nvram(self):
        self.assertEqual(
            utils.get_certificate_storage_locations(self.device),
            {"active": ["nvram:"], "standby": ["nvram:"]},
        )
        self.device.execute.assert_not_called()

    def test_inventory_runs_on_each_subconnection(self):
        locations = {"active": ["nvram:"], "standby": ["nvram:"]}
        self.assertEqual(
            utils.get_certificate_files(self.device, locations),
            {
                "active": ["nvram:IOS-Self-Sig#1.cer"],
                "standby": ["nvram:IOS-Self-Sig#1.cer"],
            },
        )
        command = "dir nvram: | include IOS-Self-Sig#|bytes"
        self.active.execute.assert_called_once_with(
            command, timeout=utils.generic.CERTIFICATE_DIRECTORY_TIMEOUT)
        self.standby.execute.assert_called_once_with(
            command, timeout=utils.generic.CERTIFICATE_DIRECTORY_TIMEOUT)

    def test_references_use_active_subconnection(self):
        self.active.execute.side_effect = [
            " certificate self-signed 01 nvram:IOS-Self-Sig#1.cer",
            " certificate self-signed 01 nvram:IOS-Self-Sig#1.cer",
        ]
        self.assertEqual(
            utils.get_certificate_references(self.device),
            {
                "running_config": ["nvram:IOS-Self-Sig#1.cer"],
                "startup_config": ["nvram:IOS-Self-Sig#1.cer"],
            },
        )
        self.standby.execute.assert_not_called()

    def test_delete_dispatches_to_selected_subconnections(self):
        self.standby.execute.return_value = DIRECTORY.replace(
            "IOS-Self-Sig#1.cer", "IOS-Self-Sig#2.cer")
        files = {
            "active": ["nvram:IOS-Self-Sig#1.cer"],
            "standby": ["nvram:IOS-Self-Sig#2.cer"],
        }
        self.assertEqual(utils.delete_certificate_files(self.device, files), files)
        self.active.execute.assert_has_calls([
            call("dir nvram:",
                 timeout=utils.generic.CERTIFICATE_DIRECTORY_TIMEOUT),
            call("delete /force nvram:IOS-Self-Sig#1.cer"),
        ])
        self.standby.execute.assert_has_calls([
            call("dir nvram:",
                 timeout=utils.generic.CERTIFICATE_DIRECTORY_TIMEOUT),
            call("delete /force nvram:IOS-Self-Sig#2.cer"),
        ])

    def test_delete_skips_files_synchronized_from_active(self):
        self.active.execute.side_effect = [DIRECTORY, ""]
        self.standby.execute.return_value = (
            "2097152 bytes total (2090000 bytes free)")
        files = {
            "active": ["nvram:IOS-Self-Sig#1.cer"],
            "standby": ["nvram:IOS-Self-Sig#1.cer"],
        }

        self.assertEqual(
            utils.delete_certificate_files(self.device, files),
            {
                "active": ["nvram:IOS-Self-Sig#1.cer"],
                "standby": [],
            },
        )
        self.standby.execute.assert_called_once_with(
            "dir nvram:",
            timeout=utils.generic.CERTIFICATE_DIRECTORY_TIMEOUT,
        )

    def test_verify_references_checks_every_subconnection(self):
        references = {"startup_config": ["nvram:IOS-Self-Sig#1.cer"]}
        self.assertTrue(
            utils.verify_certificate_references(self.device, references))
        command = "dir nvram: | include IOS-Self-Sig#1.cer|bytes"
        self.active.execute.assert_has_calls([
            call(command, timeout=utils.generic.CERTIFICATE_DIRECTORY_TIMEOUT)
        ])
        self.standby.execute.assert_has_calls([
            call(command, timeout=utils.generic.CERTIFICATE_DIRECTORY_TIMEOUT)
        ])

    def test_storage_usage_runs_on_each_subconnection(self):
        self.assertEqual(
            utils.get_certificate_storage_usage(self.device),
            {
                "active": {"total": 1048576, "free": 1032192,
                           "used": 16384},
                "standby": {"total": 1048576, "free": 1032192,
                            "used": 16384},
            },
        )

    def test_single_connection_fallback_avoids_stby_nvram(self):
        device = Mock()
        device.name = "stack"
        device.subconnections = []
        self.assertEqual(
            utils.get_certificate_storage_locations(device),
            {"active": ["nvram:"]},
        )
        device.execute.assert_not_called()
