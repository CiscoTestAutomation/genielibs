#! /usr/bin/env python
import sys
import unittest
import logging
sys.path = ['.', '..'] + sys.path
from blitz.rpcverify import RpcVerify


# TODO: Needs to be part of genielibs test run

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


operstate = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" \
  xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" \
  message-id="urn:uuid:d0c1123f-2f54-49bb-aafe-ec3723318163">
  <data>
    <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
      <interface>
        <name xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0"> \
            GigabitEthernet2</name>
        <statistics>
          <discontinuity-time>2019-05-31T14:37:03.000993+00:00 \
              </discontinuity-time>
          <in-octets>330</in-octets>
          <in-unicast-pkts>5</in-unicast-pkts>
          <in-broadcast-pkts>6</in-broadcast-pkts>
          <in-multicast-pkts>7</in-multicast-pkts>
          <in-discards>8</in-discards>
          <in-errors>9</in-errors>
          <in-unknown-protos>10</in-unknown-protos>
          <out-octets>11</out-octets>
          <out-unicast-pkts>12</out-unicast-pkts>
          <out-broadcast-pkts>13</out-broadcast-pkts>
          <out-multicast-pkts>14</out-multicast-pkts>
          <out-discards>17</out-discards>
          <out-errors>16</out-errors>
        </statistics>
      </interface>
    </interfaces-state>
  </data>
