from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sisf.configure import (
    clear_device_tracking_database,
)


class TestClearDeviceTrackingDatabase(TestCase):

    def _verify_execute(self, options, expected_command):
        device = Mock()

        result = clear_device_tracking_database(
            device=device,
            options=options,
        )

        self.assertIsNone(result)
        device.execute.assert_called_once_with([expected_command])

    def test_clear_device_tracking_database(self):
        self._verify_execute(
            options=None,
            expected_command='clear device-tracking database',
        )

    def test_clear_device_tracking_database_1(self):
        self._verify_execute(
            options=[{'force': True}],
            expected_command='clear device-tracking database force',
        )

    def test_clear_device_tracking_database_2(self):
        self._verify_execute(
            options=[{'policy': 'test'}],
            expected_command='clear device-tracking database policy test',
        )

    def test_clear_device_tracking_database_3(self):
        self._verify_execute(
            options=[{'vlanid': 10}],
            expected_command='clear device-tracking database vlanid 10',
        )

    def test_clear_device_tracking_database_4(self):
        self._verify_execute(
            options=[{
                'interface': {
                    'force': True,
                    'interface': 'te1/0/1',
                },
            }],
            expected_command=(
                'clear device-tracking database interface te1/0/1 force'
            ),
        )

    def test_clear_device_tracking_database_5(self):
        self._verify_execute(
            options=[{
                'interface': {
                    'interface': 'te1/0/1',
                    'vlanid': 10,
                },
            }],
            expected_command=(
                'clear device-tracking database interface te1/0/1 vlanid 10'
            ),
        )

    def test_clear_device_tracking_database_6(self):
        self._verify_execute(
            options=[{
                'mac': {
                    'address': 'dead.beef.0001',
                    'target': {'force': True},
                },
            }],
            expected_command=(
                'clear device-tracking database mac dead.beef.0001 force'
            ),
        )

    def test_clear_device_tracking_database_7(self):
        self._verify_execute(
            options=[{
                'mac': {
                    'address': 'dead.beef.0001',
                    'target': {'interface': 'te1/0/1'},
                },
            }],
            expected_command=(
                'clear device-tracking database mac dead.beef.0001 '
                'interface te1/0/1'
            ),
        )

    def test_clear_device_tracking_database_8(self):
        self._verify_execute(
            options=[{
                'mac': {
                    'address': 'dead.beef.0001',
                    'target': {'policy': 'test'},
                },
            }],
            expected_command=(
                'clear device-tracking database mac dead.beef.0001 '
                'policy test'
            ),
        )

    def test_clear_device_tracking_database_9(self):
        self._verify_execute(
            options=[{
                'mac': {
                    'address': 'dead.beef.0001',
                    'target': {'vlanid': 10},
                },
            }],
            expected_command=(
                'clear device-tracking database mac dead.beef.0001 '
                'vlanid 10'
            ),
        )

    def test_clear_device_tracking_database_10(self):
        self._verify_execute(
            options=[{
                'address': {
                    'address': '20.20.20.20',
                    'target': {'force': True},
                },
            }],
            expected_command=(
                'clear device-tracking database address 20.20.20.20 force'
            ),
        )

    def test_clear_device_tracking_database_11(self):
        self._verify_execute(
            options=[{
                'address': {
                    'address': '20.20.20.20',
                    'target': {'interface': 'te1/0/1'},
                },
            }],
            expected_command=(
                'clear device-tracking database address 20.20.20.20 '
                'interface te1/0/1'
            ),
        )

    def test_clear_device_tracking_database_12(self):
        self._verify_execute(
            options=[{
                'address': {
                    'address': '20.20.20.20',
                    'target': {'policy': 'test'},
                },
            }],
            expected_command=(
                'clear device-tracking database address 20.20.20.20 '
                'policy test'
            ),
        )

    def test_clear_device_tracking_database_13(self):
        self._verify_execute(
            options=[{
                'address': {
                    'address': '20.20.20.20',
                    'target': {'vlanid': 10},
                },
            }],
            expected_command=(
                'clear device-tracking database address 20.20.20.20 '
                'vlanid 10'
            ),
        )

    def test_clear_device_tracking_database_14(self):
        self._verify_execute(
            options=[{
                'prefix': {
                    'address': '3001::1/48',
                    'target': {'force': True},
                },
            }],
            expected_command=(
                'clear device-tracking database prefix 3001::1/48 force'
            ),
        )

    def test_clear_device_tracking_database_15(self):
        self._verify_execute(
            options=[{
                'prefix': {
                    'address': '3001::1/48',
                    'target': {'interface': 'te1/0/1'},
                },
            }],
            expected_command=(
                'clear device-tracking database prefix 3001::1/48 '
                'interface te1/0/1'
            ),
        )

    def test_clear_device_tracking_database_16(self):
        self._verify_execute(
            options=[{
                'prefix': {
                    'address': '3001::1/48',
                    'target': {'policy': 'test'},
                },
            }],
            expected_command=(
                'clear device-tracking database prefix 3001::1/48 '
                'policy test'
            ),
        )

    def test_clear_device_tracking_database_17(self):
        self._verify_execute(
            options=[{
                'prefix': {
                    'address': '3001::1/48',
                    'target': {'vlanid': 10},
                },
            }],
            expected_command=(
                'clear device-tracking database prefix 3001::1/48 '
                'vlanid 10'
            ),
        )
