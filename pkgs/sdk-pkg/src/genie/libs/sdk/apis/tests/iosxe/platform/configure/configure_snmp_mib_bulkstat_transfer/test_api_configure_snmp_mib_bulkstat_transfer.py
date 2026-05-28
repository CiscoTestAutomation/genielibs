import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_snmp_mib_bulkstat_transfer


class TestConfigureSnmpMibBulkstatTransfer(unittest.TestCase):

    def test_configure_snmp_mib_bulkstat_transfer(self):
        device = Mock()

        result = configure_snmp_mib_bulkstat_transfer(device, 'myTransfer1')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['snmp mib bulkstat transfer myTransfer1', 'no enable'],)
        )