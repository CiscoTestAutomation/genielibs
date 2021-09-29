#! /usr/bin/env python
import sys
import unittest
import logging
from time import time
import base64
from yang.connector.gnmi import Gnmi
from genie.libs.sdk.triggers.blitz import yangexec
from genie.libs.sdk.triggers.blitz.rpcverify import RpcVerify


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


class TestGnmi(Gnmi):
    def __init__(self, *args, **kwargs):
        pass


operstate_gnmi = {
    "timestamp": 1625231480325470151,
    "update": {
        "path": {
            "elem": [
                {
                    "name": "interfaces-state"
                },
                {
                    "name": "interface",
                    "key": {
                        "key": "name",
                        "value": "GigabitEthernet2"
                    }
                }
            ]
        },
        "val": {
            "jsonIetfVal": ''
        }
    }
}

multilist = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" \
    xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" \
        message-id="urn:uuid:39eeacc2-821e-4822-ba44-477c502d0242">
  <data>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <vrf>
        <definition>
          <name>Mgmt-vrf</name>
        </definition>
        <definition>
          <name>cisco</name>
        </definition>
        <definition>
          <name>genericstring</name>
        </definition>
        <definition>
          <name>mgmt1</name>
          <description>
            test me
          </description>
        </definition>
        <definition>
          <name>try</name>
        </definition>
      </vrf>
    </native>
  </data>
</rpc-reply>"""

listreply = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" \
    xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:851d10b3-6cf2-4ed0-a58b-a7e34a61fe66">
  <data>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <router>
        <rip xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-rip">
          <redistribute>
            <eigrp>
              <as-number xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">32768</as-number>
            </eigrp>
          </redistribute>
        </rip>
      </router>
    </native>
  </data>
</rpc-reply>"""

multientry = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:c8ced2db-d58f-4beb-9881-d9e7a01f0a2d">
  <data>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <num-exp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-voice">
        <dialled_digit>123</dialled_digit>
        <dialled_pattern>1234</dialled_pattern>
      </num-exp>
      <num-exp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-voice">
        <dialled_digit>456</dialled_digit>
        <dialled_pattern>4567</dialled_pattern>
      </num-exp>
    </native>
  </data>
