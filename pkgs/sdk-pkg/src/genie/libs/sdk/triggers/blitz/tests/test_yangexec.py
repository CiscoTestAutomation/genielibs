#! /usr/bin/env python
# Python
import unittest
import logging
import sys

from unittest.mock import patch

# Genie Libs
from genie.libs.sdk.triggers.blitz.yangexec import run_netconf, run_gnmi


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


class TestYangExec(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # create a Netconf device and copy attributes to Mock to set server_capabilities attribute
        with patch('yang.connector.netconf.Netconf') as MockNetconfDevice:
            cls.instance = MockNetconfDevice.return_value
            cls.instance.server_capabilities = []
            cls.alias = 'CSR1K-5'
            cls.via = 'yang1'

        with patch('yang.connector.gnmi.Gnmi') as MockGnmiDevice:
            cls.gnmi_device = MockGnmiDevice.return_value
            cls.alias = 'bo86'
            cls.via = 'yang2'

    @patch('genie.libs.sdk.triggers.blitz.yangexec.netconf_send')
    def test_run_netconf(self, netconf_send_mock):
        """ Test if run_netconf successfully runs with subscribe action """
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

        rpc_data['operation'] = 'subscribe'
        rpc_data['rpc'] = ''
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
            self.instance,  # device
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
            operation=operation,
            device=self.gnmi_device,
            steps=steps,
            datastore=datastore,
            rpc_data=rpc_data,
            returns=returns,
            format=format
        )

        self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()
