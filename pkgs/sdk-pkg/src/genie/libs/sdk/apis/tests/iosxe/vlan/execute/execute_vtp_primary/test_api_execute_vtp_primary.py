from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.execute import execute_vtp_primary


class TestExecuteVtpPrimary(TestCase):

    def test_execute_vtp_primary(self):
        device = Mock()
        expected_output = (
            'System can become primary server for Mst feature only when '
            'configured as a server'
        )
        device.execute.return_value = expected_output
        result = execute_vtp_primary(device, 'mst')

        self.assertEqual(result, expected_output)
        device.execute.assert_called_once()
        command = device.execute.call_args.args[0]
        call_kwargs = device.execute.call_args.kwargs
        self.assertEqual(command, 'vtp primary mst')
        self.assertEqual(
            call_kwargs['append_error_pattern'],
            ['.*Command cannot be executed.*'],
        )
        self.assertIsNotNone(call_kwargs['reply'])
