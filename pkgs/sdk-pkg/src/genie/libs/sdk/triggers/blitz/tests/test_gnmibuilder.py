#! /usr/bin/env python
import unittest
import os
import json
import base64
from copy import deepcopy

from google.protobuf import json_format

from genie.libs.sdk.triggers.blitz.gnmi_util import (
    GnmiMessage,
    GnmiMessageConstructor
)

format1 = {
    'encoding': 'JSON_IETF',
    'request_mode': 'STREAM',
    'sample_interval': 5,
    'stream_max': 20,
    'sub_mode': 'SAMPLE',
    'prefix': True,
    'origin': 'openconfig'
}

request1 = {
  'nodes': [
        {
            'datatype': 'leafref',
            'nodetype': 'leaf',
            'value': 'default',
            'xpath': '/oc-netinst:network-instances/oc-netinst:network-instance[name="default"]' # noqa
        },
        {
            'datatype': 'string',
            'nodetype': 'leaf',
            'value': 'default',
            'xpath': '/oc-netinst:network-instances/oc-netinst:network-instance[name="default"]/oc-netinst:config/oc-netinst:name' # noqa
        },
        {
            'datatype': 'leafref',
            'nodetype': 'leaf',
            'value': 'oc-pol-types:OSPF',
            'xpath': '/oc-netinst:network-instances/oc-netinst:network-instance[name="default"]/oc-netinst:protocols/oc-netinst:protocol[identifier="oc-pol-types:OSPF"][name="100"]' # noqa
        },
        {
            'datatype': 'leafref',
            'nodetype': 'leaf',
            'value': '100',
            'xpath': '/oc-netinst:network-instances/oc-netinst:network-instance[name="default"]/oc-netinst:protocols/oc-netinst:protocol[identifier="oc-pol-types:OSPF"][name="100"]' # noqa
        },
        {
            'datatype': 'identityref',
            'nodetype': 'leaf',
            'value': 'oc-pol-types:OSPF',
            'xpath': '/oc-netinst:network-instances/oc-netinst:network-instance[name="default"]/oc-netinst:protocols/oc-netinst:protocol[identifier="oc-pol-types:OSPF"][name="100"]/oc-netinst:config/oc-netinst:identifier' # noqa
        },
        {
            'datatype': 'string',
            'nodetype': 'leaf',
            'value': '100',
            'xpath': '/oc-netinst:network-instances/oc-netinst:network-instance[name="default"]/oc-netinst:protocols/oc-netinst:protocol[identifier="oc-pol-types:OSPF"][name="100"]/oc-netinst:config/oc-netinst:name' # noqa
        },
        {
            'datatype': 'leafref',
            'nodetype': 'leaf',
            'value': '1.1.1.1',
            'xpath': '/oc-netinst:network-instances/oc-netinst:network-instance[name="default"]/oc-netinst:protocols/oc-netinst:protocol[identifier="oc-pol-types:OSPF"][name="100"]/oc-netinst:bgp/oc-netinst:neighbors/oc-netinst:neighbor[neighbor-address="1.1.1.1"]' # noqa
        },
        {
            'datatype': 'union',
            'nodetype': 'leaf',
            'value': '1.1.1.1',
            'xpath': '/oc-netinst:network-instances/oc-netinst:network-instance[name="default"]/oc-netinst:protocols/oc-netinst:protocol[identifier="oc-pol-types:OSPF"][name="100"]/oc-netinst:bgp/oc-netinst:neighbors/oc-netinst:neighbor[neighbor-address="1.1.1.1"]/oc-netinst:config/oc-netinst:neighbor-address' # noqa
        }
    ],
    'namespace_modules': {
        'oc-netinst': 'openconfig-network-instance',
        'oc-pol-types': 'openconfig-policy-types'
    },
    'namespace': {
        'ianaift': 'urn:ietf:params:xml:ns:yang:iana-if-type',
        'ietf-if': 'urn:ietf:params:xml:ns:yang:ietf-interfaces',
        'if': 'urn:ietf:params:xml:ns:yang:ietf-interfaces',
        'ift': 'urn:ietf:params:xml:ns:yang:iana-if-type',
        'oc-eth': 'http://openconfig.net/yang/interfaces/ethernet',
        'oc-ext': 'http://openconfig.net/yang/openconfig-ext',
        'oc-if': 'http://openconfig.net/yang/interfaces',
        'oc-inet': 'http://openconfig.net/yang/types/inet',
        'oc-ip': 'http://openconfig.net/yang/interfaces/ip',
        'oc-ip-ext': 'http://openconfig.net/yang/interfaces/ip-ext',
        'oc-lag': 'http://openconfig.net/yang/interfaces/aggregate',
        'oc-types': 'http://openconfig.net/yang/openconfig-types',
        'oc-vlan': 'http://openconfig.net/yang/vlan',
        'oc-vlan-types': 'http://openconfig.net/yang/vlan-types',
        'oc-yang': 'http://openconfig.net/yang/types/yang',
        'xr': 'http://cisco.com/ns/yang/cisco-oc-xr-mapping',
        'oc-netinst': 'http://openconfig.net/yang/network-instance',
        'oc-pol-types': 'http://openconfig.net/yang/policy-types'
    }
}

