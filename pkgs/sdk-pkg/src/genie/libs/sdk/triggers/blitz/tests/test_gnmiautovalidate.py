#! /usr/bin/env python
import sys
import unittest
import logging

from unittest.mock import patch
from genie.libs.sdk.triggers.blitz import yangexec
from genie.libs.sdk.triggers.blitz.rpcverify import RpcVerify

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

if __name__ == '__main__':
    unittest.main()
