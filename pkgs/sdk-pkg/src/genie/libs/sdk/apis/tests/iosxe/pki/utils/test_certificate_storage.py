from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.pki import utils
from unicon.core.errors import SubCommandFailure


DIRECTORY = """
Directory of nvram:/
  11  -rw-  1076  IOS-Self-Sig#1.cer
  12  -rw-  1076  IOS-Self-Sig#2.cer
  13  -rw-  2048  other-file.txt
1048576 bytes total (1032192 bytes free)
"""


class TestCertificateStorageApis(TestCase):
    def setUp(self):
        self.device = Mock()

    def test_get_certificate_storage_locations(self):
        self.assertEqual(utils.get_certificate_storage_locations(self.device), {"active": ["nvram:"]})

    def test_get_certificate_references(self):
        self.device.execute.side_effect = [
            " certificate self-signed 01 nvram:IOS-Self-Sig#1.cer",
            " certificate self-signed 01 nvram:IOS-Self-Sig#2.cer",
        ]
        self.assertEqual(utils.get_certificate_references(self.device), {
            "running_config": ["nvram:IOS-Self-Sig#1.cer"],
            "startup_config": ["nvram:IOS-Self-Sig#2.cer"],
        })
        self.assertEqual(self.device.execute.call_args_list[0].args[0], "show running-config | include IOS-Self-Sig#")

    def test_get_certificate_references_for_non_cer_pattern(self):
        self.device.execute.side_effect = [
            " certificate identity nvram:identity-current.pem",
            " certificate identity nvram:identity-startup.pem",
        ]
        self.assertEqual(
            utils.get_certificate_references(
                self.device, patterns=("identity-*.pem",)),
            {
                "running_config": ["nvram:identity-current.pem"],
                "startup_config": ["nvram:identity-startup.pem"],
            },
        )

    def test_get_certificate_files(self):
        self.device.execute.return_value = DIRECTORY
        self.assertEqual(utils.get_certificate_files(self.device), {"nvram:": ["nvram:IOS-Self-Sig#1.cer", "nvram:IOS-Self-Sig#2.cer"]})
        self.device.execute.assert_called_once_with(
            "dir nvram: | include IOS-Self-Sig#|bytes",
            timeout=utils.CERTIFICATE_DIRECTORY_TIMEOUT,
        )

    def test_get_certificate_files_with_string_location(self):
        self.device.execute.return_value = DIRECTORY
        self.assertEqual(
            utils.get_certificate_files(self.device, locations="nvram:"),
            {
                "nvram:": [
                    "nvram:IOS-Self-Sig#1.cer",
                    "nvram:IOS-Self-Sig#2.cer",
                ]
            },
        )
        self.device.execute.assert_called_once_with(
            "dir nvram: | include IOS-Self-Sig#|bytes",
            timeout=utils.CERTIFICATE_DIRECTORY_TIMEOUT,
        )

    def test_delete_certificate_files(self):
        self.assertEqual(utils.delete_certificate_files(self.device, {"nvram:": ["nvram:IOS-Self-Sig#1.cer"]}), {"nvram:": ["nvram:IOS-Self-Sig#1.cer"]})
        self.device.execute.assert_called_once_with("delete /force nvram:IOS-Self-Sig#1.cer")

    def test_delete_certificate_file_already_absent(self):
        self.device.execute.return_value = (
            "%Error deleting nvram:IOS-Self-Sig#1.cer "
            "(No such file or directory)")
        self.assertEqual(
            utils.delete_certificate_files(
                self.device,
                {"nvram:": ["nvram:IOS-Self-Sig#1.cer"]}),
            {"nvram:": []},
        )

    def test_delete_certificate_file_cli_error(self):
        self.device.execute.return_value = (
            "%Error deleting nvram:IOS-Self-Sig#1.cer (Permission denied)")
        with self.assertRaises(SubCommandFailure):
            utils.delete_certificate_files(
                self.device,
                {"nvram:": ["nvram:IOS-Self-Sig#1.cer"]})

    def test_get_certificate_files_without_literal_prefix(self):
        self.device.execute.return_value = DIRECTORY
        self.assertEqual(
            utils.get_certificate_files(self.device, patterns=("*.cer",)),
            {"nvram:": [
                "nvram:IOS-Self-Sig#1.cer",
                "nvram:IOS-Self-Sig#2.cer",
            ]},
        )
        self.device.execute.assert_called_once_with(
            "dir nvram:", timeout=utils.CERTIFICATE_DIRECTORY_TIMEOUT)

    def test_verify_certificate_references(self):
        self.device.execute.return_value = DIRECTORY
        self.assertTrue(utils.verify_certificate_references(self.device, {"startup_config": ["nvram:IOS-Self-Sig#1.cer"]}))
        self.assertFalse(utils.verify_certificate_references(self.device, {"startup_config": ["nvram:IOS-Self-Sig#9.cer"]}))

    def test_get_certificate_storage_usage(self):
        self.device.execute.return_value = DIRECTORY
        self.assertEqual(utils.get_certificate_storage_usage(self.device), {"nvram:": {"total": 1048576, "free": 1032192, "used": 16384}})

    def test_usage_without_totals_fails(self):
        self.device.execute.return_value = "Directory of nvram:/"
        with self.assertRaises(SubCommandFailure):
            utils.get_certificate_storage_usage(self.device)
