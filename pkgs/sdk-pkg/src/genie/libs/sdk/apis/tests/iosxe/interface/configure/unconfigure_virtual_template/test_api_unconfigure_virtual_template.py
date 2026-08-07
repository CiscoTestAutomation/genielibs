from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_virtual_template


class TestUnconfigureVirtualTemplate(TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.is_connected.return_value = True
        self.device.configure.return_value = None

    def assert_configured(self, expected_config):
        self.device.configure.assert_called_once_with(expected_config)

    def test_unconfigure_virtual_template(self):
        result = unconfigure_virtual_template(self.device, '1')
        expected_config = ['no interface Virtual-Template 1']
        self.assertIsNone(result)
        self.assert_configured(expected_config)

    def test_unconfigure_virtual_template_with_extended_options(self):
        result = unconfigure_virtual_template(
            self.device,
            '2',
            negotiated=True,
            pool_name='LOCAL_POOL',
            pool_local=True,
            chap_hostname='USER@example.com',
            chap_password='cisco',
            chap_splitnames=True,
            timeout_ncp=30,
            timeout_idle=60,
            logging_event_link_status=True,
        )

        expected_config = [
            'interface Virtual-Template 2',
            'no ip address',
            'no peer default ip address pool local LOCAL_POOL',
            'no ppp chap hostname USER@example.com',
            'no ppp chap password 0 cisco',
            'no ppp chap splitnames',
            'no ppp timeout ncp 30',
            'no ppp timeout idle 60',
            'logging event link-status',
        ]
        self.assertIsNone(result)
        self.assert_configured(expected_config)

    def test_unconfigure_virtual_template_with_vrf(self):
        result = unconfigure_virtual_template(
            self.device,
            '3',
            vrf_name='VRF101',
        )

        expected_config = [
            'interface Virtual-Template 3',
            'no ip vrf forwarding VRF101',
        ]
        self.assertIsNone(result)
        self.assert_configured(expected_config)
