import logging
import unittest
from unittest.mock import Mock

log = logging.getLogger(__name__)

from genie.libs.sdk.triggers.blitz.rpcverify import DecodedResponse, OptFields
from genie.libs.sdk.triggers.blitz.verifiers import GnmiDefaultVerifier


class TestGnmiDefaultVerifier(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        device = Mock()
        returns = []
        cls.gdv = GnmiDefaultVerifier(device=device, returns=returns, log=log)

    def test__auto_validation(self):
        decoded_response = DecodedResponse(
            json_dicts=[True, 'openconfig-keychain-types:SIMPLE_KEY', 'openconfig-isis-types:TEXT', 'ISIS'],
            updates=[('DEFAULT', '/network-instances/network-instance/name'),
                    ('ISIS', '/network-instances/network-instance/protocols/protocol/identifier'),
                    ('1', '/network-instances/network-instance/protocols/protocol/name'),
                    ('2', '/network-instances/network-instance/protocols/protocol/isis/levels/level/level-number'),
                    (True, '/network-instances/network-instance/protocols/protocol/isis/levels/level/authentication/config/enabled'),
                    (True, '/network-instances/network-instance/protocols/protocol/isis/levels/level/authentication/config/enabled'),
                    ('DEFAULT', '/network-instances/network-instance/name'),
                    ('ISIS', '/network-instances/network-instance/protocols/protocol/identifier'),
                    ('1', '/network-instances/network-instance/protocols/protocol/name'),
                    ('2', '/network-instances/network-instance/protocols/protocol/isis/levels/level/level-number'),
                    ('openconfig-keychain-types:SIMPLE_KEY', '/network-instances/network-instance/protocols/protocol/isis/levels/level/authentication/config/auth-type'),
                    ('openconfig-keychain-types:SIMPLE_KEY', '/network-instances/network-instance/protocols/protocol/isis/levels/level/authentication/config/auth-type'),
                    ('DEFAULT', '/network-instances/network-instance/name'),
                    ('ISIS', '/network-instances/network-instance/protocols/protocol/identifier'),
                    ('1', '/network-instances/network-instance/protocols/protocol/name'),
                    ('2', '/network-instances/network-instance/protocols/protocol/isis/levels/level/level-number'),
                    ('openconfig-isis-types:TEXT', '/network-instances/network-instance/protocols/protocol/isis/levels/level/authentication/config/auth-mode'),
                    ('openconfig-isis-types:TEXT', '/network-instances/network-instance/protocols/protocol/isis/levels/level/authentication/config/auth-mode'),
                    ('DEFAULT', '/network-instances/network-instance/name'),
                    ('ISIS', '/network-instances/network-instance/protocols/protocol/identifier'),
                    ('1', '/network-instances/network-instance/protocols/protocol/name'),
                    ('2', '/network-instances/network-instance/protocols/protocol/isis/levels/level/level-number'),
                    ('ISIS', '/network-instances/network-instance/protocols/protocol/isis/levels/level/authentication/config/auth-password'),
                    ('ISIS', '/network-instances/network-instance/protocols/protocol/isis/levels/level/authentication/config/auth-password')],
            deletes=[],
            errors=[])

        self.gdv.rpc_data = {
            'namespace': {
                'oc-keychain-types': 'openconfig-oc-keychain-types',
                'oc-netinst': 'openconfig-network-instance',
                'oc-pol-types': 'openconfig-policy-types'
            },
            'nodes': [{
                'nodetype': 'container',
                'xpath': '/oc-netinst:network-instances/oc-netinst:network-instance[oc-netinst:name="DEFAULT"]/oc-netinst:protocols/oc-netinst:protocol[oc-netinst:identifier="ISIS"][oc-netinst:name="1"]/oc-netinst:isis/oc-netinst:levels/oc-netinst:level[oc-netinst:level-number="2"]/oc-netinst:authentication/oc-netinst:config'
            }, {
                'nodetype': 'leaf',
                'datatype': 'boolean',
                'value': 'true',
                'xpath': '/oc-netinst:network-instances/oc-netinst:network-instance[oc-netinst:name="DEFAULT"]/oc-netinst:protocols/oc-netinst:protocol[oc-netinst:identifier="ISIS"][oc-netinst:name="1"]/oc-netinst:isis/oc-netinst:levels/oc-netinst:level[oc-netinst:level-number="2"]/oc-netinst:authentication/oc-netinst:config/oc-netinst:enabled'
            }, {
                'nodetype': 'leaf',
                'datatype': 'identityref',
                'value':'openconfig-keychain-types:SIMPLE_KEY',
                'xpath': '/oc-netinst:network-instances/oc-netinst:network-instance[oc-netinst:name="DEFAULT"]/oc-netinst:protocols/oc-netinst:protocol[oc-netinst:identifier="ISIS"][oc-netinst:name="1"]/oc-netinst:isis/oc-netinst:levels/oc-netinst:level[oc-netinst:level-number="2"]/oc-netinst:authentication/oc-netinst:config/oc-netinst:auth-type'
            }, {
                'nodetype':'leaf',
                'datatype': 'identityref',
                'value': 'openconfig-isis-types:TEXT',
                'xpath': '/oc-netinst:network-instances/oc-netinst:network-instance[oc-netinst:name="DEFAULT"]/oc-netinst:protocols/oc-netinst:protocol[oc-netinst:identifier="ISIS"][oc-netinst:name="1"]/oc-netinst:isis/oc-netinst:levels/oc-netinst:level[oc-netinst:level-number="2"]/oc-netinst:authentication/oc-netinst:config/oc-netinst:auth-mode'
            }, {
                'nodetype': 'leaf',
                'datatype': 'string',
                'value': 'ISIS',
                'xpath': '/oc-netinst:network-instances/oc-netinst:network-instance[oc-netinst:name="DEFAULT"]/oc-netinst:protocols/oc-netinst:protocol[oc-netinst:identifier="ISIS"][oc-netinst:name="1"]/oc-netinst:isis/oc-netinst:levels/oc-netinst:level[oc-netinst:level-number="2"]/oc-netinst:authentication/oc-netinst:config/oc-netinst:auth-password'
            }],
            'namespace_modules': {
                'oc-keychain-types': 'openconfig-oc-keychain-types',
                'oc-netinst': 'openconfig-network-instance',
                'oc-pol-types': 'openconfig-policy-types'
            }
        }

        self.gdv.decode = Mock(return_value=decoded_response)
        result = self.gdv._auto_validation(response={}, namespace_modules={})
        self.assertTrue(result)

    def test_returns_init(self):
        returns = [{
            'datatype': bool,
            'default': '',
            'format': '',
            'name': 'enabled',
            'nodetype': '',
            'op': '==',
            'selected': 'True',
            'value': 'true',
            'xpath': '/network-instances/network-instance/protocols/protocol/isis/interfaces/interface/levels/level/hello-authentication/state/enabled'
        }]
        gdv = GnmiDefaultVerifier(device=Mock(), returns=returns, log=log)

        expected_returns = [OptFields(
            name='enabled',
            value='true',
            xpath='/network-instances/network-instance/protocols/protocol/isis/interfaces/interface/levels/level/hello-authentication/state/enabled',
            op='==',
            default='',
            selected='True',
            id='',
            datatype=bool,
            sequence=0,
            default_xpath='',
            nodetype='',
            key=False)]
        self.assertEqual(gdv.returns, expected_returns)


if __name__ == "__main__":
    unittest.main()
