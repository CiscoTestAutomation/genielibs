import unittest
from unittest.mock import MagicMock

from genie.libs.clean.stages.iosxe.sdwan.stages import Connect
from genie.metaparser.util.exceptions import SchemaError
from genie.metaparser.util.schemaengine import Schema
from pyats.aetest.signals import TerminateStepSignal
from pyats.aetest.steps import Steps
from pyats.results import Failed, Passed


class TestConnect(unittest.TestCase):

    def setUp(self):
        self.stage = Connect()
        self.device = MagicMock()
        self.device.name = 'PE1'
        self.device.connect.return_value = ''

    def test_schema_accepts_logout_false(self):
        validated = Schema(self.stage.schema).validate({'logout': False})

        self.assertFalse(validated['logout'])

    def test_schema_allows_logout_to_be_omitted(self):
        validated = Schema(self.stage.schema).validate({'timeout': 200})

        self.assertNotIn('logout', validated)
        self.assertFalse(self.stage.LOGOUT)

    def test_schema_rejects_non_boolean_logout(self):
        with self.assertRaises(SchemaError):
            Schema(self.stage.schema).validate({'logout': 'false'})

    def test_logout_true_is_rejected(self):
        steps = Steps()

        with self.assertRaisesRegex(
                ValueError, "'logout: true' is not supported"):
            self.stage.connect(
                steps=steps,
                device=self.device,
                logout=True,
            )

        self.device.connect.assert_not_called()

    def test_logout_false_preserves_connection(self):
        steps = Steps()

        self.stage.connect(
            steps=steps,
            device=self.device,
            logout=False,
        )

        self.assertEqual(Passed, steps.details[0].result)
        self.device.destroy_all.assert_not_called()
        self.device.logout.assert_not_called()

    def test_already_connected_preserves_connection_without_reconnecting(self):
        self.device.connected = True
        steps = Steps()

        self.stage.connect(steps=steps, device=self.device, logout=False)

        self.assertEqual(Passed, steps.details[0].result)
        self.device.instantiate.assert_not_called()
        self.device.connect.assert_not_called()
        self.device.destroy_all.assert_not_called()

    def test_disconnected_device_connects_normally(self):
        self.device.connected = False

        def connect():
            self.device.connected = True
            return ''

        self.device.connect.side_effect = connect
        steps = Steps()

        self.stage.connect(
            steps=steps,
            device=self.device,
            logout=False,
        )

        self.assertEqual(Passed, steps.details[0].result)
        self.device.instantiate.assert_called_once()
        self.device.connect.assert_called_once()
        self.device.destroy_all.assert_not_called()

    def test_controller_managed_device_converts_to_sdwan(self):
        self.device.connected = False

        def connect():
            self.device.connected = True
            if self.device.connect.call_count == 1:
                return 'Router operating mode: Controller-Managed'
            return ''

        def destroy_all():
            self.device.connected = False

        self.device.connect.side_effect = connect
        self.device.destroy_all.side_effect = destroy_all
        steps = Steps()

        self.stage.connect(
            steps=steps,
            device=self.device,
            logout=False,
        )

        self.assertEqual(Passed, steps.details[0].result)
        self.assertEqual('sdwan', self.device.platform)
        self.assertEqual(2, self.device.connect.call_count)
        self.assertGreaterEqual(self.device.instantiate.call_count, 2)
        self.assertTrue(self.device.connected)

    def test_initial_connection_failure_recovers(self):
        self.device.connected = False

        def connect():
            if self.device.connect.call_count == 1:
                raise RuntimeError('initial connection failed')
            self.device.connected = True
            return ''

        def destroy_all():
            self.device.connected = False

        self.device.connect.side_effect = connect
        self.device.destroy_all.side_effect = destroy_all
        self.device.api.get_username_password.return_value = (
            'admin', 'password'
        )
        steps = Steps()

        self.stage.connect(steps=steps, device=self.device, logout=False)

        self.assertEqual(Passed, steps.details[0].result)
        self.assertEqual(2, self.device.connect.call_count)
        self.assertEqual(2, self.device.instantiate.call_count)
        self.assertTrue(self.device.connected)

    def test_recovery_controller_managed_converts_and_reconnects(self):
        self.device.connected = False

        def connect():
            if self.device.connect.call_count == 1:
                raise RuntimeError('initial connection failed')
            self.device.connected = True
            if self.device.connect.call_count == 2:
                return 'Router operating mode: Controller-Managed'
            return ''

        def destroy_all():
            self.device.connected = False

        self.device.connect.side_effect = connect
        self.device.destroy_all.side_effect = destroy_all
        self.device.api.get_username_password.return_value = (
            'admin', 'password'
        )
        steps = Steps()

        self.stage.connect(steps=steps, device=self.device, logout=False)

        self.assertEqual(Passed, steps.details[0].result)
        self.assertEqual('sdwan', self.device.platform)
        self.assertEqual(3, self.device.connect.call_count)
        self.assertEqual(3, self.device.instantiate.call_count)
        self.assertTrue(self.device.connected)

    def test_initial_and_recovery_connection_fail(self):
        self.device.connected = False
        self.device.connect.side_effect = RuntimeError(
            'connection failed'
        )
        self.device.api.get_username_password.return_value = (
            'admin', 'password'
        )
        steps = Steps()

        with self.assertRaises(TerminateStepSignal):
            self.stage.connect(steps=steps, device=self.device, logout=False)

        self.assertEqual(Failed, steps.details[0].result)
        self.assertEqual(2, self.device.connect.call_count)
        self.assertEqual(2, self.device.instantiate.call_count)
        self.assertFalse(self.device.connected)
