from unittest import TestCase
from unittest.mock import Mock

from genie.conf.base import Device
from genie.libs.sdk.apis.iosxe.dual_rp.pki import utils


DIRECTORY = """
Directory of nvram:/
  11  -rw-  1076  IOS-Self-Sig#1.cer
1048576 bytes total (1032192 bytes free)
"""


class TestDualRpCertificateStorage(TestCase):
    def test_uses_active_and_standby_subconnections(self):
        active = Mock(role="active", alias="a")
        standby = Mock(role="standby", alias="b")
        active.execute.return_value = DIRECTORY
        standby.execute.return_value = DIRECTORY
        device = Mock()
        device.subconnections = [active, standby]

        locations = utils.get_certificate_storage_locations(device)

        self.assertEqual(
            locations,
            {"active": ["nvram:"], "standby": ["nvram:"]},
        )
        self.assertEqual(
            utils.get_certificate_files(device, locations),
            {
                "active": ["nvram:IOS-Self-Sig#1.cer"],
                "standby": ["nvram:IOS-Self-Sig#1.cer"],
            },
        )

    def test_abstraction_dispatches_stack_and_dual_rp_implementations(self):
        expected_modules = {
            "stack": "genie.libs.sdk.apis.iosxe.stack.pki.utils",
            "dual_rp": "genie.libs.sdk.apis.iosxe.dual_rp.pki.utils",
        }
        for chassis_type, expected_module in expected_modules.items():
            with self.subTest(chassis_type=chassis_type):
                device = Device(
                    chassis_type,
                    os="iosxe",
                    chassis_type=chassis_type,
                    custom={
                        "abstraction": {
                            "order": ["os", "chassis_type"],
                        },
                    },
                )
                function = device.api.get_api(
                    "get_certificate_storage_locations", device)
                self.assertEqual(expected_module, function.__module__)
