#! /usr/bin/env python
# Python
import unittest
import logging
import sys

from unittest.mock import patch
from collections import OrderedDict

# Genie Libs
from genie.libs.sdk.triggers.blitz.yangexec import run_netconf, run_gnmi, run_restconf
from genie.libs.sdk.triggers.blitz.yangexec_helper import DictionaryToXML, dict_to_ordereddict


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


class TestYangExec(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Mock NETCONF device with server capabilities property
        with patch('yang.connector.netconf.Netconf') as MockNetconfDevice:
            cls.netconf_device = MockNetconfDevice.return_value
            cls.netconf_device.server_capabilities = []
            cls.netconf_device.alias = 'CSR1K-5'
            cls.netconf_device.via = 'yang1'

        # Mock GNMI device
        with patch('yang.connector.gnmi.Gnmi') as MockGnmiDevice:
            cls.gnmi_device = MockGnmiDevice.return_value
            cls.gnmi_device.alias = 'bo86'
            cls.gnmi_device.via = 'yang2'

        # Mock RESTCONF device
        with patch('rest.connector.Rest') as MockRestconfDevice:
            class SuccessfulPatchRequest(object):
                def __init__(self):
                    # Empty Response
                    self.content = b'{}'
                    # Successful PATCH operation
                    self.status_code = 204

            class ErroredPostRequest(object):
                def __init__(self):
                    # Empty response
                    self.content = b'{}'
                    # Server error response status code
                    self.status_code = 500

            class SuccessfulGetRequest(object):
                def __init__(self):
                    # Valid response
                    self.content = b"""{
                        "native": {
                            "version": "17.5"
                        }
                    }"""
                    # Successful GET operation
                    self.status_code = 200

            cls.restconf_device = MockRestconfDevice.return_value
            cls.restconf_device.alias = 'CSR1K-7'
            cls.restconf_device.via = 'yang3'

            cls.restconf_device.patch.return_value = SuccessfulPatchRequest()
            cls.restconf_device.post.return_value = ErroredPostRequest()
            cls.restconf_device.get.return_value = SuccessfulGetRequest()

    def test_run_restconf(self):
        operation = 'edit-config'
        steps = 'STEP 1: Starting action yang on device \'CSR1K-7\''
        datastore = {'type': '', 'lock': True, 'retry': 40}
        returns = {}

        # Test successful PATCH request
        rpc_data = {
            'namespace': {
                'ios': 'http://cisco.com/ns/yang/Cisco-IOS-XE-native'
            },
            'nodes': [{
                'edit-op': 'merge',
                'nodetype': 'leaf',
                'datatype': 'string',
                'value': 'resttest',
                'xpath': '/ios:native/ios:interface/ios:GigabitEthernet[name="2"]/ios:description'
            }]
        }
        result = run_restconf(
            operation, self.restconf_device, steps, datastore, rpc_data, returns
        )
        self.assertEqual(result, True)

        # Test errored/unsuccessful POST request
        errored_post_rpc_data = {
            'namespace': {
                'ios': 'http://cisco.com/ns/yang/Cisco-IOS-XE-native'
            },
            'nodes': [{
                'edit-op': 'create',
                'nodetype': 'leaf',
                'datatype': 'inet:ipv4-address',
                'value': '255.255.255.0',
                'xpath': '/ios:native/ios:interface/ios:GigabitEthernet[name="2"]/ios:ip/ios:address/ios:primary/ios:mask'
            }]
        }
        result = run_restconf(
            operation, self.restconf_device, steps, datastore, errored_post_rpc_data, returns
        )
        self.assertEqual(result, False)

        # Test successful GET request with matching returns
        successful_get_rpc_data = {
            'namespace': {
                'ios': 'http://cisco.com/ns/yang/Cisco-IOS-XE-native'
            },
            'nodes': [{
                'edit-op': 'get',
                'nodetype': 'leaf',
                'datatype': 'string',
                'value': 17.5,
                'xpath': '/ios:native/ios:version'
            }]
        }
        matching_returns = [{
            'id': 1,
            'datatype': 'string',
            'default': '',
            'name': 'version',
            'nodetype': 'leaf',
            'op': '==',
            'selected': 'True',
            'value': 17.5,
            'xpath': '/ios:native/ios:version'
        }]
        result = run_restconf(
            operation, self.restconf_device, steps, datastore, successful_get_rpc_data, matching_returns
        )
        self.assertEqual(result, True)

        # Test successful GET request with non-matching returns
        non_matching_returns = [{
            'id': 1,
            'datatype': 'string',
            'default': '',
            'name': 'version',
            'nodetype': 'list',
            'op': '==',
            'selected': 'True',
            'value': '10.24.69.26',
            'xpath': '/ios:native/ios:version'
        }]
        result = run_restconf(
            operation, self.restconf_device, steps, datastore, successful_get_rpc_data, non_matching_returns
        )
        self.assertEqual(result, False)


    @patch('genie.libs.sdk.triggers.blitz.yangexec.netconf_send')
    def test_run_netconf_subscribe_lxml(self, netconf_send_mock):
        """ Test run_netconf subscribe action with lxml objects."""
        operation = 'subscribe'
        steps = "STEP 1: Starting action yang on device 'CSR1K-5'"
        datastore = {'lock': False, 'retry': 10, 'type': ''}
        rpc_data = {
            'namespace': {
                'notif-bis': 'urn:ietf:params:xml:ns:yang:ietf-event-notifications',
                'yp': 'urn:ietf:params:xml:ns:yang:ietf-yang-push'
            },
            'nodes': [{
                'xpath': '/notif-bis:establish-subscription/notif-bis:stream',
                'value': 'yp:yang-push'
            }, {
                'xpath': '/notif-bis:establish-subscription/yp:xpath-filter',
                'value': '/mdt-oper:mdt-oper-data/mdt-subscriptions'
            }, {
                'xpath': '/notif-bis:establish-subscription/yp:period',
                'value': 1000
            }]
        }
        returns = [{
            'id': 1,
            'name': 'address',
            'op': '==',
            'selected': True,
            'datatype': 'string',
            'value': '10.24.69.26',
            'xpath': '/notification/push-update/datastore-contents-xml/mdt-oper-data/mdt-subscriptions/mdt-receivers/address'
        }, {
            'id': 2,
            'name': 'port',
            'op': 'range',
            'selected': True,
            'datatype': 'uint16',
            'value': '50000 - 60000',
            'xpath': '/notification/push-update/datastore-contents-xml/mdt-oper-data/mdt-subscriptions/mdt-receivers/port'
        }, {
            'id': 3,
            'name': 'protocol',
            'op': '==',
            'selected': True,
            'datatype': 'string',
            'value': 'netconf',
            'xpath': '/notification/push-update/datastore-contents-xml/mdt-oper-data/mdt-subscriptions/mdt-receivers/protocol'
        }, {
            'id': 4,
            'name': 'state',
            'op': '==',
            'selected': True,
            'datatype': 'string',
            'value': 'rcvr-state-connected',
            'xpath': '/notification/push-update/datastore-contents-xml/mdt-oper-data/mdt-subscriptions/mdt-receivers/state'
        }]
        format = {
            'request_mode': 'STREAM',
            'sub_mode': 'ON_CHANGE',
            'encoding': 'JSON',
            'sample_interval': 5,
            'stream_max': 15
        }
        netconf_send_mock.return_value = [(
            'subscribe',
            '''<?xml version="1.0" encoding="UTF-8"?>\n
            <rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:
            base:1.0" message-id="urn:uuid:60a40a42-987d-4159-
            89d6-c67252b20f42" xmlns:nc="urn:ietf:params:xml:
            ns:netconf:base:1.0"><subscription-result xmlns=\'
            urn:ietf:params:xml:ns:yang:ietf-event-notificati
            ons\' xmlns:notif-bis="urn:ietf:params:xml:ns:yang:
            ietf-event-notifications">notif-bis:ok</subscription
            -result>\n<subscription-id xmlns=\'urn:ietf:params:
            xml:ns:yang:ietf-event-notifications\'>2147483760
            </subscription-id>\n</rpc-reply>\''''
        )]
        result = run_netconf(
            operation, self.netconf_device, steps, datastore, rpc_data, returns, format=format
        )

        self.assertEqual(result, True)

    @patch('genie.libs.sdk.triggers.blitz.yangexec.netconf_send')
    def test_run_netconf_subscribe_raw(self, netconf_send_mock):
        """ Test run_netconf subscribe action with string rpc."""
        operation = 'subscribe'
        steps = "STEP 1: Starting action yang on device 'CSR1K-5'"
        datastore = {'lock': False, 'retry': 10, 'type': ''}
        returns = [{
            'id': 1,
            'name': 'address',
            'op': '==',
            'selected': True,
            'datatype': 'string',
            'value': '10.24.69.26',
            'xpath': '/notification/push-update/datastore-contents-xml/mdt-oper-data/mdt-subscriptions/mdt-receivers/address'
        }, {
            'id': 2,
            'name': 'port',
            'op': 'range',
            'selected': True,
            'datatype': 'uint16',
            'value': '50000 - 60000',
            'xpath': '/notification/push-update/datastore-contents-xml/mdt-oper-data/mdt-subscriptions/mdt-receivers/port'
        }, {
            'id': 3,
            'name': 'protocol',
            'op': '==',
            'selected': True,
            'datatype': 'string',
            'value': 'netconf',
            'xpath': '/notification/push-update/datastore-contents-xml/mdt-oper-data/mdt-subscriptions/mdt-receivers/protocol'
        }, {
            'id': 4,
            'name': 'state',
            'op': '==',
            'selected': True,
            'datatype': 'string',
            'value': 'rcvr-state-connected',
            'xpath': '/notification/push-update/datastore-contents-xml/mdt-oper-data/mdt-subscriptions/mdt-receivers/state'
        }]
        format = {
            'request_mode': 'STREAM',
            'sub_mode': 'ON_CHANGE',
            'encoding': 'JSON',
            'sample_interval': 5,
            'stream_max': 15
        }

        rpc_data = {
            'operation': 'subscribe',
            'rpc': """<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101">
                    <establish-subscription xmlns="urn:ietf:params:xml:ns:yang:ietf-event-notifications">
                        <stream xmlns:yp="urn:ietf:params:xml:ns:yang:ietf-yang-push">yp:yang-push</stream>
                        <xpath-filter xmlns="urn:ietf:params:xml:ns:yang:ietf-yang-push">/mdt-oper:mdt-oper-data/mdt-subscriptions</xpath-filter>
                        <period xmlns="urn:ietf:params:xml:ns:yang:ietf-yang-push">1000</period>
                    </establish-subscription>
                </rpc>
            """
        }
        netconf_send_mock.return_value = [(
            'subscribe',
            '''<?xml version="1.0" encoding="UTF-8"?>\n
            <rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:
            base:1.0" message-id="urn:uuid:60a40a42-987d-4159-
            89d6-c67252b20f42" xmlns:nc="urn:ietf:params:xml:
            ns:netconf:base:1.0"><subscription-result xmlns=\'
            urn:ietf:params:xml:ns:yang:ietf-event-notificati
            ons\' xmlns:notif-bis="urn:ietf:params:xml:ns:yang:
            ietf-event-notifications">notif-bis:ok</subscription
            -result>\n<subscription-id xmlns=\'urn:ietf:params:
            xml:ns:yang:ietf-event-notifications\'>2147483760
            </subscription-id>\n</rpc-reply>\''''
        )]
        result = run_netconf(
            operation,  # operation
            self.netconf_device,  # device
            steps,  # steps
            datastore,  # datastore
            rpc_data,  # rpc_data
            returns,  # returns
            format=format  # format
        )

        self.assertEqual(result, True)

    @patch('yang.connector.gnmi.Gnmi.get')
    def test_run_gnmi(self, gnmi_get_mock):
        """ Test run_gnmi with get action and range op """
        operation = 'get'
        steps = "STEP 1: Starting action yang on device 'ncs1004'"
        datastore = {
            'type': '',
            'lock': False,
            'retry': 10
        }
        rpc_data = {
            'namespace': {
                'oc-sys': 'http://openconfig.net/yang/system'
            },
            'nodes': [{
                'xpath': '/oc-sys:system'
            }]
        }
        returns = [{
            'id': 1,
            'name': 'rate-limit',
            'op': 'range',
            'selected': True,
            'datatype': 'integer',
            'value': '50 - 70',
            'xpath': '/system/ssh-server/state/rate-limit'
        }]
        response = [{
            'update': [[
                (True, '/system/ssh-server/state/enable'),
                ('V2', '/system/ssh-server/state/protocol-version'),
                (30, '/system/ssh-server/state/timeout'),
                (64, '/system/ssh-server/state/session-limit'),
                (60, '/system/ssh-server/state/rate-limit'),
                ('NONE', '/system/logging/console/selectors/selector/facility'),
                ('DISABLE', '/system/logging/console/selectors/selector/severity'),
                ('DISABLE', '/system/logging/console/selectors/selector/state/severity'),
                (True, '/system/grpc-server/state/enable'),
                (57400, '/system/grpc-server/state/port'),
                (False, '/system/grpc-server/state/transport-security'),
                ('SM/HW_ENVMON_FAN_ALARM/201#CHASSIS/LCC/1', '/system/alarms/alarm/id'),
                ('SM/HW_ENVMON_FAN_ALARM/201#CHASSIS/LCC/1', '/system/alarms/alarm/state/id'),
                ('0', '/system/alarms/alarm/state/resource'),
                ('Fan: One or more LCs missing, running fans at max speed.', '/system/alarms/alarm/state/text'),
                ('1612588606', '/system/alarms/alarm/state/time-created'),
                ('openconfig-alarm-types:CRITICAL', '/system/alarms/alarm/state/severity'),
                ('openconfig-alarm-types:HW_ENVMON_RM_LC_REMOVAL', '/system/alarms/alarm/state/type-id'),
                ('SYSTEM/HW_ERROR/82#CHASSIS/LCC/1:CONTAINER/LC/1', '/system/alarms/alarm/id'),
                ('SYSTEM/HW_ERROR/82#CHASSIS/LCC/1:CONTAINER/LC/1', '/system/alarms/alarm/state/id'),
                ('0/0', '/system/alarms/alarm/state/resource'), ('Verification of SUDI Certificate Failed On LC.', '/system/alarms/alarm/state/text'),
                ('1612590967', '/system/alarms/alarm/state/time-created'), ('openconfig-alarm-types:MAJOR', '/system/alarms/alarm/state/severity'),
                ('openconfig-alarm-types:LC_SUDI_FAILURE', '/system/alarms/alarm/state/type-id'),
                ('SYSTEM/HW_ERROR/12#CHASSIS/LCC/1:CONTAINER/LC/4', '/system/alarms/alarm/id'),
                ('SYSTEM/HW_ERROR/12#CHASSIS/LCC/1:CONTAINER/LC/4', '/system/alarms/alarm/state/id'),
                ('0/3', '/system/alarms/alarm/state/resource'),
                ('LC_CPU_MOD_FW is corrupt, system booted with golden copy.', '/system/alarms/alarm/state/text'),
                ('1612590967', '/system/alarms/alarm/state/time-created'),
                ('openconfig-alarm-types:MAJOR', '/system/alarms/alarm/state/severity'),
                ('openconfig-alarm-types:LC_CPU_CORRUPTION', '/system/alarms/alarm/state/type-id'),
                ('root', '/system/aaa/authentication/users/user/username'),
                ('root', '/system/aaa/authentication/users/user/state/username'),
                ('root-lr', '/system/aaa/authentication/users/user/state/role'),
                ('$6$O/qa30UhNVPK630.$fwZsgRvyIkhIAcwwhaaAEbQEggRCNaEMHbUayTvJzPb9MNBsxXjVVJ76R8.t2K/fkz6RnONCa8/EOff2XaxO7.', '/system/aaa/authentication/users/user/state/password-hashed')
            ]]
        }]

        format = {
            'auto-validate': False
        }

        gnmi_get_mock.return_value = response
        result = run_gnmi(
            operation, self.gnmi_device, steps, datastore, rpc_data, returns, format=format
        )

        self.assertEqual(result, True)

    def test_dict_to_ordereddict(self):
        valid_dictionary = {
            'native': {
                'version': '17.5',
                'username': [{
                    'name': 'test',
                    'privilege': 15
                }],
                'memory': {
                    'free': {
                        'low-watermark': {
                            'processor': 69201
                        }
                    }
                }
            }
        }
        empty_input = {}
        none_input = None
        list_input = ['item1', 'item2', 'item3']

        expected_valid_ordereddict = OrderedDict([
            ('native', OrderedDict([
                ('version', '17.5'),
                ('username', [OrderedDict([
                    ('name', 'test'),
                    ('privilege', 15)])]
                ),
                ('memory', OrderedDict([
                    ('free', OrderedDict([
                        ('low-watermark', OrderedDict([
                            ('processor', 69201)]))
                        ])
                    )])
                )
            ]))
        ])

        actual_valid_ordereddict = dict_to_ordereddict(valid_dictionary)
        actual_empty_result = dict_to_ordereddict(empty_input)
        actual_none_result = dict_to_ordereddict(none_input)
        actual_list_result = dict_to_ordereddict(list_input)

        # Expect valid dictionary input to match expected output, and not None
        self.assertEqual(actual_valid_ordereddict, expected_valid_ordereddict)
        self.assertNotEqual(actual_valid_ordereddict, None)
        # Expect the result will be empty OrderedDict if the input was empty dictionary
        self.assertEqual(actual_empty_result, OrderedDict())
        # Expect the result will be None if None is the input, and itself
        self.assertEqual(actual_none_result, None)
        self.assertEqual(actual_none_result, none_input)
        # Expect the result will be itself if list is the input
        self.assertEqual(actual_list_result, list_input)

if __name__ == '__main__':
    unittest.main()
