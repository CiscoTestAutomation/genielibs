import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.snmp.configure import (
    unconfigure_snmp_server_view,
)


class TestUnconfigureSnmpServerView(unittest.TestCase):

    def test_unconfigure_snmp_server_view(self):
        device = Mock()

        result = unconfigure_snmp_server_view(
            device,
            'readwrite',
            'iso',
            'excluded',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no snmp-server view readwrite iso excluded'
        )
