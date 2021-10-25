#! /usr/bin/env python
import sys
import re
import os
import unittest
import logging
from unittest.mock import patch

from genie.libs.sdk.triggers.blitz.requestbuilder import RestconfRequestBuilder


# TODO: Needs to be part of genielibs test run

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


class TestRestconfRequestBuilder(unittest.TestCase):
    """Test cases for the RestconfRequestBuilder class,
       tests are based on URL and body generated as the result
       of request data"""

    basedir = os.path.join(os.path.dirname(__file__), 'data')

    @classmethod
    def setUpClass(cls):
        """Initialization for all test cases"""
        with patch('rest.connector.Rest') as MockRestconfDevice:
            cls.instance = MockRestconfDevice.return_value
            cls.instance.server_capabilities = []
            cls.alias = 'testdevice'
            cls.via = 'yang1'

    def test_leaf_nodes(self):
        """Test single and nested leaf nodes"""
        request_data = {
            'namespace': {
                'ios': 'http://cisco.com/ns/yang/Cisco-IOS-XE-native'
            },
            'nodes': [{
                'edit-op': 'merge',
                'nodetype': 'leaf',
                'datatype': 'string',
                'value': '17.6',
                'xpath': '/ios:native/ios:version'
            }, {
                'edit-op': 'merge',
                'nodetype': 'leaf',
                'datatype': 'uint32',
                'value': '68976',
                'xpath': '/ios:native/ios:memory/ios:free/ios:low-watermark/ios:processor'
            }]
        }
        expected_url = '/restconf/data/Cisco-IOS-XE-native:native'
        expected_body = {
            'native': {
                'version': '17.6',
                'memory': {
                    'free': {
                        'low-watermark': {
                            'processor': '68976'
                        }
                    }
                }
            }
        }
        returns = {}
        # Build RESTCONF request
        request_builder = RestconfRequestBuilder(request_data, returns)
        actual_url = request_builder.url
        actual_body = request_builder.body

        # Test URL
        self.assertEqual(expected_url, actual_url)
        # Test body
        self.assertEqual(actual_body, expected_body)
        self.assertNotEqual(actual_body, None)
        self.assertNotEqual(actual_body, {})

        # Test POST method
        request_data_post = {
            'namespace': {
                'ios': 'http://cisco.com/ns/yang/Cisco-IOS-XE-native'
            },
            'nodes': [{
                'edit-op': 'create',
                'nodetype': 'leaf',
                'datatype': 'uint32',
                'value': '1',
                'xpath': '/ios:native/ios:memory/ios:free/ios:low-watermark/ios:IO'
            }]
        }
        expected_url_post = '/restconf/data/Cisco-IOS-XE-native:native/Cisco-IOS-XE-native:memory/Cisco-IOS-XE-native:free/Cisco-IOS-XE-native:low-watermark'
        expected_body_post = {
            'IO': '1'
        }
        # Build RESTCONF request
        request_builder = RestconfRequestBuilder(request_data_post, returns)
        actual_url_post = request_builder.url
        actual_body_post = request_builder.body

        # Test URL
        self.assertEqual(expected_url_post, actual_url_post)
        # Test body
        self.assertEqual(actual_body_post, expected_body_post)
        self.assertNotEqual(actual_body_post, None)
        self.assertNotEqual(actual_body_post, {})

    def test_list_nodes(self):
        """Test single and nested list nodes"""
        # Test PATCH/merge on a nested leaf and list node
        request_data_patch = {
            'namespace': {
                'ios': 'http://cisco.com/ns/yang/Cisco-IOS-XE-native'
            },
            'nodes': [{
                'edit-op': 'merge',
                'nodetype': 'leaf',
                'datatype': 'string',
                'value': 'abcd',
                'xpath': '/ios:native/ios:interface/ios:GigabitEthernet[name="2"]/description'
            }, {
                'edit-op': 'merge',
                'nodetype': 'leaf',
                'datatype': 'uint8',
                'value': 1,
                'xpath': '/ios:native/ios:username[name="test"]/privilege'
            }]
        }
        returns = {}
        expected_url_patch = '/restconf/data/Cisco-IOS-XE-native:native'
        expected_body_patch = {
            'native': {
                'interface': {
                    'GigabitEthernet': {
                        'description': 'abcd',
                        'name': '2'
                    }
                },
                'username': {
                    'privilege': 1,
                    'name': 'test'
                }
            }
        }
        # Build RESTCONF request
        request_builder = RestconfRequestBuilder(request_data_patch, returns)
        actual_url_patch = request_builder.url
        actual_body_patch = request_builder.body

        # Test PATCH URL
        self.assertEqual(expected_url_patch, actual_url_patch)
        # Test PATCH body
        self.assertEqual(actual_body_patch, expected_body_patch)
        self.assertNotEqual(actual_body_patch, None)
        self.assertNotEqual(actual_body_patch, {})

        # Test POST/create on list node
        request_data_post = {
            'namespace': {
                'ios': 'http://cisco.com/ns/yang/Cisco-IOS-XE-native'
            },
            'nodes': [{
                'edit-op': 'create',
                'nodetype': 'leaf',
                'datatype': 'uint8',
                'value': 1,
                'xpath': '/ios:native/ios:username[name="test"]/privilege'
            }]
        }
        expected_url_post = '/restconf/data/Cisco-IOS-XE-native:native'
        expected_body_post = {
            'username': [{
                'privilege': 1,
                'name': 'test'
            }]
        }
        returns = {}

        # Build RESTCONF request
        request_builder = RestconfRequestBuilder(request_data_post, returns)
        actual_url = request_builder.url
        actual_body = request_builder.body

        # Test POST URL
        self.assertEqual(expected_url_post, actual_url)
        # Test POST body
        self.assertEqual(actual_body, expected_body_post)
        self.assertNotEqual(actual_body, None)
        self.assertNotEqual(actual_body, {})

    def test_container_nodes(self):
        """Test for container nodes"""
        request_data = {
            'namespace': {
                'ios': 'http://cisco.com/ns/yang/Cisco-IOS-XE-native'
            },
            'nodes': [{
                'edit-op': 'get',
                'nodetype': 'leaf',
                'datatype': 'string',
                'value': '17.6',
                'xpath': '/ios:native/ios:boot/ios:system/'
            }]
        }
        returns = {}
        expected_url = '/restconf/data/Cisco-IOS-XE-native:native/Cisco-IOS-XE-native:boot/Cisco-IOS-XE-native:system'
        expected_body = {}

        request_builder = RestconfRequestBuilder(request_data, returns)
        actual_url = request_builder.url
        actual_body = request_builder.body

        # Test URL
        self.assertEqual(expected_url, actual_url)
        # Test body
        self.assertEqual(actual_body, expected_body)
        self.assertNotEqual(actual_body, None)

    def test_leaf_list_nodes(self):
        """Test leaf-list nodes"""
        request_data = {
            'namespace': {
                'oc-if': 'http://openconfig.net/yang/interfaces'
            },
            'nodes': [{
                'edit-op': 'get',
                'nodetype': 'leaf',
                'datatype': 'identityref',
                'value': 'ianaift:a12MppSwitch',
                'xpath': '/oc-if:interfaces/oc-if:interface/oc-if:config/oc-if:type'
            }]
        }
        returns = {}
        expected_url = '/restconf/data/interfaces:interfaces/interfaces:interface/interfaces:config/interfaces:type'
        expected_body = {}

        request_builder = RestconfRequestBuilder(request_data, returns)
        actual_url = request_builder.url
        actual_body = request_builder.body

        # Test URL
        self.assertEqual(expected_url, actual_url)
        # Test body
        self.assertEqual(actual_body, expected_body)
        self.assertNotEqual(actual_body, None)

    def test_combine_all_node_types(self):
        request_data = {
            'namespace': {
                'ios': 'http://cisco.com/ns/yang/Cisco-IOS-XE-native'
            },
            'nodes': [{
                'edit-op': 'get',
                'nodetype': 'leaf',
                'datatype': 'string',
                'value': '17.6',
                'xpath': '/ios:native/ios:version' # Non-nested leaf
            }, {
                'edit-op': 'get',
                'nodetype': 'container',
                'datatype': '',
                'value': '',
                'xpath': '/ios:native/ios:memory/ios:free' # Nested container
            }, {
                'edit-op': 'get',
                'nodetype': 'leaf',
                'datatype': 'uint32',
                'value': '68976',
                'xpath': '/ios:native/ios:memory/ios:free/ios:low-watermark/ios:processor' # Nested leaf in nested container
            }, {
                'edit-op': 'get',
                'nodetype': 'list',
                'datatype': '',
                'value': '',
                'xpath': '/ios:native/ios:username' # List
            }]
        }
        expected_url = '/restconf/data/Cisco-IOS-XE-native:native'
        expected_body = {}
        returns = [{
            'id': 1,
            'datatype': 'string',
            'default': '',
            'name': 'version',
            'nodetype': 'leaf',
            'op': '==',
            'selected': 'True',
            'value': 17.6,
            'xpath': '/ios:native/ios:version'
        }, {
            'id': 2,
            'datatype': 'container',
            'default': '',
            'name': 'free',
            'nodetype': 'leaf',
            'op': '==',
            'selected': 'True',
            'value': '',
            'xpath': '/ios:native/ios:memory/ios:free'
        }, {
            'id': 3,
            'datatype': 'uint32',
            'default': '',
            'name': 'processor',
            'nodetype': 'leaf',
            'op': '==',
            'selected': 'True',
            'value': 68976,
            'xpath': '/ios:native/ios:memory/ios:free/ios:low-watermark/ios:processor'
        }, {
            'id': 4,
            'datatype': 'list',
            'default': '',
            'name': 'username',
            'nodetype': 'list',
            'op': '==',
            'selected': 'True',
            'value': '',
            'xpath': '/ios:native/ios:username'
        }]
        # Build RESTCONF request
        request_builder = RestconfRequestBuilder(request_data, returns)
        actual_url = request_builder.url
        actual_body = request_builder.body

        # Test URL
        self.assertEqual(expected_url, actual_url)
        # Test body
        self.assertEqual(actual_body, expected_body)
        self.assertNotEqual(actual_body, None)

if __name__ == '__main__':
    unittest.main()