json_decoded = {
  'prefix': {
    'origin': 'openconfig'
  },
  'update': [
    {
      'path': {
        'elem': [
          {
            'name': 'openconfig-network-instance:network-instances'
          },
          {
            'key': {
              'name': 'default'
            },
            'name': 'network-instance'
          }
        ],
        'origin': 'openconfig'
      }
    }
  ]
}

json_val_decoded = {
  'config': {
    'name': 'default'
  },
  'protocols': {
    'protocol': {
      'bgp': {
        'neighbors': {
          'neighbor': {
            'config': {
              'neighbor-address': '1.1.1.1'
            },
            'neighbor-address': '1.1.1.1'
          }
        }
      },
      'config': {
        'identifier': 'openconfig-policy-types:OSPF',
        'name': '100'
      },
      'identifier': 'openconfig-policy-types:OSPF',
      'name': '100'
    }
  }
}

json_decoded2 = {
  'update': [
    {
      'path': {
        'elem': [
          {
            'name': 'interfaces'
          },
          {
            'key': {
              'name': 'TenGigabitEthernet1/0/1'
              },
            'name': 'interface'
          },
          {
            'name': 'ethernet'
          },
          {
            'name': 'config'
          }
        ],
        'origin': 'openconfig'
      },
      'val': {
        'jsonVal': 'eyJlbmFibGUtZmxvdy1jb250cm9sIjogdHJ1ZX0='
      }
    }
  ]
}

json_val_decoded2 = {'enable-flow-control': True}

format2 = {
    'encoding': 'JSON_IETF',
    'request_mode': 'STREAM',
    'sample_interval': 5,
    'stream_max': 20,
    'sub_mode': 'SAMPLE',
    'prefix': False,
    'origin': False
}

request2 = {
  'action': 'get',
  'device': 'ddmi-9500-2',
  'encoding': 'json_ietf',
  'nodes': [
    {
        'datatype': 'uint16',
        'default': '',
        'nodetype': 'leaf',
        'xpath': '/vlan-ios-xe-oper:vlans/vlan-ios-xe-oper:vlan[id="100"]'
    },
    {
        'datatype': 'string',
        'default': '',
        'nodetype': 'leaf',
        'value': '',
        'xpath': '/vlan-ios-xe-oper:vlans/vlan-ios-xe-oper:vlan[id="100"]/vlan-ios-xe-oper:ports/vlan-ios-xe-oper:interface' # noqa
    },
    {
        'datatype': 'string',
        'default': '',
        'nodetype': 'leaf',
        'xpath': '/vlan-ios-xe-oper:vlans/vlan-ios-xe-oper:vlan[id="100"]/vlan-ios-xe-oper:vlan-interfaces[interface="TenGigabitEthernet1/0/1"]' # noqa
    },
    {
        'datatype': 'uint32',
        'default': '',
        'nodetype': 'leaf',
        'value': '',
        'xpath': '/vlan-ios-xe-oper:vlans/vlan-ios-xe-oper:vlan[id="100"]/vlan-ios-xe-oper:vlan-interfaces[interface="TenGigabitEthernet1/0/1"]/vlan-ios-xe-oper:subinterface' # noqa
    }
    ],
    'namespace_modules': {
        'cisco-semver': 'cisco-semver',
        'vlan-ios-xe-oper': 'Cisco-IOS-XE-vlan-oper'
    },
    'namespace': {
        'cisco-semver': 'http://cisco.com/ns/yang/cisco-semver',
        'vlan-ios-xe-oper': 'http://cisco.com/ns/yang/Cisco-IOS-XE-vlan-oper'
    }
}

