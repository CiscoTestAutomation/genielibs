import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.snmp.configure import (
    unconfigure_snmp_server_engineid,
)


class TestUnconfigureSnmpServerEngineid(unittest.TestCase):

    def test_unconfigure_snmp_server_engineid(self):
        device = Mock()

        result = unconfigure_snmp_server_engineid(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no snmp-server engineID local'
        )
