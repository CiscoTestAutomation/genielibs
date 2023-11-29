#! /usr/bin/env python
import sys
import unittest
import logging
from time import time, time_ns
import base64
from google.protobuf import json_format
from yang.connector.gnmi import Gnmi
from yang.connector import proto
from genie.libs.sdk.triggers.blitz import yangexec
from genie.libs.sdk.triggers.blitz import netconf_util
from genie.libs.sdk.triggers.blitz.rpcverify import RpcVerify, OptFields
from genie.libs.sdk.triggers.blitz.gnmi_util import GnmiMessage
from genie.libs.sdk.triggers.blitz.tests.device_mocks import TestDevice

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

rpcerror = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" \
xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" \
message-id="urn:uuid:d46bac3e-596e-44d9-a568-d332eb5547bf">
  <rpc-error>
    <error-type>application</error-type>
    <error-tag>invalid-value</error-tag>
    <error-severity>error</error-severity>
    <error-message xml:lang="en"> \
        inconsistent value: Device refused one or more commands</error-message>
    <error-info>
      <severity xmlns="http://cisco.com/yang/cisco-ia">error_cli</severity>
      <detail xmlns="http://cisco.com/yang/cisco-ia">
        <bad-cli>
          <bad-command>router bgp 0</bad-command>
          <error-location>11</error-location>
          <parser-response/>
          <parser-context>router bgp 0</parser-context>
        </bad-cli>
        <bad-cli>
          <bad-command> bgp router-id 30.30.30.3</bad-command>
          <error-location>0</error-location>
          <parser-response/>
          <parser-context>router bgp 0 \
      bgp router-id 30.30.30.3</parser-context>
        </bad-cli>
      </detail>
    </error-info>
  </rpc-error>
</rpc-reply>"""

ocresp = """<rpc-reply message-id="urn:uuid:86affd6b-4eeb-42a4-8b9c-e47a170537fa" \
xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" \
xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
  <data>
    <network-instances xmlns="http://openconfig.net/yang/network-instance">
      <network-instance>
        <name>default</name>
        <protocols>
          <protocol>
            <identifier xmlns:idx="http://openconfig.net/yang/policy-types">idx:BGP</identifier>
            <name>default</name>
            <bgp>
              <global>
                <config>
                  <as>100</as>
                </config>
              </global>
            </bgp>
          </protocol>
        </protocols>
      </network-instance>
    </network-instances>
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

gnmi_leaf_list = {
    "timestamp": 1683062825442372317,
    "update": {
        "path": {
            "origin": "openconfig",
            "elem": [
                {
                "name": "network-instances"
                },
                {
                    "name": "network-instance",
                    "key": {
                        "key": "name",
                        "value": "test10"
                    }
                }
            ]
        },
        "val": {
            "jsonIetfVal": ''
        }
    }
}

gnmi_list_entry = {
    "timestamp": 1694027409978062184,
    "update": {
        "path": {
            "origin": "openconfig",
            "elem": [
                {
                    "name": "sampling"
                },
                {
                    "name": "sflow"
                }
            ]
        },
        "val": {
            "jsonIetfVal": ''
        }
    }
}