dictfrom2 = {
    'encoding': 'JSON_IETF',
    'path': [
        {'elem': [
            {'name': 'vlans'},
            {'key': {'id': '100'}, 'name': 'vlan'},
            {'name': 'ports'},
            {'name': 'interface'}
        ]},
        {'elem': [{'name': 'vlans'},
                  {'key': {'id': '100'}, 'name': 'vlan'},
                  {'key': {'interface': 'TenGigabitEthernet1/0/1'},
                  'name': 'vlan-interfaces'},
                  {'name': 'subinterface'}]}]
}

format3 = {
    'encoding': 'json_ietf',
    'origin': 'rfc7951',
    'prefix': True,
    'sample_interval': 20,
    'request_mode': 'STREAM',
    'sub_mode': 'SAMPLE'
}

request3 = {
    'nodes': [
        {
            'datatype': 'string',
            'default': '',
            'name': '',
            'nodetype': 'leaf',
            'value': '',
            'xpath': 'lldp-ios-xe-oper:lldp-entries/lldp-ios-xe-oper:lldp-intf-details[if-name="TenGigabitEthernet1/0/1"]' # noqa
        }
    ],
    'namespace_modules': {
        'cisco-semver': 'cisco-semver',
        'lldp-ios-xe-oper': 'Cisco-IOS-XE-lldp-oper'
    },
    'namespace': {
        'cisco-semver': 'http://cisco.com/ns/yang/cisco-semver',
        'lldp-ios-xe-oper': 'http://cisco.com/ns/yang/Cisco-IOS-XE-lldp-oper' # noqa
    },
}

subscribe_dict = {
    'subscribe': {
        'encoding': 'JSON_IETF',
        'prefix': {'origin': 'rfc7951'},
        'subscription': [
            {
                'mode': 'SAMPLE',
                'path': {
                    'elem': [{'name': 'Cisco-IOS-XE-lldp-oper:lldp-entries'},
                             {'key': {'if-name': 'TenGigabitEthernet1/0/1'},
                              'name': 'lldp-intf-details'}]
                },
                'sampleInterval': '20000000000'}]
    }
}

format4 = {
    'encoding': 'json',
    'origin': 'openconfig',
    'prefix': False,
}

