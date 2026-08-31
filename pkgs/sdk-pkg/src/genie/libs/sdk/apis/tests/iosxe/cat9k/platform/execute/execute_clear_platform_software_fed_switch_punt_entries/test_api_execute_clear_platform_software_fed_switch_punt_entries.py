from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.iosxe.cat9k.platform.execute import (
    execute_clear_platform_software_fed_switch_punt_entries,
)


class TestExecuteClearPlatformSoftwareFedSwitchPuntEntries(TestCase):

    def test_execute_clear_platform_software_fed_switch_punt_entries(self):
        device = Mock()
        device.name = "9250-TB5"

        execute_clear_platform_software_fed_switch_punt_entries(
            device=device,
            switch_number=1,
        )

        device.execute.assert_called_once_with(
            "show platform software fed switch 1 punt entries clear",
            timeout=60,
        )

    def test_execute_clear_platform_software_fed_switch_punt_entries_failure(
            self):
        device = Mock()
        device.name = "9250-TB5"
        device.execute.side_effect = SubCommandFailure("command failed")

        with self.assertRaisesRegex(
                SubCommandFailure,
                "Could not clear FED punt entry counters on switch 1"):
            execute_clear_platform_software_fed_switch_punt_entries(
                device=device,
                switch_number=1,
                timeout=30,
            )

        device.execute.assert_called_once_with(
            "show platform software fed switch 1 punt entries clear",
            timeout=30,
        )
