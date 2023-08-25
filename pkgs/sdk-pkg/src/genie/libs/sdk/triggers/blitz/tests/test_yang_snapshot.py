import os
import unittest

from lxml import etree
from ncclient import xml_
from genie import testbed
from unittest.mock import Mock
from genie.libs.sdk.triggers.blitz.yang_snapshot import YangSnapshot


class Testcase(object):

    def __init__(self):
        self.parent = Mock()
        self.parent.triggers = {
            'cisco_ios_xe_ntp_00077_native_ntp_peer_ipv6_basic_create': {
                'source': {
                    'class': 'triggers.blitz.blitz.Blitz',
                    'pkg': 'genie.libs.sdk',
                },
                'test_sections': [{
                    'take_snapshot': [
                        {
                            'yang_snapshot': {
                                'banner': 'TAKE YANG SNAPSHOT 1',
                                'connection': 'netconf',
                                'device': 'uut',
                                'protocol': 'netconf',
                            }
                        },
                        {
                            'sleep': {
                                'log': 'Sleeping for 2 seconds...',
                                'sleep_time': 2.0,
                            }
                        },
                        {
                            'configure': {
                                'banner': 'CLI CONFIGURE',
                                'command': 'logging console',
                                'device': 'uut'
                            }
                        },
                        {
                            'yang_snapshot': {
                                'banner': 'TAKE YANG SNAPSHOT 2',
                                'connection': 'netconf',
                                'device': 'uut',
                                'protocol': 'netconf',
                            }
                        },
                        {
                            'yang': {
                                'banner': 'YANG EDIT-CONFIG',
                                'connection': 'netconf',
                                'content': {
                                    'namespace': {
                                        'ios': 'http://cisco.com/ns/yang'
                                               '/Cisco-IOS-XE-native',
                                        'ios-ntp': 'http://cisco.com/ns/yang'
                                                   '/Cisco-IOS-XE-ntp',
                                    },
                                    'nodes': [
                                        {
                                            'datatype': 'string',
                                            'edit-op': 'create',
                                            'nodetype': 'leaf',
                                            'value': 'genericstring',
                                            'xpath': '/ios:native/ios:ntp'
                                            '/ios-ntp:peer/ios-ntp:ipv6'
                                            '[ios-ntp:host-name='
                                            '"genericstring"]'
                                            '/ios-ntp:source'
                                        },
                                        {
                                            'datatype': 'empty',
                                            'edit-op': 'merge',
                                            'nodetype': 'leaf',
                                            'xpath': '/ios:native/ios:ntp'
                                            '/ios-ntp:peer/ios-ntp:ipv6'
                                            '[ios-ntp:host-name='
                                            '"genericstring"]'
                                            '/ios-ntp:burst-opt',
                                        }
                                    ]
                                },
                                'datastore': {
                                    'lock': True,
                                    'retry': 10,
                                    'type': '',
                                },
                                'device': 'uut',
                                'format': {
                                    'auto_validate': True,
                                    'negative_test': False,
                                    'pause': 0,
                                    'timeout': 30,
                                },
                                'operation': 'edit-config',
                                'protocol': 'netconf'
                            }
                        },
                        {
                            'sleep': {
                                'log': 'Sleeping for 12 seconds...',
                                'sleep_time': 12.0,
                            }
                        },
                        {
                            'configure': {
                                'banner': 'CLI CONFIGURE',
                                'command': 'logging console',
                                'device': 'uut',
                            }
                        },
                        {
                            'yang': {
                                'banner': 'YANG EDIT-CONFIG',
                                'connection': 'netconf',
                                'content': {
                                    'namespace': {
                                        'ios': 'http://cisco.com/ns/yang'
                                        '/Cisco-IOS-XE-native',
                                        'ios-ntp': 'http://cisco.com/ns'
                                        '/yang/Cisco-IOS-XE-ntp',
                                    },
                                    'nodes': [
                                        {
                                            'datatype': 'string',
                                            'edit-op': 'merge',
                                            'nodetype': 'leaf',
                                            'value': 'GigabitEthernet2',
                                            'xpath': '/ios:native/ios:ntp'
                                            '/ios-ntp:peer/ios-ntp:ipv6'
                                            '[ios-ntp:host-name='
                                            '"genericstring"]'
                                            '/ios-ntp:source',
                                        },
                                        {
                                            'datatype': 'empty',
                                            'edit-op': 'merge',
                                            'nodetype': 'leaf',
                                            'xpath': '/ios:native/ios:ntp'
                                            '/ios-ntp:peer/ios-ntp:ipv6'
                                            '[ios-ntp:host-name='
                                            '"genericstring"]'
                                            '/ios-ntp:burst-opt',
                                        }
                                    ]
                                },
                                'datastore': {
                                    'lock': True,
                                    'retry': 10,
                                    'type': '',
                                },
                                'device': 'uut',
                                'format': {
                                    'auto_validate': True,
                                    'negative_test': False,
                                    'pause': 0,
                                    'timeout': 30,
                                },
                                'operation': 'edit-config',
                                'protocol': 'netconf',
                            }
                        }
                    ]
                }]
            },
            'cisco_ios_xe_ntp_00077_native_ntp_peer_ipv6_'
            'yang_snapshot_restore': {
                'source': {
                    'pkg': 'genie.libs.sdk',
                    'class': 'triggers.blitz.blitz.Blitz'
                },
                'test_sections': [{
                    'restore_snapshot': [{
                        'yang_snapshot_restore': {
                            'device': 'uut',
                            'connection': 'netconf',
                            'protocol': 'netconf',
                            'banner': 'RESTORE YANG SNAPSHOT 2',
                        }
                    }]
                }]
            },
        }
        self.uid = 'cisco_ios_xe_ntp_00077_native_ntp_peer_ipv6_' \
                   'basic_create.uut'


