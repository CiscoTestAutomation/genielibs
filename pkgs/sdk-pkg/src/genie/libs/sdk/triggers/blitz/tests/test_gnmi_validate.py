#! /usr/bin/env python
import sys
import unittest
import logging

from unittest.mock import patch
from genie.libs.sdk.triggers.blitz import yangexec
from genie.libs.sdk.triggers.blitz.rpcverify import RpcVerify
from genie.libs.sdk.triggers.blitz.verifiers import GnmiDefaultVerifier

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


class TestRpcRun(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Mock GNMI device
        with patch('yang.connector.gnmi.Gnmi') as MockGnmiDevice:
            cls.gnmi_device = MockGnmiDevice.return_value
            cls.gnmi_device.alias = 'ddmi-500-2'
            cls.gnmi_device.via = 'yang2'

    def setUp(self):
        self.format = {
            'auto_validate': True,
        }
        self.rpc_data = {
            'namespace':  {'oc-netinst': 'http://openconfig.net/yang/network-instance'},
            'nodes': [
                {
                    'datatype': 'leafref', 'default': '', 'edit-op': '', 'nodetype': 'leaf', 'value': 'test', 'xpath': '/oc-netinst:network-instances/oc-netinst:network-instance/oc-netinst:name'
                },
                {
                    'datatype': 'leafref', 'default': '', 'edit-op': '', 'nodetype': 'leaf', 'value': 'test', 'xpath': '/oc-netinst:network-instances/oc-netinst:network-instance/oc-netinst:config/oc-netinst:name'
                }
            ],
        }
        self.returns = []

    def test_auto_validate_off(self):
        """Check if auto_validate False does not try validation."""
        self.format['auto_validate'] = False
        result = yangexec.run_gnmi(
            'edit-config',
            self.gnmi_device,
            None,  # steps
            {},  # datastore
            self.rpc_data,
            self.returns,
            format=self.format
        )
        self.assertTrue(result)

    def test_auto_validate_on(self):
        """Check if auto_validate True will try validation."""
        result = yangexec.run_gnmi(
            'edit-config',
            self.gnmi_device,
            None,  # steps
            {},  # datastore
            self.rpc_data,
            self.returns,
            format=self.format
        )
        self.assertFalse(result)

    def test_validate_subscribe_keys(self):
        """Check if keys in Xpath are validated."""
        decoded_response = [
            ('default', '/network-instances/network-instance/name'),
            ('nve1',
            '/network-instances/network-instance/connection-points/connection-point/connection-point-id'),
            ('nve1',
            '/network-instances/network-instance/connection-points/connection-point/endpoints/endpoint/endpoint-id'),
            (3120400,
            '/network-instances/network-instance/connection-points/connection-point/endpoints/endpoint/vxlan/endpoint-vnis/endpoint-vni/vni'),
            (312040,
            '/network-instances/network-instance/connection-points/connection-point/endpoints/endpoint/vxlan/endpoint-vnis/endpoint-vni/state/vni'),
            ('UP',
            '/network-instances/network-instance/connection-points/connection-point/endpoints/endpoint/vxlan/endpoint-vnis/endpoint-vni/state/vni-state')
        ]
        returns = [
            {'nodetype': 'leaf',
            'value': 3120400,
            'op': '==',
            'selected': True,
            'name': 'vni',
            'xpath': '/network-instances/network-instance[name=default]/connection-points/connection-point[connection-point-id=nve1]/endpoints/endpoint[endpoint-id=nve1]/vxlan/endpoint-vnis/endpoint-vni[vni=3120400]/state/vni'},
            {'nodetype': 'leaf',
            'value': "UP",
            'op': '==',
            'selected': True,
            'name': 'vni-state',
            'xpath': '/network-instances/network-instance[name=default]/connection-points/connection-point[connection-point-id=nve1]/endpoints/endpoint[endpoint-id=nve1]/vxlan/endpoint-vnis/endpoint-vni[vni=3120400]/state/vni-state'}
        ]
        gv = GnmiDefaultVerifier(self.gnmi_device, returns, log)
        found = []
        for field in decoded_response:
            for ret in returns:
                ret_found = gv._find_xpath(ret['xpath'], field[1], decoded_response)
                if ret_found:
                    found.append(ret_found)
                    break
        self.assertTrue(all(found))


if __name__ == '__main__':
    unittest.main()
