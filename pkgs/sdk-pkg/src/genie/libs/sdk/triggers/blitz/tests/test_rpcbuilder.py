#! /usr/bin/env python
import sys
import unittest
import logging
import os.path
import lxml.etree as et

from genie.libs.sdk.triggers.blitz.rpcverify import RpcVerify
from genie.libs.sdk.triggers.blitz.rpcbuilder import YSNetconfRPCBuilder, RpcInputError


# TODO: Needs to be part of genielibs test run

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


class TestNetconfRPCBuilder(unittest.TestCase):
    """Test cases for the YSNetconfRPCBuilder class."""

    basedir = os.path.join(os.path.dirname(__file__), 'data')

    @classmethod
    def setUpClass(cls):

        cls.nsmap = {
            'ocif': "http://openconfig.net/yang/interfaces",
            'ianaift': "urn:ietf:params:xml:ns:yang:iana-if-type",
            'eth': "http://openconfig.net/yang/interfaces/ethernet",
            'cisco-ia': "http://cisco.com/yang/cisco-ia",
            'aaa': "http://cisco.com/ns/yang/Cisco-IOS-XR-aaa-lib-cfg",
            'ocni': "http://openconfig.net/yang/network-instance",
            'oc-pol-types': "http://openconfig.net/yang/policy-types",
        }
        cls.maxDiff = None

    def setUp(self):
        """Initialization for each test case."""
        self.rpcbld = YSNetconfRPCBuilder(prefix_namespaces="always",
                                          nsmap=self.nsmap)
        self.rpcbld_minimal = YSNetconfRPCBuilder(prefix_namespaces="minimal",
                                                  nsmap=self.nsmap)

    def test_init_negative(self):
        """Negative tests for initialization."""
        self.assertRaises(ValueError, YSNetconfRPCBuilder,
                          prefix_namespaces="invalid")

    def test_get_payload(self):
        """Test the YSNetconfRPCBuilder.get_payload() instance method."""
        cfgs = [{
            "xpath": "/ocif:interfaces/ocif:interface/ocif:name",
            "value": "eth0",
        }]
        payload = self.rpcbld.get_payload(cfgs, et.Element("x"))

        # get_payload returns an Element tree.
        xml = et.tostring(payload, encoding='unicode', pretty_print=True)
        self.assertEqual("""\
<x>
  <ocif:interfaces xmlns:ocif="http://openconfig.net/yang/interfaces">
    <ocif:interface>
      <ocif:name>eth0</ocif:name>
    </ocif:interface>
  </ocif:interfaces>
</x>
""", xml)

        payload_min = self.rpcbld_minimal.get_payload(cfgs, et.Element('x'))
        # get_payload returns an Element tree.
        xml_min = et.tostring(payload_min, encoding='unicode',
                              pretty_print=True)
        self.assertEqual("""\
<x>
  <interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
      <name>eth0</name>
    </interface>
  </interfaces>
</x>
""", xml_min)

    def test_get_payload_negative(self):
        """Test get_payload() with invalid inputs.

        Note that some of these are valid XPaths; they simply do not
        fall within the scope of schema node identifiers currently supported.
        """
        cfgs = [
            {
                # Only absolute XPaths supported presently
                "xpath": "a/relative/xpath",
            }, {
                # Unknown namespace prefix 'foo' on intermediate node
                "xpath": "/ocif:interfaces/foo:bar/ocif:name",
            }, {
                # Unknown namespace prefix 'foo' on leaf node
                "xpath": "/ocif:interfaces/ocif:interface/foo:name",
            }, {
                # Missing segment between //
                "xpath": "/ocif:interfaces//ocif:name",
            }, {
                # Trailing slash
                "xpath": "/ocif:interfaces/",
                "value": "100",
            }, {
                # Need at least one segment
                "xpath": "/",
                "value": "100",
            }, {
                # Prefix missing localname
                "xpath": "/ocif:/ocif:bar",
            }, {
                # Localname missing prefix
                "xpath": "/:bar/ocif:bar",
            }, {
                # Missing : separator
                "xpath": "/ocifinterfaces/ocif:name",
            }, {
                # Extra : separator
                "xpath": "/ocif:interfaces/ocif::name",
            }, {
                # Unknown prefix on list key
                "xpath": '/ocif:interfaces/ocif:interface[foo:bar="baz"]',
            }, {
                # Malformed list key
                "xpath": '/ocif:interfaces/ocif:interface[foo',
            }, {
                # Another malformed list key
                "xpath": '/ocif:interfaces/ocif:interface[foo="bar"][baz="',
            }, {
                # Malformed xml_value
                "xpath": "/ocif:foo/ocif:bar",
                "xml_value": "<foo",
            },
        ]
        for cfg in cfgs:
            payload = et.Element("x")
            self.assertRaises(RpcInputError, self.rpcbld.get_payload,
                              [cfg], payload)
            xml = et.tostring(payload, encoding='unicode', pretty_print=True)
            # For invalid xpath, we shouldn't create any nodes, even those that
            # are valid up to a point.
            self.assertEqual("""\
<x/>
""", xml)

    def test_get_payload_identityref_namespace(self):
        """Test get_payload() where the value has its own namespace.

        Seen most commonly with identityrefs.
        """
        cfgs = [{
            "xpath": "/ocif:interfaces/ocif:interface/ocif:config/ocif:type",
            "value": "ianaift:ethernetCsmacd",
        }]
        payload = self.rpcbld.get_payload(cfgs, et.Element("y"))

        xml = et.tostring(payload, encoding='unicode', pretty_print=True)
        self.assertEqual(u"""\
<y>
  <ocif:interfaces xmlns:ocif="http://openconfig.net/yang/interfaces"\
 xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
    <ocif:interface>
      <ocif:config>
        <ocif:type>ianaift:ethernetCsmacd</ocif:type>
      </ocif:config>
    </ocif:interface>
  </ocif:interfaces>
</y>
""", xml)

        payload_min = self.rpcbld_minimal.get_payload(cfgs, et.Element("y"))
        xml_min = et.tostring(payload_min, encoding="unicode",
                              pretty_print=True)
        self.assertEqual(u"""\
<y>
  <interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
      <config>
        <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">\
ianaift:ethernetCsmacd</type>
      </config>
    </interface>
  </interfaces>
</y>
""", xml_min)

    def test_get_payload_value_characters(self):
        """Test get_payload() with special characters in the value."""
        cfgs = [{
            "xpath": "/ocif:interfaces/ocif:interface/ocif:name",
            # Mixture of pre-escaped characters and those needing to escape
            "value": "This:is:some&#92;silly-interface<haha>",
        }]
        payload = self.rpcbld.get_payload(cfgs, et.Element("x"))
        xml = et.tostring(payload, encoding='unicode', pretty_print=True)
        self.assertEqual("""\
<x>
  <ocif:interfaces xmlns:ocif="http://openconfig.net/yang/interfaces">
    <ocif:interface>
      <ocif:name>This:is:some\\silly-interface&lt;haha&gt;</ocif:name>
    </ocif:interface>
  </ocif:interfaces>
</x>
""", xml)

        payload_min = self.rpcbld_minimal.get_payload(cfgs, et.Element('x'))
        xml_min = et.tostring(payload_min, encoding='unicode',
                              pretty_print=True)
        self.assertEqual("""\
<x>
  <interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
      <name>This:is:some\\silly-interface&lt;haha&gt;</name>
    </interface>
  </interfaces>
</x>
""", xml_min)

    def test_get_payload_xml_value(self):
        """Test get_payload with xml_value."""
        cfgs = [{
            "xpath": "/nc:get-config/nc:filter",
            "xml_value": """\
<oc-if:interfaces xmlns:oc-if=\"http://openconfig.net/yang/interfaces\">
  <oc-if:interface>
    <oc-if:name>eth0</oc-if:name>
  </oc-if:interface>
</oc-if:interfaces>""",
        }]
        payload = self.rpcbld.get_payload(cfgs, et.Element("rpc"))
        xml = et.tostring(payload, encoding='unicode', pretty_print=True)

        self.assertEqual("""\
<rpc>
  <nc:get-config xmlns:ocif="http://openconfig.net/yang/interfaces" \
xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
    <nc:filter>
      <ocif:interfaces>
  <ocif:interface>
    <ocif:name>eth0</ocif:name>
  </ocif:interface>
</ocif:interfaces>
    </nc:filter>
  </nc:get-config>
</rpc>
""", xml)

    def test_get_payload_multiple_leafs(self):
        """Test get_payload() with multiple cfgs."""
        cfgs = [{
            "xpath": "/ocif:interfaces/ocif:interface/ocif:config/ocif:type",
            "value": "ianaift:ethernetCsmacd",
        }, {
            "xpath": "/ocif:interfaces/ocif:interface/eth:ethernet/\
eth:config/eth:port-speed",
            "value": "eth:SPEED_1Gb",
        }]
        payload = self.rpcbld.get_payload(cfgs, et.Element("z"))
        xml = et.tostring(payload, encoding='unicode', pretty_print=True)

        self.assertEqual("""\
<z>
  <ocif:interfaces xmlns:ocif="http://openconfig.net/yang/interfaces" \
xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type" \
xmlns:eth="http://openconfig.net/yang/interfaces/ethernet">
    <ocif:interface>
      <ocif:config>
        <ocif:type>ianaift:ethernetCsmacd</ocif:type>
      </ocif:config>
      <eth:ethernet>
        <eth:config>
          <eth:port-speed>eth:SPEED_1Gb</eth:port-speed>
        </eth:config>
      </eth:ethernet>
    </ocif:interface>
  </ocif:interfaces>
</z>
""", xml)

        payload_min = self.rpcbld_minimal.get_payload(cfgs, et.Element("z"))
        xml_min = et.tostring(payload_min, encoding='unicode',
                              pretty_print=True)

        # In this case, because the value is under the same namespace as the
        # parent, we actually strip the value namespace prefix.
        self.assertEqual("""\
<z>
  <interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
      <config>
        <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">\
ianaift:ethernetCsmacd</type>
      </config>
      <ethernet xmlns="http://openconfig.net/yang/interfaces/ethernet">
        <config>
          <port-speed>SPEED_1Gb</port-speed>
        </config>
      </ethernet>
    </interface>
  </interfaces>
</z>
""", xml_min)

    def test_get_payload_list_leaf_list(self):
        """Test ParseYang.get_payload() with list key and leaf-list entries."""
        cfgs = [
            # First list entry - explicit key nodes in cfgs
            {
                "xpath": ('/aaa:aaa/aaa:accountings/'
                          'aaa:accounting[type="exec"][listname="first:list"]/'
                          'aaa:type'),
                "value": "exec",
                "edit-op": "create",
            }, {
                "xpath": ('/aaa:aaa/aaa:accountings/'
                          'aaa:accounting[type="exec"][listname="first:list"]/'
                          'aaa:listname'),
                "value": "first:list",
            }, {
                "xpath": ('/aaa:aaa/aaa:accountings/'
                          'aaa:accounting[type="exec"][listname="first:list"]/'
                          'aaa:method'),
                "value": "local",
            }, {
                "xpath": ('/aaa:aaa/aaa:accountings/'
                          'aaa:accounting[type="exec"][listname="first:list"]/'
                          'aaa:method'),
                "value": "TACACS+",
            },
            # Second list entry - key nodes are implied by the XPaths given
            {
                "xpath": ('/aaa:aaa/aaa:accountings/'
                          'aaa:accounting[type="exec"][listname="second:one"]/'
                          'aaa:method'),
                "value": "radius",
            }, {
                "xpath": ('/aaa:aaa/aaa:accountings/'
                          'aaa:accounting[type="exec"][listname="second:one"]/'
                          'aaa:method'),
                "value": "none",
                "edit-op": "delete",
            },
        ]

        payload = self.rpcbld.get_payload(cfgs, et.Element("config"))
        xml = et.tostring(payload, encoding='unicode', pretty_print=True)

        self.assertEqual("""\
<config>
  <aaa:aaa xmlns:aaa="http://cisco.com/ns/yang/Cisco-IOS-XR-aaa-lib-cfg" \
xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
    <aaa:accountings>
      <aaa:accounting>
        <aaa:type nc:operation="create">exec</aaa:type>
        <aaa:listname>first:list</aaa:listname>
        <aaa:method>local</aaa:method>
        <aaa:method>TACACS+</aaa:method>
      </aaa:accounting>
      <aaa:accounting>
        <aaa:type>exec</aaa:type>
        <aaa:listname>second:one</aaa:listname>
        <aaa:method>radius</aaa:method>
        <aaa:method nc:operation="delete">none</aaa:method>
      </aaa:accounting>
    </aaa:accountings>
  </aaa:aaa>
</config>
""", xml)