class Parameters(object):

    def __init__(self):
        self.data = [
            {
                'yang_snapshot': {
                    'banner': 'TAKE YANG SNAPSHOT 1',
                    'connection': 'netconf',
                    'device': 'uut',
                    'protocol': 'netconf',
                }
            },
            {
                'sleep': {
                    'log': 'Sleeping for 2 seconds...',
                    'sleep_time': 2.0,
                }
            },
            {
                'configure': {
                    'banner': 'CLI CONFIGURE',
                    'command': 'logging console',
                    'device': 'uut',
                }
            },
            {
                'yang_snapshot': {
                    'banner': 'TAKE YANG SNAPSHOT 2',
                    'connection': 'netconf',
                    'device': 'uut',
                    'protocol': 'netconf',
                }
            },
            {
                'yang': {
                    'banner': 'YANG EDIT-CONFIG',
                    'connection': 'netconf',
                    'content': {
                        'namespace': {
                            'ios': 'http://cisco.com/ns/yang'
                            '/Cisco-IOS-XE-native',
                            'ios-ntp': 'http://cisco.com/ns/yang'
                            '/Cisco-IOS-XE-ntp'
                        },
                        'nodes': [
                            {
                                'datatype': 'string',
                                'edit-op': 'create',
                                'nodetype': 'leaf',
                                'value': 'genericstring',
                                'xpath': '/ios:native/ios:ntp/ios-ntp:peer'
                                '/ios-ntp:ipv6[ios-ntp:host-name='
                                '"genericstring"]/ios-ntp:source'
                            },
                            {
                                'datatype': 'empty',
                                'edit-op': 'merge',
                                'nodetype': 'leaf',
                                'xpath': '/ios:native/ios:ntp/ios-ntp:peer'
                                '/ios-ntp:ipv6[ios-ntp:host-name='
                                '"genericstring"]/ios-ntp:burst-opt',
                            }
                        ]
                    },
                    'datastore': {
                        'lock': True,
                        'retry': 10,
                        'type': ''
                    },
                    'device': 'uut',
                    'format': {
                        'auto_validate': True,
                        'negative_test': False,
                        'pause': 0,
                        'timeout': 30
                    },
                    'operation': 'edit-config',
                    'protocol': 'netconf'
                }
            },
            {
                'sleep': {
                    'log': 'Sleeping for 12 seconds...',
                    'sleep_time': 12.0
                }
            },
            {
                'configure': {
                    'banner': 'CLI CONFIGURE',
                    'command': 'logging console',
                    'device': 'uut',
                }
            },
            {
                'yang': {
                    'banner': 'YANG EDIT-CONFIG',
                    'connection': 'netconf',
                    'content': {
                        'namespace': {
                            'ios': 'http://cisco.com/ns/yang'
                            '/Cisco-IOS-XE-native',
                            'ios-ntp': 'http://cisco.com/ns/yang'
                            '/Cisco-IOS-XE-ntp'
                        },
                        'nodes': [
                            {
                                'datatype': 'string',
                                'edit-op': 'merge',
                                'nodetype': 'leaf',
                                'value': 'GigabitEthernet2',
                                'xpath': '/ios:native/ios:ntp/ios-ntp:peer'
                                '/ios-ntp:ipv6[ios-ntp:host-name='
                                '"genericstring"]/ios-ntp:source'
                            },
                            {
                                'datatype': 'empty',
                                'edit-op': 'merge',
                                'nodetype': 'leaf',
                                'xpath': '/ios:native/ios:ntp/ios-ntp:peer'
                                '/ios-ntp:ipv6[ios-ntp:host-name='
                                '"genericstring"]/ios-ntp:burst-opt'
                            }
                        ]
                    },
                    'datastore': {
                        'lock': True,
                        'retry': 10,
                        'type': ''
                    },
                    'device': 'uut',
                    'format': {
                        'auto_validate': True,
                        'negative_test': False,
                        'pause': 0,
                        'timeout': 30,
                    },
                    'operation': 'edit-config',
                    'protocol': 'netconf'
                }
            }
        ]

    def get(self, key):
        if key == 'data':
            return self.data


