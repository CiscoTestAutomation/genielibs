from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ntp.configure import unconfigure_ntp_server

class TestUnconfigureNtpServer(TestCase):

    def test_unconfigure_ntp_server(self):
        device = Mock()
        result = unconfigure_ntp_server(device, ['1.1.1.1', '2.2.2.2'], 'Mgmt-vrf')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'no ntp server vrf Mgmt-vrf 1.1.1.1',
                'no ntp server vrf Mgmt-vrf 2.2.2.2'
            ],)
        )