from unittest import TestCase
from unittest.mock import Mock, call, patch
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.cloud_mgmt.execute import (
    _execute_cloud_mgmt_level_3_reset,
    _get_cloud_mgmt_reset_event_counts,
    _verify_cloud_mgmt_reset_event,
    _verify_tls_vif_down_or_absent,
    execute_cloud_mgmt_reset_level,
)


class TestExecuteCloudMgmtResetLevel(TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = 'test_device'
        self.device.api.verify_cloud_mgmt_connect_status.return_value = True
        self.device.api.verify_cloud_mgmt_tunnel_config.return_value = True
        self.device.api.verify_cloud_mgmt_tunnel_state.return_value = True
        self.device.api.verify_interface_state_up.return_value = True
        down_patcher = patch(
            "genie.libs.sdk.apis.iosxe.cloud_mgmt.execute."
            "_verify_tls_vif_down_or_absent",
            return_value=True,
        )
        self.verify_tls_vif_down = down_patcher.start()
        self.addCleanup(down_patcher.stop)
        counts_patcher = patch(
            "genie.libs.sdk.apis.iosxe.cloud_mgmt.execute."
            "_get_cloud_mgmt_reset_event_counts",
            return_value=(0, 0, 0),
        )
        self.get_reset_counts = counts_patcher.start()
        self.addCleanup(counts_patcher.stop)
        event_patcher = patch(
            "genie.libs.sdk.apis.iosxe.cloud_mgmt.execute."
            "_verify_cloud_mgmt_reset_event",
            return_value=True,
        )
        self.verify_reset_event = event_patcher.start()
        self.addCleanup(event_patcher.stop)

    def test_reset_level_1_success(self):
        """Test reset level 1 - restarts nextunnel"""
        self.device.execute.return_value = (
            "Reset : Reset Level: 1 Triggered Successfully"
        )
        result = execute_cloud_mgmt_reset_level(self.device, level=1)
        self.device.execute.assert_called_once_with(
            "test platform software cloud-mgmt reset level 1", timeout=60
        )
        self.assertEqual(
            self.device.api.verify_cloud_mgmt_tunnel_state.call_count,
            3,
        )
        self.device.api.verify_cloud_mgmt_tunnel_state.assert_any_call(
            expected_primary_status="Down",
            expected_secondary_status="Down",
            max_time=60,
            check_interval=5,
        )
        self.device.api.verify_cloud_mgmt_tunnel_state.assert_called_with(
            expected_primary_status="Up",
            expected_secondary_status="Up",
            max_time=180,
            check_interval=5,
        )
        self.assertEqual(
            self.device.api.verify_interface_state_up.call_count,
            2,
        )
        self.verify_tls_vif_down.assert_called_once_with(
            self.device,
            max_time=60,
            check_interval=5,
        )
        self.assertEqual(
            self.device.api.verify_cloud_mgmt_tunnel_config.call_count,
            2,
        )
        self.assertIn("Triggered Successfully", result)

    def test_reset_level_2_success(self):
        """Test reset level 2 - triggers config rollback"""
        verify_tunnels = self.device.api.verify_cloud_mgmt_tunnel_state
        self.device.execute.return_value = (
            "Reset : Reset Level: 2 Triggered Successfully"
        )
        result = execute_cloud_mgmt_reset_level(self.device, level=2)
        self.device.execute.assert_called_once_with(
            "test platform software cloud-mgmt reset level 2", timeout=60
        )
        self.assertEqual(self.get_reset_counts.call_count, 3)
        self.get_reset_counts.assert_called_with(self.device, 2)
        self.verify_reset_event.assert_called_once_with(
            self.device,
            level=2,
            initial_counts=(0, 0, 0),
            max_time=60,
            check_interval=5,
        )
        self.assertEqual(
            self.device.api.verify_cloud_mgmt_tunnel_state.call_count,
            3,
        )
        verify_tunnels.assert_any_call(
            expected_primary_status="Down",
            expected_secondary_status="Down",
            max_time=60,
            check_interval=5,
        )
        self.assertEqual(
            self.device.api.verify_interface_state_up.call_count,
            2,
        )
        self.verify_tls_vif_down.assert_called_once_with(
            self.device,
            max_time=60,
            check_interval=5,
        )
        self.assertIn("Triggered Successfully", result)

    def test_level_2_records_down_before_recovery_event(self):
        """Test Level 2 captures transient Down before recovery is logged."""
        recovery_seen = {"value": False}

        def verify_tunnel_state(**kwargs):
            if kwargs["expected_primary_status"] == "Down":
                return not recovery_seen["value"]
            return True

        def verify_tls_down(*args, **kwargs):
            return not recovery_seen["value"]

        def verify_reset_event(*args, **kwargs):
            recovery_seen["value"] = True
            return True

        self.device.api.verify_cloud_mgmt_tunnel_state.side_effect = (
            verify_tunnel_state
        )
        self.verify_tls_vif_down.side_effect = verify_tls_down
        self.verify_reset_event.side_effect = verify_reset_event
        self.device.execute.return_value = (
            "Reset : Reset Level: 2 Triggered Successfully"
        )

        result = execute_cloud_mgmt_reset_level(self.device, level=2)

        self.assertTrue(recovery_seen["value"])
        self.assertIn("Triggered Successfully", result)

    def test_level_2_fails_without_down_transition(self):
        """Test Level 2 requires the tunnels to transition down."""
        verify_tunnels = self.device.api.verify_cloud_mgmt_tunnel_state
        verify_tunnels.side_effect = [True, False]
        self.device.execute.return_value = (
            "Reset : Reset Level: 2 Triggered Successfully"
        )

        with self.assertRaisesRegex(
            SubCommandFailure, "tunnels did not transition down"
        ):
            execute_cloud_mgmt_reset_level(self.device, level=2)

    def test_level_2_fails_without_reset_recovery_event(self):
        """Test Level 2 requires a new reset recovery event."""
        self.verify_reset_event.return_value = False
        self.device.execute.return_value = (
            "Reset : Reset Level: 2 Triggered Successfully"
        )

        with self.assertRaisesRegex(
            SubCommandFailure, "reset notification and recovery events"
        ):
            execute_cloud_mgmt_reset_level(self.device, level=2)

    def test_level_2_fails_with_new_config_updater_error(self):
        """Test Level 2 rejects a new configuration updater error."""
        self.get_reset_counts.side_effect = [
            (0, 0, 1),
            (1, 1, 2),
        ]
        self.device.execute.return_value = (
            "Reset : Reset Level: 2 Triggered Successfully"
        )

        with self.assertRaisesRegex(
            SubCommandFailure, "new CONFIG_UPDATER_ERR"
        ):
            execute_cloud_mgmt_reset_level(self.device, level=2)

    def test_level_2_fails_with_delayed_config_updater_error(self):
        """Test Level 2 detects an updater error during recovery."""
        self.get_reset_counts.side_effect = [
            (0, 0, 1),
            (1, 1, 1),
            (1, 1, 2),
        ]
        self.device.execute.return_value = (
            "Reset : Reset Level: 2 Triggered Successfully"
        )

        with self.assertRaisesRegex(
            SubCommandFailure, "new CONFIG_UPDATER_ERR"
        ):
            execute_cloud_mgmt_reset_level(self.device, level=2)

    def test_reset_level_3_success(self):
        """Test Level 3 waits for factory reset console recovery."""
        self.device.reload.return_value.output = (
            "Reset : Reset Level: 3 Triggered Successfully\nSwitch#"
        )

        result = execute_cloud_mgmt_reset_level(self.device, level=3)

        self.device.reload.assert_called_once_with(
            reload_command=(
                "test platform software cloud-mgmt reset level 3"
            ),
            prompt_recovery=True,
            timeout=600,
            return_output=True,
        )
        self.assertIn("Triggered Successfully", result)

    def test_level_3_custom_reset_timeout(self):
        """Test Level 3 passes its reset timeout to reload."""
        self.device.reload.return_value.output = (
            "Reset : Reset Level: 3 Triggered Successfully"
        )

        execute_cloud_mgmt_reset_level(
            self.device, level=3, reset_timeout=300
        )

        self.device.reload.assert_called_once_with(
            reload_command=(
                "test platform software cloud-mgmt reset level 3"
            ),
            prompt_recovery=True,
            timeout=300,
            return_output=True,
        )

    def test_level_3_reload_failure(self):
        """Test Level 3 rejects a failed factory reset/reconnect."""
        self.device.reload.side_effect = RuntimeError("reload timed out")

        with self.assertRaisesRegex(
            SubCommandFailure, "Level 3 reset did not complete"
        ):
            execute_cloud_mgmt_reset_level(self.device, level=3)

    def test_level_3_missing_success_marker(self):
        """Test Level 3 requires the immediate trigger marker."""
        self.device.reload.return_value.output = "Switch#"

        with self.assertRaisesRegex(
            SubCommandFailure, "did not trigger successfully"
        ):
            execute_cloud_mgmt_reset_level(self.device, level=3)

    def test_custom_timeout(self):
        """Test that custom timeout is passed through"""
        self.device.execute.return_value = (
            "Reset : Reset Level: 1 Triggered Successfully"
        )
        execute_cloud_mgmt_reset_level(self.device, level=1, timeout=120)
        self.device.execute.assert_called_once_with(
            "test platform software cloud-mgmt reset level 1", timeout=120
        )

    def test_execute_failure(self):
        """Test SubCommandFailure is raised on execute error"""
        self.device.execute.side_effect = SubCommandFailure("timeout")
        with self.assertRaises(SubCommandFailure):
            execute_cloud_mgmt_reset_level(self.device, level=1)

    def test_invalid_level(self):
        """Test unsupported levels are rejected before command execution"""
        for level in (0, 4, "1", None, True):
            with self.subTest(level=level):
                self.device.reset_mock()
                with self.assertRaises(ValueError):
                    execute_cloud_mgmt_reset_level(self.device, level=level)
                self.device.execute.assert_not_called()

    def test_output_missing_success_marker(self):
        """Test output without the success marker is rejected"""
        self.device.execute.return_value = "Reset : Reset Level: 1 Failed"

        with self.assertRaises(SubCommandFailure):
            execute_cloud_mgmt_reset_level(self.device, level=1)

    def test_output_reports_different_level(self):
        """Test output for a different reset level is rejected"""
        self.device.execute.return_value = (
            "Reset : Reset Level: 2 Triggered Successfully"
        )

        with self.assertRaises(SubCommandFailure):
            execute_cloud_mgmt_reset_level(self.device, level=1)

    def test_empty_output(self):
        """Test missing command output is rejected"""
        self.device.execute.return_value = None

        with self.assertRaises(SubCommandFailure):
            execute_cloud_mgmt_reset_level(self.device, level=1)

    def test_level_1_fails_when_initial_tunnels_are_down(self):
        """Test Level 1 requires both tunnels to be up before reset."""
        verify_tunnels = self.device.api.verify_cloud_mgmt_tunnel_state
        verify_tunnels.return_value = False

        with self.assertRaisesRegex(
            SubCommandFailure, "tunnels are not up before"
        ):
            execute_cloud_mgmt_reset_level(self.device, level=1)

        self.device.execute.assert_not_called()

    def test_level_1_fails_when_cloud_mgmt_is_disabled(self):
        """Test Level 1 requires cloud management to be enabled."""
        self.device.api.verify_cloud_mgmt_connect_status.return_value = False

        with self.assertRaisesRegex(
            SubCommandFailure, "Cloud-mgmt is not enabled before"
        ):
            execute_cloud_mgmt_reset_level(self.device, level=1)

        self.device.execute.assert_not_called()

    def test_level_1_fails_when_initial_config_fetch_failed(self):
        """Test Level 1 requires a successful configuration fetch."""
        self.device.api.verify_cloud_mgmt_tunnel_config.return_value = False

        with self.assertRaisesRegex(
            SubCommandFailure, "config fetch has not succeeded before"
        ):
            execute_cloud_mgmt_reset_level(self.device, level=1)

        self.device.execute.assert_not_called()

    def test_level_1_fails_when_initial_interface_is_down(self):
        """Test Level 1 requires TLS-VIF2 to be up before reset."""
        self.device.api.verify_interface_state_up.return_value = False

        with self.assertRaisesRegex(
            SubCommandFailure, "TLS-VIF2 is not up before"
        ):
            execute_cloud_mgmt_reset_level(self.device, level=1)

        self.device.execute.assert_not_called()

    def test_level_1_fails_without_tunnel_down_transition(self):
        """Test Level 1 must observe the tunnel down transition."""
        verify_tunnels = self.device.api.verify_cloud_mgmt_tunnel_state
        verify_tunnels.side_effect = [True, False]
        self.device.execute.return_value = (
            "Reset : Reset Level: 1 Triggered Successfully"
        )

        with self.assertRaisesRegex(
            SubCommandFailure, "tunnels did not transition down"
        ):
            execute_cloud_mgmt_reset_level(self.device, level=1)

    def test_level_1_fails_without_interface_down_transition(self):
        """Test Level 1 must observe the TLS-VIF2 down transition."""
        self.verify_tls_vif_down.return_value = False
        self.device.execute.return_value = (
            "Reset : Reset Level: 1 Triggered Successfully"
        )

        with self.assertRaisesRegex(
            SubCommandFailure, "TLS-VIF2 did not transition down or disappear"
        ):
            execute_cloud_mgmt_reset_level(self.device, level=1)

    def test_level_1_fails_without_tunnel_recovery(self):
        """Test Level 1 requires tunnel recovery within the timeout."""
        verify_tunnels = self.device.api.verify_cloud_mgmt_tunnel_state
        verify_tunnels.side_effect = [True, True, False]
        self.device.execute.return_value = (
            "Reset : Reset Level: 1 Triggered Successfully"
        )

        with self.assertRaisesRegex(
            SubCommandFailure, "tunnels did not recover within 180"
        ):
            execute_cloud_mgmt_reset_level(self.device, level=1)

    def test_level_1_fails_without_interface_recovery(self):
        """Test Level 1 requires TLS-VIF2 to recover."""
        self.device.api.verify_interface_state_up.side_effect = [True, False]
        self.device.execute.return_value = (
            "Reset : Reset Level: 1 Triggered Successfully"
        )

        with self.assertRaisesRegex(
            SubCommandFailure, "TLS-VIF2 did not recover"
        ):
            execute_cloud_mgmt_reset_level(self.device, level=1)

    def test_level_1_fails_without_config_fetch_recovery(self):
        """Test Level 1 requires configuration fetch to recover."""
        verify_config = self.device.api.verify_cloud_mgmt_tunnel_config
        verify_config.side_effect = [True, False]
        self.device.execute.return_value = (
            "Reset : Reset Level: 1 Triggered Successfully"
        )

        with self.assertRaisesRegex(
            SubCommandFailure, "config fetch did not succeed after"
        ):
            execute_cloud_mgmt_reset_level(self.device, level=1)

    def test_level_1_custom_state_timeouts(self):
        """Test Level 1 passes custom timing values to state checks."""
        self.device.execute.return_value = (
            "Reset : Reset Level: 1 Triggered Successfully"
        )

        execute_cloud_mgmt_reset_level(
            self.device,
            level=1,
            transition_timeout=30,
            recovery_timeout=90,
            check_interval=2,
        )

        self.device.api.verify_cloud_mgmt_tunnel_state.assert_called_with(
            expected_primary_status="Up",
            expected_secondary_status="Up",
            max_time=90,
            check_interval=2,
        )
        self.verify_tls_vif_down.assert_called_once_with(
            self.device,
            max_time=30,
            check_interval=2,
        )

    def test_recovery_checks_config_after_operational_state(self):
        """Test recovery checks config after tunnels and TLS-VIF2."""
        checks = Mock()
        checks.attach_mock(
            self.device.api.verify_cloud_mgmt_tunnel_state,
            "tunnels",
        )
        checks.attach_mock(
            self.device.api.verify_interface_state_up,
            "interface",
        )
        checks.attach_mock(
            self.device.api.verify_cloud_mgmt_tunnel_config,
            "config",
        )
        self.device.execute.return_value = (
            "Reset : Reset Level: 1 Triggered Successfully"
        )

        execute_cloud_mgmt_reset_level(self.device, level=1)

        recovery_tunnels = call.tunnels(
            expected_primary_status="Up",
            expected_secondary_status="Up",
            max_time=180,
            check_interval=5,
        )
        recovery_interface = call.interface(
            interface="TLS-VIF2",
            max_time=60,
            check_interval=5,
        )
        recovery_config = call.config(
            expected_fetch_state="Config fetch succeeded",
            max_time=60,
            check_interval=5,
        )
        calls = checks.mock_calls
        tunnel_index = calls.index(recovery_tunnels)
        interface_index = len(calls) - 1 - calls[::-1].index(
            recovery_interface
        )
        config_index = len(calls) - 1 - calls[::-1].index(
            recovery_config
        )

        self.assertLess(tunnel_index, interface_index)
        self.assertLess(interface_index, config_index)


class TestVerifyTlsVifDownOrAbsent(TestCase):

    def setUp(self):
        self.device = Mock()

    def test_absent_interface_is_valid_down_state(self):
        """Test an absent TLS-VIF2 is treated as down."""
        self.device.parse.return_value = {
            "interface": {
                "Vlan42": {"status": "up", "protocol": "up"},
            }
        }

        result = _verify_tls_vif_down_or_absent(
            self.device, max_time=1, check_interval=1
        )

        self.assertTrue(result)

    def test_explicit_interface_down_is_valid_down_state(self):
        """Test an explicit TLS-VIF2 down/down state is accepted."""
        self.device.parse.return_value = {
            "interface": {
                "TLS-VIF2": {"status": "down", "protocol": "down"},
            }
        }

        result = _verify_tls_vif_down_or_absent(
            self.device, max_time=1, check_interval=1
        )

        self.assertTrue(result)


class TestCloudMgmtResetEvents(TestCase):

    def setUp(self):
        self.device = Mock()

    def test_get_reset_event_counts(self):
        """Test reset event counts are scoped to the requested level."""
        self.device.execute.return_value = "\n".join(
            [
                "Reset Notification Called with Reset Level : 1",
                "CLOUD_MGMT_RESET_RECOVERY",
                "Reset Notification Called with Reset Level : 2",
                "CLOUD_MGMT_RESET_RECOVERY",
                "CONFIG_UPDATER_ERR",
            ]
        )

        result = _get_cloud_mgmt_reset_event_counts(self.device, level=2)

        self.assertEqual(result, (1, 2, 1))

    def test_verify_new_reset_event(self):
        """Test a new notification and recovery pair is detected."""
        self.device.execute.return_value = "\n".join(
            [
                "Reset Notification Called with Reset Level : 2",
                "CLOUD_MGMT_RESET_RECOVERY",
                "Reset Notification Called with Reset Level : 2",
                "CLOUD_MGMT_RESET_RECOVERY",
            ]
        )

        result = _verify_cloud_mgmt_reset_event(
            self.device,
            level=2,
            initial_counts=(1, 1, 0),
            max_time=1,
            check_interval=1,
        )

        self.assertTrue(result)


class TestExecuteCloudMgmtLevel3Reset(TestCase):

    def test_missing_reload_output_is_rejected(self):
        """Test Level 3 rejects a reload result without output."""
        device = Mock()
        device.name = "test_device"
        device.reload.return_value = True

        with self.assertRaisesRegex(
            SubCommandFailure, "did not trigger successfully"
        ):
            _execute_cloud_mgmt_level_3_reset(
                device,
                "test platform software cloud-mgmt reset level 3",
                600,
            )
