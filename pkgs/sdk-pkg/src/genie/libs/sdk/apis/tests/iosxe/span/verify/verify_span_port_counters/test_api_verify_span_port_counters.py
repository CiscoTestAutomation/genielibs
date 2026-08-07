import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.span.verify import verify_span_port_counters


SRC_PORT = 'Gi0/1/0'
DST_PORT = 'Gi0/1/1'


def _build_intf_parsed_output(interface, in_pkts, out_pkts):
    """Mimic the parsed dict returned by `show interfaces <intf>`.

    Schema (subset used by `get_interface_packet_counter`):
        {
            <intf>: {
                'counters': {
                    'in_pkts': int,
                    'out_pkts': int,
                    ...
                },
                ...
            }
        }
    """
    return {
        interface: {
            'counters': {
                'in_pkts': in_pkts,
                'out_pkts': out_pkts,
            },
        }
    }


class TestVerifySpanPortCounters(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def _set_outputs(self, src_in, src_out, dst_out):
        """Configure mocks to behave like real api helpers."""
        outputs = {
            SRC_PORT: _build_intf_parsed_output(
                SRC_PORT, in_pkts=src_in, out_pkts=src_out),
            DST_PORT: _build_intf_parsed_output(
                DST_PORT, in_pkts=0, out_pkts=dst_out),
        }

        def _show_intf(interface):
            return outputs.get(interface)

        def _get_counter(interface, counter_field, output):
            return (output or {}).get(interface, {}).get(
                'counters', {}).get(counter_field)

        self.device.api.get_show_interface_output.side_effect = _show_intf
        self.device.api.get_interface_packet_counter.side_effect = (
            _get_counter)

    def test_tx_within_tolerance(self):
        # tx: exp = src_out (1000) - 0 = 1000.
        # actual dst out increment = 950 -> within 10% tolerance.
        self._set_outputs(src_in=0, src_out=1000, dst_out=950)
        self.assertTrue(verify_span_port_counters(
            self.device, SRC_PORT, DST_PORT, 'tx',
            max_time=1, check_interval=1))

    def test_rx_within_tolerance(self):
        self._set_outputs(src_in=1000, src_out=0, dst_out=1050)
        self.assertTrue(verify_span_port_counters(
            self.device, SRC_PORT, DST_PORT, 'rx',
            max_time=1, check_interval=1))

    def test_both_within_tolerance(self):
        # both: exp = (in - 0) + (out - 0) = 1500. Allow +/-10%.
        self._set_outputs(src_in=500, src_out=1000, dst_out=1500)
        self.assertTrue(verify_span_port_counters(
            self.device, SRC_PORT, DST_PORT, 'both',
            max_time=1, check_interval=1))

    def test_outside_tolerance_returns_false(self):
        # exp = 1000, actual = 500, way outside +/-10%.
        self._set_outputs(src_in=0, src_out=1000, dst_out=500)
        self.assertFalse(verify_span_port_counters(
            self.device, SRC_PORT, DST_PORT, 'tx',
            max_time=1, check_interval=1))

    def test_no_interface_output_returns_false(self):
        self.device.api.get_show_interface_output.return_value = None
        self.assertFalse(verify_span_port_counters(
            self.device, SRC_PORT, DST_PORT, 'tx',
            max_time=1, check_interval=1))


if __name__ == '__main__':
    unittest.main()