# TODO: Build minimal is setting netconf prefix "nc" to "ns0" and "ns1"
#       for create and delete operations. I don't know if we will ever
#       need "build minimal" so disabled this test.
#
#         payload_min = self.rpcbld_minimal.get_payload(cfgs,
#                                                       et.Element('config'))
#         xml_min = et.tostring(payload_min, encoding='unicode',
#                               pretty_print=True)
#         self.assertEqual("""\
# <config>
#   <aaa xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-aaa-lib-cfg">
#     <accountings>
#       <accounting>
#         <type xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" \
# nc:operation="create">exec</type>
#         <listname>first:list</listname>
#         <method>local</method>
#         <method>TACACS+</method>
#       </accounting>
#       <accounting>
#         <type>exec</type>
#         <listname>second:one</listname>
#         <method>radius</method>
#         <method xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" \
# nc:operation="delete">none</method>
#       </accounting>
#     </accountings>
#   </aaa>
# </config>
# """, xml_min)

    def test_get_payload_list_key_mismatch(self):
        """Negative test - xpath key value doesn't match requested value."""
        cfgs = [{
            "xpath": '/ocif:interfaces/ocif:interface[name="eth0"]/ocif:name',
            "value": "wrong-value",
        }]
        payload = self.rpcbld.get_payload(cfgs, et.Element('wrapper'))
        xml = et.tostring(payload, encoding='unicode', pretty_print=True)

        self.assertEqual("""\
<wrapper>
  <ocif:interfaces xmlns:ocif="http://openconfig.net/yang/interfaces">
    <ocif:interface>
      <ocif:name>eth0</ocif:name>
    </ocif:interface>
  </ocif:interfaces>
</wrapper>
""", xml)

    def test_get_payload_implied_terminal_key(self):
        """Test get_payload() where the list key is implied at the end."""
        cfgs = [{
            "xpath": '/ocif:interfaces/ocif:interface[name="eth0"]',
            "edit-op": "create",
        }]

        payload = self.rpcbld.get_payload(cfgs, et.Element('config'))
        xml = et.tostring(payload, encoding='unicode', pretty_print=True)

        self.assertEqual("""\
<config>
  <ocif:interfaces xmlns:ocif="http://openconfig.net/yang/interfaces" \
xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
    <ocif:interface nc:operation="create">
      <ocif:name>eth0</ocif:name>
    </ocif:interface>
  </ocif:interfaces>
</config>
""", xml)

    def test_get_payload_rpc(self):
        """Build a Netconf RPC that uses an rpc statement."""
        # These leaves are 'type empty', so no value needed/given.
        cfgs = [{
            'xpath': "/cisco-ia:sync-from/cisco-ia:sync-defaults",
        }, {
            'xpath': "/cisco-ia:sync-from/cisco-ia:ignore-presrv-paths",
        }]

        payload = self.rpcbld.get_payload(cfgs, et.Element('wrapper'))
        xml = et.tostring(payload, encoding='unicode', pretty_print=True)

        self.assertEqual("""\
<wrapper>
  <cisco-ia:sync-from xmlns:cisco-ia="http://cisco.com/yang/cisco-ia">
    <cisco-ia:sync-defaults/>
    <cisco-ia:ignore-presrv-paths/>
  </cisco-ia:sync-from>
</wrapper>
""", xml)

        payload_min = self.rpcbld_minimal.get_payload(
            cfgs, et.Element('wrapper'))
        xml_min = et.tostring(payload_min, encoding='unicode',
                              pretty_print=True)

        self.assertEqual("""\
<wrapper>
  <sync-from xmlns="http://cisco.com/yang/cisco-ia">
    <sync-defaults/>
    <ignore-presrv-paths/>
  </sync-from>
</wrapper>
""", xml_min)

    def test_get_payload_invalid(self):
        """Call get_payload with invalid data and make sure it's handled."""

        # Invalid (legacy) input args
        payload = self.rpcbld.get_payload([{
            'name': 'type',
            'prefix': 'ocif',
            'parents': [{}],
        }], et.Element("hello"))
        self.assertEqual("<hello/>", et.tostring(payload, encoding='unicode'))

    def test_get_payload_with_and_without_keys(self):
        """Test get_payload with and without explicitly specified keys."""

        # Without explicitly specifying keys
        payload_min = self.rpcbld_minimal.get_payload([{
            'xpath': '/ocif:interfaces/ocif:interface/ocif:name',
            'value': 'GigabitEthernet0/1/1',
        }, {
            'xpath': '/ocif:interfaces/ocif:interface/ocif:config/ocif:type',
            'value': 'ianaift:ethernetCsmacd',
        }, {
            'xpath': '/ocif:interfaces/ocif:interface/ocif:config/ocif:mtu',
            'value': '9216',
        }, {
            'xpath': '/ocif:interfaces/ocif:interface/ocif:config/\
ocif:description',
            'value': '10b-oc-if-mtu-upper-bound-rtr',
        }], et.Element('config'))
        xml_min = et.tostring(payload_min, encoding='unicode',
                              pretty_print=True)
        self.assertEqual("""\
<config>
  <interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
      <name>GigabitEthernet0/1/1</name>
      <config>
        <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">\
ianaift:ethernetCsmacd</type>
        <mtu>9216</mtu>
        <description>10b-oc-if-mtu-upper-bound-rtr</description>
      </config>
    </interface>
  </interfaces>
</config>
""", xml_min)

        # With explicitly specified keys
        payload_min_2 = self.rpcbld_minimal.get_payload([{
            'xpath': '/ocif:interfaces/ocif:interface\
[ocif:name="GigabitEthernet0/1/1"]/ocif:config/ocif:type',
            'value': 'ianaift:ethernetCsmacd',
        }, {
            'xpath': '/ocif:interfaces/ocif:interface\
[ocif:name="GigabitEthernet0/1/1"]/ocif:config/ocif:mtu',
            'value': '9216',
        }, {
            'xpath': '/ocif:interfaces/ocif:interface\
[ocif:name="GigabitEthernet0/1/1"]/ocif:config/ocif:description',
            'value': '10b-oc-if-mtu-upper-bound-rtr',
        }], et.Element('config'))
        xml_min_2 = et.tostring(payload_min_2, encoding='unicode',
                                pretty_print=True)
        self.assertEqual(xml_min, xml_min_2)

    def test_get_payload_with_and_without_keys_2(self):
        """Try get_payload with and without more explicitly specified keys."""
        payload_min = self.rpcbld_minimal.get_payload([{
            'xpath': '/ocni:network-instances/ocni:network-instance/ocni:name',
            'value': 'VRF_1',
        }, {
            'xpath': '/ocni:network-instances/ocni:network-instance/\
ocni:protocols/ocni:protocol/ocni:identifier',
            'value': 'oc-pol-types:STATIC',
        }, {
            'xpath': '/ocni:network-instances/ocni:network-instance/\
ocni:protocols/ocni:protocol/ocni:name',
            'value': 'DEFAULT',
        }, {
            'xpath': '/ocni:network-instances/ocni:network-instance/\
ocni:protocols/ocni:protocol/ocni:static-routes/ocni:static/ocni:prefix',
            'value': '2.2.2.2/32',
        }, {
            'xpath': '/ocni:network-instances/ocni:network-instance/\
ocni:protocols/ocni:protocol/ocni:static-routes/ocni:static/ocni:config/\
ocni:prefix',
            'value': '2.2.2.2/32',
        }, {
            'xpath': '/ocni:network-instances/ocni:network-instance/\
ocni:protocols/ocni:protocol/ocni:static-routes/ocni:static/ocni:next-hops/\
ocni:next-hop/ocni:index',
            'value': 'NH_1',
        }, {
            'xpath': '/ocni:network-instances/ocni:network-instance/\
ocni:protocols/ocni:protocol/ocni:static-routes/ocni:static/ocni:next-hops/\
ocni:next-hop/ocni:config/ocni:index',
            'value': 'NH_1',
        }, {
            'xpath': '/ocni:network-instances/ocni:network-instance/\
ocni:protocols/ocni:protocol/ocni:static-routes/ocni:static/ocni:next-hops/\
ocni:next-hop/ocni:config/ocni:next-hop',
            'value': '8.8.8.8',
        }, {
            'xpath': '/ocni:network-instances/ocni:network-instance/\
ocni:protocols/ocni:protocol/ocni:static-routes/ocni:static/ocni:next-hops/\
ocni:next-hop/ocni:config/ocni:metric',
            'value': '160',
        }], et.Element('config'))
        xml_min = et.tostring(payload_min, encoding='unicode',
                              pretty_print=True)
        self.assertEqual("""\
<config>
  <network-instances xmlns="http://openconfig.net/yang/network-instance">
    <network-instance>
      <name>VRF_1</name>
      <protocols>
        <protocol>
          <identifier \
xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">\
oc-pol-types:STATIC</identifier>
          <name>DEFAULT</name>
          <static-routes>
            <static>
              <prefix>2.2.2.2/32</prefix>
              <config>
                <prefix>2.2.2.2/32</prefix>
              </config>
              <next-hops>
                <next-hop>
                  <index>NH_1</index>
                  <config>
                    <index>NH_1</index>
                    <next-hop>8.8.8.8</next-hop>
                    <metric>160</metric>
                  </config>
                </next-hop>
              </next-hops>
            </static>
          </static-routes>
        </protocol>
      </protocols>
    </network-instance>
  </network-instances>
</config>
""", xml_min)

        payload_min_2 = self.rpcbld_minimal.get_payload([{
            'xpath': '/ocni:network-instances/\
ocni:network-instance[ocni:name="VRF_1"]/ocni:protocols/\
ocni:protocol[ocni:identifier="oc-pol-types:STATIC"][ocni:name="DEFAULT"]/\
ocni:static-routes/ocni:static[ocni:prefix="2.2.2.2/32"]/ocni:config/\
ocni:prefix',
            'value': '2.2.2.2/32',
        }, {
            'xpath': '/ocni:network-instances/\
ocni:network-instance[ocni:name="VRF_1"]/ocni:protocols/\
ocni:protocol[ocni:identifier="oc-pol-types:STATIC"][ocni:name="DEFAULT"]/\
ocni:static-routes/ocni:static[ocni:prefix="2.2.2.2/32"]/ocni:next-hops/\
ocni:next-hop[ocni:index="NH_1"]/ocni:config/ocni:index',
            'value': 'NH_1',
        }, {
            'xpath': '/ocni:network-instances/\
ocni:network-instance[ocni:name="VRF_1"]/ocni:protocols/\
ocni:protocol[ocni:identifier="oc-pol-types:STATIC"][ocni:name="DEFAULT"]/\
ocni:static-routes/ocni:static[ocni:prefix="2.2.2.2/32"]/ocni:next-hops/\
ocni:next-hop[ocni:index="NH_1"]/ocni:config/ocni:next-hop',
            'value': '8.8.8.8',
        }, {
            'xpath': '/ocni:network-instances/\
ocni:network-instance[ocni:name="VRF_1"]/ocni:protocols/\
ocni:protocol[ocni:identifier="oc-pol-types:STATIC"][ocni:name="DEFAULT"]/\
ocni:static-routes/ocni:static[ocni:prefix="2.2.2.2/32"]/ocni:next-hops/\
ocni:next-hop[ocni:index="NH_1"]/ocni:config/ocni:metric',
            'value': '160',
        }], et.Element('config'))
        xml_min_2 = et.tostring(payload_min_2, encoding='unicode',
                                pretty_print=True)
        self.assertEqual(xml_min, xml_min_2)