request4 = {
    'nodes': [
    {
        'datatype': 'leafref',
        'default': '',
        'nodetype': 'leaf',
        'xpath': '/oc-if:interfaces/oc-if:interface[name="TenGigabitEthernet1/0/1"]' # noqa
    },
    {
        'datatype': 'boolean',
        'default': 'false',
        'name': 'enable-flow-control',
        'nodetype': 'leaf',
        'value': 'true',
        'xpath': '/interfaces/interface[name="TenGigabitEthernet1/0/1"]/ethernet/config/enable-flow-control' # noqa
    }
    ],
    'namespace_modules': {
    'cisco': 'oc-xr-mapping',
    'ianaift': 'iana-if-type',
    'if': 'ietf-interfaces',
    'inet': 'ietf-inet-types',
    'ldp': 'openconfig-mpls-ldp',
    'oc-acl': 'openconfig-acl',
    'oc-aft': 'openconfig-aft',
    'oc-aftni': 'openconfig-aft-network-instance',
    'oc-aftt': 'openconfig-aft-types',
    'oc-bgp': 'openconfig-bgp',
    'oc-bgp-pol': 'openconfig-bgp-policy',
    'oc-bgp-types': 'openconfig-bgp-types',
    'oc-bgprib-types': 'openconfig-rib-bgp-types',
    'oc-eth': 'openconfig-if-ethernet',
    'oc-ext': 'openconfig-extensions',
    'oc-if': 'openconfig-interfaces',
    'oc-igmp': 'openconfig-igmp',
    'oc-igmp-types': 'openconfig-igmp-types',
    'oc-inet': 'openconfig-inet-types',
    'oc-ip': 'openconfig-if-ip',
    'oc-ip-ext': 'openconfig-if-ip-ext',
    'oc-isis': 'openconfig-isis',
    'oc-isis-lsdb-types': 'openconfig-isis-lsdb-types',
    'oc-isis-pol': 'openconfig-isis-policy',
    'oc-isis-types': 'openconfig-isis-types',
    'oc-lag': 'openconfig-if-aggregate',
    'oc-loc-rt': 'openconfig-local-routing',
    'oc-mpls': 'openconfig-mpls',
    'oc-mpls-sr': 'openconfig-mpls-sr',
    'oc-mplst': 'openconfig-mpls-types',
    'oc-netinst': 'openconfig-network-instance',
    'oc-netinst-devs': 'cisco-nx-openconfig-network-instance-deviations',
    'oc-ni-l3': 'openconfig-network-instance-l3',
    'oc-ni-pol': 'openconfig-network-instance-policy',
    'oc-ni-types': 'openconfig-network-instance-types',
    'oc-ospf-pol': 'openconfig-ospf-policy',
    'oc-ospf-types': 'openconfig-ospf-types',
    'oc-ospfv2': 'openconfig-ospfv2',
    'oc-pf': 'openconfig-policy-forwarding',
    'oc-pim': 'openconfig-pim',
    'oc-pim-types': 'openconfig-pim-types',
    'oc-pkt-match': 'openconfig-packet-match',
    'oc-pkt-match-types': 'openconfig-packet-match-types',
    'oc-pol-types': 'openconfig-policy-types',
    'oc-rib-bgp': 'openconfig-rib-bgp',
    'oc-rpol': 'openconfig-routing-policy',
    'oc-rsvp': 'openconfig-mpls-rsvp',
    'oc-sr': 'openconfig-segment-routing',
    'oc-sr-rsvp-ext': 'openconfig-rsvp-sr-ext',
    'oc-srt': 'openconfig-segment-routing-types',
    'oc-types': 'openconfig-types',
    'oc-vlan': 'openconfig-vlan',
    'oc-vlan-types': 'openconfig-vlan-types',
    'oc-yang': 'openconfig-yang-types',
    'yang': 'ietf-yang-types'
    },
    'namespace': {
    'ianaift': 'urn:ietf:params:xml:ns:yang:iana-if-type',
    'ietf-if': 'urn:ietf:params:xml:ns:yang:ietf-interfaces',
    'if': 'urn:ietf:params:xml:ns:yang:ietf-interfaces',
    'ift': 'urn:ietf:params:xml:ns:yang:iana-if-type',
    'oc-eth': 'http://openconfig.net/yang/interfaces/ethernet',
    'oc-ext': 'http://openconfig.net/yang/openconfig-ext',
    'oc-if': 'http://openconfig.net/yang/interfaces',
    'oc-inet': 'http://openconfig.net/yang/types/inet',
    'oc-ip': 'http://openconfig.net/yang/interfaces/ip',
    'oc-ip-ext': 'http://openconfig.net/yang/interfaces/ip-ext',
    'oc-lag': 'http://openconfig.net/yang/interfaces/aggregate',
    'oc-types': 'http://openconfig.net/yang/openconfig-types',
    'oc-vlan': 'http://openconfig.net/yang/vlan',
    'oc-vlan-types': 'http://openconfig.net/yang/vlan-types',
    'oc-yang': 'http://openconfig.net/yang/types/yang',
    'xr': 'http://cisco.com/ns/yang/cisco-oc-xr-mapping'
    }
}

raw_set_dict = {
  "update": [
    {
      "path": {
        "origin": "openconfig",
        "elem": [
          {
            "name": "network-instances"
          },
          {
            "name": "network-instance",
            "key": {
              "name": "default"
            }
          }
        ]
      },
      "val": {
        "jsonIetfVal": {
          "config": {
            "name": "default"
          },
          "protocols": {
            "protocol": {
              "identifier": "openconfig-policy-types:OSPF",
              "name": "100",
              "config": {
                "identifier": "openconfig-policy-types:OSPF",
                "name": "100"
              },
              "ospfv2": {
                "global": {
                  "config": {
                    "router-id": "5.5.5.5"
                  }
                }
              }
            }
          }
        }
      }
    }
  ]
}

raw_get_dict = {
  "path": [
    {
      "origin": "openconfig",
      "elem": [
        {
          "name": "network-instances"
        },
        {
          "name": "network-instance",
          "key": {
            "name": "default"
          }
        },
        {
          "name": "protocols"
        },
        {
          "name": "protocol",
          "key": {
            "name": "100",
            "identifier": "openconfig-policy-types:OSPF"
          }
        },
        {
          "name": "ospfv2"
        },
        {
          "name": "global"
        },
        {
          "name": "config"
        },
        {
          "name": "router-id"
        }
      ]
    }
  ],
  "encoding": "JSON_IETF"
}

