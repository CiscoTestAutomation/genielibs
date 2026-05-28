import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_snmp_mib_bulkstat


class TestConfigureSnmpMibBulkstat(unittest.TestCase):

    def test_configure_snmp_mib_bulkstat(self):
        device = Mock()

        result = configure_snmp_mib_bulkstat(
            device,
            'name',
            'test1',
            'name',
            '1',
            'g1/1/1',
            'test2',
            '1',
            '123@cisco.com',
            '2',
            '2'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'snmp mib bulkstat object-list name',
                'add test1',
                'exit',
                'snmp mib bulkstat schema name',
                'object-list name',
                'poll-interval 1',
                'instance wild interface g1/1/1',
                'exit',
                'snmp mib bulkstat transfer test2',
                'schema name',
                'format schemaASCII',
                'transfer-interval 1',
                'url primary 123@cisco.com',
                'retry 2',
                'retain 2',
                'enable'
            ],)
        )