</rpc-reply>"""


class TestRpcVerify(unittest.TestCase):
    """Test cases for the rpcverify.RpcVerify methods."""

    @classmethod
    def setUpClass(cls):
        cls.log = log
        cls.cap = ['urn:ietf:params:netconf:capability:with-defaults:1.0?\
basic-mode=explicit&also-supported=report-all-tagged']
        cls.rpcv = RpcVerify(log=cls.log, capabilities=cls.cap)
        cls.operstate = operstate

    def test_operational_state_pass(self):
        """Process rpc-reply and check opfields for match."""
        # xpath used for match instead of ID.
        opfields = [
            {'selected': 'true',
             'name': 'in-unicast-pkts',
             'xpath': '/interfaces-state/interface/statistics/in-unicast-pkts',
             'value': '5',
             'op': '=='},
            {'selected': 'true',
             'name': 'in-octets',
             'xpath': '/interfaces-state/interface/statistics/in-octets',
             'value': '330',
             'op': '>='},
            {'selected': 'true',
             'name': 'out-discards',
             'xpath': '/interfaces-state/interface/statistics/out-discards',
             'value': '17',
             'op': '=='},
            {'selected': 'true',
             'name': 'out-errors',
             'xpath': '/interfaces-state/interface/statistics/out-errors',
             'value': '16',
             'op': '=='}]

        resp = self.rpcv.process_rpc_reply(operstate)
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

    def test_operational_state_fail(self):
        """Process rpc-reply and check opfields with one mismatch."""
        # xpath used for match instead of ID.
        opfields = [
            {'selected': 'true',
             'name': 'in-unicast-pkts',
             'xpath': '/interfaces-state/interface/statistics/in-unicast-pkts',
             'value': '5',
             'op': '=='},
            {'selected': 'true',
             'name': 'in-octets',
             'xpath': '/interfaces-state/interface/statistics/in-octets',
             'value': '3300',
             'op': '>='},
            {'selected': 'true',
             'name': 'out-discards',
             'xpath': '/interfaces-state/interface/statistics/out-discards',
             'value': '17',
             'op': '=='},
            {'selected': 'true',
             'name': 'out-errors',
             'xpath': '/interfaces-state/interface/statistics/out-errors',
             'value': '16',
             'op': '=='}]

        resp = self.rpcv.process_rpc_reply(self.operstate)
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertFalse(result)

    def test_operational_state_uint_datatype_pass(self):
        """Process rpc-reply and check opfields for datatype match."""
        # xpath used for match instead of ID.
        opfields = [
            {'selected': 'true',
             'name': 'in-unicast-pkts',
             'xpath': '/interfaces-state/interface/statistics/in-unicast-pkts',
             'value': 5,
             'datatype': 'uint8',
             'op': '=='},
            {'selected': 'true',
             'name': 'in-octets',
             'xpath': '/interfaces-state/interface/statistics/in-octets',
             'value': 330,
             'datatype': 'uint16',
             'op': '>='},
            {'selected': 'true',
             'name': 'out-discards',
             'xpath': '/interfaces-state/interface/statistics/out-discards',
             'value': '17',
             'op': '=='},
            {'selected': 'true',
             'name': 'out-errors',
             'xpath': '/interfaces-state/interface/statistics/out-errors',
             'value': '16',
             'datatype': 'uint8',
             'op': '=='}]

        resp = self.rpcv.process_rpc_reply(self.operstate)
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

    def test_operational_state_int_datatype_positive(self):
        """Process rpc-reply and check opfields with int8-64 > 0 matchs."""
        oper = self.operstate.replace('330', '30000')
        oper = oper.replace('17', '70000')
        oper = oper.replace('16', '7000000000')
        opfields = [
            {'selected': 'true',
             'name': 'in-unicast-pkts',
             'xpath': '/interfaces-state/interface/statistics/in-unicast-pkts',
             'value': 5,
             'datatype': 'int8',
             'op': '=='},
            {'selected': 'true',
             'name': 'in-octets',
             'xpath': '/interfaces-state/interface/statistics/in-octets',
             'value': 30000,
             'datatype': 'int16',
             'op': '>='},
            {'selected': 'true',
             'name': 'out-discards',
             'xpath': '/interfaces-state/interface/statistics/out-discards',
             'value': 70000,
             'datatype': 'int32',
             'op': '=='},
            {'selected': 'true',
             'name': 'out-errors',
             'xpath': '/interfaces-state/interface/statistics/out-errors',
             'value': 7000000000,
             'datatype': 'int64',
             'op': '=='}]
        resp = self.rpcv.process_rpc_reply(oper)
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

    def test_operational_state_int_datatype_negative(self):
        """Process rpc-reply and check opfields with int8-64 > 0 matchs."""
        oper = self.operstate.replace('5', '-5')
        oper = oper.replace('330', '-30000')
        oper = oper.replace('17', '-70000')
        oper = oper.replace('16', '-7000000000')
        opfields = [
            {'selected': 'true',
             'name': 'in-unicast-pkts',
             'xpath': '/interfaces-state/interface/statistics/in-unicast-pkts',
             'value': -5,
             'datatype': 'int8',
             'op': '=='},
            {'selected': 'true',
             'name': 'in-octets',
             'xpath': '/interfaces-state/interface/statistics/in-octets',
             'value': -30000,
             'datatype': 'int16',
             'op': '>='},
            {'selected': 'true',
             'name': 'out-discards',
             'xpath': '/interfaces-state/interface/statistics/out-discards',
             'value': -70000,
             'datatype': 'int32',
             'op': '=='},
            {'selected': 'true',
             'name': 'out-errors',
             'xpath': '/interfaces-state/interface/statistics/out-errors',
             'value': -7000000000,
             'datatype': 'int64',
             'op': '=='}]

        resp = self.rpcv.process_rpc_reply(oper)
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

    def test_operational_state_uint_datatypes(self):
        """Process rpc-reply and check opfields with uint8-64 match."""
        oper = self.operstate.replace('330', '30000')
        oper = oper.replace('17', '70000')
        oper = oper.replace('16', '18446744073709551614')
        opfields = [
            {'selected': 'true',
             'name': 'in-unicast-pkts',
             'xpath': '/interfaces-state/interface/statistics/in-unicast-pkts',
             'value': 5,
             'datatype': 'uint8',
             'op': '=='},
            {'selected': 'true',
             'name': 'in-octets',
             'xpath': '/interfaces-state/interface/statistics/in-octets',
             'value': 30000,
             'datatype': 'uint16',
             'op': '>='},
            {'selected': 'true',
             'name': 'out-discards',
             'xpath': '/interfaces-state/interface/statistics/out-discards',
             'value': 70000,
             'datatype': 'uint32',
             'op': '=='},
            {'selected': 'true',
             'name': 'out-errors',
             'xpath': '/interfaces-state/interface/statistics/out-errors',
             'value': 18446744073709551614,
             'datatype': 'uint64',
             'op': '=='}]

        resp = self.rpcv.process_rpc_reply(oper)
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

    def test_operational_state_other_datatype(self):
        """Check opfields empty, boolean, pattern matches."""
        oper = self.operstate.replace('5', '')
        oper = oper.replace('330', 'true')
        oper = oper.replace('17', 'false')
        oper = oper.replace('16', 'abc[123]DEFghblahblah')
        opfields = [
            {'selected': 'true',
             'name': 'in-unicast-pkts',
             'xpath': '/interfaces-state/interface/statistics/in-unicast-pkts',
             'value': 'empty',
             'datatype': 'empty',
             'op': '=='},
            {'selected': 'true',
             'name': 'in-octets',
             'xpath': '/interfaces-state/interface/statistics/in-octets',
             'value': 'true',
             'datatype': 'boolean',
             'op': '=='},
            {'selected': 'true',
             'name': 'out-discards',
             'xpath': '/interfaces-state/interface/statistics/out-discards',
             'value': 'False',
             'datatype': 'boolean',
             'op': '=='},
            {'selected': 'true',
             'name': 'out-errors',
             'xpath': '/interfaces-state/interface/statistics/out-errors',
             'value': '([^a-zA-Z1-3\\[])|(blah)',
             'datatype': 'pattern',
             'op': '=='}]

        resp = self.rpcv.process_rpc_reply(oper)
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