raw_subscribe_dict = {
  "subscribe": {
    "prefix": {
      "origin": "rfc7951"
    },
    "subscription": [
      {
        "path": {
          "elem": [
            {
              "name": "Cisco-IOS-XE-lldp-oper:lldp-entries"
            },
            {
              "name": "lldp-intf-details",
              "key": {
                "if-name": "TenGigabitEthernet1/0/1"
              }
            }
          ]
        },
        "mode": "SAMPLE",
        "sampleInterval": "20000000000"
      }
    ],
    "encoding": "JSON_IETF"
  }
}


class TestGnmiTestRpc(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None

    def test_set_oc_net_instance(self):
        """Verify a complex SET constructs json_val correct."""
        r1 = deepcopy(request1)
        gmc = GnmiMessageConstructor('set', r1, **format1)
        jdict = json_format.MessageToDict(gmc.payload)
        jdict['update'][0].pop('val')
        self.assertEqual(jdict, json_decoded)
        self.assertEqual(gmc.json_val, json_val_decoded)

    def test_set_one_xpath(self):
        """Verify SET constructs json_val correct for one leaf node."""
        r4 = deepcopy(request4)
        gmc = GnmiMessageConstructor('set', r4, **format4)
        self.assertEqual(
            json_format.MessageToDict(gmc.payload),
            json_decoded2
        )
        self.assertEqual(gmc.json_val, json_val_decoded2)

    def test_set_no_namespace_modules(self):
        """Verify SET constructs correct without namespace passed in."""
        r4 = deepcopy(request4)
        r4.pop('namespace_modules')
        gmc = GnmiMessageConstructor('set', r4, **format4)
        self.assertEqual(
            json_format.MessageToDict(gmc.payload),
            json_decoded2
        )
        self.assertEqual(gmc.json_val, json_val_decoded2)

    def test_get_2_paths(self):
        """Verify 2 paths are added to a GET (one with no list key)."""
        r2 = deepcopy(request2)
        gmc = GnmiMessageConstructor('get', r2, **format2)
        self.assertEqual(
            json_format.MessageToDict(gmc.payload),
            dictfrom2
        )

    def test_subscribe_sample(self):
        """Verify subscribe message is constructed properly."""
        r3 = deepcopy(request3)
        gmc = GnmiMessageConstructor('subscribe', r3, **format3)
        self.assertEqual(
            json_format.MessageToDict(gmc.payload),
            subscribe_dict
        )

    def test_raw_set_base64(self):
        """Verify conversion of set dict to gNMI SetRequest."""
        raw_json = json.dumps(raw_set_dict)
        gnmi_msg = GnmiMessageConstructor.json_to_gnmi(
          'set', raw_json, **{'base64': True}
        )
        test_dict = json_format.MessageToDict(gnmi_msg)
        jval = base64.b64decode(test_dict['update'][0]['val']['jsonIetfVal'])
        jval = json.loads(base64.b64decode(jval).decode('utf-8'))
        test_dict['update'][0]['val']['jsonIetfVal'] = jval
        self.assertEqual(test_dict, raw_set_dict)

    def test_raw_set_json(self):
        """Verify conversion of set dict without base64 json_val."""
        raw_json = json.dumps(raw_set_dict)
        gnmi_msg = GnmiMessageConstructor.json_to_gnmi('set', raw_json)
        test_dict = json_format.MessageToDict(gnmi_msg)
        jval = gnmi_msg.update[0].val.json_ietf_val
        jval = json.loads(jval.decode('utf-8'))
        test_dict['update'][0]['val']['jsonIetfVal'] = jval
        self.assertEqual(test_dict, raw_set_dict)

    def test_raw_get(self):
        """Verify conversion of get dict to gNMI GetRequest."""
        raw_json = json.dumps(raw_get_dict)
        gnmi_msg = GnmiMessageConstructor.json_to_gnmi('get', raw_json)
        self.assertEqual(json_format.MessageToDict(gnmi_msg), raw_get_dict)

    def test_raw_subscribe(self):
        """Verify conversion of subscribe dict to gNMI SubscribeRequest."""
        raw_json = json.dumps(raw_subscribe_dict)
        gnmi_msg = GnmiMessageConstructor.json_to_gnmi('subscribe', raw_json)
        self.assertEqual(
          json_format.MessageToDict(gnmi_msg), raw_subscribe_dict
        )


if __name__ == '__main__':
    unittest.main()