class TestRPCBuilderNamespaces(unittest.TestCase):
    """Test a set of modules with more complex namespaces."""

    basedir = os.path.join(os.path.dirname(__file__), 'data')

    @classmethod
    def setUpClass(cls):
        cls.nsmap = {
            'ocif': "http://openconfig.net/yang/interfaces",
            'ianaift': "urn:ietf:params:xml:ns:yang:iana-if-type",
            'eth': "http://openconfig.net/yang/interfaces/ethernet",
            'cisco-ia': "http://cisco.com/yang/cisco-ia",    # TODO move me
            'vlan': "http://openconfig.net/yang/vlan",
            'lag': "http://openconfig.net/yang/interface/aggregate",
            'ocip': "http://openconfig.net/yang/interfaces/ip",
            'if': "urn:ietf:params:xml:ns:yang:ietf-interfaces",
            'infra-objmgr-cfg':
            "http://cisco.com/ns/yang/Cisco-IOS-XR-infra-objmgr-cfg",
        }
        cls.maxDiff = None

    def setUp(self):
        self.rpcbld = YSNetconfRPCBuilder(prefix_namespaces="always",
                                          nsmap=self.nsmap)
        self.rpcbld_minimal = YSNetconfRPCBuilder(nsmap=self.nsmap)

    def test_add_netconf_attr_prefix(self):
        """Handling of netconf attributes with and without prefix."""
        elem = self.rpcbld.netconf_element('rpc')
        self.rpcbld.add_netconf_attr(elem, 'message-id', 101)
        et.cleanup_namespaces(
            elem, keep_ns_prefixes=sorted(self.rpcbld.keep_prefixes))

        self.assertEqual("""\
<nc:rpc xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" \
nc:message-id="101"/>
""", et.tostring(elem, encoding='unicode', pretty_print=True))

        elem = self.rpcbld_minimal.netconf_element('rpc')
        self.rpcbld_minimal.add_netconf_attr(elem, 'message-id', 101)
        et.cleanup_namespaces(
            elem, keep_ns_prefixes=sorted(self.rpcbld_minimal.keep_prefixes))

        self.assertEqual("""\
<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101"/>
""", et.tostring(elem, encoding='unicode', pretty_print=True))

    def test_namespace_next_hop(self):
        """Case where we have a known next-hop with a different namespace."""
        cfgs = [{
            "xpath": "/ocif:interfaces/ocif:interface/eth:ethernet/\
vlan:vlan/vlan:config/vlan:interface-mode",
            "value": "ACCESS"
        }, {
            "xpath": "/ocif:interfaces/ocif:interface/lag:aggregation/\
vlan:vlan/vlan:config/vlan:interface-mode",
            "value": "ACCESS",
        }, {
            "xpath": "/ocif:interfaces/ocif:interface/vlan:routed-vlan/\
ocip:ipv4/ocip:address/ocip:ip",
            "value": "1.1.1.1",
        }]
        payload = self.rpcbld.get_payload(cfgs, et.Element("foobar"))
        xml = et.tostring(payload, encoding='unicode', pretty_print=True)
        self.assertEqual("""\
<foobar>
  <ocif:interfaces xmlns:ocif="http://openconfig.net/yang/interfaces" \
xmlns:eth="http://openconfig.net/yang/interfaces/ethernet" \
xmlns:vlan="http://openconfig.net/yang/vlan" \
xmlns:lag="http://openconfig.net/yang/interface/aggregate" \
xmlns:ocip="http://openconfig.net/yang/interfaces/ip">
    <ocif:interface>
      <eth:ethernet>
        <vlan:vlan>
          <vlan:config>
            <vlan:interface-mode>ACCESS</vlan:interface-mode>
          </vlan:config>
        </vlan:vlan>
      </eth:ethernet>
      <lag:aggregation>
        <vlan:vlan>
          <vlan:config>
            <vlan:interface-mode>ACCESS</vlan:interface-mode>
          </vlan:config>
        </vlan:vlan>
      </lag:aggregation>
      <vlan:routed-vlan>
        <ocip:ipv4>
          <ocip:address>
            <ocip:ip>1.1.1.1</ocip:ip>
          </ocip:address>
        </ocip:ipv4>
      </vlan:routed-vlan>
    </ocif:interface>
  </ocif:interfaces>
</foobar>
""", xml)

        payload_min = self.rpcbld_minimal.get_payload(
            cfgs, et.Element("foobar"))
        xml_min = et.tostring(payload_min, encoding='unicode',
                              pretty_print=True)
        self.assertEqual("""\
<foobar>
  <interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
      <ethernet xmlns="http://openconfig.net/yang/interfaces/ethernet">
        <vlan xmlns="http://openconfig.net/yang/vlan">
          <config>
            <interface-mode>ACCESS</interface-mode>
          </config>
        </vlan>
      </ethernet>
      <aggregation xmlns="http://openconfig.net/yang/interface/aggregate">
        <vlan xmlns="http://openconfig.net/yang/vlan">
          <config>
            <interface-mode>ACCESS</interface-mode>
          </config>
        </vlan>
      </aggregation>
      <routed-vlan xmlns="http://openconfig.net/yang/vlan">
        <ipv4 xmlns="http://openconfig.net/yang/interfaces/ip">
          <address>
            <ip>1.1.1.1</ip>
          </address>
        </ipv4>
      </routed-vlan>
    </interface>
  </interfaces>
</foobar>
""", xml_min)

    def test_multiple_root_elements(self):
        """Test RPC construction with multiple top-level elements."""
        cfgs = [{
            "xpath": "/if:interfaces",
        }, {
            "xpath": "/if:interfaces-state",
        }]

        payload = self.rpcbld.get_payload(cfgs, et.Element("filter"))
        xml = et.tostring(payload, encoding='unicode', pretty_print=True)
        self.assertEqual("""\
<filter>
  <if:interfaces xmlns:if="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
  <if:interfaces-state xmlns:if="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
</filter>
""", xml)

        payload_min = self.rpcbld_minimal.get_payload(
            cfgs, et.Element("filter"))
        xml_min = et.tostring(payload_min, encoding='unicode',
                              pretty_print=True)
        self.assertEqual("""\
<filter>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
  <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
</filter>
""", xml_min)

    def test_ipv6_address_key_value(self):
        """Test IPv6 address (i.e., value with ':' chars) as key/value."""
        cfgs = [
            {
                "xpath": """\
/infra-objmgr-cfg:object-group/infra-objmgr-cfg:network/infra-objmgr-cfg:ipv6/\
infra-objmgr-cfg:udf-objects/infra-objmgr-cfg:udf-object/\
infra-objmgr-cfg:object-name""",
                "value": "foobar",
            }, {
                "xpath": """\
/infra-objmgr-cfg:object-group/infra-objmgr-cfg:network/infra-objmgr-cfg:ipv6/\
infra-objmgr-cfg:udf-objects/infra-objmgr-cfg:udf-object/\
infra-objmgr-cfg:hosts/infra-objmgr-cfg:host\
[infra-objmgr-cfg:host-address="1:1:1::"]/infra-objmgr-cfg:host-address""",
                "value": "1:1:1::",
            }
        ]
        payload = self.rpcbld.get_payload(cfgs, et.Element("config"))
        xml = et.tostring(payload, encoding='unicode', pretty_print=True)
        self.assertEqual("""\
<config>
  <infra-objmgr-cfg:object-group xmlns:infra-objmgr-cfg=\
"http://cisco.com/ns/yang/Cisco-IOS-XR-infra-objmgr-cfg">
    <infra-objmgr-cfg:network>
      <infra-objmgr-cfg:ipv6>
        <infra-objmgr-cfg:udf-objects>
          <infra-objmgr-cfg:udf-object>
            <infra-objmgr-cfg:object-name>foobar</infra-objmgr-cfg:object-name>
            <infra-objmgr-cfg:hosts>
              <infra-objmgr-cfg:host>
                <infra-objmgr-cfg:host-address>1:1:1::\
</infra-objmgr-cfg:host-address>
              </infra-objmgr-cfg:host>
            </infra-objmgr-cfg:hosts>
          </infra-objmgr-cfg:udf-object>
        </infra-objmgr-cfg:udf-objects>
      </infra-objmgr-cfg:ipv6>
    </infra-objmgr-cfg:network>
  </infra-objmgr-cfg:object-group>
</config>
""", xml)

        payload_min = self.rpcbld_minimal.get_payload(
            cfgs, et.Element("config"))
        xml_min = et.tostring(payload_min, encoding='unicode',
                              pretty_print=True)
        self.assertEqual("""\
<config>
  <object-group xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-infra-objmgr-cfg">
    <network>
      <ipv6>
        <udf-objects>
          <udf-object>
            <object-name>foobar</object-name>
            <hosts>
              <host>
                <host-address>1:1:1::</host-address>
              </host>
            </hosts>
          </udf-object>
        </udf-objects>
      </ipv6>
    </network>
  </object-group>
</config>
""", xml_min)

    def test_key_value_predicates(self):
        """Test various key-value predicates."""
        cfgs = [{
            "xpath": '/if:interfaces/if:interface[name="Ethernet1/1"]/if:type',
            "value": "ianaift:ethernetCsmacd",
        }, {
            "xpath": """/vlan:vlans/vlan:vlan[name='"hello world"']/vlan:id""",
            "value": '1',
        }, {
            "xpath": """/ocif:interfaces/ocif:interface[name=concat("""
            """"I said ", '"', "I said 'hello'", '"', "!")]/ocif:enabled""",
            "value": "true",
        }]
        payload_min = self.rpcbld_minimal.get_payload(cfgs,
                                                      et.Element("filter"))
        xml_min = et.tostring(payload_min, encoding='unicode',
                              pretty_print=True)
        self.assertEqual("""\
<filter>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>Ethernet1/1</name>
      <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">\
ianaift:ethernetCsmacd</type>
    </interface>
  </interfaces>
  <vlans xmlns="http://openconfig.net/yang/vlan">
    <vlan>
      <name>"hello world"</name>
      <id>1</id>
    </vlan>
  </vlans>
  <interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
      <name>I said "I said 'hello'"!</name>
      <enabled>true</enabled>
    </interface>
  </interfaces>
</filter>
""", xml_min)


if __name__ == '__main__':
    unittest.main()