</rpc-reply>"""

no_data_rpc_reply = """<rpc-reply message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <data/>
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
        cls.gnmi = TestGnmi()
        cls.operstate_gnmi = operstate_gnmi
        cls.jsonIetfVal = ""

    def setUp(self):
        self.jsonIetfVal = """{"statistics": {"in-octets": 330, \
"in-unicast-pkts": 5, "in-broadcast-pkts": 6, \
"in-multicast-pkts": 7, "in-discards": 8, "in-errors": 9, \
"in-unknown-protos": 10, "out-octets": 11, \
"out-unicast-pkts": 12, "out-broadcast-pkts": 13, \
"out-multicast-pkts": 14, "out-discards": 17, \
"out-errors": 16}}"""

    def _base64encode(self):
        self.operstate_gnmi['update']['val']['jsonIetfVal'] = base64.encodebytes(
            bytes(self.jsonIetfVal, encoding='utf-8')
        )

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

        self._base64encode()
        resp = self.gnmi.decode_opfields(self.operstate_gnmi['update'])
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

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

        self._base64encode()
        resp = self.gnmi.decode_opfields(self.operstate_gnmi['update'])
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertFalse(result)

        resp = self.rpcv.process_rpc_reply(self.operstate)
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertFalse(result)

    def test_operational_state_in_range(self):
        """Process rpc-reply and check opfield in specified range."""
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
             'value': '300-400',
             'op': 'range'},
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

        self._base64encode()
        resp = self.gnmi.decode_opfields(self.operstate_gnmi['update'])
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

        resp = self.rpcv.process_rpc_reply(operstate)
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

    def test_operational_state_in_range_typedef_datatype(self):
        """Process rpc-reply and check opfield range with typedef datatype."""
        # xpath used for match instead of ID.
        opfields = [
            {'selected': 'true',
             'name': 'in-unicast-pkts',
             'xpath': '/interfaces-state/interface/statistics/in-unicast-pkts',
             'value': '5',
             'op': '=='},
            {'datatype': 'oc-types:ieeefloat32',
             'selected': 'true',
             'name': 'in-octets',
             'xpath': '/interfaces-state/interface/statistics/in-octets',
             'value': '300-400',
             'op': 'range'},
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

        self._base64encode()
        resp = self.gnmi.decode_opfields(self.operstate_gnmi['update'])
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

        resp = self.rpcv.process_rpc_reply(operstate)
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

    def test_operational_state_in_range_invalid_datatype(self):
        """Process rpc-reply and check opfield range wrong datatype."""
        # xpath used for match instead of ID.
        opfields = [
            {'selected': 'true',
             'name': 'in-unicast-pkts',
             'xpath': '/interfaces-state/interface/statistics/in-unicast-pkts',
             'value': '5',
             'op': '=='},
            {'datatype': 'int',
             'selected': 'true',
             'name': 'in-octets',
             'xpath': '/interfaces-state/interface/statistics/in-octets',
             'value': '300.0-400.0',
             'op': 'range'},
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

        self._base64encode()
        resp = self.gnmi.decode_opfields(self.operstate_gnmi['update'])
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertFalse(result)

        resp = self.rpcv.process_rpc_reply(operstate)
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertFalse(result)

    def test_operational_state_in_range_space_format(self):
        """Process rpc-reply and check opfield in "n - n" range."""
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
             'value': '300 - 400',
             'op': 'range'},
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

        self._base64encode()
        resp = self.gnmi.decode_opfields(self.operstate_gnmi['update'])
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

        resp = self.rpcv.process_rpc_reply(operstate)
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

    def test_operational_state_over_range(self):
        """Process rpc-reply and check opfield over specified range."""
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
             'value': '340-400',
             'op': 'range'},
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

        self._base64encode()
        resp = self.gnmi.decode_opfields(self.operstate_gnmi['update'])
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertFalse(result)

        resp = self.rpcv.process_rpc_reply(operstate)
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertFalse(result)

    def test_operational_state_under_range(self):
        """Process rpc-reply and check opfield under specified range."""
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
             'value': '200-300',
             'op': 'range'},
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

        self._base64encode()
        resp = self.gnmi.decode_opfields(self.operstate_gnmi['update'])
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertFalse(result)

        resp = self.rpcv.process_rpc_reply(operstate)
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

        self._base64encode()
        resp = self.gnmi.decode_opfields(self.operstate_gnmi['update'])
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

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

        oper_gnmi = self.jsonIetfVal.replace('330', '30000')
        oper_gnmi = oper_gnmi.replace('17', '70000')
        oper_gnmi = oper_gnmi.replace('16', '7000000000')
        self.jsonIetfVal = oper_gnmi
        self._base64encode()

        resp = self.gnmi.decode_opfields(self.operstate_gnmi['update'])
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

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

        oper_gnmi = self.jsonIetfVal.replace('5', '-5')
        oper_gnmi = oper_gnmi.replace('330', '-3000')
        oper_gnmi = oper_gnmi.replace('17', '-70000')
        oper_gnmi = oper_gnmi.replace('16', '-7000000000')
        self.jsonIetfVal = oper_gnmi
        self._base64encode()

        resp = self.gnmi.decode_opfields(self.operstate_gnmi['update'])
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

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

        oper_gnmi = self.jsonIetfVal.replace('330', '30000')
        oper_gnmi = oper_gnmi.replace('17', '70000')
        oper_gnmi = oper_gnmi.replace('16', '18446744073709551614')
        self.jsonIetfVal = oper_gnmi
        self._base64encode()

        resp = self.gnmi.decode_opfields(self.operstate_gnmi['update'])
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

        resp = self.rpcv.process_rpc_reply(oper)
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

    def test_operational_state_other_datatype(self):
        """Check opfields empty == '', boolean, pattern matches."""
        oper = self.operstate.replace('5', '')
        oper = oper.replace('330', 'true')
        oper = oper.replace('17', 'false')
        oper = oper.replace('16', 'abc[123]DEFghblahblah')
        opfields = [
            {'selected': 'true',
             'name': 'in-unicast-pkts',
             'xpath': '/interfaces-state/interface/statistics/in-unicast-pkts',
             'value': '',
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

        oper_gnmi = self.jsonIetfVal.replace('5', '""')
        oper_gnmi = oper_gnmi.replace('330', '"true"')
        oper_gnmi = oper_gnmi.replace('17', '"false"')
        oper_gnmi = oper_gnmi.replace('16', '"abc[123]DEFghblahblah"')
        self.jsonIetfVal = oper_gnmi
        self._base64encode()

        resp = self.gnmi.decode_opfields(self.operstate_gnmi['update'])
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

        resp = self.rpcv.process_rpc_reply(oper)
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

    def test_operational_state_other_empty_value(self):
        """Check opfields empty == 'empty', boolean, pattern matches."""
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

        oper_gnmi = self.jsonIetfVal.replace('5', '""')
        oper_gnmi = oper_gnmi.replace('330', '"true"')
        oper_gnmi = oper_gnmi.replace('17', '"false"')
        oper_gnmi = oper_gnmi.replace('16', '"abc[123]DEFghblahblah"')
        self.jsonIetfVal = oper_gnmi
        self._base64encode()

        resp = self.gnmi.decode_opfields(self.operstate_gnmi['update'])
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

        resp = self.rpcv.process_rpc_reply(oper)
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

    def test_operational_state_boolean_datatype(self):
        """Check opfields with boolean 1, true, 0, and false."""
        oper = self.operstate.replace('5', 'true')
        oper = oper.replace('330', '1')
        oper = oper.replace('17', 'false')
        oper = oper.replace('16', '0')
        opfields = [
            {'selected': 'true',
             'name': 'in-unicast-pkts',
             'xpath': '/interfaces-state/interface/statistics/in-unicast-pkts',
             'value': 'TRUE',
             'datatype': 'boolean',
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
             'value': '0',
             'datatype': 'boolean',
             'op': '=='},
            {'selected': 'true',
             'name': 'out-errors',
             'xpath': '/interfaces-state/interface/statistics/out-errors',
             'value': 'False',
             'datatype': 'boolean',
             'op': '=='}]

        self._base64encode()
        resp = self.rpcv.process_rpc_reply(oper)
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

    def test_operational_state_identityref_datatype(self):
        """Check opfields identityref values."""
        oper = self.operstate.replace('5', 'oc-policy-types:L2VPN')
        oper = oper.replace('330', 'openconfig-policy-types:L2VPN')
        oper = oper.replace('17', 'L2VPN')
        oper = oper.replace('16', 'oc-policy-types:L2VPN')
        opfields = [
            {'selected': 'true',
             'name': 'in-unicast-pkts',
             'xpath': '/interfaces-state/interface/statistics/in-unicast-pkts',
             'value': 'openconfig-policy-types:L2VPN',
             'datatype': 'identityref',
             'op': '=='},
            {'selected': 'true',
             'name': 'in-octets',
             'xpath': '/interfaces-state/interface/statistics/in-octets',
             'value': 'oc-policy-types:L2VPN',
             'datatype': 'identityref',
             'op': '=='},
            {'selected': 'true',
             'name': 'out-discards',
             'xpath': '/interfaces-state/interface/statistics/out-discards',
             'value': 'openconfig-policy-types:L2VPN',
             'datatype': 'identityref',
             'op': '=='},
            {'selected': 'true',
             'name': 'out-errors',
             'xpath': '/interfaces-state/interface/statistics/out-errors',
             'value': 'L2VPN',
             'datatype': 'identityref',
             'op': '=='}]

        self._base64encode()
        resp = self.rpcv.process_rpc_reply(oper)
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

    def test_operational_state_multiple_entries(self):
        """Check verifying one entry exists in a list of multiple entries."""
        opfields = [
            {'selected': 'true',
             'default': '',
             'id': 'somthing unique',
             'name': 'name',
             'xpath': '/native/vrf/definition/name',
             'value': 'mgmt1',
             'datatype': 'string',
             'op': '=='}]
        resp = self.rpcv.process_rpc_reply(multilist)
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

    def test_opfields_selected(self):
        """Check "selected" parameter True or False."""
        opfields_in = [
            {
                'selected': 'true',
                'name': 'name',
                'xpath': '/native/vrf/definition/name',
                'value': 'mgmt1',
                'datatype': 'string',
                'op': '=='
            },
            {
                'selected': 'true',
                'name': 'description',
                'xpath': '/native/vrf/definition/description',
                'value': 'test me',
                'datatype': 'string',
                'op': '=='
            }
        ]
        opfields = opfields_in.copy()
        for select in ['true', 'True', 'TRUE', True]:
            opfields[0]['selected'] = select
            resp = self.rpcv.process_rpc_reply(multilist)
            result = self.rpcv.process_operational_state(resp, opfields)
            self.assertTrue(result, str(select))
            opfields = opfields_in.copy()
        for select in ['false', 'False', 'FALSE', False]:
            opfields[0]['selected'] = select
            resp = self.rpcv.process_rpc_reply(multilist)
            result = self.rpcv.process_operational_state(resp, opfields)
            self.assertTrue(result, str(select))
            opfields = opfields_in.copy()

    def test_auto_validate_list_key(self):
        """List entry with only key should auto-validate the key."""
        rpc_data = {
            'nodes': [
                {
                    'datatype': '',
                    'edit-op': 'create',
                    'nodetype': 'list',
                    'xpath': '/ios:native/ios:router/ios-rip:rip/ios-rip:redistribute/ios-rip:eigrp[ios-rip:as-number="32768"]'
                }
            ]
        }
        resp = self.rpcv.process_rpc_reply(listreply)
        result = self.rpcv.verify_rpc_data_reply(resp, rpc_data)
        self.assertTrue(result)

    def test_auto_validate_delete_list_key_with_defaults(self):
        """Deleted nested list entry expecting parent key in return."""
        rpc_data = {
            'nodes': [
                {
                    'edit-op': 'delete',
                    'nodetype': 'list',
                    'datatype': '',
                    'xpath': '/um-segment-routing-cfg:segment-routing/um-segment-routing-traffic-eng-cfg:traffic-eng/um-segment-routing-traffic-eng-cfg:policies/um-segment-routing-traffic-eng-cfg:policy[um-segment-routing-traffic-eng-cfg:policy-name="genericstring"]/um-segment-routing-traffic-eng-cfg:autoroute/um-segment-routing-traffic-eng-cfg:include/um-segment-routing-traffic-eng-cfg:ipv4s/um-segment-routing-traffic-eng-cfg:ipv4[um-segment-routing-traffic-eng-cfg:address="10.1.1.1"][um-segment-routing-traffic-eng-cfg:length="64"]'
                }
            ]
        }
        rpc_reply = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101">
  <data>
    <segment-routing xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-um-segment-routing-cfg">
      <traffic-eng xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-um-segment-routing-traffic-eng-cfg">
        <policies>
          <policy>
            <policy-name>genericstring</policy-name>
          </policy>
        </policies>
      </traffic-eng>
    </segment-routing>
  </data>
</rpc-reply>"""
        resp = self.rpcv.process_rpc_reply(rpc_reply)
        result = self.rpcv.verify_rpc_data_reply(resp, rpc_data)
        self.assertTrue(result)

    def test_auto_validate_multiple_list_entries(self):
        """Edit-config of multiple list entries in one RPC."""
        rpc_data = {
            'nodes': [
                {
                    'datatype': 'string',
                    'edit-op': 'create',
                    'nodetype': 'leaf',
                    'value': '1234',
                    'xpath': '/ios:native/ios-voice:num-exp[ios-voice:dialled_digit="123"]/ios-voice:dialled_pattern'
                },
                {
                    'datatype': 'string',
                    'edit-op': 'create',
                    'nodetype': 'leaf',
                    'value': '4567',
                    'xpath': '/ios:native/ios-voice:num-exp[ios-voice:dialled_digit="456"]/ios-voice:dialled_pattern'
                }
            ]
        }
        resp = self.rpcv.process_rpc_reply(multientry)
        result = self.rpcv.verify_rpc_data_reply(resp, rpc_data)
        self.assertTrue(result)

    def test_auto_validate_delete_presence_with_children(self):
        """Edit-config of multiple list entries in one RPC."""
        rpc_data = {
            'nodes': [
                {
                    'datatype': '',
                    'edit-op': 'delete',
                    'nodetype': 'container',
                    'xpath': '/um-segment-routing-cfg:segment-routing/um-segment-routing-cfg:global-block'
                },
                {
                    'datatype': 'uint32',
                    'nodetype': 'leaf',
                    'value': '16000',
                    'xpath': '/um-segment-routing-cfg:segment-routing/um-segment-routing-cfg:global-block/um-segment-routing-cfg:lower-bound'
                },
                {
                    'datatype': 'uint32',
                    'nodetype': 'leaf',
                    'value': '16001',
                    'xpath': '/um-segment-routing-cfg:segment-routing/um-segment-routing-cfg:global-block/um-segment-routing-cfg:upper-bound'
                }
            ]
        }
        resp = self.rpcv.process_rpc_reply(no_data_rpc_reply)
        result = self.rpcv.verify_rpc_data_reply(resp, rpc_data)
        self.assertTrue(result)

    def test_auto_validate_delete_nested_list_no_key(self):
        rpc_data = {
            'nodes': [
                {
                    'edit-op': 'delete',
                    'nodetype': 'list',
                    'datatype': '',
                    'xpath': '/um-segment-routing-cfg:segment-routing/um-segment-routing-traffic-eng-cfg:traffic-eng/um-segment-routing-traffic-eng-cfg:policies/um-segment-routing-traffic-eng-cfg:policy[um-segment-routing-traffic-eng-cfg:policy-name="genericstring"]/um-segment-routing-traffic-eng-cfg:autoroute/um-segment-routing-traffic-eng-cfg:include/um-segment-routing-traffic-eng-cfg:ipv4s/um-segment-routing-traffic-eng-cfg:ipv4[um-segment-routing-traffic-eng-cfg:address="10.1.1.1"][um-segment-routing-traffic-eng-cfg:length="64"]'
                }
            ]
        }
        resp = self.rpcv.process_rpc_reply(no_data_rpc_reply)
        result = self.rpcv.verify_rpc_data_reply(resp, rpc_data)
        self.assertTrue(result)

    def test_auto_validate_remove_leaf(self):
        """Test a removed leaf is ok with no data returned."""
        rpc_data = {
            'nodes': [
                {
                    'edit-op': 'remove',
                    'nodetype': 'leaf',
                    'datatype': '',
                    'value': '3',
                    'xpath': '/segment-routing/um-segment-routing-traffic-eng-cfg:traffic-eng/um-segment-routing-traffic-eng-cfg:policies/um-segment-routing-traffic-eng-cfg:policy[um-segment-routing-traffic-eng-cfg:policy-id="1"]/um-segment-routing-traffic-eng-cfg:candidate-paths/um-segment-routing-traffic-eng-cfg:preferences/um-segment-routing-traffic-eng-cfg:preference[um-segment-routing-traffic-eng-cfg:preference-id="2"]/um-segment-routing-traffic-eng-cfg:per-flow/um-segment-routing-traffic-eng-cfg:forward-class/um-segment-routing-traffic-eng-cfg:default'
                }
            ]
        }
        resp = self.rpcv.process_rpc_reply(no_data_rpc_reply)
        result = self.rpcv.verify_rpc_data_reply(resp, rpc_data)
        self.assertTrue(result)


class Device:
    server_capabilities = []


def netconf_send(*args, **kwargs):
    global operstate
    return [('rpc', operstate)]


class TestRpcRun(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.log = log
        cls.cap = ['urn:ietf:params:netconf:capability:with-defaults:1.0?\
basic-mode=explicit&also-supported=report-all-tagged']

    def setUp(self):
        self.format = {
            'auto_validate': True,
            'negative_test': False,
            'pause': 0,
            'timeout': 30
        }
        self.rpc_data = {
            'datastore': 'running',
            'namespace': {'ios': 'http://cisco.com/ns/yang/Cisco-IOS-XE-native',
                        'ios-bgp': 'http://cisco.com/ns/yang/Cisco-IOS-XE-bgp'},
            'nodes': [
                {'datatype': '',
                'edit-op': 'create',
                'nodetype': 'list',
                'xpath': '/ios:native/ios:router/ios-bgp:bgp[ios-bgp:id="100"]/ios-bgp:address-family/ios-bgp:no-vrf/ios-bgp:ipv4[ios-bgp:af-name="unicast"]'}
            ],
            'operation': 'edit-config'
        }
        self.device = Device()
        self.device.server_capabilities = self.cap
        self.returns = [{
            'id': 1,
            'name': 'name',
            'op': '==',
            'selected': True,
            'value': 'genericstring',
            'xpath': '/acl/acl-sets/acl-set/state/name',
        }]
        self.rpc = {'rpc': '<rpc><bad-rpc/></rpc>'}

    def test_auto_validate_off(self):
        """Check if auto_validate False does not try validation."""
        self.format['auto_validate'] = False
        yangexec.netconf_send = netconf_send
        result = yangexec.run_netconf(
            'edit-config',
            self.device,
            None,  # steps
            {},  # datastore
            self.rpc_data,
            self.returns[0],
            format=self.format
        )
        self.assertTrue(result)

    def test_auto_validate_on(self):
        """Check if auto_validate True will try validation."""
        yangexec.netconf_send = netconf_send
        result = yangexec.run_netconf(
            'edit-config',
            self.device,
            None,  # steps
            {},  # datastore
            self.rpc_data,
            self.returns[0],
            format=self.format
        )
        self.assertFalse(result)

    def test_edit_config_negative_test_on(self):
        """Check if edit-config test will pass with failure."""
        self.format['negative_test'] = True
        yangexec.netconf_send = netconf_send
        result = yangexec.run_netconf(
            'edit-config',
            self.device,
            None,  # steps
            {},  # datastore
            self.rpc_data,
            self.returns,
            format=self.format
        )
        self.assertTrue(result)

    def test_get_negative_test_on(self):
        """Check if GET test will pass with failure."""
        self.format['negative_test'] = True
        yangexec.netconf_send = netconf_send
        result = yangexec.run_netconf(
            'get',
            self.device,
            None,  # steps
            {},  # datastore
            self.rpc_data,
            self.returns,
            format=self.format
        )
        self.assertTrue(result)

    def test_pause_on(self):
        """Check if pause 2 seconds operates correctly."""
        self.format['pause'] = 2
        yangexec.netconf_send = netconf_send
        n1 = time()
        log.info('Pausing 2 seconds before edit-config and 2 seconds after get-config')
        yangexec.run_netconf(
            'edit-config',
            self.device,
            None,  # steps
            {},  # datastore
            self.rpc_data,
            self.returns[0],
            format=self.format
        )
        self.assertGreater(time() - n1, 3)

    def test_custom_rpc_bad_xml(self):
        """Send invalid custom RPC and make sure it fails."""
        self.rpc_data['operation'] = 'rpc'
        self.rpc_data['rpc'] = '<top><next>odusrej></next></top>'
        yangexec.netconf_send = netconf_send
        result = yangexec.run_netconf(
            'edit-config',
            self.device,
            None,  # steps
            {},  # datastore
            self.rpc_data,
            self.returns[0],
            format=self.format
        )
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
