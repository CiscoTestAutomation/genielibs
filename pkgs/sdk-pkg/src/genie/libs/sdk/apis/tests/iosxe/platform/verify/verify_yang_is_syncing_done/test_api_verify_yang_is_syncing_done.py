import os
import unittest
from textwrap import dedent
from unittest.mock import Mock, patch

from lxml import etree
from ncclient.operations.retrieve import GetReply

from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.verify import verify_yang_is_syncing_done

class yMock(Mock):

    __name__ = 'Netconf'

    dispatch_response = iter([])

    @property
    def connected(self):
        return True

    def connect(self, *args, **kwargs):
        netconf_connect_output = '''
Connected (version 2.0, client OpenSSH_9.1)
Authentication (password) successful!
[host 127.0.0.1 session 0x7fe8b169c6d0] Sending:
<nc:hello xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
  <nc:capabilities>
    <nc:capability>urn:ietf:params:netconf:base:1.0</nc:capability>
    <nc:capability>urn:ietf:params:netconf:base:1.1</nc:capability>
    <nc:capability>urn:ietf:params:netconf:capability:writable-running:1.0</nc:capability>
    <nc:capability>urn:ietf:params:netconf:capability:candidate:1.0</nc:capability>
    <nc:capability>urn:ietf:params:netconf:capability:confirmed-commit:1.0</nc:capability>
    <nc:capability>urn:ietf:params:netconf:capability:rollback-on-error:1.0</nc:capability>
    <nc:capability>urn:ietf:params:netconf:capability:startup:1.0</nc:capability>
    <nc:capability>urn:ietf:params:netconf:capability:url:1.0?scheme=http,ftp,file,https,sftp</nc:capability>
    <nc:capability>urn:ietf:params:netconf:capability:validate:1.0</nc:capability>
    <nc:capability>urn:ietf:params:netconf:capability:xpath:1.0</nc:capability>
    <nc:capability>urn:ietf:params:netconf:capability:notification:1.0</nc:capability>
    <nc:capability>urn:ietf:params:netconf:capability:interleave:1.0</nc:capability>
    <nc:capability>urn:ietf:params:netconf:capability:with-defaults:1.0</nc:capability>
  </nc:capabilities>
</nc:hello>
]]>]]>
[host 127.0.0.1 session 0x7fe8b169c6d0] Received message from host
[host 127.0.0.1 session-id 34] initialized: session-id=34 | server_capabilities=<dict_keyiterator object at 0x7fe8b2dbfba0>
NETCONF CONNECTED'''
        return netconf_connect_output

    def dispatch(self, *args, **kwargs):
        xml_string = next(self.dispatch_response)

        # Parse the XML string
        xml_element = etree.fromstring(xml_string)

        # Create the GetReply object
        reply = GetReply(xml_element)
        return reply


class TestVerifyYangIsSyncingDone(unittest.TestCase):

    @classmethod
    def setUpClass(self) -> None:
        self.testbed_yaml = '''
            devices:
                switch:
                    alias: uut
                    platform: 'c8kv'
                    os: 'iosxe'
                    credentials:
                        netconf:
                            username: lab
                            password: lab
                    connections:
                        defaults:
                            class: unicon.Unicon
                        netconf:
                            class: yang.connector.Netconf
                            protocol: netconf
                            ip: 127.0.0.1
                            port: 830
        '''
        self.testbed = loader.load(self.testbed_yaml)
        self.device = self.testbed.devices['switch']

    def test_verify_yang_is_syncing_done(self):
        with patch('yang.connector.Netconf', new_callable=yMock) as ymock:
            self.testbed = loader.load(self.testbed_yaml)
            self.device = self.testbed.devices['switch']

            self.device.connect(via='netconf', alias='nc')

            self.device.nc.dispatch_response = iter([dedent('''\
                <rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:f04afc5b-7f1a-4ac6-9eb4-14f7c2ab5089">
                <result xmlns="http://cisco.com/yang/cisco-ia">No sync in progress</result>
                </rpc-reply>
                ''')])

            result = self.device.api.verify_yang_is_syncing_done()
            self.assertEqual(result, True)

    def test_verify_yang_is_syncing_done_retry(self):
        with patch('yang.connector.Netconf', new_callable=yMock) as ymock:
            self.testbed = loader.load(self.testbed_yaml)
            self.device = self.testbed.devices['switch']

            self.device.connect(via='netconf', alias='nc')

            self.device.nc.dispatch_response = iter([dedent('''\
                <rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:f04afc5b-7f1a-4ac6-9eb4-14f7c2ab5089">
                <result xmlns="http://cisco.com/yang/cisco-ia">Sync is Still in Progress</result>
                </rpc-reply>
                '''),
                dedent('''\
                <rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:f04afc5b-7f1a-4ac6-9eb4-14f7c2ab5089">
                <result xmlns="http://cisco.com/yang/cisco-ia">No sync in progress</result>
                </rpc-reply>
                ''')
                ])

            result = self.device.api.verify_yang_is_syncing_done()
            self.assertEqual(result, False)

            result = self.device.api.verify_yang_is_syncing_done()
            self.assertEqual(result, True)
