import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_ip_source_binding


class TestConfigureIpSourceBinding(unittest.TestCase):

    def test_configure_ip_source_binding(self):
        device = Mock()

        result = configure_ip_source_binding(device, '000A.000B.0001', '10', '10.1.1.101', 'Gi1/0/13')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip source binding 000A.000B.0001 vlan 10 10.1.1.101 interface Gi1/0/13',)
        )