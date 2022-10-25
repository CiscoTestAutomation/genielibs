#! /usr/bin/env python
# Python
import unittest
import logging
import sys
import json

from unittest.mock import patch
from collections import OrderedDict
import yang
from cisco_gnmi import proto
from google.protobuf import json_format

# Genie Libs
from genie.libs.sdk.triggers.blitz.yangexec import run_netconf, run_gnmi, run_restconf
from genie.libs.sdk.triggers.blitz.yangexec_helper import DictionaryToXML, dict_to_ordereddict
from genie.libs.sdk.triggers.blitz.gnmi_util import GnmiNotification, GnmiMessage, GnmiMessageConstructor
from genie.libs.sdk.triggers.blitz.rpcverify import RpcVerify


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


class Service:
    def __init__(self, response):
        self.response = response

    def Get(self, blah, metadata=None):
        return self.response


class Gnmi:
    def __init__(self, response):
        self.response = response
        self.service = Service(response)


class Default:
    default = {'username': 'test', 'password': 'password'}


class Creds:
    credentials = Default()


class TestDevice:
    device = Creds()

    def __init__(self, response):
        self.gnmi = Gnmi(response)


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

    def test_run_get_gnmi(self):
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
                'xpath': '/oc-sys:system/oc-sys:ssh-server/oc-sys:state/oc-sys:rate-limit'
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

        format = {
            'auto-validate': False
        }
        response = proto.gnmi_pb2.GetResponse()
        upd = {
          'path': {
            'elem': [
                {
                'name': "system"
                },
                {
                  'name': "ssh-server"
                },
                {
                  'name': "state"
                },
                {
                  'name': "rate-limit"
                }
            ]
          }
        }
        update = json_format.ParseDict(
            upd,
            proto.gnmi_pb2.Update()
        )
        update.val.json_ietf_val = json.dumps(60).encode('utf-8')
        notif = proto.gnmi_pb2.Notification()
        notif.update.append(update)
        response.notification.append(notif)
        device = TestDevice(response)

        result = run_gnmi(
            operation, device, steps, datastore, rpc_data, returns, format=format
        )

        self.assertEqual(result, True)

    def test_run_subscribe_once_gnmi(self):
        """ Test GNMI Subscribe ONCE mode for Subscription List"""

        rpc_verify = RpcVerify(log=log, capabilities=[])
        operation = "subscribe"
        request = {
                    'namespace': 
                    {
                        'top': 'Cisco-NX-OS-device'
                    }, 
                    'nodes': 
                    [
                        {
                            'nodetype': 'leaf',
                            'datatype': '',
                            'xpath': 'System/igmp-items/inst-items/bootupDelay',
                            'name': 'bootupDelay',
                            'value': ''
                        }, 
                        {
                            'nodetype': 'leaf', 
                            'datatype': '', 
                            'xpath': 'System/igmp-items/inst-items/flushRoute', 
                            'name': 'flushRoute', 'value': ''
                        }
                    ], 
                    'request_mode': 'ONCE', 
                    'sub_mode': 'SAMPLE', 
                    'negative_test': False, 
                    'encoding': 'JSON', 
                    'returns': 
                    [
                        {
                            'datatype': 'ipmc_BootupDelay', 
                            'nodetype': 'leaf', 
                            'name': 'bootupDelay', 
                            'op': '==', 
                            'selected': 'True', 
                            'value': 0, 
                            'xpath': '/System/igmp-items/inst-items/bootupDelay'
                        }, 
                        {
                            'datatype': 'boolean', 
                            'nodetype': 'leaf', 
                            'name': 'flushRoute', 
                            'op': '==', 
                            'selected': 'True', 
                            'value': 'False', 
                            'xpath': '/System/igmp-items/inst-items/flushRoute'
                        }
                    ], 
                    'verifier': rpc_verify.process_operational_state, 
                    'namespace_modules': 
                    {
                        'top': 'Cisco-NX-OS-device'
                    }, 
                    'decode': GnmiMessage.decode_notification, 
                    'log': log
                }

        # Response 1
        path_elem1 = proto.gnmi_pb2.PathElem()
        path_elem1.KeyEntry.key = ""
        path_elem1.KeyEntry.value = ""
        path_elem1.name = "System"
        
        path1 = proto.gnmi_pb2.Path()
        path1.origin = "device"
        path1.elem.append(path_elem1)

        val1 = {
                'igmp-items': 
                {
                    'inst-items': 
                    {
                        'bootupDelay': 0
                    }
                }
            }
        val1 = json.dumps(val1).encode('utf-8')

        value1 = proto.gnmi_pb2.TypedValue()
        value1.json_val = val1

        update1 = proto.gnmi_pb2.Update()
        update1.path.MergeFrom(path1)
        update1.val.MergeFrom(value1)

        notification1 = proto.gnmi_pb2.Notification()
        notification1.timestamp = 0
        notification1.prefix.MergeFrom(proto.gnmi_pb2.Path())
        notification1.update.append(update1)

        response1 = proto.gnmi_pb2.SubscribeResponse()
        response1.update.MergeFrom(notification1)

        # Response 2
        path_elem2 = proto.gnmi_pb2.PathElem()
        path_elem2.KeyEntry.key = ""
        path_elem2.KeyEntry.value = ""
        path_elem2.name = "System"
        
        path2 = proto.gnmi_pb2.Path()
        path2.origin = "device"
        path2.elem.append(path_elem2)

        val2 = {
                'igmp-items': 
                {
                    'inst-items': 
                    {
                        'flushRoute': 'false'
                    }
                }
            }
        val2 = json.dumps(val2).encode('utf-8')

        value2 = proto.gnmi_pb2.TypedValue()
        value2.json_val = val2

        update2 = proto.gnmi_pb2.Update()
        update2.path.MergeFrom(path2)
        update2.val.MergeFrom(value2)

        notification2 = proto.gnmi_pb2.Notification()
        notification2.timestamp = 0
        notification2.prefix.MergeFrom(proto.gnmi_pb2.Path())
        notification2.update.append(update2)

        response2 = proto.gnmi_pb2.SubscribeResponse()
        response2.update.MergeFrom(notification2)

        # Response 3
        response3 = proto.gnmi_pb2.SubscribeResponse()
        response3.sync_response = True
    
        # initiate subscription thread
        subscribe_thread = GnmiNotification(
            [response1, response2, response3],
            **request
        )
        subscribe_thread.start()

        # Wait till the thread is stopped.
        subscribe_thread.join()

        # Test the result
        self.assertEqual(subscribe_thread.result, True)

    def test_run_subscribe_stream_gnmi(self):
        """ Test GNMI STREAM Subscribe for invalid xpath"""

        rpc_verify = RpcVerify(log=log, capabilities=[])
        operation = "subscribe"
        request = {
                    'namespace': 
                        {
                            'top': 'Cisco-NX-OS-device'
                        }, 
                    'nodes': 
                        [
                            {
                                'nodetype': 'leaf',
                                'datatype': '',
                                'xpath': 'System/invalid-path',
                            }
                        ], 
                    'request_mode': 'STREAM', 
                    'sub_mode': 'SAMPLE', 
                    'negative_test': False, 
                    'encoding': 'JSON',
                    'sample_interval': 1,
                    'stream_max': 5,
                    'returns':
                        [
                            {
                                'datatype': 'boolean',
                                'value': 'true',
                                'op': '==',
                                'selected': 'True',
                                'name': 'heavyTemplate',
                                'xpath': '/System/igmp-items/inst-items/heavyTemplate'
                            }
                        ], 
                    'verifier': rpc_verify.process_operational_state,
                    'namespace_modules': 
                        {
                            'top': 'Cisco-NX-OS-device'
                        }, 
                    'decode': GnmiMessage.decode_notification, 
                    'log': log
                }

        # Response
        response = proto.gnmi_pb2.SubscribeResponse()
        response.sync_response = True
    
        # initiate subscription thread
        subscribe_thread = GnmiNotification(
            [response],
            **request
        )
        subscribe_thread.start()

        # Wait till the thread is stopped
        while not subscribe_thread.stopped():
            log.info('Waiting for notification...')

        # Test the result
        self.assertEqual(subscribe_thread.result, False)

    def test_run_subscribe_once_gnmi_list(self):
        """ Test GNMI Subscribe for list xpaths ONCE mode for Subscription List"""

        rpc_verify = RpcVerify(log=log, capabilities=[])
        operation = "subscribe"
        request = {
                    'namespace': 
                        {
                            'top': 'Cisco-NX-OS-device'
                        }, 
                    'nodes': 
                        [
                            {
                                'nodetype': 'leaf',
                                'datatype': '',
                                'xpath': 'System/igmp-items/inst-items/dom-items/Dom-list[name="default"]/eventHist-items/EventHistory-list[type="nbm"]/size',
                                'name': 'size',
                                'value': ''
                            }, 
                            {
                                'nodetype': 'leaf', 
                                'datatype': '', 
                                'xpath': 'System/igmp-items/inst-items/dom-items/Dom-list[name="default"]/eventHist-items/EventHistory-list[type="intfDebugs"]/size', 
                                'name': 'size', 
                                'value': ''
                            }
                        ], 
                    'request_mode': 'ONCE', 
                    'sub_mode': 'SAMPLE', 
                    'negative_test': False, 
                    'encoding': 'JSON', 
                    'returns': 
                        [
                            {
                                'datatype': '', 
                                'nodetype': 'leaf', 
                                'name': 'type', 
                                'op': '==', 
                                'selected': 'True', 
                                'value': 'nbm', 
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/type'
                            }, 
                            {
                                'datatype': 'uint32',
                                'nodetype': 'leaf', 
                                'name': 'size', 
                                'op': '==',
                                'selected': 'True', 
                                'value': 4, 
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/size'
                            },
                            {
                                'datatype': '', 
                                'nodetype': 'leaf', 
                                'name': 'type', 
                                'op': '==', 
                                'selected': 'True', 
                                'value': 'intfDebugs', 
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/type'
                            }, 
                            {
                                'datatype': 'uint32',
                                'nodetype': 'leaf', 
                                'name': 'size', 
                                'op': '==',
                                'selected': 'True', 
                                'value': 3, 
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/size'
                            }
                        ], 
                    'verifier': rpc_verify.process_operational_state,
                    'namespace_modules': 
                        {
                            'top': 'Cisco-NX-OS-device'
                        }, 
                    'decode': GnmiMessage.decode_notification, 
                    'log': log
                }

        # Response 1
        path_elem1 = proto.gnmi_pb2.PathElem()
        path_elem1.KeyEntry.key = ""
        path_elem1.KeyEntry.value = ""
        path_elem1.name = "System"
        
        path1 = proto.gnmi_pb2.Path()
        path1.origin = "device"
        path1.elem.append(path_elem1)

        val1 = {
                "igmp-items":
                    {
                    "inst-items":
                        {
                        "dom-items":
                            {
                            "Dom-list":
                                [
                                    {
                                    "name":"default",
                                    "eventHist-items":
                                        {
                                        "EventHistory-list":
                                            [
                                                {
                                                    "type":"nbm",
                                                    "size":4
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
        val1 = json.dumps(val1).encode('utf-8')

        value1 = proto.gnmi_pb2.TypedValue()
        value1.json_val = val1

        update1 = proto.gnmi_pb2.Update()
        update1.path.MergeFrom(path1)
        update1.val.MergeFrom(value1)

        notification1 = proto.gnmi_pb2.Notification()
        notification1.timestamp = 0
        notification1.prefix.MergeFrom(proto.gnmi_pb2.Path())
        notification1.update.append(update1)

        response1 = proto.gnmi_pb2.SubscribeResponse()
        response1.update.MergeFrom(notification1)

        # Response 2
        path_elem2 = proto.gnmi_pb2.PathElem()
        path_elem2.KeyEntry.key = ""
        path_elem2.KeyEntry.value = ""
        path_elem2.name = "System"
        
        path2 = proto.gnmi_pb2.Path()
        path2.origin = "device"
        path2.elem.append(path_elem2)

        val2 = {
                "igmp-items":
                    {
                    "inst-items":
                        {
                        "dom-items":
                            {
                            "Dom-list":
                                [
                                    {
                                    "name":"default",
                                    "eventHist-items":
                                        {
                                        "EventHistory-list":
                                            [
                                                {
                                                    "type":"intfDebugs",
                                                    "size": 3
                                                }
                                            ]
                                        }
                                }   
                                ]
                            }
                        }
                    }
                }
        val2 = json.dumps(val2).encode('utf-8')

        value2 = proto.gnmi_pb2.TypedValue()
        value2.json_val = val2

        update2 = proto.gnmi_pb2.Update()
        update2.path.MergeFrom(path2)
        update2.val.MergeFrom(value2)

        notification2 = proto.gnmi_pb2.Notification()
        notification2.timestamp = 0
        notification2.prefix.MergeFrom(proto.gnmi_pb2.Path())
        notification2.update.append(update2)

        response2 = proto.gnmi_pb2.SubscribeResponse()
        response2.update.MergeFrom(notification2)

        # Response 3
        response3 = proto.gnmi_pb2.SubscribeResponse()
        response3.sync_response = True
    
        # initiate subscription thread
        subscribe_thread = GnmiNotification(
            [response1, response2, response3],
            **request
        )
        subscribe_thread.start()
        
        # Wait till the thread is stopped.
        subscribe_thread.join()

        # Test the result
        self.assertEqual(subscribe_thread.result, True)

    def test_run_subscribe_once_2_gnmi(self):
        """ Test GNMI Subscribe ONCE mode for Container having multiple lists"""

        rpc_verify = RpcVerify(log=log, capabilities=[])
        operation = "subscribe"
        request = {
                    'namespace': 
                        {
                            'top': 'Cisco-NX-OS-device'
                        }, 
                    'nodes':
                        [
                            {
                                'nodetype': 'container',
                                'datatype': '',
                                'xpath': 'System/igmp-items/inst-items/dom-items/Dom-list[name="default"]/eventHist-items',
                                'name': '',
                                'value': ''
                            }
                        ], 
                    'request_mode': 'ONCE', 
                    'sub_mode': 'SAMPLE', 
                    'negative_test': False, 
                    'encoding': 'JSON', 
                    'returns': 
                        [
                            {
                                'nodetype': 'leaf',
                                'datatype': '',
                                'value': 'cli',
                                'op': '==',
                                'selected': 'True',
                                'name': 'type',
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/type'
                            },
                            {
                                'nodetype': 'leaf',
                                'datatype': 'igmp_Size',
                                'value': 20,
                                'op': '==',
                                'selected': 'True',
                                'name': 'size',
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/size'
                            },
                            {
                                'nodetype': 'leaf',
                                'datatype': '',
                                'value': 'groupDebugs',
                                'op': '==',
                                'selected': 'True',
                                'name': 'type',
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/type'
                            },
                            {
                                'nodetype': 'leaf',
                                'datatype': 'igmp_Size',
                                'value': 20,
                                'op': '==',
                                'selected': 'True',
                                'name': 'size',
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/size'
                            },
                            {
                                'nodetype': 'leaf',
                                'datatype': '',
                                'value': 'groupEvents',
                                'op': '==',
                                'selected': 'True',
                                'name': 'type',
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/type'
                            },
                            {
                                'nodetype': 'leaf',
                                'datatype': 'igmp_Size',
                                'value': 20,
                                'op': '==',
                                'selected': 'True',
                                'name': 'size',
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/size'
                            },
                            {
                                'nodetype': 'leaf',
                                'datatype': '',
                                'value': 'ha',
                                'op': '==',
                                'selected': 'True',
                                'name': 'type',
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/type'
                            },
                            {
                                'nodetype': 'leaf',
                                'datatype': 'igmp_Size',
                                'value': 20,
                                'op': '==',
                                'selected': 'True',
                                'name': 'size',
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/size'
                            },
                            {
                                'nodetype': 'leaf',
                                'datatype': '',
                                'value': 'intfDebugs',
                                'op': '==',
                                'selected': 'True',
                                'name': 'type',
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/type'
                            },
                            {
                                'nodetype': 'leaf',
                                'datatype': 'igmp_Size',
                                'value': 20,
                                'op': '==',
                                'selected': 'True',
                                'name': 'size',
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/size'
                            },
                            {
                                'nodetype': 'leaf',
                                'datatype': '',
                                'value': 'intfEvents',
                                'op': '==',
                                'selected': 'True',
                                'name': 'type',
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/type'
                            },
                            {
                                'nodetype': 'leaf',
                                'datatype': 'igmp_Size',
                                'value': 20,
                                'op': '==',
                                'selected': 'True',
                                'name': 'size',
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/size'
                            },
                            {
                                'nodetype': 'leaf',
                                'datatype': '',
                                'value': 'mtrace',
                                'op': '==',
                                'selected': 'True',
                                'name': 'type',
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/type'
                            },
                            {
                                'nodetype': 'leaf',
                                'datatype': 'igmp_Size',
                                'value': 20,
                                'op': '==',
                                'selected': 'True',
                                'name': 'size',
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/size'
                            },
                            {
                                'nodetype': 'leaf',
                                'datatype': '',
                                'value': 'mvr',
                                'op': '==',
                                'selected': 'True',
                                'name': 'type',
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/type'
                            },
                            {
                                'nodetype': 'leaf',
                                'datatype': 'igmp_Size',
                                'value': 20,
                                'op': '==',
                                'selected': 'True',
                                'name': 'size',
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/size'
                            },
                            {
                                'nodetype': 'leaf',
                                'datatype': '',
                                'value': 'policy',
                                'op': '==',
                                'selected': 'True',
                                'name': 'type',
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/type'
                            },
                            {
                                'nodetype': 'leaf',
                                'datatype': 'igmp_Size',
                                'value': 20,
                                'op': '==',
                                'selected': 'True',
                                'name': 'size',
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/size'
                            },
                            {
                                'nodetype': 'leaf',
                                'datatype': '',
                                'value': 'vrf',
                                'op': '==',
                                'selected': 'True',
                                'name': 'type',
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/type'
                            },
                            {
                                'nodetype': 'leaf',
                                'datatype': 'igmp_Size',
                                'value': 20,
                                'op': '==',
                                'selected': 'True',
                                'name': 'size',
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/size'
                            },
                            {
                                'nodetype': 'leaf',
                                'datatype': '',
                                'value': 'nbm',
                                'op': '==',
                                'selected': 'True',
                                'name': 'type',
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/type'
                            },
                            {
                                'nodetype': 'leaf',
                                'datatype': 'igmp_Size',
                                'value': 20,
                                'op': '==',
                                'selected': 'True',
                                'name': 'size',
                                'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/eventHist-items/EventHistory-list/size'
                            }
                        ], 
                    'verifier': rpc_verify.process_operational_state, 
                    'namespace_modules': 
                        {
                            'top': 'Cisco-NX-OS-device'
                        }, 
                    'decode': GnmiMessage.decode_notification, 
                    'log': log
                }

        # Response 1
        path_elem1 = proto.gnmi_pb2.PathElem()
        path_elem1.KeyEntry.key = ""
        path_elem1.KeyEntry.value = ""
        path_elem1.name = "System"
        
        path1 = proto.gnmi_pb2.Path()
        path1.origin = "device"
        path1.elem.append(path_elem1)

        val1 = {
            "igmp-items":
                {
                "inst-items":
                    {
                    "dom-items":
                        {
                        "Dom-list":
                            [
                                {
                                    "name":"default",
                                    "eventHist-items":
                                        {
                                    "EventHistory-list":
                                        [
                                            {
                                                "type":"nbm",
                                                "size":20
                                            },
                                            {
                                                "type":"groupDebugs",
                                                "size":20
                                            },
                                            {
                                                "type":"intfDebugs",
                                                "size":20
                                            },
                                            {
                                                "type":"ha",
                                                "size":20
                                            },
                                            {
                                                "type":"mtrace",
                                                "size":20
                                            },
                                            {
                                                "type":"igmpInternal",
                                                "size":20
                                            },
                                            {
                                                "type":"intfEvents",
                                                "size":20
                                            },
                                            {
                                                "type":"groupEvents",
                                                "size":20
                                            },
                                            {
                                                "type":"cli",
                                                "size":20
                                            },
                                            {
                                                "type":"policy",
                                                "size":20
                                            },
                                            {
                                                "type":"mvr",
                                                "size":20
                                            },
                                            {
                                                "type":"vrf",
                                                "size":20
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        val1 = json.dumps(val1).encode('utf-8')

        value1 = proto.gnmi_pb2.TypedValue()
        value1.json_val = val1

        update1 = proto.gnmi_pb2.Update()
        update1.path.MergeFrom(path1)
        update1.val.MergeFrom(value1)

        notification1 = proto.gnmi_pb2.Notification()
        notification1.timestamp = 0
        notification1.prefix.MergeFrom(proto.gnmi_pb2.Path())
        notification1.update.append(update1)

        response1 = proto.gnmi_pb2.SubscribeResponse()
        response1.update.MergeFrom(notification1)

        # Response 2
        response2 = proto.gnmi_pb2.SubscribeResponse()
        response2.sync_response = True
    
        # initiate subscription thread
        subscribe_thread = GnmiNotification(
            [response1, response2],
            **request
        )
        subscribe_thread.start()
                
        # Wait till the thread is stopped.
        subscribe_thread.join()

        # Test the result
        self.assertEqual(subscribe_thread.result, True)

    def test_run_get_config_gnmi(self):
        """ Test run_gnmi with get-config action and range op """
        operation = 'get-config'
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
                'xpath': '/oc-sys:system/oc-sys:ssh-server/oc-sys:state/oc-sys:rate-limit'
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

        format = {
            'auto-validate': False,
            'get_type': 'CONFIG'
        }
        response = proto.gnmi_pb2.GetResponse()
        upd = {
          'path': {
            'elem': [
                {
                'name': "system"
                },
                {
                  'name': "ssh-server"
                },
                {
                  'name': "state"
                },
                {
                  'name': "rate-limit"
                }
            ]
          }
        }
        update = json_format.ParseDict(
            upd,
            proto.gnmi_pb2.Update()
        )
        update.val.json_ietf_val = json.dumps(60).encode('utf-8')
        notif = proto.gnmi_pb2.Notification()
        notif.update.append(update)
        response.notification.append(notif)
        device = TestDevice(response)

        result = run_gnmi(
            operation, device, steps, datastore, rpc_data, returns, format=format
        )

        self.assertEqual(result, True)

    def test_run_get_config_gnmi_ascii(self):
        """ Test run_gnmi with get-config action and range op using ASCII encoding """
        operation = 'get-config'
        steps = "STEP 1: Starting action yang on device 'ncs1004'"
        datastore = {
            'type': '',
            'lock': False,
            'retry': 10
        }
        rpc_data = {
            'nodes': [{
                'xpath': 'show interface loopback10'
            }]
        }
        returns = [{
            'id': 1,
            'name': 'rate-limit',
            'op': '==',
            'selected': True,
            'datatype': 'ascii',
            'value': "-------------------------- show interface loopback10 --------------------------\n% failed to get item (con0_RP0_CPU0/taskmap), rc 0x40818600(\'sysdb\' detected the \'warning\' condition \'A SysDB client tried to access a nonexistent item or list an empty directory\')\nLoopback10 is up, line protocol is up \n  Interface state transitions: 1\n  Hardware is Loopback interface(s)\n  Description: test description miott\n  Internet address is 3.3.3.3/32\n  MTU 1500 bytes, BW 0 Kbit\n     reliability Unknown, txload Unknown, rxload Unknown\n  Encapsulation Loopback,  loopback not set,\n  Last link flapped 20w1d\n  Last input Unknown, output Unknown\n  Last clearing of \"show interface\" counters Unknown\n  Input/output data rate is disabled.",
            'xpath': '/show interface loopback10'
        }]

        format = {
            'encoding': 'ascii',
            'get_type': 'CONFIG',
            'origin': 'cli'
        }
        response = proto.gnmi_pb2.GetResponse()
        upd = {
          'path': {
            'elem': [
                {
                'name': "show interface loopback10"
                },
            ]
          }
        }
        update = json_format.ParseDict(
            upd,
            proto.gnmi_pb2.Update()
        )
        update.val.ascii_val = "\n-------------------------- show interface loopback10 --------------------------\n% failed to get item (con0_RP0_CPU0/taskmap), rc 0x40818600(\'sysdb\' detected the \'warning\' condition \'A SysDB client tried to access a nonexistent item or list an empty directory\')\nLoopback10 is up, line protocol is up \n  Interface state transitions: 1\n  Hardware is Loopback interface(s)\n  Description: test description miott\n  Internet address is 3.3.3.3/32\n  MTU 1500 bytes, BW 0 Kbit\n     reliability Unknown, txload Unknown, rxload Unknown\n  Encapsulation Loopback,  loopback not set,\n  Last link flapped 20w1d\n  Last input Unknown, output Unknown\n  Last clearing of \"show interface\" counters Unknown\n  Input/output data rate is disabled.\n\n\n\n"
        notif = proto.gnmi_pb2.Notification()
        notif.update.append(update)
        response.notification.append(notif)
        device = TestDevice(response)

        result = run_gnmi(
            operation, device, steps, datastore, rpc_data, returns, format=format
        )

        self.assertEqual(result, True)

    def test_run_2_get_config_gnmi(self):
        """ Test run_gnmi with get-config action and == op for Boolean Value Properties """
        operation = 'get-config'
        steps = "STEP 1: Starting action yang on device 'N9k1-Spine1'"
        datastore = {
            'type': '',
            'lock': False,
            'retry': 10
        }
        rpc_data = {
            'namespace': {
                'top': 'http://cisco.com/ns/yang/cisco-nx-os-device'
            },
            'nodes': [{
                'xpath': '/top:System/top:igmp-items/top:inst-items/top:heavyTemplate'
            }]
        }
        returns = [{
            'id': 1,
            'name': 'heavyTemplate',
            'op': '==',
            'selected': True,
            'datatype': 'boolean',
            'value': 'false',
            'xpath': '/System/igmp-items/inst-items/heavyTemplate'
        }]

        format = {
            'auto-validate': False,
            'get_type': 'CONFIG'
        }
        response = proto.gnmi_pb2.GetResponse()
        upd = {
          'path': {
            'elem': [
                {
                'name': "System"
                },
                {
                  'name': "igmp-items"
                },
                {
                  'name': "inst-items"
                },
                {
                  'name': "heavyTemplate"
                }
            ]
          }
        }
        update = json_format.ParseDict(
            upd,
            proto.gnmi_pb2.Update()
        )
        update.val.json_ietf_val = json.dumps(False).encode('utf-8')
        notif = proto.gnmi_pb2.Notification()
        notif.update.append(update)
        response.notification.append(notif)
        device = TestDevice(response)

        result = run_gnmi(
            operation, device, steps, datastore, rpc_data, returns, format=format
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


    @patch('genie.libs.sdk.triggers.blitz.yangexec.netconf_send')
    def test_run_netconf_get_lxml(self, netconf_send_mock):
        """ Test run_netconf get action with lxml objects with sequence"""
        operation = 'get'
        steps = "STEP 1: Starting action yang on device 'CSR1K-5'"
        datastore = {'lock': True, 'retry': 40, 'type': ''}
        rpc_data = {
            'namespace': {
                'oc-if': 'http://openconfig.net/yang/interfaces',
            },
            'nodes': [{
                'xpath': '/oc-if:interfaces',
                'nodetype': 'container'
            }]
        }
        returns = [{
            'id': 0,
            'name': 'name',
            'op': '==',
            'selected': True,
            'value': 'GigabitEthernet3',
            'xpath': '/interfaces/interface/config/name'
        }, {
            'id': 1,
            'name': 'type',
            'op': '==',
            'selected': True,
            'value': 'ianaift:ethernetCsmacd',
            'xpath': '/interfaces/interface/config/type'
        }, {
            'id': 2,
            'name': 'description',
            'op': '==',
            'selected': False,
            'value': 'test3',
            'xpath': '/interfaces/interface/config/description'
        }, {
            'id': 3,
            'name': 'enabled',
            'op': '==',
            'selected': True,
            'value': 'true',
            'xpath': '/interfaces/interface/config/enabled'
        }]

        format = {
            'auto_validate': True,
            'negative_test': False,
            'pause': 0,
            'timeout': 30,
            'sequence': True
        }

        netconf_send_mock.return_value = [(
            'get',
            '<?xml version="1.0" encoding="UTF-8"?>\n<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"\
             message-id="urn:uuid:0833adc1-8b89-4365-8bf5-99c607c3232d" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">\
             <data><interfaces xmlns="http://openconfig.net/yang/interfaces"><interface><name>GigabitEthernet1</name><config>\
             <name>GigabitEthernet1</name><type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>\
             <description>test3</description><enabled>true</enabled></config></interface><interface><name>GigabitEthernet2</name><config>\
             <name>GigabitEthernet2</name><type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>\
             <description>mike</description><enabled>true</enabled></config></interface><interface><name>GigabitEthernet3</name><config>\
             <name>GigabitEthernet3</name><type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>\
             <description>mike test</description><enabled>false</enabled></config></interface></interfaces></data></rpc-reply>'
        )]

        result = run_netconf(
            operation, self.netconf_device, steps, datastore, rpc_data, returns, format=format
        )

        self.assertEqual(result, False)

    @patch('genie.libs.sdk.triggers.blitz.yangexec.netconf_send')
    def test_run_netconf_get_config_sequence_fail(self, netconf_send_mock):
        """ Test run_netconf get-config with List Keys in returns"""
        operation = 'get-config'
        steps = "STEP 1: Starting action yang on device 'CSR1K-5'"
        datastore = {'lock': True, 'retry': 40, 'type': 'running'}
        rpc_data = {
            'namespace': {
                'top': 'http://cisco.com/ns/yang/cisco-nx-os-device',
            },
            'nodes': [{
                'xpath': '/top:System/top:igmp-items/top:inst-items/top:dom-items',
                'nodetype': 'container'
            }]
        }
        returns = [{
            'nodetype': 'leaf',
            'value': 'test03',
            'op': '==',
            'selected': 'True',
            'name': 'rtMap',
            'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list[name="default"]/if-items/If-list[id="eth1/2"]/streppol-items/StRepP-list[joinType="0"]/rtMap'
        }, {
            'nodetype': 'leaf',
            'value': 'test13',
            'op': '==',
            'selected': 'True',
            'name': 'rtMap',
            'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list[name="default"]/if-items/If-list[id="eth1/2"]/streppol-items/StRepP-list[joinType="1"]/rtMap'
        }, {
            'nodetype': 'leaf',
            'value': 'test02',
            'op': '==',
            'selected': 'True',
            'name': 'rtMap',
            'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list[name="default"]/if-items/If-list[id="eth1/3"]/streppol-items/StRepP-list[joinType="0"]/rtMap'
        }, {
            'nodetype': 'leaf',
            'value': 'test12',
            'op': '==',
            'selected': 'True',
            'name': 'rtMap',
            'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list[name="default"]/if-items/If-list[id="eth1/3"]/streppol-items/StRepP-list[joinType="1"]/rtMap'
        }]

        format = {
            'auto_validate': False,
            'negative_test': False,
            'pause': 0,
            'timeout': 30,
        }

        netconf_send_mock.return_value = [(
            'get-config',
            '<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\
            <data><System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device"><igmp-items><inst-items>\
            <dom-items><Dom-list><name>default</name><if-items><If-list>\
            <id>eth1/3</id><adminSt>enabled</adminSt><allowv3Asm>true</allowv3Asm>\
            <grpTimeout>260</grpTimeout><immediateLeave>false</immediateLeave>\
            <reportLl>false</reportLl><streppol-items><StRepP-list><joinType>1</joinType>\
            <rtMap>test13</rtMap><useAccessGrpCommand>false</useAccessGrpCommand>\
            </StRepP-list><StRepP-list><joinType>0</joinType><rtMap>test03</rtMap>\
            <useAccessGrpCommand>false</useAccessGrpCommand></StRepP-list>\
            </streppol-items><suppressv3Gsq>false</suppressv3Gsq><ver>v2</ver>\
            </If-list><If-list><id>eth1/2</id><adminSt>enabled</adminSt>\
            <allowv3Asm>true</allowv3Asm><grpTimeout>260</grpTimeout>\
            <immediateLeave>false</immediateLeave><reportLl>false</reportLl>\
            <streppol-items><StRepP-list><joinType>1</joinType><rtMap>test12</rtMap>\
            <useAccessGrpCommand>false</useAccessGrpCommand></StRepP-list>\
            <StRepP-list><joinType>0</joinType><rtMap>test02</rtMap>\
            <useAccessGrpCommand>false</useAccessGrpCommand></StRepP-list>\
            </streppol-items><suppressv3Gsq>false</suppressv3Gsq><ver>v2</ver>\
            </If-list></if-items></Dom-list></dom-items></inst-items>\
            </igmp-items></System></data></rpc-reply>'
        )]

        result = run_netconf(
            operation, self.netconf_device, steps, datastore, rpc_data, returns, format=format
        )

        self.assertEqual(result, False)

    @patch('genie.libs.sdk.triggers.blitz.yangexec.netconf_send')
    def test_run_netconf_get_config_sequence_pass(self, netconf_send_mock):
        """ Test run_netconf get-config with List Keys in returns"""
        operation = 'get-config'
        steps = "STEP 1: Starting action yang on device 'CSR1K-5'"
        datastore = {'lock': True, 'retry': 40, 'type': 'running'}
        rpc_data = {
            'namespace': {
                'top': 'http://cisco.com/ns/yang/cisco-nx-os-device',
            },
            'nodes': [{
                'xpath': '/top:System/top:igmp-items/top:inst-items/top:dom-items',
                'nodetype': 'container'
            }]
        }
        returns = [{
            'nodetype': 'leaf',
            'value': 'test02',
            'op': '==',
            'selected': 'True',
            'name': 'rtMap',
            'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list[name="default"]/if-items/If-list[id="eth1/2"]/streppol-items/StRepP-list[joinType="0"]/rtMap'
        }, {
            'nodetype': 'leaf',
            'value': 'test12',
            'op': '==',
            'selected': 'True',
            'name': 'rtMap',
            'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list[name="default"]/if-items/If-list[id="eth1/2"]/streppol-items/StRepP-list[joinType="1"]/rtMap'
        }, {
            'nodetype': 'leaf',
            'value': 'test03',
            'op': '==',
            'selected': 'True',
            'name': 'rtMap',
            'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list[name="default"]/if-items/If-list[id="eth1/3"]/streppol-items/StRepP-list[joinType="0"]/rtMap'
        }, {
            'nodetype': 'leaf',
            'value': 'test13',
            'op': '==',
            'selected': 'True',
            'name': 'rtMap',
            'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list[name="default"]/if-items/If-list[id="eth1/3"]/streppol-items/StRepP-list[joinType="1"]/rtMap'
        }]

        format = {
            'auto_validate': False,
            'negative_test': False,
            'pause': 0,
            'timeout': 30,
        }

        netconf_send_mock.return_value = [(
            'get-config',
            '<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\
            <data><System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device"><igmp-items><inst-items>\
            <dom-items><Dom-list><name>default</name><if-items><If-list>\
            <id>eth1/3</id><adminSt>enabled</adminSt><allowv3Asm>true</allowv3Asm>\
            <grpTimeout>260</grpTimeout><immediateLeave>false</immediateLeave>\
            <reportLl>false</reportLl><streppol-items><StRepP-list><joinType>1</joinType>\
            <rtMap>test13</rtMap><useAccessGrpCommand>false</useAccessGrpCommand>\
            </StRepP-list><StRepP-list><joinType>0</joinType><rtMap>test03</rtMap>\
            <useAccessGrpCommand>false</useAccessGrpCommand></StRepP-list>\
            </streppol-items><suppressv3Gsq>false</suppressv3Gsq><ver>v2</ver>\
            </If-list><If-list><id>eth1/2</id><adminSt>enabled</adminSt>\
            <allowv3Asm>true</allowv3Asm><grpTimeout>260</grpTimeout>\
            <immediateLeave>false</immediateLeave><reportLl>false</reportLl>\
            <streppol-items><StRepP-list><joinType>1</joinType><rtMap>test12</rtMap>\
            <useAccessGrpCommand>false</useAccessGrpCommand></StRepP-list>\
            <StRepP-list><joinType>0</joinType><rtMap>test02</rtMap>\
            <useAccessGrpCommand>false</useAccessGrpCommand></StRepP-list>\
            </streppol-items><suppressv3Gsq>false</suppressv3Gsq><ver>v2</ver>\
            </If-list></if-items></Dom-list></dom-items></inst-items>\
            </igmp-items></System></data></rpc-reply>'
        )]

        result = run_netconf(
            operation, self.netconf_device, steps, datastore, rpc_data, returns, format=format
        )

        self.assertEqual(result, True)

    @patch('genie.libs.sdk.triggers.blitz.yangexec.netconf_send')
    def test_run_netconf_get_config_sequence_2(self, netconf_send_mock):
        """ Test run_netconf get-config with Wrong List Key in returns"""
        operation = 'get-config'
        steps = "STEP 1: Starting action yang on device 'CSR1K-5'"
        datastore = {'lock': True, 'retry': 40, 'type': ''}
        rpc_data = {
            'namespace': {
                'top': 'http://cisco.com/ns/yang/cisco-nx-os-device',
            },
            'nodes': [{
                'xpath': '/top:System/top:igmp-items/top:inst-items/top:dom-items',
                'nodetype': 'container'
            }]
        }
        returns = [{
            'nodetype': 'leaf',
            'value': '0',
            'op': '==',
            'selected': 'True',
            'name': 'joinType',
            'key': 'True',
            'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list[name="Wrong key"]/if-items/If-list[id="eth1/2"]/streppol-items/StRepP-list/joinType'
        }]

        format = {
            'auto_validate': False,
            'negative_test': False,
            'pause': 0,
            'timeout': 30,
        }

        netconf_send_mock.return_value = [(
            'get-config',
            '<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\
            <data><System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device"><igmp-items><inst-items>\
            <dom-items><Dom-list><name>default</name><if-items><If-list>\
            <id>eth1/3</id><adminSt>enabled</adminSt><allowv3Asm>true</allowv3Asm>\
            <grpTimeout>260</grpTimeout><immediateLeave>false</immediateLeave>\
            <reportLl>false</reportLl><streppol-items><StRepP-list><joinType>1</joinType>\
            <rtMap>test13</rtMap><useAccessGrpCommand>false</useAccessGrpCommand>\
            </StRepP-list><StRepP-list><joinType>0</joinType><rtMap>test03</rtMap>\
            <useAccessGrpCommand>false</useAccessGrpCommand></StRepP-list>\
            </streppol-items><suppressv3Gsq>false</suppressv3Gsq><ver>v2</ver>\
            </If-list><If-list><id>eth1/2</id><adminSt>enabled</adminSt>\
            <allowv3Asm>true</allowv3Asm><grpTimeout>260</grpTimeout>\
            <immediateLeave>false</immediateLeave><reportLl>false</reportLl>\
            <streppol-items><StRepP-list><joinType>1</joinType><rtMap>test12</rtMap>\
            <useAccessGrpCommand>false</useAccessGrpCommand></StRepP-list>\
            <StRepP-list><joinType>0</joinType><rtMap>test02</rtMap>\
            <useAccessGrpCommand>false</useAccessGrpCommand></StRepP-list>\
            </streppol-items><suppressv3Gsq>false</suppressv3Gsq><ver>v2</ver>\
            </If-list></if-items></Dom-list></dom-items></inst-items>\
            </igmp-items></System></data></rpc-reply>'
        )]

        result = run_netconf(
            operation, self.netconf_device, steps, datastore, rpc_data, returns, format=format
        )

        self.assertEqual(result, False)

    def test_run_gnmi_get_config_sequence(self):
        """ Test run_gnmi get-config with List Keys in returns"""
        operation = 'get'
        steps = "STEP 1: Starting action yang on device 'ncs1004'"
        datastore = {
            'type': '',
            'lock': False,
            'retry': 10
        }
        rpc_data = {
            'namespace': {
                'top': 'http://cisco.com/ns/yang/cisco-nx-os-device',
            },
            'nodes': [{
                'xpath': '/top:System/top:igmp-items/top:inst-items/top:dom-items',
                'nodetype': 'container'
            }]
        }
        returns = [{
            'nodetype': 'leaf',
            'value': '2',
            'op': '==',
            'selected': 'True',
            'name': 'size',
            'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list[name="default"]/eventHist-items/EventHistory-list[type="cli"]/size'
        },{
            'nodetype': 'leaf',
            'value': '3',
            'op': '==',
            'selected': 'True',
            'name': 'size',
            'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list[name="default"]/eventHist-items/EventHistory-list[type="groupEvents"]/size'
        }]

        format = {
            'auto_validate': False,
            'negative_test': False,
            'pause': 0,
            'timeout': 30,
        }

        response = proto.gnmi_pb2.GetResponse()
        upd = {
          'path': {
            'elem': [
                {
                'name': "System"
                },
                {
                  'name': "igmp-items"
                },
                {
                  'name': "inst-items"
                },
                {
                  'name': "dom-items"
                }
            ]
          }
        }
        update = json_format.ParseDict(
            upd,
            proto.gnmi_pb2.Update()
        )

        json_val = {
            "Dom-list":
            [
                {
                    "name":"default",
                    "eventHist-items":
                    {
                        "EventHistory-list":
                        [
                            {
                                "type":"nbm",
                                "size":4
                            },
                            {
                                "type":"igmpInternal",
                                "size":2
                            },
                            {
                                "type":"vrf",
                                "size":2
                            },
                            {
                                "type":"mtrace",
                                "size":2
                            },
                            {
                                "type":"ha",
                                "size":3
                            },
                            {
                                "type":"groupEvents",
                                "size":3
                            },
                            {
                                "type":"intfEvents",
                                "size":3
                            },
                            {
                                "type":"intfDebugs",
                                "size":3
                            },
                            {
                                "type":"policy",
                                "size":2
                            },
                            {
                                "type":"cli",
                                "size":3
                            },
                            {
                                "type":"mvr",
                                "size":3
                            },
                            {
                                "type":"groupDebugs",
                                "size":3
                            }
                        ]
                    }
                }
            ]
        }
        
        update.val.json_ietf_val = json.dumps(json_val).encode('utf-8')
        notif = proto.gnmi_pb2.Notification()
        notif.update.append(update)
        response.notification.append(notif)
        device = TestDevice(response)

        result = run_gnmi(
            operation, device, steps, datastore, rpc_data, returns, format=format
        )

        self.assertEqual(result, False)

    @patch('genie.libs.sdk.triggers.blitz.yangexec.netconf_send')
    def test_run_netconf_get_lxml_without_format(self, netconf_send_mock):
        """ Test run_netconf get action with lxml objects"""
        operation = 'get'
        steps = "STEP 1: Starting action yang on device 'CSR1K-5'"
        datastore = {'lock': True, 'retry': 40, 'type': ''}
        rpc_data = {
            'namespace': {
                'oc-if': 'http://openconfig.net/yang/interfaces',
            },
            'nodes': [{
                'xpath': '/oc-if:interfaces',
                'nodetype': 'container'
            }]
        }
        returns = [{
            'id': 0,
            'name': 'name',
            'op': '==',
            'selected': True,
            'value': 'GigabitEthernet3',
            'xpath': '/interfaces/interface/config/name'
        }, {
            'id': 1,
            'name': 'type',
            'op': '==',
            'selected': True,
            'value': 'ianaift:ethernetCsmacd',
            'xpath': '/interfaces/interface/config/type'
        }]

        netconf_send_mock.return_value = [(
            'get',
            '<?xml version="1.0" encoding="UTF-8"?>\n<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"\
             message-id="urn:uuid:0833adc1-8b89-4365-8bf5-99c607c3232d" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">\
             <data><interfaces xmlns="http://openconfig.net/yang/interfaces"><interface><name>GigabitEthernet1</name><config>\
             <name>GigabitEthernet1</name><type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>\
             <description>test3</description><enabled>true</enabled></config></interface><interface><name>GigabitEthernet2</name><config>\
             <name>GigabitEthernet2</name><type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>\
             <description>mike</description><enabled>true</enabled></config></interface><interface><name>GigabitEthernet3</name><config>\
             <name>GigabitEthernet3</name><type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>\
             <description>mike test</description><enabled>false</enabled></config></interface></interfaces></data></rpc-reply>'
        )]

        result = run_netconf(
            operation, self.netconf_device, steps, datastore, rpc_data, returns
        )
        self.assertEqual(result, True)

    def test_run_subscribe_multiple_leaf_nodes(self):
        """ Test _trim_nodes for multiple leaf nodes"""
        rpc_verify = RpcVerify(log=log, capabilities=[])
        rpc_data =  {
                        'namespace':
                        {
                            'oc-netinst': 'http://openconfig.net/yang/network-instance'
                        },
                        'nodes':
                        [
                            {
                                'nodetype': 'leaf',
                                'xpath': '/oc-netinst:network-instances/oc-netinst:network-instance[oc-netinst:name="default"]/oc-netinst:connection-points/oc-netinst:connection-point[oc-netinst:connection-point-id="nve1"]/oc-netinst:endpoints/oc-netinst:endpoint[oc-netinst:endpoint-id="nve1"]/oc-netinst:vxlan/oc-netinst:endpoint-vnis/oc-netinst:endpoint-vni[oc-netinst:vni="3120400"]/oc-netinst:state/oc-netinst:vni'
                            },
                            {
                                'nodetype': 'leaf',
                                'xpath': '/oc-netinst:network-instances/oc-netinst:network-instance[oc-netinst:name="default"]/oc-netinst:connection-points/oc-netinst:connection-point[oc-netinst:connection-point-id="nve1"]/oc-netinst:endpoints/oc-netinst:endpoint[oc-netinst:endpoint-id="nve1"]/oc-netinst:vxlan/oc-netinst:endpoint-vnis/oc-netinst:endpoint-vni[oc-netinst:vni="3120400"]/oc-netinst:state/oc-netinst:vni-state'
                            }
                        ],
                        'request_mode': 'ONCE',
                        'negative_test': False,
                        'sub_mode': 'SAMPLE',
                        'encoding': 'PROTO',
                        'returns':
                        [
                            {
                                'nodetype': 'leaf',
                                'value': 3120400,
                                'op': '==',
                                'selected': True,
                                'name': 'vni',
                                'xpath': '/network-instances/network-instance[name=default]/connection-points/connection-point[connection-point-id=nve1]/endpoints/endpoint[endpoint-id=nve1]/vxlan/endpoint-vnis/endpoint-vni[vni=3120400]/state/vni'
                            },
                            {
                                'nodetype': 'leaf',
                                'value': 'UP',
                                'op': '==',
                                'selected': True,
                                'name': 'vni-state',
                                'xpath': '/network-instances/network-instance[name=default]/connection-points/connection-point[connection-point-id=nve1]/endpoints/endpoint[endpoint-id=nve1]/vxlan/endpoint-vnis/endpoint-vni[vni=3120400]/state/vni-state'
                            }
                        ],
                        'verifier': rpc_verify.process_operational_state
                    }

        format = {'request_mode': 'ONCE', 'negative_test': False, 'sub_mode': 'SAMPLE', 'encoding': 'PROTO'}
        gmc = GnmiMessageConstructor('subscribe', rpc_data, **format)
        nodes = gmc._trim_nodes(rpc_data['nodes'])
        nodes_len = len(nodes)
        self.assertEqual(nodes_len, 2)

if __name__ == '__main__':
    unittest.main()