class TestSection(object):

    def __init__(self):
        self.parameters = Parameters()
        self.uid = 'take_snapshot'


class Steps(object):

    def __init__(self):
        self.index = '4'


class Netconf(object):

    def __init__(self):
        self.server_capabilities = []
        self.alias = 'netconf'
        self.via = 'yang'
        self.name = 'anything'

    def get_config(*args, **kwargs):
        return NetconfReply()


class NetconfReply(object):

    def __init__(self):
        self.ok = True
        reply = """
        <data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
          <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"/>
        </data>
        """
        self.data_ele = etree.ElementTree(xml_.to_ele(reply))


class TestYangSnapshot(unittest.TestCase):

    def setUp(self):
        dir_name = os.path.dirname(os.path.abspath(__file__))
        self.testbed = testbed.load(os.path.join(
            dir_name, 'mock_testbeds/testbed.yaml'))
        self.device = self.testbed.devices['PE1']
        self.testcase = Testcase()
        self.section = TestSection()
        self.steps = Steps()
        self.kwargs = {
            'connection': 'netconf',
            'protocol': 'netconf',
            'ret_dict': {
                'device': 'CSR117',
                'continue_': True,
                'action': 'yang_snapshot',
                'saved_vars': {},
            }
        }
        self.yang_snapshot = YangSnapshot(self.device)
        self.device.netconf = Netconf()
        self.data = [{
            'yang': {
                'banner': 'YANG EDIT-CONFIG',
                'connection': 'netconf',
                'content': {
                    'namespace': {
                        'ios': 'http://cisco.com/ns/yang/Cisco-IOS-XE-native',
                        'ios-ntp': 'http://cisco.com/ns/yang/Cisco-IOS-XE-ntp'
                    },
                    'nodes': [
                        {
                            'datatype': 'string',
                            'edit-op': 'merge',
                            'nodetype': 'leaf',
                            'value': 'GigabitEthernet2',
                            'xpath': '/ios:native/ios:ntp/ios-ntp:peer'
                            '/ios-ntp:ipv6[ios-ntp:host-name='
                            '"genericstring"]/ios-ntp:source'
                        },
                        {
                            'datatype': 'empty',
                            'edit-op': 'merge',
                            'nodetype': 'leaf',
                            'xpath': '/ios:native/ios:ntp/ios-ntp:peer'
                            '/ios-ntp:ipv6[ios-ntp:host-name='
                            '"genericstring"]/ios-ntp:burst-opt'
                        }
                    ]
                },
                'datastore': {
                    'lock': True,
                    'retry': 10,
                    'type': ''
                },
                'device': 'uut',
                'format': {
                    'auto_validate': True,
                    'negative_test': False,
                    'pause': 0,
                    'timeout': 30,
                },
                'operation': 'edit-config',
                'protocol': 'netconf'
            }
        }]
        self.yang_snapshot.snapshot(
            testcase=self.testcase,
            device=self.device,
            steps=self.steps,
            section=self.section,
        )

    def test_snapshot(self):
        self.assertTrue(bool(self.yang_snapshot.pre_config))
        self.assertDictEqual(self.yang_snapshot.namespace, {
            'ios': 'http://cisco.com/ns/yang/Cisco-IOS-XE-native',
            'ios-ntp': 'http://cisco.com/ns/yang/Cisco-IOS-XE-ntp',
        })

    def test_register(self):
        self.yang_snapshot.register(
            device=self.device,
            connection='netconf',
            protocol='netconf',
            operation='edit-config',
            content=self.data[0]['yang']['content'],
        )
        self.assertIn('PE1', self.yang_snapshot.xpath)
        self.assertIn(
            '/ios:native/ios:ntp/ios-ntp:peer'
            '/ios-ntp:ipv6[ios-ntp:host-name="genericstring"]'
            '/ios-ntp:burst-opt',
            self.yang_snapshot.xpath['PE1']
        )
        self.assertIn(
            '/ios:native/ios:ntp/ios-ntp:peer'
            '/ios-ntp:ipv6[ios-ntp:host-name="genericstring"]'
            '/ios-ntp:source',
            self.yang_snapshot.xpath['PE1']
        )

    def test_get_root(self):
        output = self.yang_snapshot.get_root(
            '/ios:native/ios:ntp/ios-ntp:peer'
            '/ios-ntp:ipv6[ios-ntp:host-name="genericstring"]'
            '/ios-ntp:burst-opt'
        )
        self.assertEqual(output, 'ios:native')

    def test_split_tag(self):
        prefix, id = self.yang_snapshot.split_tag('ios:native')
        self.assertEqual(prefix, 'ios')
        self.assertEqual(id, 'native')

    def test_build_rpc(self):
        self.yang_snapshot.register(
            device=self.device,
            connection='netconf',
            protocol='netconf',
            operation='edit-config',
            content=self.data[0]['yang']['content'],
        )
        rpc_args = self.yang_snapshot.build_rpc(set([
            '/ios:native/ios:ntp/ios-ntp:peer'
            '/ios-ntp:ipv6[ios-ntp:host-name="genericstring"]'
        ]))
        self.assertEqual(rpc_args['target'], 'running')
        self.assertIsInstance(rpc_args['config'], etree._Element)
        output = rpc_args['config'].xpath(
            '//ios:native/ios:ntp/ios-ntp:peer'
            '/ios-ntp:ipv6[ios-ntp:host-name="genericstring"]',
            namespaces=self.yang_snapshot.namespace,
        )
        self.assertEqual(len(output), 1)
        e = output[0]
        self.assertTrue(
            '{urn:ietf:params:xml:ns:netconf:base:1.0}operation' in e.attrib
        )
        self.assertEqual(
            e.attrib['{urn:ietf:params:xml:ns:netconf:base:1.0}operation'],
            'remove',
        )