gnmi_nested_list = {
    "timestamp": 1694027409978062184,
    "update": {
        "path": {
            "origin": "openconfig",
            "elem": [
                {
                    "name": "network-instances"
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

remove_rpc_reply = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101">
   <data>
    <evpn xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-um-l2vpn-cfg">
     <evis>
      <segment-routing>
       <srv6>
        <evi>
         <vpn-id>32767</vpn-id>
        </evi>
       </srv6>
      </segment-routing>
     </evis>
    </evpn>
   </data>
</rpc-reply>"""

remove_response_fail = """<rpc-reply message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
 <data>
  <l2vpn xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-um-l2vpn-cfg">
   <bridge>
    <groups>
     <group>
      <group-name>BridgeGroup1</group-name>
      <bridge-domains>
       <bridge-domain>
        <bridge-domain-name>BridgeDomain1</bridge-domain-name>
        <neighbors>
         <neighbor>
          <address>10.10.10.10</address>
          <pw-id>1</pw-id>
          <mac>
           <secure>
            <logging/>
           </secure>
          </mac>
         </neighbor>
        </neighbors>
       </bridge-domain>
      </bridge-domains>
     </group>
    </groups>
   </bridge>
  </l2vpn>
 </data>
</rpc-reply>"""

delete_only_one_node_response = """
<rpc-reply xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:bb6fb478-4e27-4826-9fd6-08454515e503">
    <data>
        <network-instances xmlns="http://openconfig.net/yang/network-instance">
            <network-instance>
                <name>DEFAULT</name>
                <protocols>
                    <protocol>
                        <identifier xmlns:idx="http://openconfig.net/yang/policy-types">idx:BGP</identifier>
                        <name>default</name>
                        <bgp>
                            <global>
                                <config>
                                    <as>200</as>
                                </config>
                            </global>
                        </bgp>
                    </protocol>
                </protocols>
            </network-instance>
        </network-instances>
    </data>
</rpc-reply>
"""

list_key_with_forward_slash = """
<rpc-reply xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:bb6fb478-4e27-4826-9fd6-08454515e503">
    <data>
        <network-instances xmlns="http://openconfig.net/yang/network-instance">
            <network-instance>
                <name>1/0/1</name>
                <protocols>
                    <protocol>
                        <identifier xmlns:idx="http://openconfig.net/yang/policy-types">idx:BGP</identifier>
                        <name>default</name>
                        <bgp>
                            <global>
                                <config>
                                    <as>200</as>
                                </config>
                            </global>
                        </bgp>
                    </protocol>
                </protocols>
            </network-instance>
        </network-instances>
    </data>
</rpc-reply>"""

bgp_community_list_get_config_response = """
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:7e4cfd6b-1435-4a06-bd34-9afa39142f2f">
  <data>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <route-map>
        <name>set-community-list</name>
        <route-map-seq xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-route-map">
          <ordering-seq>10</ordering-seq>
          <operation>permit</operation>
          <description>set community to neighbor for edge</description>
          <set>
            <community>
              <community-well-known>
                <community-list>100:6001</community-list>
              </community-well-known>
            </community>
          </set>
        </route-map-seq>
      </route-map>
      <router>
        <bgp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-bgp">
          <id>100</id>
          <address-family>
            <with-vrf>
              <ipv4>
                <af-name>unicast</af-name>
                <vrf>
                  <name>vrf-1</name>
                  <ipv4-unicast>
                    <neighbor>
                      <id>99.5.6.6</id>
                      <route-map>
                        <inout>out</inout>
                        <route-map-name>set-community-list</route-map-name>
                      </route-map>
                    </neighbor>
                  </ipv4-unicast>
                </vrf>
              </ipv4>
            </with-vrf>
          </address-family>
        </bgp>
      </router>
    </native>
  </data>
</rpc-reply>
"""

bgp_community_list_same_parent_response = """
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:e90cbc88-c5b0-4a14-acdc-793c62ff4370">
    <data>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <ip>
          <as-path>
            <access-list xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-bgp">
              <name>100</name>
                <extended-grouping>
                  <extended_grouping>
                    <action>permit</action>
                    <string>_65001$</string>
                  </extended_grouping>
                  <extended_grouping>
                    <action>permit</action>
                    <string>_65002$</string>
                  </extended_grouping>
                  <extended_grouping>
                    <action>permit</action>
                    <string>_65003$</string>
                  </extended_grouping>
              </extended-grouping>
            </access-list>
          </as-path>
        </ip>
      </native>
    </data>
</rpc-reply>
"""

bgp_community_list_namespace_prefix_response = """
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:ed36dbb6-a0bb-4e24-b5d1-974739ac0ad9">
    <data>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <route-map>
          <name>SET_COMMUNITY</name>
          <route-map-seq xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-route-map">
            <ordering-seq>10</ordering-seq>
            <operation>permit</operation>
            <description>Setting Community values</description>
            <set>
              <community>
                <community-well-known>
                  <community-list>100:10</community-list>
                  <community-list>100:20</community-list>
                  <community-list>100:30</community-list>
                  <community-list>100:40</community-list>
                  <community-list>100:200</community-list>
                  <community-list>internet</community-list>
                  <community-list>4465:4000</community-list>
                  <community-list>3000:2222</community-list>
                </community-well-known>
              </community>
            </set>
          </route-map-seq>
        </route-map>
      </native>
    </data>
</rpc-reply>
"""


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
        cls.gnmi_leaf_list = gnmi_leaf_list
        cls.gnmi_list_entry = gnmi_list_entry
        cls.gnmi_nested_list = gnmi_nested_list
        cls.jsonIetfVal = ""
        cls.leafListVal = ""
        cls.listEntryVal = ""
        cls.nestedListEntry = ""

    def setUp(self):
        self.jsonIetfVal = """{"statistics": {"in-octets": 330, \
"in-unicast-pkts": 5, "in-broadcast-pkts": 6, \
"in-multicast-pkts": 7, "in-discards": 8, "in-errors": 9, \
"in-unknown-protos": 10, "out-octets": 11, \
"out-unicast-pkts": 12, "out-broadcast-pkts": 13, \
"out-multicast-pkts": 14, "out-discards": 17, \
"out-errors": 16}}"""
        self.leafListVal = """{"name": "test10",
"inter-instance-policies": {"apply-policy": {"config": {"export-policy": ["policy1"], \
"import-policy": ["policy1", "policy2"]}}}, "config": {"enabled-address-families": ["openconfig-types:IPV4"], \
"name": "test10"}, "state": {"name": "test10", "type": "openconfig-network-instance-types:L3VRF", \
"enabled": true, "enabled-address-families": ["openconfig-types:IPV4", "openconfig-types:IPV6"]}}"""

        self.listEntryVal = """{"config": {"enabled": true, "agent-id-ipv4": "4.4.4.4", \
"agent-id-ipv6": "4::4"}, "collectors": {"collector": [{"address": "6.37.16.200", "port": 2055, \
"config": {"address": "6.37.16.200", "port": 2055}}]}}"""

        self.nestedListEntry = """{"network-instance": [{"name": "DEFAULT", \
"protocols": {"protocol": [{"identifier": "BGP", "name": "default", \
"config": {"identifier": "openconfig-policy-types:BGP", "name": "default"}}]}}]}"""

    def _base64encode(self):
        self.operstate_gnmi['update']['val']['jsonIetfVal'] = base64.encodebytes(
            bytes(self.jsonIetfVal, encoding='utf-8')
        )
        self.gnmi_leaf_list['update']['val']['jsonIetfVal'] = base64.encodebytes(
            bytes(self.leafListVal, encoding='utf-8')
        )
        self.gnmi_list_entry['update']['val']['jsonIetfVal'] = base64.encodebytes(
            bytes(self.listEntryVal, encoding='utf-8')
        )
        self.gnmi_nested_list['update']['val']['jsonIetfVal'] = base64.encodebytes(
            bytes(self.nestedListEntry, encoding='utf-8')
        )

    def parse_dict_to_gnmi_msg(self, data: dict):
        update = proto.gnmi_pb2.Update()
        update = json_format.ParseDict(data, update)
        notification = proto.gnmi_pb2.Notification()
        notification.timestamp = time_ns()
        notification.prefix.MergeFrom(proto.gnmi_pb2.Path())
        notification.update.append(update)

        response = proto.gnmi_pb2.GetResponse()
        response.notification.append(notification)
        return response

    def make_test_args(self, opfields: list):
        format = {
            'encoding': 'JSON',
        }
        rpc_data = {'nodes': [{'xpath': val['xpath'] for val in opfields}]}
        return rpc_data, opfields, format

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
        device = TestDevice(self.parse_dict_to_gnmi_msg(
            self.operstate_gnmi['update']))
        rpc_data, returns, format = self.make_test_args(opfields)

        result = yangexec.run_gnmi('get-config', device, '', '',
                                   rpc_data, returns, format=format)
        # result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

        resp = self.rpcv.process_rpc_reply(operstate)
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

    def test_operational_state_namespace(self):
        """Process rpc-reply with different namespaces."""
        opfields = [
            {'selected': 'true',
             'name': 'name',
             'xpath': '/network-instances/network-instance/name',
             'value': 'default',
             'op': '=='},
            {'selected': 'true',
             'name': 'identifier',
             'xpath': '/network-instances/network-instance/protocols/protocol/identifier',
             'value': 'oc-pol-types:BGP',
             'op': '=='},
            {'selected': 'true',
             'name': 'name',
             'xpath': '/network-instances/network-instance/protocols/protocol/name',
             'value': 'default',
             'op': '=='},
            {'selected': 'true',
             'name': 'as',
             'xpath': '/network-instances/network-instance/protocols/protocol/bgp/global/config/as',
             'value': '100',
             'op': '=='}]

        resp = self.rpcv.process_rpc_reply(ocresp)
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
        device = TestDevice(self.parse_dict_to_gnmi_msg(self.operstate_gnmi['update']))
        rpc_data, returns, format = self.make_test_args(opfields)

        result = yangexec.run_gnmi('get-config', device, '', '',
                                   rpc_data, returns, format=format)
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
        device = TestDevice(self.parse_dict_to_gnmi_msg(self.operstate_gnmi['update']))
        rpc_data, returns, format = self.make_test_args(opfields)

        result = yangexec.run_gnmi('get-config', device, '', '',
                                   rpc_data, returns, format=format)
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
        device = TestDevice(self.parse_dict_to_gnmi_msg(self.operstate_gnmi['update']))
        rpc_data, returns, format = self.make_test_args(opfields)

        result = yangexec.run_gnmi('get-config', device, '', '',
                                   rpc_data, returns, format=format)
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
        device = TestDevice(self.parse_dict_to_gnmi_msg(self.operstate_gnmi['update']))
        rpc_data, returns, format = self.make_test_args(opfields)

        result = yangexec.run_gnmi('get-config', device, '', '',
                                   rpc_data, returns, format=format)
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
        device = TestDevice(self.parse_dict_to_gnmi_msg(self.operstate_gnmi['update']))
        rpc_data, returns, format = self.make_test_args(opfields)

        result = yangexec.run_gnmi('get-config', device, '', '',
                                   rpc_data, returns, format=format)
        self.assertTrue(result)

        resp = self.rpcv.process_rpc_reply(operstate)
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

    def test_operational_state_in_range_negative_num_format(self):
        """Process rpc-reply and check opfield in "n - n" range."""
        oper = self.operstate.replace('330', '-330')
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
             'value': '-400, -300',
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

        oper_gnmi = self.jsonIetfVal.replace('330', '-330')
        self.jsonIetfVal = oper_gnmi
        self._base64encode()
        device = TestDevice(self.parse_dict_to_gnmi_msg(self.operstate_gnmi['update']))
        rpc_data, returns, format = self.make_test_args(opfields)

        result = yangexec.run_gnmi('get-config', device, '', '',
                                   rpc_data, returns, format=format)
        self.assertTrue(result)

        resp = self.rpcv.process_rpc_reply(oper)
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

    def test_operational_state_in_range_swapped(self):
        """Process rpc-reply and check opfield in "n - n" range."""
        oper = self.operstate.replace('330', '-330')
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
             'value': '-300, -400',
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

        oper_gnmi = self.jsonIetfVal.replace('330', '-330')
        self.jsonIetfVal = oper_gnmi
        self._base64encode()
        device = TestDevice(self.parse_dict_to_gnmi_msg(self.operstate_gnmi['update']))
        rpc_data, returns, format = self.make_test_args(opfields)

        result = yangexec.run_gnmi('get-config', device, '', '',
                                   rpc_data, returns, format=format)
        self.assertTrue(result)

        resp = self.rpcv.process_rpc_reply(oper)
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
        device = TestDevice(self.parse_dict_to_gnmi_msg(self.operstate_gnmi['update']))
        rpc_data, returns, format = self.make_test_args(opfields)

        result = yangexec.run_gnmi('get-config', device, '', '',
                                   rpc_data, returns, format=format)
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
        device = TestDevice(self.parse_dict_to_gnmi_msg(self.operstate_gnmi['update']))
        rpc_data, returns, format = self.make_test_args(opfields)

        result = yangexec.run_gnmi('get-config', device, '', '',
                                   rpc_data, returns, format=format)
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
        device = TestDevice(self.parse_dict_to_gnmi_msg(self.operstate_gnmi['update']))
        rpc_data, returns, format = self.make_test_args(opfields)

        result = yangexec.run_gnmi('get-config', device, '', '',
                                   rpc_data, returns, format=format)
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

        device = TestDevice(self.parse_dict_to_gnmi_msg(self.operstate_gnmi['update']))
        rpc_data, returns, format = self.make_test_args(opfields)

        result = yangexec.run_gnmi('get-config', device, '', '',
                                   rpc_data, returns, format=format)
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

        device = TestDevice(self.parse_dict_to_gnmi_msg(self.operstate_gnmi['update']))
        rpc_data, returns, format = self.make_test_args(opfields)

        result = yangexec.run_gnmi('get-config', device, '', '',
                                   rpc_data, returns, format=format)
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

        device = TestDevice(self.parse_dict_to_gnmi_msg(self.operstate_gnmi['update']))
        rpc_data, returns, format = self.make_test_args(opfields)

        result = yangexec.run_gnmi('get-config', device, '', '',
                                   rpc_data, returns, format=format)
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

        device = TestDevice(self.parse_dict_to_gnmi_msg(self.operstate_gnmi['update']))
        rpc_data, returns, format = self.make_test_args(opfields)

        result = yangexec.run_gnmi('get-config', device, '', '',
                                   rpc_data, returns, format=format)
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

        device = TestDevice(self.parse_dict_to_gnmi_msg(self.operstate_gnmi['update']))
        rpc_data, returns, format = self.make_test_args(opfields)

        result = yangexec.run_gnmi('get-config', device, '', '',
                                   rpc_data, returns, format=format)
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

    def test_operational_state_any_operator(self):
        """Check opfields with "any" operator."""
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
             'op': 'any'},
            {'selected': 'true',
             'name': 'in-octets',
             'xpath': '/interfaces-state/interface/statistics/in-octets',
             'value': 'oc-policy-types:L2VPN',
             'datatype': 'identityref',
             'op': 'any'},
            {'selected': 'true',
             'name': 'out-discards',
             'xpath': '/interfaces-state/interface/statistics/out-discards',
             'value': 'openconfig-policy-types:L2VPN',
             'datatype': 'identityref',
             'op': 'any'},
            {'selected': 'true',
             'name': 'out-errors',
             'xpath': '/interfaces-state/interface/statistics/out-errors',
             'value': 'L2VPN',
             'datatype': 'identityref',
             'op': 'any'}]

        self._base64encode()
        resp = self.rpcv.process_rpc_reply(oper)
        result = self.rpcv.process_operational_state(resp, opfields)
        self.assertTrue(result)

    def test_auto_validate_gnmi_leaf_list(self):
        """Check leaf list values in get response"""
        opfields = [
            {
                'selected': 'true',
                'default': '',
                'name': 'import-policy',
                'xpath': '/network-instances/network-instance/inter-instance-policies/apply-policy/config/import-policy',
                'value': 'policy1',
                'datatype': 'leafref',
                'nodetype': 'leaf-list',
                'op': '=='
            },
            {
                'selected': 'true',
                'default': '',
                'name': 'import-policy',
                'xpath': '/network-instances/network-instance/inter-instance-policies/apply-policy/config/import-policy',
                'value': 'policy2',
                'datatype': 'leafref',
                'nodetype': 'leaf-list',
                'op': '=='
            }
        ]
        self._base64encode()
        device = TestDevice(self.parse_dict_to_gnmi_msg(
            self.gnmi_leaf_list['update']))
        rpc_data, returns, format = self.make_test_args(opfields)

        result = yangexec.run_gnmi('get-config', device, '', '',
                                   rpc_data, returns, format=format)
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

    def test_add_key_nodes_without_prefix(self):
        """ Check if we can find the names of the key nodes properly without prefixes """
        xpath = '/network-instances/network-instance[name="DEFAULT"]/protocols/protocol[identifier="ISIS"][name="1"]/isis/levels/level[level-number="2"]/authentication/config/enabled'
        nodes = []
        self.rpcv.add_key_nodes(xpath=xpath, nodes=nodes)
        expected_nodes = [
            OptFields(name='name',
                    value='DEFAULT',
                    xpath='/network-instances/network-instance/name',
                    op='==',
                    default='',
                    selected=True,
                    id='',
                    datatype='',
                    sequence=0,
                    default_xpath='',
                    nodetype='',
                    key=False),
            OptFields(name='identifier',
                    value='ISIS',
                    xpath='/network-instances/network-instance/protocols/protocol/identifier',
                    op='==',
                    default='',
                    selected=True,
                    id='',
                    datatype='',
                    sequence=0,
                    default_xpath='',
                    nodetype='',
                    key=False),
            OptFields(name='name',
                    value='1',
                    xpath='/network-instances/network-instance/protocols/protocol/name',
                    op='==',
                    default='',
                    selected=True,
                    id='',
                    datatype='',
                    sequence=0,
                    default_xpath='',
                    nodetype='',
                    key=False),
            OptFields(name='level-number',
                    value='2',
                    xpath='/network-instances/network-instance/protocols/protocol/isis/levels/level/level-number',
                    op='==',
                    default='',
                    selected=True,
                    id='',
                    datatype='',
                    sequence=0,
                    default_xpath='',
                    nodetype='',
                    key=False)
        ]
        self.assertEqual(nodes, expected_nodes)

    def test_add_key_nodes_with_prefix(self):
        """ Check if we can find the names of the key nodes properly when prefixed """
        xpath = '/network-instances/network-instance[prefix1:name="DEFAULT"]/protocols/protocol[prefix2:identifier="ISIS"][prefix3:name="1"]/isis/levels/level[prefix4:level-number="2"]/authentication/config/enabled'
        nodes = []
        self.rpcv.add_key_nodes(xpath=xpath, nodes=nodes)
        expected_nodes = [
            OptFields(name='name',
                    value='DEFAULT',
                    xpath='/network-instances/network-instance/name',
                    op='==',
                    default='',
                    selected=True,
                    id='',
                    datatype='',
                    sequence=0,
                    default_xpath='',
                    nodetype='',
                    key=False),
            OptFields(name='identifier',
                    value='ISIS',
                    xpath='/network-instances/network-instance/protocols/protocol/identifier',
                    op='==',
                    default='',
                    selected=True,
                    id='',
                    datatype='',
                    sequence=0,
                    default_xpath='',
                    nodetype='',
                    key=False),
            OptFields(name='name',
                    value='1',
                    xpath='/network-instances/network-instance/protocols/protocol/name',
                    op='==',
                    default='',
                    selected=True,
                    id='',
                    datatype='',
                    sequence=0,
                    default_xpath='',
                    nodetype='',
                    key=False),
            OptFields(name='level-number',
                    value='2',
                    xpath='/network-instances/network-instance/protocols/protocol/isis/levels/level/level-number',
                    op='==',
                    default='',
                    selected=True,
                    id='',
                    datatype='',
                    sequence=0,
                    default_xpath='',
                    nodetype='',
                    key=False)
        ]
        self.assertEqual(nodes, expected_nodes)

    def test_add_key_nodes_invalid_name(self):
        """ Check if we catch invalid key names in xpath keys """
        xpath = '/network-instances/network-instance["DEFAULT"]'
        nodes = []
        with self.assertRaisesRegex(ValueError,
                                    r'Unable to find key name in xpath '
                                    r'/network-instances/network-instance\["DEFAULT"] for key \["DEFAULT"]'):
            self.rpcv.add_key_nodes(xpath=xpath, nodes=nodes)

    def test_add_key_nodes_invalid_value(self):
        """ Check if we catch invalid value from the xpath key """
        xpath = '/network-instances/network-instance[name=]'
        nodes = []
        with self.assertRaisesRegex(ValueError,
                                    r'Unable to find value in xpath '
                                    r'/network-instances/network-instance\[name=] for key \[name=]'):
            self.rpcv.add_key_nodes(xpath=xpath, nodes=nodes)

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

    def test_auto_validate_remove_only_one_leaf(self):
        """Test a remove operation only on one leaf with data returned"""
        rpc_data = {
            'nodes' : [
                {
                    'datatype': 'uint32', 
                    'nodetype': 'leaf', 
                    'value': '200',
                    'xpath': '/oc-netinst:network-instances/oc-netinst:network-instance[oc-netinst:name="DEFAULT"]/oc-netinst:protocols/oc-netinst:protocol[oc-netinst:identifier="oc-pol-types:BGP"][oc-netinst:name="default"]/oc-netinst:bgp/oc-netinst:global/oc-netinst:config/oc-netinst:as'
                }, 
                {
                    'datatype': 'boolean', 
                    'edit-op': 'delete', 
                    'nodetype': 'leaf', 
                    'value': 'true', 
                    'xpath': '/oc-netinst:network-instances/oc-netinst:network-instance[oc-netinst:name="DEFAULT"]/oc-netinst:protocols/oc-netinst:protocol[oc-netinst:identifier="oc-pol-types:BGP"][oc-netinst:name="default"]/oc-netinst:bgp/oc-netinst:global/oc-netinst:graceful-restart/oc-netinst:config/oc-netinst:enabled'
                }
            ],
            'datastore' : 'candidate',
            'operation': 'edit-config',
        }
        resp = self.rpcv.process_rpc_reply(delete_only_one_node_response)
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

    def test_auto_validate_operation_remove_leaf(self):
        """Test a remove operation on a leaf node with data returned."""
        rpc_data = {
            'nodes': [
                {
                    'edit-op': 'remove',
                    'nodetype': 'leaf',
                    'datatype': 'string',
                    'value': 'Setting vpn-id',
                    'xpath': '/evpn/evis/segment-routing/srv6/evi[vpn-id=32767]/description'
                }
            ]
        }
        resp = self.rpcv.process_rpc_reply(remove_rpc_reply)
        result = self.rpcv.verify_rpc_data_reply(resp, rpc_data)
        self.assertTrue(result)

    def test_auto_validate_operation_remove_fail(self):
        """Test for the failed remove operation on a node."""
        rpc_data = {
                'nodes': [
                    {
                        'edit-op': 'remove',
                        'nodetype': 'container',
                        'datatype': '',
                        'value': '',
                        'xpath': '/l2vpn/bridge/groups/group[group-name="BridgeGroup1"]/bridge-domains/bridge-domain[bridge-domain-name="BridgeDomain1"]/neighbors/neighbor[address="10.10.10.10"][pw-id=1]/mac/secure'
                    }
                ]
        }
        resp = self.rpcv.process_rpc_reply(remove_response_fail)
        result = self.rpcv.verify_rpc_data_reply(resp, rpc_data)
        self.assertFalse(result)

    def test_auto_validate_list_key_with_forward_slash(self):
        """Test key values with forward slash"""
        rpc_data = {
            'nodes' : [
                {
                    'datatype': 'uint32',
                    'nodetype': 'leaf',
                    'value': '200',
                    'xpath': '/oc-netinst:network-instances/oc-netinst:network-instance[oc-netinst:name="1/0/1"]/oc-netinst:protocols/oc-netinst:protocol[oc-netinst:identifier="oc-pol-types:BGP"][oc-netinst:name="default"]/oc-netinst:bgp/oc-netinst:global/oc-netinst:config/oc-netinst:as'
                },
            ],
            'datastore' : 'candidate',
            'operation': 'edit-config',
        }
        resp = self.rpcv.process_rpc_reply(list_key_with_forward_slash)
        result = self.rpcv.verify_rpc_data_reply(resp, rpc_data)
        self.assertTrue(result)

    def test_auto_validate_without_key_prefix(self):
        rpc_data = {
            "namespace": {
                "ios": "http://cisco.com/ns/yang/Cisco-IOS-XE-native",
                "ios-bgp": "http://cisco.com/ns/yang/Cisco-IOS-XE-bgp",
                "ios-route-map": "http://cisco.com/ns/yang/Cisco-IOS-XE-route-map"
            },
            "nodes": [
                {
                "datatype": "",
                "default": "",
                "edit-op": "create",
                "nodetype": "list",
                "value": "",
                "xpath": "/ios:native/ios:route-map[name=\"set-community-list\"]"
                },
                {
                "datatype": "string",
                "default": "",
                "edit-op": "",
                "nodetype": "leaf",
                "value": "",
                "xpath": "/ios:native/ios:route-map[name=\"set-community-list\"]/ios-route-map:route-map-seq[ios-route-map:ordering-seq=\"10\"]"
                }
            ],
            "datastore": "running",
            "operation": "edit-config"
        }
        resp = self.rpcv.process_rpc_reply(bgp_community_list_get_config_response)
        result = self.rpcv.verify_rpc_data_reply(resp, rpc_data)
        self.assertTrue(result)

    def test_auto_validate_with_key_prefix(self):
        rpc_data = {
            "namespace": {
                "ios": "http://cisco.com/ns/yang/Cisco-IOS-XE-native",
                "ios-bgp": "http://cisco.com/ns/yang/Cisco-IOS-XE-bgp",
                "ios-route-map": "http://cisco.com/ns/yang/Cisco-IOS-XE-route-map"
            },
            "nodes": [
                {
                "datatype": "",
                "default": "",
                "edit-op": "create",
                "nodetype": "list",
                "value": "",
                "xpath": "/ios:native/ios:route-map[ios:name=\"set-community-list\"]"
                },
                {
                "datatype": "string",
                "default": "",
                "edit-op": "",
                "nodetype": "leaf",
                "value": "",
                "xpath": "/ios:native/ios:route-map[ios:name=\"set-community-list\"]/ios-route-map:route-map-seq[ios-route-map:ordering-seq=\"10\"]"
                }
            ],
            "datastore": "running",
            "operation": "edit-config"
        }
        resp = self.rpcv.process_rpc_reply(bgp_community_list_get_config_response)
        result = self.rpcv.verify_rpc_data_reply(resp, rpc_data)
        self.assertTrue(result)

    def test_auto_validate_without_space_in_key_content(self):
        rpc_data = {
            'namespace': {
                'ios': 'http://cisco.com/ns/yang/Cisco-IOS-XE-native',
                'ios-bgp': 'http://cisco.com/ns/yang/Cisco-IOS-XE-bgp',
                'ios-route-map': 'http://cisco.com/ns/yang/Cisco-IOS-XE-route-map'
            },
            'nodes': [
                {
                'datatype': '',
                'default': '',
                'edit-op': 'create',
                'nodetype': 'list',
                'value': '',
                'xpath': '/ios:native/ios:route-map[ios:name="set-community-list"]'
                },
                {
                'datatype': 'string',
                'default': '',
                'edit-op': '',
                'nodetype': 'leaf',
                'value': '',
                'xpath': '/ios:native/ios:route-map[ios:name="set-community-list"]/ios-route-map:route-map-seq[ios-route-map:ordering-seq="10"]'
                }
            ],
            'datastore': 'running',
            'operation': 'edit-config'
        }
        resp = self.rpcv.process_rpc_reply(bgp_community_list_get_config_response)
        result = self.rpcv.verify_rpc_data_reply(resp, rpc_data)
        self.assertTrue(result)

    def test_auto_validate_with_space_in_key_content(self):
        rpc_data = {
            'namespace': {
                'ios': 'http://cisco.com/ns/yang/Cisco-IOS-XE-native',
                'ios-bgp': 'http://cisco.com/ns/yang/Cisco-IOS-XE-bgp',
                'ios-route-map': 'http://cisco.com/ns/yang/Cisco-IOS-XE-route-map'
            },
            'nodes': [
                {
                'datatype': '',
                'default': '',
                'edit-op': 'create',
                'nodetype': 'list',
                'value': '',
                'xpath': '/ios:native/ios:route-map[ios:name="  set-community-list "]'
                },
                {
                'datatype': 'string',
                'default': '',
                'edit-op': '',
                'nodetype': 'leaf',
                'value': '',
                'xpath': '/ios:native/ios:route-map[ios:name=" set-community-list  "]/ios-route-map:route-map-seq[ios-route-map:ordering-seq="  10  "]'
                }
            ],
            'datastore': 'running',
            'operation': 'edit-config'
        }
        resp = self.rpcv.process_rpc_reply(bgp_community_list_get_config_response)
        result = self.rpcv.verify_rpc_data_reply(resp, rpc_data)
        self.assertTrue(result)

    def test_auto_validate_with_same_parent_key(self):
        rpc_data = {
            'namespace': {
                'ios': 'http://cisco.com/ns/yang/Cisco-IOS-XE-native',
                'ios-bgp': 'http://cisco.com/ns/yang/Cisco-IOS-XE-bgp'
            },
            'nodes': [
                {
                'datatype': 'string',
                'default': '',
                'edit-op': '',
                'nodetype': 'leaf',
                'value': '',
                'xpath': '/ios:native/ios:ip/ios:as-path/ios-bgp:access-list[ios-bgp:name=100]/ios-bgp:extended-grouping/ios-bgp:extended_grouping[ios-bgp:action="permit"][ios-bgp:string="_65001$"]'
                },
                {
                'datatype': 'string',
                'default': '',
                'edit-op': '',
                'nodetype': 'leaf',
                'value': '',
                'xpath': '/ios:native/ios:ip/ios:as-path/ios-bgp:access-list[ios-bgp:name=100]/ios-bgp:extended-grouping/ios-bgp:extended_grouping[ios-bgp:action="permit"][ios-bgp:string="_65002$"]'
                },
                {
                'datatype': 'string',
                'default': '',
                'edit-op': '',
                'nodetype': 'leaf',
                'value': '',
                'xpath': '/ios:native/ios:ip/ios:as-path/ios-bgp:access-list[ios-bgp:name=100]/ios-bgp:extended-grouping/ios-bgp:extended_grouping[ios-bgp:action="permit"][ios-bgp:string="_65003$"]'
                }
            ],
            'datastore': 'running',
            'operation': 'edit-config'
        }
        resp = self.rpcv.process_rpc_reply(bgp_community_list_same_parent_response)
        result = self.rpcv.verify_rpc_data_reply(resp, rpc_data)
        self.assertTrue(result)

    def test_autovalidate_list_entry(self):
        """check list entry enclosed in [] in response"""
        opfields = [
            {
                'selected': 'true',
                'default': '',
                'name': 'address',
                'xpath': '/sampling/sflow/collectors/collector/config/address',
                'value': '6.37.16.200',
                'datatype': 'oc-inet:ip-address',
                'nodetype': 'leaf',
                'op': '=='
            },
            {
                'selected': 'true',
                'default': '',
                'name': 'port',
                'xpath': '/sampling/sflow/collectors/collector/config/port',
                'value': 2055,
                'datatype': 'oc-inet:port-number',
                'nodetype': 'leaf',
                'op': '=='
            }
        ]
        self._base64encode()
        device = TestDevice(self.parse_dict_to_gnmi_msg(
            self.gnmi_list_entry['update']))
        rpc_data, returns, format = self.make_test_args(opfields)

        result = yangexec.run_gnmi('get-config', device, '', '',
                                   rpc_data, returns, format=format)
        self.assertTrue(result)

    def test_autovalidate_nested_list(self):
        """check nested list entry enclosed in brackets"""
        opfields = [
            {
                'selected': 'true',
                'default': '',
                'name': 'identifier',
                'xpath': '/network-instances/network-instance/protocols/protocol/config/identifier',
                'value': 'oc-pol-types:BGP',
                'datatype': 'identityref',
                'nodetype': 'leaf',
                'op': '=='
            },
            {
                'selected': 'true',
                'default': '',
                'name': 'name',
                'xpath': '/network-instances/network-instance/protocols/protocol/config/name',
                'value': 'default',
                'datatype': 'string',
                'nodetype': 'leaf',
                'op': '=='
            }
        ]
        self._base64encode()
        device = TestDevice(self.parse_dict_to_gnmi_msg(
            self.gnmi_nested_list['update']))
        rpc_data, returns, format = self.make_test_args(opfields)

        result = yangexec.run_gnmi('get-config', device, '', '',
                                   rpc_data, returns, format=format)
        self.assertTrue(result)

    def test_auto_validate_with_namespace_prefix_without_key(self):
        rpc_data = {
            'namespace': {
                'ios': 'http: //cisco.com/ns/yang/Cisco-IOS-XE-native',
                'ios-bgp': 'http://cisco.com/ns/yang/Cisco-IOS-XE-bgp',
                'ios-route-map': 'http://cisco.com/ns/yang/Cisco-IOS-XE-route-map'
            },
            'nodes': [{
                'datatype': 'string',
                'default': '',
                'edit-op': 'create',
                'nodetype': 'leaf',
                'value': '',
                'xpath': '/ios:native/ios:route-map[name="SET_COMMUNITY"]'
            }, {
                'datatype': 'string',
                'default': '',
                'edit-op': 'merge',
                'nodetype': 'leaf',
                'value': '',
                'xpath': '/ios:native/ios:route-map[name="SET_COMMUNITY"]/ios-route-map:route-map-seq[ordering-seq="10"]'
            }, {
                'datatype': 'enumeration',
                'default': '',
                'edit-op': 'merge',
                'nodetype': 'leaf',
                'value': 'permit',
                'xpath': '/ios:native/ios:route-map[name="SET_COMMUNITY"]/ios-route-map:route-map-seq[ordering-seq="10"]/ios-route-map:operation'
            }, {
                'datatype': 'string',
                'default': '',
                'edit-op': 'merge',
                'nodetype': 'leaf',
                'value': 'Setting Community values',
                'xpath': '/ios:native/ios:route-map[name="SET_COMMUNITY"]/ios-route-map:route-map-seq[ordering-seq="10"]/ios-route-map:description'
            }, {
                'datatype': 'string',
                'default': '',
                'edit-op': 'merge',
                'nodetype': 'leaf-list',
                'value': '100:10',
                'xpath': '/ios:native/ios:route-map[name="SET_COMMUNITY"]/ios-route-map:route-map-seq[ordering-seq="10"]/ios-route-map:set/ios-route-map:community/ios-route-map:community-well-known/ios-route-map:community-list'
            }, {
                'datatype': 'string',
                'default': '',
                'edit-op': 'merge',
                'nodetype': 'leaf-list',
                'value': '100:20',
                'xpath': '/ios:native/ios:route-map[name="SET_COMMUNITY"]/ios-route-map:route-map-seq[ordering-seq="10"]/ios-route-map:set/ios-route-map:community/ios-route-map:community-well-known/ios-route-map:community-list'
            }, {
                'datatype': 'union',
                'default': '',
                'edit-op': 'merge',
                'nodetype': 'leaf-list',
                'value': '100:30',
                'xpath': '/ios:native/ios:route-map[name="SET_COMMUNITY"]/ios-route-map:route-map-seq[ordering-seq="10"]/ios-route-map:set/ios-route-map:community/ios-route-map:community-well-known/ios-route-map:community-list'
            }, {
                'datatype': 'union',
                'default': '',
                'edit-op': 'merge',
                'nodetype': 'leaf-list',
                'value': '100:40',
                'xpath': '/ios:native/ios:route-map[name="SET_COMMUNITY"]/ios-route-map:route-map-seq[ordering-seq="10"]/ios-route-map:set/ios-route-map:community/ios-route-map:community-well-known/ios-route-map:community-list'
            }, {
                'datatype': 'union',
                'default': '',
                'edit-op': 'merge',
                'nodetype': 'leaf-list',
                'value': '100:200',
                'xpath': '/ios:native/ios:route-map[name="SET_COMMUNITY"]/ios-route-map:route-map-seq[ordering-seq="10"]/ios-route-map:set/ios-route-map:community/ios-route-map:community-well-known/ios-route-map:community-list'
            }, {
                'datatype': 'union',
                'default': '',
                'edit-op': 'merge',
                'nodetype': 'leaf-list',
                'value': 'internet',
                'xpath': '/ios:native/ios:route-map[name="SET_COMMUNITY"]/ios-route-map:route-map-seq[ordering-seq="10"]/ios-route-map:set/ios-route-map:community/ios-route-map:community-well-known/ios-route-map:community-list'
            }, {
                'datatype': 'union',
                'default': '',
                'edit-op': 'merge',
                'nodetype': 'leaf-list',
                'value': '4465:4000',
                'xpath': '/ios:native/ios:route-map[name="SET_COMMUNITY"]/ios-route-map:route-map-seq[ordering-seq="10"]/ios-route-map:set/ios-route-map:community/ios-route-map:community-well-known/ios-route-map:community-list'
            }, {
                'datatype': 'union',
                'default': '',
                'edit-op': 'merge',
                'nodetype': 'leaf-list',
                'value': '3000:2222',
                'xpath': '/ios:native/ios:route-map[name="SET_COMMUNITY"]/ios-route-map:route-map-seq[ordering-seq="10"]/ios-route-map:set/ios-route-map:community/ios-route-map:community-well-known/ios-route-map:community-list'
            }],
            'datastore': 'running',
            'operation': 'edit-config'
        }
        resp = self.rpcv.process_rpc_reply(bgp_community_list_namespace_prefix_response)
        result = self.rpcv.verify_rpc_data_reply(resp, rpc_data)
        self.assertTrue(result)

    def test_auto_validate_with_namespace_prefix_with_key(self):
        rpc_data = {
            'namespace': {
                'ios': 'http: //cisco.com/ns/yang/Cisco-IOS-XE-native',
                'ios-bgp': 'http://cisco.com/ns/yang/Cisco-IOS-XE-bgp',
                'ios-route-map': 'http://cisco.com/ns/yang/Cisco-IOS-XE-route-map'
            },
            'nodes': [{
                'datatype': 'string',
                'default': '',
                'edit-op': 'create',
                'nodetype': 'leaf',
                'value': '',
                'xpath': '/ios:native/ios:route-map[ios:name="SET_COMMUNITY"]'
            }, {
                'datatype': 'string',
                'default': '',
                'edit-op': 'merge',
                'nodetype': 'leaf',
                'value': '',
                'xpath': '/ios:native/ios:route-map[ios:name="SET_COMMUNITY"]/ios-route-map:route-map-seq[ios-route-map:ordering-seq="10"]'
            }, {
                'datatype': 'enumeration',
                'default': '',
                'edit-op': 'merge',
                'nodetype': 'leaf',
                'value': 'permit',
                'xpath': '/ios:native/ios:route-map[ios:name="SET_COMMUNITY"]/ios-route-map:route-map-seq[ios-route-map:ordering-seq="10"]/ios-route-map:operation'
            }, {
                'datatype': 'string',
                'default': '',
                'edit-op': 'merge',
                'nodetype': 'leaf',
                'value': 'Setting Community values',
                'xpath': '/ios:native/ios:route-map[ios:name="SET_COMMUNITY"]/ios-route-map:route-map-seq[ios-route-map:ordering-seq="10"]/ios-route-map:description'
            }, {
                'datatype': 'string',
                'default': '',
                'edit-op': 'merge',
                'nodetype': 'leaf-list',
                'value': '100:10',
                'xpath': '/ios:native/ios:route-map[ios:name="SET_COMMUNITY"]/ios-route-map:route-map-seq[ios-route-map:ordering-seq="10"]/ios-route-map:set/ios-route-map:community/ios-route-map:community-well-known/ios-route-map:community-list'
            }, {
                'datatype': 'string',
                'default': '',
                'edit-op': 'merge',
                'nodetype': 'leaf-list',
                'value': '100:20',
                'xpath': '/ios:native/ios:route-map[ios:name="SET_COMMUNITY"]/ios-route-map:route-map-seq[ios-route-map:ordering-seq="10"]/ios-route-map:set/ios-route-map:community/ios-route-map:community-well-known/ios-route-map:community-list'
            }, {
                'datatype': 'union',
                'default': '',
                'edit-op': 'merge',
                'nodetype': 'leaf-list',
                'value': '100:30',
                'xpath': '/ios:native/ios:route-map[ios:name="SET_COMMUNITY"]/ios-route-map:route-map-seq[ios-route-map:ordering-seq="10"]/ios-route-map:set/ios-route-map:community/ios-route-map:community-well-known/ios-route-map:community-list'
            }, {
                'datatype': 'union',
                'default': '',
                'edit-op': 'merge',
                'nodetype': 'leaf-list',
                'value': '100:40',
                'xpath': '/ios:native/ios:route-map[ios:name="SET_COMMUNITY"]/ios-route-map:route-map-seq[ios-route-map:ordering-seq="10"]/ios-route-map:set/ios-route-map:community/ios-route-map:community-well-known/ios-route-map:community-list'
            }, {
                'datatype': 'union',
                'default': '',
                'edit-op': 'merge',
                'nodetype': 'leaf-list',
                'value': '100:200',
                'xpath': '/ios:native/ios:route-map[ios:name="SET_COMMUNITY"]/ios-route-map:route-map-seq[ios-route-map:ordering-seq="10"]/ios-route-map:set/ios-route-map:community/ios-route-map:community-well-known/ios-route-map:community-list'
            }, {
                'datatype': 'union',
                'default': '',
                'edit-op': 'merge',
                'nodetype': 'leaf-list',
                'value': 'internet',
                'xpath': '/ios:native/ios:route-map[ios:name="SET_COMMUNITY"]/ios-route-map:route-map-seq[ios-route-map:ordering-seq="10"]/ios-route-map:set/ios-route-map:community/ios-route-map:community-well-known/ios-route-map:community-list'
            }, {
                'datatype': 'union',
                'default': '',
                'edit-op': 'merge',
                'nodetype': 'leaf-list',
                'value': '4465:4000',
                'xpath': '/ios:native/ios:route-map[ios:name="SET_COMMUNITY"]/ios-route-map:route-map-seq[ios-route-map:ordering-seq="10"]/ios-route-map:set/ios-route-map:community/ios-route-map:community-well-known/ios-route-map:community-list'
            }, {
                'datatype': 'union',
                'default': '',
                'edit-op': 'merge',
                'nodetype': 'leaf-list',
                'value': '3000:2222',
                'xpath': '/ios:native/ios:route-map[ios:name="SET_COMMUNITY"]/ios-route-map:route-map-seq[ios-route-map:ordering-seq="10"]/ios-route-map:set/ios-route-map:community/ios-route-map:community-well-known/ios-route-map:community-list'
            }],
            'datastore': 'running',
            'operation': 'edit-config'
        }
        resp = self.rpcv.process_rpc_reply(bgp_community_list_namespace_prefix_response)
        result = self.rpcv.verify_rpc_data_reply(resp, rpc_data)
        self.assertTrue(result)


class Device:
    server_capabilities = []

    def connect(self, *args, **kwargs):
        pass

    def get_config(self, *args, **kwargs):
        return NetconfResponse()

    def get(self, *args, **kwargs):
        return NetconfResponse()

    def edit_config(self, *args, **kwargs):
        return NetconfResponse()


class ErrorDevice(Device):

    def get_config(self, *args, **kwargs):
        return NetconfErrorResponse()

    def get(self, *args, **kwargs):
        return NetconfErrorResponse()

    def edit_config(self, *args, **kwargs):
        return NetconfErrorResponse()


class NetconfResponse:
    def __init__(self):
        self.ok = True

    def __str__(self) -> str:
        global operstate
        return operstate


class NetconfErrorResponse(NetconfResponse):

    def __str__(self) -> str:
        global rpcerror
        return rpcerror


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

    def test_auto_validate_on(self):
        """Check if auto_validate True will try validation."""
        result = yangexec.run_netconf(
            'edit-config',
            self.device,
            None,  # steps
            {},  # datastore
            self.rpc_data,
            self.returns,
            format=self.format
        )
        self.assertFalse(result)

    def test_edit_config_negative_test_on(self):
        """Check if edit-config test will pass with failure."""
        self.format['negative_test'] = True
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

    def test_edit_negative_test_error(self):
        """Check if edit test returns correct error."""
        self.format['negative_test'] = True
        self.format['auto_validate'] = False
        device = ErrorDevice()
        rpc_data = {
            'datastore': 'running',
            'namespace': {'ios': 'http://cisco.com/ns/yang/Cisco-IOS-XE-native',
                        'ios-bgp': 'http://cisco.com/ns/yang/Cisco-IOS-XE-bgp'},
            'nodes': [
                {'datatype': 'string',
                 'edit-op': 'create',
                 'nodetype': 'leaf',
                 'xpath': '/ios:native/ios:router/ios-bgp:bgp[ios-bgp:id="0"]/ios-bgp:bgp/ios-bgp:router-id/ios-bgp:ip-id',
                 'value': '30.30.30.3'}
            ],
            'operation': 'edit-config'
        }
        returns = [{
            'id': 1,
            'name': 'error-tag',
            'op': '==',
            'selected': True,
            'value': 'invalid-value',
            'xpath': '/rpc-reply/rpc-error/error-tag',
        }]
        result = yangexec.run_netconf(
            'edit-config',
            device,
            None, # steps
            {}, # datastore
            rpc_data,
            returns,
            format=self.format)
        self.assertTrue(result)

    def test_edit_negative_error_fail(self):
        """Check for the failed case of error check."""
        self.format['negative_test'] = True
        self.format['auto_validate'] = False
        device = ErrorDevice()
        rpc_data = {
            'datastore': 'running',
            'namespace': {'ios': 'http://cisco.com/ns/yang/Cisco-IOS-XE-native',
                        'ios-bgp': 'http://cisco.com/ns/yang/Cisco-IOS-XE-bgp'},
            'nodes': [
                {'datatype': 'string',
                 'edit-op': 'create',
                 'nodetype': 'leaf',
                 'xpath': '/ios:native/ios:router/ios-bgp:bgp[ios-bgp:id="0"]/ios-bgp:bgp/ios-bgp:router-id/ios-bgp:ip-id',
                 'value': '30.30.30.3'}
            ],
            'operation': 'edit-config'
        }
        returns = [{
            'id': 1,
            'name': 'error-tag',
            'op': '==',
            'selected': True,
            'value': 'data-exists',
            'xpath': '/rpc-reply/rpc-error/error-tag',
        }]
        result = yangexec.run_netconf(
            'edit-config',
            device,
            None, # steps
            {}, # datastore
            rpc_data,
            returns,
            format=self.format)
        self.assertFalse(result)

    def test_pause_on(self):
        """Check if pause 2 seconds operates correctly."""
        self.format['pause'] = 2
        n1 = time()
        log.info('Pausing 2 seconds before edit-config and 2 seconds after get-config')
        yangexec.run_netconf(
            'edit-config',
            self.device,
            None,  # steps
            {},  # datastore
            self.rpc_data,
            self.returns,
            format=self.format
        )
        self.assertGreater(time() - n1, 3)

    def test_custom_rpc_bad_xml(self):
        """Send invalid custom RPC and make sure it fails."""
        self.rpc_data['operation'] = 'rpc'
        self.rpc_data['rpc'] = '<top><next>odusrej></next></top>'
        result = yangexec.run_netconf(
            'edit-config',
            self.device,
            None,  # steps
            {},  # datastore
            self.rpc_data,
            self.returns,
            format=self.format
        )
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
