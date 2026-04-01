import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.flow.configure import configure_fnf_flow_record


class TestConfigureFnfFlowRecord(TestCase):

    def test_configure_fnf_flow_record(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_fnf_flow_record(
            device,
            'test_record',
            False,  # ip
            None,   # ipv4
            None,   # ipv6
            None,   # mac
            None,   # datalink
            None,   # vlan
            False,  # collect_counter
            False,  # collect_interface
            None,   # collect_ipv4
            None,   # collect_ipv6
            False,  # collect_mac
            False,  # collect_transport
            False,  # collect_timestamp
            None,   # collect_flow
            None,   # collect_routing
            False,  # match_interface
            None,   # match_routing
            False,  # match_transport
            False,  # match_ipv4
            False,  # match_ipv6
            None,   # match_datalink
            None,   # match_flow
            None,   # match_timestamp
            None,   # match_application
            None,   # match_metadata
            True    # match_routing_vrf_input
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        cfg_arg = device.configure.mock_calls[0].args[0]

        # Normalize to list for assertions (API may pass list or multiline string)
        if isinstance(cfg_arg, str):
            cfg_lines = [line.strip() for line in cfg_arg.splitlines() if line.strip()]
        else:
            cfg_lines = list(cfg_arg)

        self.assertIn('flow record test_record', cfg_lines)
        self.assertIn('match routing vrf input', cfg_lines)


if __name__ == '__main__':
    unittest.main()