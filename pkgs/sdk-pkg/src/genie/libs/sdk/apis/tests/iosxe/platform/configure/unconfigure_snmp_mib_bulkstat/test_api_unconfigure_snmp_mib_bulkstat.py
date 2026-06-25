import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_snmp_mib_bulkstat


class TestUnconfigureSnmpMibBulkstat(unittest.TestCase):

    def test_unconfigure_snmp_mib_bulkstat(self):
        device = Mock()

        result = unconfigure_snmp_mib_bulkstat(
            device,
            'cleanupObject',
            'cleanupSchema',
            'cleanupTransfer'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'bulkstat profile cleanupTransfer',
                'no enable',
                'exit',
                'no snmp mib bulkstat object-list cleanupObject',
                'no snmp mib bulkstat schema cleanupSchema',
                'no snmp mib bulkstat transfer cleanupTransfer'
            ],)
        )