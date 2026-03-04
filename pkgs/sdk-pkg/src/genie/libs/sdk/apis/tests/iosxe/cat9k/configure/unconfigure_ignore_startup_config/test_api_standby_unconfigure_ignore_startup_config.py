from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat9k.configure import unconfigure_ignore_startup_config

class TestUnconfigureIgnoreStartupConfigStandby(TestCase):

    def test_standby_connection_is_skipped(self):
        device = Mock()
        device.name = "mock_device"

        active_con = Mock()
        active_con.state_machine.current_state = "any_state"
        active_con.role = "active"

        standby_con = Mock()
        standby_con.state_machine.current_state = "any_state"
        standby_con.role = "standby"

        device.subconnections = [active_con, standby_con]

        unconfigure_ignore_startup_config(device)

        self.assertEqual(
            active_con.configure.mock_calls[0].args,
            ('no system ignore startupconfig switch all',)
        )
        self.assertEqual(standby_con.configure.mock_calls, [])

    def test_rommon_connection_is_handled(self):
        device = Mock()
        device.name = "mock_device"

        rommon_con = Mock()
        rommon_con.state_machine.current_state = "rommon"
        rommon_con.role = "active"

        device.subconnections = [rommon_con]

        unconfigure_ignore_startup_config(device)

        self.assertEqual(
            rommon_con.execute.mock_calls[0].args,
            ('SWITCH_IGNORE_STARTUP_CFG=0',)
        )